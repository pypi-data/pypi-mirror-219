
if __package__=="eznet_torch.models":
    from .pytorch_smart_module import *
    from .dense_block import *
    from ..utils import *
else:
    import sys, os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, current_dir)
    sys.path.insert(0, parent_dir)
    from pytorch_smart_module import *
    from dense_block import *
    from utils import *


class ANN(PyTorchSmartModule):
    
    sample_hparams = {
        "model_name": "ANN",
        "input_size": 10,
        "output_size": 3,
        "width": 32,
        "depth": 2,
        "hidden_activation": "ReLU",
        "hidden_activation_params": None,
        "output_activation": None,
        "output_activation_params": None,
        "norm_layer_type":"BatchNorm1d",
        "norm_layer_position": "before",
        "norm_layer_params": None,
        "dropout": 0.2,
        "learning_rate": 0.001,
        "learning_rate_decay_gamma": 0.99,
        "optimizer": "Adam",
        "optimizer_params": {"eps": 1e-08},
        "batch_size": 32,
        "epochs": 2,
        "validation_tolerance_epochs": 2,
        "validation_data":[0.05,'trainset'],
        "l2_reg": 0.0001,
        "loss_function": "CrossEntropyLoss",
        "loss_function_params": None
    }
    
    
    def __init__(self, hparams:dict=None):
        """Typical Artificial Neural Network class, also known as multilayer perceptron. This class will create a fully connected feedforward artificial neural network.
        It can be used for classification, regression, etc. It basically encompasses enough options to build all kinds of ANNs with any number of 
        inputs, outputs, layers with custom or arbitrary width or depth, etc. Supports multiple activation functions for hidden layers and the output layer,
        but the activation function of the hidden layers are all the same.
        
        ### Usage
        `net = ANN(hparams)` where `hparams` is the dictionary of hyperparameters.

        It can include the following keys:
            - `input_size` (int): number of inputs to the ANN, i.e. size of the input layer.
            - `output_size` (int): number of outputs to predict, i.e. size of the output layer.
            - `width` (int|list): (list of) hidden layer widths. 
                a number sets them all the same, and a list/array sets each hidden layer according to the list.
            - `depth` (int): Specifies the depth of the network (number of hidden layers).
                It must be specified unless `width` is provided as a list. Then the depth will be inferred form it.
            - `hidden_activation` (str): (list of) Activations of the hidden layers. Examples include "ReLU", "LeakuReLU", "Sigmoid", "Tanh", "Softmax", "LogSoftmax", etc.
            - `hidden_activation_params` (dict): (list of) Parameters for the hidden activation function, if any.
            - `output_activation` (str): Activation of the output layer, if any.
                **Note**: For classification problems, you may want to choose "Sigmoid", "Softmax" or "LogSoftmax".
                That being said, you usually don't need to specify an activation for the output layer at all.
                Some loss functions in PyTorch have the classification activation functions embedded in them.
                **Note**: For regression problems, no activation is needed. It is by default linear, unless you want to manually specify an activation.
            - `output_activation_params` (dict): Parameters for the output activation function, if any.
            - `norm_layer_type` (str): (list of) Types of normalization layers to use for each hidden layer. Options are "BatchNorm1d", "LayerNorm", "GroupNorm", etc.
            - `norm_layer_position` (str): (list of) where the normalization layer should be included relative to the activation function.
            - `norm_layer_params` (dict): (list of) Dictionaries of parameters for the normalization layers.
            - `dropout` (float): (list of) the dropout rates after every hidden layer. It should be a probability value between 0 and 1.
            - `learning_rate` (float): Initial learning rate of training.
            - `learning_rate_decay_gamma` (float): Exponential decay rate gamma for learning rate, if any.
            - `optimizer` (str): Optimizer. Examples: "Adam", "SGD" ,"RMSProp", etc.
            - `optimizer_params` (dict): Additional parameters of the optimizer, if any.
            - `batch_size` (int): Minibatch size for training.
            - `epochs` (int): Maximum number of epochs for training.
            - `validation_tolerance_epochs` (int): Epochs to tolerate unimproved val loss, before early stopping.
            - `validation_data` (list): List of [validation_split, 'trainset'|'testset'].
            - `l2_reg` (float): L2 regularization parameter.
            - `loss_function` (str): Loss function. Examples: "MSELoss", "BCELoss", "CrossEntropyLoss", etc.
            - `loss_function_params` (dict): Additional parameters for the loss function, if any.
        
        Note that for all such hyperparameters that have a (list of) at the beginning, the entry can be a single item repeated for all hidden layers, or it can be a list of items
        for all hidden layers. If a list is provided, it must have the same length as the depth of the network. Also note that depth does not include the input and output layers.
        This gives you the ability to specify different width, dropout rate, normalization layer and its parameters, and so forth.
        
        Also note that the hidden layer just before the output layer will not have any dropout, which is typical.

        ### Returns
        It returns a `torch.nn.Module` object that corresponds with an ANN model.
        run `print(net)` afterwards to see what the ANN holds.
        The returned module is a `PyTorchSmartModule` object, which is a subclass of `torch.nn.Module`. It has built-in functions for training, evaluation, prediction, etc.
        """
        super(ANN, self).__init__(hparams)
        # Read and store hyperparameters
        layers = []
        self._insize = hparams["input_size"]
        self._outsize = hparams["output_size"]
        self._dropout = hparams.get("dropout")
        self._width = hparams.get("width")
        self._depth = hparams.get("depth")
        self._denseactivation = actdict_pytorch[hparams["hidden_activation"]]
        self._denseactivation_params = hparams.get("hidden_activation_params")
        self._outactivation = actdict_pytorch[hparams.get("output_activation")] if hparams.get("output_activation") else None
        self._outactivation_params = hparams.get("output_activation_params")
        self._norm_layer_type = hparams.get("norm_layer_type")
        self._norm_layer_position = hparams.get("norm_layer_position")
        self._norm_layer_params = hparams.get("norm_layer_params")
        self.batch_input_shape = (self._batch_size, self._insize)
        self.batch_output_shape = (self._batch_size, self._outsize)
        
        # Generate arrays containing parameters of each Dense Block (Every block contains a linear, normalization, activation, and dropout layer).
        self._dense_width_vec = self._gen_hparam_vec_for_dense(self._width, 'width')
        self._dense_activation_vec = self._gen_hparam_vec_for_dense(self._denseactivation, 'hidden_activation')
        self._dense_activation_params_vec = self._gen_hparam_vec_for_dense(self._denseactivation_params, 'hidden_activation_params')
        self._dense_norm_layer_type_vec = self._gen_hparam_vec_for_dense(self._norm_layer_type, 'norm_layer_type')
        self._dense_norm_layer_params_vec = self._gen_hparam_vec_for_dense(self._norm_layer_params, 'norm_layer_params')
        self._dense_norm_layer_position_vec = self._gen_hparam_vec_for_dense(self._norm_layer_position, 'norm_layer_position')
        self._dense_dropout_vec = self._gen_hparam_vec_for_dense(self._dropout, 'dropout')
        
        # Construct the dense layers
        in_size = self._insize
        for i in range(self._depth):
            out_size = self._dense_width_vec[i]
            temp_dropout_rate = self._dense_dropout_vec[i] if (i != self._depth-1) else None # The hidden layer just before the output layer rarely has Dropout.
            layers.append(Dense_Block(in_size, out_size, self._dense_activation_vec[i], self._dense_activation_params_vec[i], 
                                            self._dense_norm_layer_type_vec[i], self._dense_norm_layer_position_vec[i], self._dense_norm_layer_params_vec[i], temp_dropout_rate))
            in_size = out_size
        
        # Output layer
        layers.append(nn.Linear(out_size, self._outsize))
        if self._outactivation:
            if self._outactivation_params:
                layers.append(getattr(nn, self._outactivation)(**self._outactivation_params))
            else:
                layers.append(getattr(nn, self._outactivation)())
        
        # Sequentiating the layers
        self.net = nn.Sequential(*layers)

    def _gen_hparam_vec_for_dense(self, hparam, hparam_name, **kwargs):
        return generate_array_for_hparam(hparam, self._depth, hparam_name=hparam_name, count_if_not_list_name='depth', **kwargs)
        
    def forward(self, x):
        return self.net(x)

