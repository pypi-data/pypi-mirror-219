import json
import os
import shutil
from copy import deepcopy

import dgl
import easydict
import numpy as np
import scipy.sparse as sp
import networkx as nx
import torch
import torch.nn.functional as F
import yaml
import random
from dgl.data import DGLDataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

from GSL.metric import CosineSimilarity
from GSL.processor import KNearestNeighbour

EOS = 1e-10
VERY_SMALL_NUMBER = 1e-12

def load_config(cfg_file):
    with open(cfg_file, "r") as fin:
        raw_text = fin.read()
        configs = [easydict.EasyDict(yaml.safe_load(raw_text))]
    return configs


def save_config(cfg, path):
    with open(os.path.join(path, "config.yaml"), "w") as fo:
        yaml.dump(dict(cfg), fo)


def get_feat_mask(features, mask_rate):
    feat_node = features.shape[1]
    mask = torch.zeros(features.shape)
    samples = np.random.choice(
        feat_node, size=int(feat_node * mask_rate), replace=False
    )
    mask[:, samples] = 1
    return mask.cuda(), samples


def torch_sparse_to_dgl_graph(torch_sparse_mx):
    torch_sparse_mx = torch_sparse_mx.coalesce()
    indices = torch_sparse_mx.indices()
    values = torch_sparse_mx.values()
    rows_, cols_ = indices[0, :], indices[1, :]
    dgl_graph = dgl.graph(
        (rows_, cols_), num_nodes=torch_sparse_mx.shape[0], device="cuda"
    )
    dgl_graph.edata["w"] = values.detach().cuda()
    return dgl_graph


def torch_sparse_eye(num_nodes):
    indices = torch.arange(num_nodes).repeat(2, 1)
    values = torch.ones(num_nodes)
    return torch.sparse.FloatTensor(indices, values)


def normalize(adj, mode, sparse=False):
    if not sparse:
        if mode == "sym":
            inv_sqrt_degree = 1.0 / (torch.sqrt(adj.sum(dim=1, keepdim=False)) + EOS)
            return inv_sqrt_degree[:, None] * adj * inv_sqrt_degree[None, :]
        elif mode == "row":
            inv_degree = 1.0 / (adj.sum(dim=1, keepdim=False) + EOS)
            return inv_degree[:, None] * adj
        else:
            exit("wrong norm mode")
    else:
        adj = adj.coalesce()
        if mode == "sym":
            inv_sqrt_degree = 1.0 / (torch.sqrt(torch.sparse.sum(adj, dim=1).values()))
            D_value = (
                inv_sqrt_degree[adj.indices()[0]] * inv_sqrt_degree[adj.indices()[1]]
            )

        elif mode == "row":
            aa = torch.sparse.sum(adj, dim=1)
            bb = aa.values()
            inv_degree = 1.0 / (torch.sparse.sum(adj, dim=1).values() + EOS)
            D_value = inv_degree[adj.indices()[0]]
        else:
            exit("wrong norm mode")
        new_values = adj.values() * D_value

        return torch.sparse.FloatTensor(adj.indices(), new_values, adj.size())


def accuracy(output, labels):
    if not hasattr(labels, "__len__"):
        labels = [labels]
    if type(labels) is not torch.Tensor:
        labels = torch.LongTensor(labels)
    preds = output.max(1)[1].type_as(labels)
    correct = preds.eq(labels).double()
    correct = correct.sum()
    return correct / len(labels)

def auc_f1_mima(logits, label):
    preds = torch.argmax(logits, dim=1)
    test_f1_macro = f1_score(label.cpu(), preds.cpu(), average='macro')
    test_f1_micro = f1_score(label.cpu(), preds.cpu(), average='micro')

    best_proba = F.softmax(logits, dim=1)
    if logits.shape[1] != 2:
        auc = roc_auc_score(y_true=label.detach().cpu().numpy(),
                            y_score=best_proba.detach().cpu().numpy(),
                            multi_class='ovr'
                            )
    else:
        auc = roc_auc_score(y_true=label.detach().cpu().numpy(),
                            y_score=best_proba[:, 1].detach().cpu().numpy()
                            )
    return test_f1_macro, test_f1_micro, auc

def split_batch(init_list, batch_size):
    groups = zip(*(iter(init_list),) * batch_size)
    end_list = [list(i) for i in groups]
    count = len(init_list) % batch_size
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


def symmetrize(adj):  # only for non-sparse
    return (adj + adj.T) / 2


def knn_fast(X, k, b):
    X = F.normalize(X, dim=1, p=2)
    index = 0
    values = torch.zeros(X.shape[0] * (k + 1)).cuda()
    rows = torch.zeros(X.shape[0] * (k + 1)).cuda()
    cols = torch.zeros(X.shape[0] * (k + 1)).cuda()
    norm_row = torch.zeros(X.shape[0]).cuda()
    norm_col = torch.zeros(X.shape[0]).cuda()
    while index < X.shape[0]:
        if (index + b) > (X.shape[0]):
            end = X.shape[0]
        else:
            end = index + b
        sub_tensor = X[index : index + b]
        similarities = torch.mm(sub_tensor, X.t())
        vals, inds = similarities.topk(k=k + 1, dim=-1)
        values[index * (k + 1) : (end) * (k + 1)] = vals.view(-1)
        cols[index * (k + 1) : (end) * (k + 1)] = inds.view(-1)
        rows[index * (k + 1) : (end) * (k + 1)] = (
            torch.arange(index, end).view(-1, 1).repeat(1, k + 1).view(-1)
        )
        norm_row[index:end] = torch.sum(vals, dim=1)
        norm_col.index_add_(-1, inds.view(-1), vals.view(-1))
        index += b
    norm = norm_row + norm_col
    rows = rows.long()
    cols = cols.long()
    values *= torch.pow(norm[rows], -0.5) * torch.pow(norm[cols], -0.5)
    return rows, cols, values


def top_k(raw_graph, K):
    values, indices = raw_graph.topk(k=int(K), dim=-1)
    assert torch.max(indices) < raw_graph.shape[1]
    mask = torch.zeros(raw_graph.shape).cuda()
    mask[torch.arange(raw_graph.shape[0]).view(-1, 1), indices] = 1.0

    mask.requires_grad = False
    sparse_graph = raw_graph * mask
    return sparse_graph


def dgl_graph_to_torch_sparse(dgl_graph):
    values = dgl_graph.edata["w"].cpu().detach()
    rows_, cols_ = dgl_graph.edges()
    indices = torch.cat((torch.unsqueeze(rows_, 0), torch.unsqueeze(cols_, 0)), 0).cpu()
    torch_sparse_mx = torch.sparse.FloatTensor(indices, values)
    return torch_sparse_mx


def get_train_val_test(nnodes, val_size=0.1, test_size=0.8, stratify=None, seed=None):
    """This setting follows nettack/mettack, where we split the nodes
    into 10% training, 10% validation and 80% testing data

    Parameters
    ----------
    nnodes : int
        number of nodes in total
    val_size : float
        size of validation set
    test_size : float
        size of test set
    stratify :
        data is expected to split in a stratified fashion. So stratify should be labels.
    seed : int or None
        random seed

    Returns
    -------
    idx_train :
        node training indices
    idx_val :
        node validation indices
    idx_test :
        node test indices
    """

    assert stratify is not None, "stratify cannot be None!"

    if seed is not None:
        np.random.seed(seed)

    idx = np.arange(nnodes)
    train_size = 1 - val_size - test_size
    idx_train_and_val, idx_test = train_test_split(
        idx,
        random_state=None,
        train_size=train_size + val_size,
        test_size=test_size,
        stratify=stratify,
    )

    if stratify is not None:
        stratify = stratify[idx_train_and_val]

    idx_train, idx_val = train_test_split(
        idx_train_and_val,
        random_state=None,
        train_size=(train_size / (train_size + val_size)),
        test_size=(val_size / (train_size + val_size)),
        stratify=stratify,
    )

    return idx_train, idx_val, idx_test


def get_train_val_test_gcn(labels, seed=None):
    """This setting follows gcn, where we randomly sample 20 instances for each class
    as training data, 500 instances as validation data, 1000 instances as test data.
    Note here we are not using fixed splits. When random seed changes, the splits
    will also change.

    Parameters
    ----------
    labels : numpy.array
        node labels
    seed : int or None
        random seed

    Returns
    -------
    idx_train :
        node training indices
    idx_val :
        node validation indices
    idx_test :
        node test indices
    """
    if seed is not None:
        np.random.seed(seed)

    idx = np.arange(len(labels))
    nclass = labels.max() + 1
    idx_train = []
    idx_unlabeled = []
    for i in range(nclass):
        labels_i = idx[labels == i]
        labels_i = np.random.permutation(labels_i)
        idx_train = np.hstack((idx_train, labels_i[:20])).astype(np.int32)
        idx_unlabeled = np.hstack((idx_unlabeled, labels_i[20:])).astype(np.int32)

    idx_unlabeled = np.random.permutation(idx_unlabeled)
    idx_val = idx_unlabeled[:500]
    idx_test = idx_unlabeled[500:1500]
    return idx_train, idx_val, idx_test


def get_random_mask(features, r, nr):
    nones = torch.sum(features > 0.0).float()
    nzeros = features.shape[0] * features.shape[1] - nones
    pzeros = nones / nzeros / r * nr
    probs = torch.zeros(features.shape).cuda()
    probs[features == 0.0] = pzeros
    probs[features > 0.0] = 1 / r
    mask = torch.bernoulli(probs)
    return mask


def get_random_mask_ogb(features, r):
    probs = torch.full(features.shape, 1 / r)
    mask = torch.bernoulli(probs)
    return mask


def sys_normalized_adjacency(adj):
    adj = sp.coo_matrix(adj)
    adj = adj + sp.eye(adj.shape[0])
    row_sum = np.array(adj.sum(1))
    row_sum = (row_sum == 0) * 1 + row_sum
    d_inv_sqrt = np.power(row_sum, -0.5).flatten()
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.0
    d_mat_inv_sqrt = sp.diags(d_inv_sqrt)
    return d_mat_inv_sqrt.dot(adj).dot(d_mat_inv_sqrt).tocoo()


def sparse_mx_to_torch_sparse_tensor(sparse_mx):
    """Convert a scipy sparse matrix to a torch sparse tensor."""
    sparse_mx = sparse_mx.tocoo().astype(np.float32)
    indices = torch.from_numpy(
        np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64)
    )
    values = torch.from_numpy(sparse_mx.data)
    shape = torch.Size(sparse_mx.shape)
    return torch.sparse.FloatTensor(indices, values, shape)


class AverageMeter(object):
    """Computes and stores the average and current value."""

    def __init__(self):
        self.history = []
        self.last = None
        self.val = 0
        self.sum = 0
        self.count = 0

    def reset(self):
        self.last = self.mean()
        self.history.append(self.last)
        self.val = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n

    def mean(self):
        if self.count == 0:
            return 0.0
        return self.sum / self.count


class DummyLogger(object):
    def __init__(self, config, dirname=None, pretrained=None):
        self.config = config
        if dirname is None:
            if pretrained is None:
                raise Exception("Either --dir or --pretrained needs to be specified.")
            self.dirname = pretrained
        else:
            self.dirname = dirname
            if os.path.exists(dirname):
                shutil.rmtree(dirname)
            os.makedirs(dirname)
            os.mkdir(os.path.join(dirname, "metrics"))
            self.log_json(config, os.path.join(self.dirname, "config.json"))
        if config["logging"]:
            self.f_metric = open(
                os.path.join(self.dirname, "metrics", "metrics.log"), "a"
            )

    def log_json(self, data, filename, mode="w"):
        with open(filename, mode) as outfile:
            outfile.write(json.dumps(data, indent=4, ensure_ascii=False))

    def log(self, data, filename):
        print(data)

    def write_to_file(self, text):
        if self.config["logging"]:
            self.f_metric.writelines(text + "\n")
            self.f_metric.flush()

    def close(self):
        if self.config["logging"]:
            self.f_metric.close()


def to_scipy(tensor):
    """Convert a dense/sparse tensor to scipy matrix"""
    if is_sparse_tensor(tensor):
        values = tensor._values()
        indices = tensor._indices()
        return sp.csr_matrix(
            (values.cpu().numpy(), indices.cpu().numpy()), shape=tensor.shape
        )
    else:
        indices = tensor.nonzero().t()
        values = tensor[indices[0], indices[1]]
        return sp.csr_matrix(
            (values.cpu().numpy(), indices.cpu().numpy()), shape=tensor.shape
        )


def is_sparse_tensor(tensor):
    """Check if a tensor is sparse tensor.

    Parameters
    ----------
    tensor : torch.Tensor
        given tensor

    Returns
    -------
    bool
        whether a tensor is sparse tensor
    """
    # if hasattr(tensor, 'nnz'):
    if tensor.layout == torch.sparse_coo:
        return True
    else:
        return False


def to_tensor(adj, features, labels=None, device="cpu"):
    """Convert adj, features, labels from array or sparse matrix to
    torch Tensor on target device.
    Args:
        adj : scipy.sparse.csr_matrix
            the adjacency matrix.
        features : scipy.sparse.csr_matrix
            node features
        labels : numpy.array
            node labels
        device : str
            'cpu' or 'cuda'
    """
    if sp.issparse(adj):
        adj = sparse_mx_to_sparse_tensor(adj)
    else:
        adj = torch.FloatTensor(adj)
    if sp.issparse(features):
        features = sparse_mx_to_sparse_tensor(features)
    else:
        features = torch.FloatTensor(np.array(features))

    if labels is None:
        return adj.to(device), features.to(device)
    else:
        labels = torch.LongTensor(labels)
        return adj.to(device), features.to(device), labels.to(device)


def sparse_mx_to_sparse_tensor(sparse_mx):
    """sparse matrix to sparse tensor matrix(torch)
    Args:
        sparse_mx : scipy.sparse.csr_matrix
            sparse matrix
    """
    sparse_mx_coo = sparse_mx.tocoo().astype(np.float32)
    sparse_row = torch.LongTensor(sparse_mx_coo.row).unsqueeze(1)
    sparse_col = torch.LongTensor(sparse_mx_coo.col).unsqueeze(1)
    sparse_indices = torch.cat((sparse_row, sparse_col), 1)
    sparse_data = torch.FloatTensor(sparse_mx.data)
    return torch.sparse.FloatTensor(
        sparse_indices.t(), sparse_data, torch.Size(sparse_mx.shape)
    )


class EarlyStopping:
    def __init__(self, patience=10):
        self.patience = patience
        self.counter = 0
        self.best_score = None
        self.best_epoch = None
        self.early_stop = False
        self.best_weight = None

    def step(self, acc, model, epoch):
        score = acc
        if self.best_score is None:
            self.best_score = score
            self.best_epoch = epoch
            self.best_weight = deepcopy(model.state_dict())
        elif score < self.best_score:
            self.counter += 1
            print(
                f"EarlyStopping counter: {self.counter}/{self.patience}, best_val_score:{self.best_score:.4f} at E{self.best_epoch}"
            )
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.best_epoch = epoch
            self.best_weight = deepcopy(model.state_dict())
            self.counter = 0

        return self.early_stop
    

def true_positive(pred, target, n_class):
    return torch.tensor(
        [((pred == i) & (target == i)).sum() for i in range(n_class)]
    )

def false_positive(pred, target, n_class):
    return torch.tensor(
        [((pred == i) & (target != i)).sum() for i in range(n_class)]
    )

def false_negative(pred, target, n_class):
    return torch.tensor(
        [((pred != i) & (target == i)).sum() for i in range(n_class)]
    )

def precision(tp, fp):
    res = tp / (tp + fp)
    res[torch.isnan(res)] = 0
    return res

def recall(tp, fn):
    res = tp / (tp + fn)
    res[torch.isnan(res)] = 0
    return res

def f1_score(prec, rec):
    f1_score = 2 * (prec * rec) / (prec + rec)
    f1_score[torch.isnan(f1_score)] = 0
    return f1_score

def cal_maf1(tp, fp, fn):
    prec = precision(tp, fp)
    rec = recall(tp, fn)
    ma_f1 = f1_score(prec, rec)
    return torch.mean(ma_f1).cpu().numpy()

def cal_mif1(tp, fp, fn):
        gl_tp, gl_fp, gl_fn = torch.sum(tp), torch.sum(fp), torch.sum(fn)
        gl_prec = precision(gl_tp, gl_fp)
        gl_rec = recall(gl_tp, gl_fn)
        mi_f1 = f1_score(gl_prec, gl_rec)
        return mi_f1.cpu().numpy()
    

def macro_f1(pred, target, n_class):
    tp = true_positive(pred, target, n_class).to(torch.float)
    fn = false_negative(pred, target, n_class).to(torch.float)
    fp = false_positive(pred, target, n_class).to(torch.float)

    ma_f1 = cal_maf1(tp, fp, fn)
    return ma_f1


def micro_f1(pred, target, n_class):
    tp = true_positive(pred, target, n_class).to(torch.float)
    fn = false_negative(pred, target, n_class).to(torch.float)
    fp = false_positive(pred, target, n_class).to(torch.float)

    mi_f1 = cal_mif1(tp, fp, fn)
    return mi_f1


def sparse_dense_mul(s, d):
    if not s.is_sparse:
        return s * d
    i = s._indices()
    v = s._values()
    dv = d[i[0, :], i[1, :]]  # get values from relevant entries of dense matrix
    return torch.sparse.FloatTensor(i, v * dv, s.size())


def prob_to_adj(mx, threshold):
    mx = np.triu(mx, 1)
    mx += mx.T
    (row, col) = np.where(mx > threshold)
    adj = sp.coo_matrix(
        (np.ones(row.shape[0]), (row, col)),
        shape=(mx.shape[0], mx.shape[0]),
        dtype=np.int64,
    )
    adj = sparse_mx_to_sparse_tensor(adj)
    return adj


def get_homophily(label, adj):
    label = label.cpu().numpy()
    adj = adj.cpu().numpy()
    num_node = len(label)
    label = label.repeat(num_node).reshape(num_node, -1)
    n = np.triu((label == label.T) & (adj == 1)).sum(axis=0)
    d = np.triu(adj).sum(axis=0)
    homos = []
    for i in range(num_node):
        if d[i] > 0:
            homos.append(n[i] * 1.0 / d[i])
    return np.mean(homos)


def diff(X, Y, Z):
    assert X.shape == Y.shape
    diff_ = torch.sum(torch.pow(X - Y, 2))
    norm_ = torch.sum(torch.pow(Z, 2))
    diff_ = diff_ / torch.clamp(norm_, min=VERY_SMALL_NUMBER)
    return diff_


def SquaredFrobeniusNorm(X):
    return torch.sum(torch.pow(X, 2)) / int(np.prod(X.shape))


def sample_mask(idx, l):
    """Create mask."""
    mask = np.zeros(l)
    mask[idx] = 1
    return np.array(mask, dtype=np.bool)

def row_normalize_features(features):
    """Row-normalize feature matrix and convert to tuple representation"""
    if isinstance(features, torch.Tensor):
        rowsum = torch.sum(features, dim=1)
        r_inv = torch.pow(rowsum, -1).flatten()
        r_inv[torch.isinf(r_inv)] = 0.
        r_mat_inv = torch.diag(r_inv)
        features = r_mat_inv @ features
    else:
        rowsum = np.array(features.sum(1))
        r_inv = np.power(rowsum, -1).flatten()
        r_inv[np.isinf(r_inv)] = 0.0
        r_mat_inv = sp.diags(r_inv)
        features = r_mat_inv.dot(features)
    return features


def dense_adj_to_edge_index(adj):
    edge_index = sp.coo_matrix(adj.cpu())
    indices = np.vstack((edge_index.row, edge_index.col))
    edge_index = torch.LongTensor(indices).to(adj.device)
    return edge_index


def k_fold(dataset, folds):
    skf = StratifiedKFold(folds, shuffle=True, random_state=12345)

    test_indices, train_indices = [], []
    if isinstance(dataset, DGLDataset):
        labels = dataset.graph_labels
        for _, idx in skf.split(torch.zeros(len(dataset)), labels):
            test_indices.append(torch.from_numpy(idx).to(torch.long))
    elif isinstance(dataset, list):
        for _, idx in skf.split(torch.zeros(len(dataset)), [data.y for data in dataset]):
            test_indices.append(torch.from_numpy(idx).to(torch.long))

    val_indices = [test_indices[i - 1] for i in range(folds)]

    for i in range(folds):
        train_mask = torch.ones(len(dataset), dtype=torch.bool)
        train_mask[test_indices[i]] = 0
        train_mask[val_indices[i]] = 0
        train_indices.append(train_mask.nonzero(as_tuple=False).view(-1))

    return train_indices, test_indices, val_indices


def transform_relation_graph_list(hg, category, identity=True):

    # get target category id
    for i, ntype in enumerate(hg.ntypes):
        if ntype == category:
            category_id = i
    g = dgl.to_homogeneous(hg, ndata='h')
    # find out the target node ids in g
    loc = (g.ndata[dgl.NTYPE] == category_id).to('cpu')
    category_idx = torch.arange(g.num_nodes())[loc]

    edges = g.edges()
    etype = g.edata[dgl.ETYPE]
    ctx = g.device
    # g.edata['w'] = th.ones(g.num_edges(), device=ctx)
    num_edge_type = torch.max(etype).item()

    # norm = EdgeWeightNorm(norm='right')
    # edata = norm(g.add_self_loop(), th.ones(g.num_edges() + g.num_nodes(), device=ctx))
    graph_list = []
    for i in range(num_edge_type + 1):
        e_ids = torch.nonzero(etype == i).squeeze(-1)
        sg = dgl.graph((edges[0][e_ids], edges[1][e_ids]), num_nodes=g.num_nodes())
        # sg.edata['w'] = edata[e_ids]
        sg.edata['w'] = torch.ones(sg.num_edges(), device=ctx)
        graph_list.append(sg)
    if identity == True:
        x = torch.arange(0, g.num_nodes(), device=ctx)
        sg = dgl.graph((x, x))
        # sg.edata['w'] = edata[g.num_edges():]
        sg.edata['w'] = torch.ones(g.num_nodes(), device=ctx)
        graph_list.append(sg)
    return graph_list, g.ndata['h'], category_idx

def get_nodes_dict(hg):
    n_dict = {}
    for n in hg.ntypes:
        n_dict[n] = hg.num_nodes(n)
    return n_dict


def to_undirected(edge_index, num_nodes=None):
    if num_nodes is None:
        num_nodes = edge_index.max() + 1
    else:
        num_nodes = max(num_nodes, edge_index.max() + 1)

    row, col = edge_index
    data = np.ones(edge_index.shape[1])
    adj = sp.csr_matrix((data, (row, col)), shape=(num_nodes, num_nodes))
    adj = (adj + adj.transpose()) > 0
    return adj.astype(np.float64)


def seed_everything(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    np.random.seed(seed)
    random.seed(seed)
    dgl.seed(seed)
    dgl.random.seed(seed)


def random_drop_edge(adj, drop_rate):
    row, col = adj.nonzero()
    num_nodes = max(row.max(), col.max()) + 1
    edge_num = adj.nnz
    drop_edge_num = int(edge_num * drop_rate)
    edge_mask = np.ones(edge_num, dtype=np.bool)
    indices = np.random.permutation(edge_num)[:drop_edge_num]
    edge_mask[indices] = False
    row, col = row[edge_mask], col[edge_mask]
    data = np.ones(edge_num - drop_edge_num)
    adj = sp.csr_matrix((data, (row, col)), shape=(num_nodes, num_nodes))
    return adj


def random_add_edge(adj, add_rate):
    row, col = adj.nonzero()
    num_nodes = max(row.max(), col.max()) + 1
    edge_num = adj.nnz
    num_edges_to_add = int(edge_num * add_rate)
    row_ = np.random.randint(0, num_nodes, size=(num_edges_to_add, ))
    col_ = np.random.randint(0, num_nodes, size=(num_edges_to_add, ))
    new_row = np.concatenate((row, row_), axis=0)
    new_col = np.concatenate((col, col_), axis=0)
    data = np.ones(edge_num + num_edges_to_add)
    adj = sp.csr_matrix((data, (new_row, new_col)), shape=(num_nodes, num_nodes))
    return adj


def get_knn_graph(features, k, dataset):
    metric = CosineSimilarity()
    adj = metric(features, features)
    adj = KNearestNeighbour(k=k)(adj).numpy()
    if dataset != 'ogbn-arxiv':
        adj = nx.adjacency_matrix(nx.from_numpy_array(adj))
    else:
        row, col = adj.nonzero()
        num_nodes = max(max(row), max(col)) + 1
        edge_index = np.array([row, col])
        adj = to_undirected(edge_index, num_nodes)
    return adj