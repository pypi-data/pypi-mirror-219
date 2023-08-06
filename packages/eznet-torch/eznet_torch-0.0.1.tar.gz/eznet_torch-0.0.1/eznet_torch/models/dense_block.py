if __package__=="eznet_torch.models":
    from ..utils import *
else:
    import os, sys
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(parent_dir)
    from utils import *


class Dense_Block(nn.Module):
    def __init__(self, input_size:int, output_size:int=None, activation:str=None, activation_params:dict=None, norm_layer_type:str=None, norm_layer_position:str='before', 
                 norm_layer_params:dict=None, dropout:float=None):
        """Dense (fully connected) block containing one linear layer, followed optionally by a normalization layer, an activation function and a Dropout layer.

        ### Args:
            - `input_size` (int): Number of input features.
            - `output_size` (int, optional): Number of output features. Defaults to None, in which case it will be input_size.
            - `activation` (str, optional): Activation function in string form. Defaults to None. Examples: 'ReLU', 'LeakyReLU', 'Tanh', 'Sigmoid', etc.
            - `activation_params` (dict, optional): kwargs to pass to the activation function constructor. Defaults to None.
            - `norm_layer_type` (str, optional): Type of normalization layer. Defaults to None. Examples: 'BatchNorm1d', 'LayerNorm', etc.
            - `norm_layer_position` (str, optional): Position of norm layer relative to activation. Defaults to 'before'. Alternative is 'after'.
            - `norm_layer_params` (dict, optional): kwargs to pass to the norm layer constructor. Defaults to None.
            - `dropout` (float, optional): Dropout rate at the end. Defaults to None. Must be a float between 0 and 1.
            
        ### Returns:
        An `nn.Module` object.
        """
        super(Dense_Block, self).__init__()
        if not output_size: output_size = input_size
        self._activation_module = getattr(nn, activation) if activation else None
        self._norm_layer_module = getattr(nn, norm_layer_type) if norm_layer_type else None
        self._dropout_module = nn.Dropout if dropout else None
        layers_vec = []
        layers_vec.append(nn.Linear(input_size, output_size))
        if norm_layer_type and norm_layer_position=='before': 
            if norm_layer_params: layers_vec.append(self._norm_layer_module(output_size, **norm_layer_params))
            else: layers_vec.append(self._norm_layer_module(output_size))
        if activation: 
            if activation_params: layers_vec.append(self._activation_module(**activation_params))
            else: layers_vec.append(self._activation_module())
        if norm_layer_type and norm_layer_position=='after': 
            if norm_layer_params: layers_vec.append(self._norm_layer_module(output_size, **norm_layer_params))
            else: layers_vec.append(self._norm_layer_module(output_size))
        if dropout: layers_vec.append(self._dropout_module(dropout))
        self.net = nn.Sequential(*layers_vec)
    
    def forward(self, x):
        return self.net(x)