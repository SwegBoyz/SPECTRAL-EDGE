"""
SPECTRAL-EDGE: Core GNN Architecture (Phase 2 Design)
Model: Chebyshev Spectral Graph Convolution (ChebNet)
Target: Node-level anomaly classification for IoT networks.
"""

import torch
import torch.nn.functional as F
from torch_geometric.nn import ChebConv
from torch.nn import Linear, BatchNorm1d, Dropout

class SpectralEdgeGNN(torch.nn.Module):
    def __init__(self, num_node_features, hidden_channels, num_classes, k_hops=2):
        super(SpectralEdgeGNN, self).__init__()
        
        # Phase 2 Design: Spectral Convolution Layers using ChebNet
        # K defines the Chebyshev filter size (localized hop radius)
        self.conv1 = ChebConv(num_node_features, hidden_channels, K=k_hops)
        self.bn1 = BatchNorm1d(hidden_channels)
        self.dropout1 = Dropout(p=0.3)
        
        self.conv2 = ChebConv(hidden_channels, hidden_channels // 2, K=k_hops)
        self.bn2 = BatchNorm1d(hidden_channels // 2)
        
        # Node-level anomaly classification head
        self.classifier = Linear(hidden_channels // 2, num_classes)

    def forward(self, x, edge_index, edge_weight=None):
        # First Spectral Block
        x = self.conv1(x, edge_index, edge_weight)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout1(x)
        
        # Second Spectral Block
        x = self.conv2(x, edge_index, edge_weight)
        x = self.bn2(x)
        x = F.relu(x)
        
        # Anomaly Classification Head
        out = self.classifier(x)
        return F.log_softmax(out, dim=1)

# Schema defined in Phase 2:
# num_node_features = 8 (Traffic stats + behavioral indicators)
# num_classes = 5 (1 Normal + 4 Attack Types)
