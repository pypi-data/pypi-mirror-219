from GSL.model import *
from GSL.encoder import *
from GSL.data import *
from GSL.utils import (random_drop_edge, random_add_edge, get_knn_graph, accuracy, macro_f1,
                       micro_f1, seed_everything, sparse_mx_to_torch_sparse_tensor)

import torch
import numpy as np


class Experiment(object):
    def __init__(self, model_name, 
                 dataset, ntrail, 
                 data_path, config_path,
                 sparse: bool = False,
                 metric: str = 'acc',
                 gpu_num: int = 0,
                 use_knn: bool = False,
                 k: int = 5,
                 drop_rate: float = 0.,
                 add_rate: float = 0.,
                 use_mettack: bool = False,
                 ptb_rate: float = 0.05
                 ):
        
        self.sparse = sparse
        self.ntrail = ntrail
        self.metric = metric
        self.config_path = config_path
        self.device = torch.device("cuda:"+str(gpu_num) if torch.cuda.is_available() else "cpu")

        self.model_name = model_name
        self.dataset_name = dataset.lower()
        self.model_dict = {
            'GCN': GCN, 'GAT': GAT, 'SAGE': GraphSAGE, 'GIN': GIN, 'GRCN': GRCN, 'ProGNN': ProGNN,
            'IDGL': IDGL, 'GEN': GEN, 'CoGSL': CoGSL, 'SLAPS': SLAPS, 'SUBLIME': SUBLIME, 'STABLE': STABLE,
            'GTN': GTN, 'HGSL': HGSL, 'HGPSL': HGPSL, 'VIBGSL': VIBGSL, 'HESGSL': HESGSL
            # 'nodeformer': NodeFormer,
        }

        # Load graph datasets
        if self.dataset_name in ['cora', 'citeseer', 'pubmed', 'ogbn-arxiv',
                                 'cornell', 'texas', 'wisconsin', 'actor']:
            self.data = Dataset(root=data_path, name=self.dataset_name, use_mettack=use_mettack, ptb_rate=ptb_rate)
        elif self.dataset_name in ['acm', 'dblp', 'yelp']:
            self.data = HeteroDataset(root=data_path, name=self.dataset_name)
        elif self.dataset_name in ['imdb-b', 'imdb-m', 'collab', 'reddit-b', 'mutag',
                                   'proteins', 'peptides-func', 'peptides-struct']:
            self.data = GraphDataset(root=data_path, name=self.dataset_name)

        # Modify graph structures
        adj = self.data.adj
        features = self.data.features

        # Randomly drop edges
        if drop_rate > 0:
            adj = random_drop_edge(adj, drop_rate)
        
        # Randomly add edges
        if add_rate > 0:
            adj = random_add_edge(adj, drop_rate)

        # Use knn graph instead of the original structure
        if use_knn:
            adj = get_knn_graph(features, k, self.dataset_name)

        # Sparse or notyao
        if not self.sparse:
            self.data.adj = torch.from_numpy(adj.todense()).to(torch.float)
        else:
            self.data.adj = sparse_mx_to_torch_sparse_tensor(adj)

        # Select the metric of evaluation
        self.eval_metric = {
            'acc': accuracy,
            'macro-f1': macro_f1,
            'micro-f1': micro_f1,
        }[metric]

        
    def run(self):
        """
        Run the experiment
        """
        test_results = []
        num_feat, num_class = self.data.num_feat, self.data.num_class

        for i in range(self.ntrail):

            seed_everything(i)

            # Initialize the GSL model
            model = self.model_dict[self.model_name](num_feat, num_class, self.eval_metric, 
                                                          self.config_path, self.dataset_name, self.device)
            self.model = model.to(self.device)
            self.data = self.data.to(self.device)

            # Structure Learning
            self.model.fit(self.data)

            result = self.model.best_result
            test_results.append(result)
            print('Run: {} | Test result: {}'.format(i+1, result))

        exp_info = '------------------------------------------------------------------------------\n' \
                   'Experimental settings: \n' \
                   'Model: {} | Dataset: {} | Metric: {} \n' \
                   'Result: {} \n' \
                   'Final test result: {} +- {} \n' \
                   '------------------------------------------------------------------------------'.\
                   format(self.model_name, self.dataset_name, self.metric,
                          test_results, np.mean(test_results), np.std(test_results))
        print(exp_info)