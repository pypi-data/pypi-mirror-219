
if __package__=="eznet_torch.models":
    from .pytorch_smart_module import *
    from .conv_block import *
    from .dense_block import *
else:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from pytorch_smart_module import *
    from conv_block import *
    from dense_block import *

class Conv_Network(PyTorchSmartModule):
    sample_hparams = {
        "model_name": "Conv_Network",
        # I/O shapes (without the batch dimension)
        "input_shape": [3, 28, 28],
        "output_shape": [10],
        # Convolution blocks
        "num_conv_blocks": 2,
        "conv_dim": 2,
        "conv_params": None,
        "conv_channels": "auto",
        "conv_kernel_size": 3,
        "conv_padding": "valid",
        "conv_stride": 1,
        "conv_dilation": 1,
        "conv_activation": "LeakyReLU",
        "conv_activation_params": {"negative_slope": 0.1},
        "conv_norm_layer_type": "BatchNorm",
        "conv_norm_layer_position": "before",
        "conv_norm_layer_params": None,
        "conv_dropout": 0.1,
        "pool_type": "Max",
        "pool_kernel_size": 2,
        "pool_padding": 0,
        "pool_stride": 1,
        "pool_dilation": 1,
        "pool_params": None,
        "min_image_size": 4,
        "adaptive_pool_output_size": None,
        # Fully connected blocks
        "dense_width": "auto",
        "dense_depth": 2,
        "dense_activation": "ReLU",
        "dense_activation_params": None,
        "output_activation": None,
        "output_activation_params": None,
        "dense_norm_layer_type": "BatchNorm1d",
        "dense_norm_layer_position": "before",
        "dense_norm_layer_params": None,
        "dense_dropout": 0.1,
        # Training procedure
        "l2_reg": 0.0001,
        "batch_size": 32,
        "epochs": 40,
        "validation_data": [0.05,'testset'],
        "validation_tolerance_epochs": 5,
        "learning_rate": 0.01,
        "learning_rate_decay_gamma": 0.9,
        "loss_function": "CrossEntropyLoss",
        "optimizer": "Adam",
        "optimizer_params": {"eps": 1e-07}
    }
    
    
    def __init__(self, hparams:dict=None):
        """Standard Convolutional Neural Network, containing convolutional blocks followed by fully-connected blocks.
        It supports 1D, 2D, and 3D convolutions, and can be used for image classification, timeseries classification,
        video classification, and so forth. The module can easily be trained and evaluated using its own methods,
        because it inherits from `PyTorchSmartModule`.

        ### Usage

        `model = Conv_Network(hparams)` where `hparams` is dictionary of hyperparameters containing the following:

        #### I/O shapes
        
        - `input_shape` (list): Input shape *WITHOUT* the batch dimension. For instance, for 2D images, input should be [N, C, H, W], therefore `input_shape` should be [C, H, W].
        - `output_shape` (int): Output shape *WITHOUT* the batch dimension. For instance, for K-class classification, model outputs can be [N, K], so `output_shape` should be [K].
            
        #### Convolution blocks
        
        - `num_conv_blocks` (int): Number of convolutional blocks. Every block contains a convolutional layer, and
            optionally a normalization layer, an activation layer, a pooling layer, and finally a dropout layer.
        - `conv_dim` (int): Dimensionality of the convolution. 1, 2, or 3.
        - `conv_params` (dict): kwargs dict to pass to the convolution constructor in *ALL* blocks. Defaults to None.
        - `conv_channels` (int|list|str): Number of filters of the convolution layers. If `auto`, it will start
            with the input channels, and double with every block, in powers of two. If `list`, it should be a list
            of channels for each conv block. If `int`, it will be the same for all conv blocks. Default is `auto`.
        - `conv_kernel_size` (int|list): Kernel size of the convolution layers. Should be a list of integers,
            a list of tuples of integers (for conv2d or conv3d), or an integer. If it is a list, it MUST have the same 
            length as `num_conv_blocks`. If it is an integer, it will be the same for all conv blocks. Defaults to 3.
        - `conv_padding` (int|str|list): Padding of convolution layers. Format is as `conv_kernel_size`. Defaults to "valid".
        - `conv_stride` (int|list): Stride of convolution layers. Format is as `conv_kernel_size`. Defaults to 1.
        - `conv_dilation` (int|list): Dilation of convolution layers. Format is as `conv_kernel_size`. Defaults to 1.
        - `conv_activation` (str|list): (list of) string(s) representing activation func of the convolution layers. Examples: 'ReLU', 'LeakyReLU', 'Sigmoid', 'Tanh', etc.
        - `conv_activation_params` (dict|list): (list of) dicts for the convolution activation functions' constructors. Defaults to None.
        - `conv_norm_layer_type` (str|list): (list of) types of normalization layers to use in the conv blocks. Examples: 'BatchNorm', 'LayerNorm', etc.
            If 'BatchNorm' is used, its dimensionality will match that of `conv_dim`. Defaults to None.
        - `conv_norm_layer_position` ("before"|"after"|list): (list of) positions of the normalization layers in the 
            convolutional blocks relative to the activation functions. Defaults to "before". If it is a list, it should be a list of strings of the same length as `num_conv_blocks`
        - `conv_norm_layer_params` (dict|list): kwargs dict for the convolution normalization layers' constructors. Defaults to None.    
        - `conv_dropout` (float|list): (list of) Dropout rates of the convolution blocks. Defaults to None.
        - `pool_type` (str|list): (list of) types of pooling layer. "Max", "Avg", "AdaptiveMax", "AdaptiveAvg", etc. Defaults to None, in which case there will be no pooling layer.
        - `pool_kernel_size` (int|list): (list of) kernel sizes of the pooling layers, with similar format to 
            `conv_kernel_size`. Again, it can be a list of integers, a list of tuples of integers, or an integer.
        - `pool_padding` (int|list): (list of) paddings of the pooling layers.
        - `pool_stride` (int|list): (list of) strides of the pooling layers.
        - `pool_dilation` (int|list): (list of) dilations of the pooling layers.
        - `pool_params` (dict|list): (list of) kwargs dicts for the pooling layers' constructors.
        - `adaptive_pool_output_size` (int|list): (list of) output sizes of the adaptive pooling layers, if any.
            If it is a list, it should contain one element (integer or tuple) per adaptive pooling layer.
        - `min_image_size` (int): Minimum size of the image to be reduced to in convolutions and poolings.
            After this point, the padding and striding will be chosen such that image size does not decrease further. Defaults to 1.
            
        #### Dense blocks
        
        - `dense_width` ("auto"|int|list): Width of the hidden layers of the Dense network. "auto", a number (for all of them) or a list holding width of each hidden layer.
            If "auto", it will start with the output size of the Flatten() layer, halving at every Dense block.
        - `dense_depth` (int): Depth (number of hidden layers) of the Dense network.
        - `dense_activation` (str|list): (list of) activation function for hidden layers of the Dense network. Examples: 'ReLU', 'LeakyReLU', 'Sigmoid', 'Tanh', etc.
        - `dense_activation_params` (dict|list): (list of) dicts for the dense activation functions' constructors.
        - `output_activation` (str): Activation function for the output layer of the Dense network, if any.
            **NOTE** If the loss function is cross entropy, then no output activation is erquired. However, if the loss function is `NLLLoss` (negative loglikelihood), 
            then you MUST specify an output activation as in `LogSoftmax`.
        - `output_activation_params` (dict): Dictionary of parameters for the output activation function's constructor.
        - `dense_norm_layer_type` (str|list): (list of) types of normalization layers to use in the dense blocks. Examples: 'BatchNorm', 'LayerNorm', etc.
            If 'BatchNorm' is used, it will be `BatchNorm1d`. Defaults to None, in which case no normalization layer will be used.
        - `dense_norm_layer_position` ("before"|"after"|list): (list of) positions of the normalization layers in the dense blocks relative to the activation functions. 
            Defaults to "before". If it is a list, it should be a list of strings of the same length as `dense_depth`.
        - `dense_norm_layer_params` (dict|list): (list of) kwargs dict for the dense normalization layers' constructors.
        - `dense_dropout` (float|list): (list of) Dropout rates (if any) for the hidden layers of the Dense network.
        
        #### Training procedure
        
        - `batch_size` (int): Minibatch size, the expected input size of the network.
        - `learning_rate` (float): Initial learning rate of training.
        - `learning_rate_decay_gamma` (float): Exponential decay rate gamma for learning rate, if any.
        - `optimizer` (str): Optimizer. Examples: 'Adam', 'SGD', 'RMSprop', etc.
        - `optimizer_params` (dict): Additional parameters of the optimizer, if any.
        - `epochs` (int): Maximum number of epochs for training.
        - `validation_tolerance_epochs` (int): Epochs to tolerate unimproved val loss, before early stopping.
        - `l2_reg` (float): L2 regularization parameter.
        - `loss_function` (str): Loss function. Examples: 'CrossEntropyLoss', 'NLLLoss', 'MSELoss', etc.
        - `loss_function_params` (dict): Additional parameters for the loss function, if any.
        - `validation_data` (tuple): Validation data, if any. It should be a tuple of (portion, from_dataset). For instance, [0.05, 'testset'] means 5% of the testset will be used 
            for validation.The second element of the tuple can only be 'trainset' and 'testset'. The first element must be a float between 0 and 1. 
            If the second element is not specified, testset will be used by default.
        
        ### Returns
        
        - Returns a `nn.Module` object that can be trained and used accordingly.
        - Run `print(net)` afterwards to see what you have inside the network.
        - A `PyTorchSmartModule` object is returned, which is a subclass of `nn.Module`. This module has its own functions for training, evaluation, etc.
        """
        super(Conv_Network, self).__init__(hparams)
        if not hparams: hparams = self.sample_hparams
        # Input and output shapes
        self.model_name = hparams["model_name"] if hparams.get("model_name") else "Conv_Network"
        self.input_shape = hparams["input_shape"]
        self.output_shape = hparams["output_shape"]
        self._N = int(hparams["batch_size"])
        self.batch_input_shape = list(self.input_shape).copy()
        self.batch_input_shape.insert(0, self._N)
        self.batch_output_shape = list(self.output_shape).copy()
        self.batch_output_shape.insert(0, self._N)
        self.size_list = [self.input_shape]
        modules_list = []
        
        # Convolutional layers hyperparameters
        self._num_conv_blocks = hparams.get("num_conv_blocks")
        self._conv_dim = hparams.get("conv_dim")
        self._conv_params = hparams.get("conv_params")    
        self._conv_channels = hparams.get("conv_channels") if hparams.get("conv_channels") else "auto"
        self._conv_kernel_size = hparams.get("conv_kernel_size") if hparams.get("conv_kernel_size") else 3
        self._conv_padding = hparams["conv_padding"] if hparams.get("conv_padding") else "valid"
        self._conv_stride = hparams["conv_stride"] if hparams.get("conv_stride") else 1
        self._conv_dilation = hparams["conv_dilation"] if hparams.get("conv_dilation") else 1
        self._conv_activation = hparams["conv_activation"] if hparams.get("conv_activation") else "relu"
        self._conv_activation_params = hparams.get("conv_activation_params")
        self._conv_norm_layer_type = hparams.get("conv_norm_layer_type")
        self._conv_norm_layer_position = hparams.get("conv_norm_layer_position")
        self._conv_norm_layer_params = hparams.get("conv_norm_layer_params")
        self._conv_dropout = hparams.get("conv_dropout")
        self._pool_type = hparams.get("pool_type")
        self._pool_kernel_size = hparams.get("pool_kernel_size") if hparams.get("pool_kernel_size") else 2
        self._pool_padding = hparams["pool_padding"] if hparams.get("pool_padding") else 0
        self._pool_stride = hparams["pool_stride"] if hparams.get("pool_stride") else 1
        self._pool_dilation = hparams["pool_dilation"] if hparams.get("pool_dilation") else 1
        self._pool_params = hparams.get("pool_params")
        self._min_image_size = hparams["min_image_size"] if hparams.get("min_image_size") else 1
        self._adaptive_pool_output_size = hparams.get("adaptive_pool_output_size")
        
        
        # Generate lists of hyperparameters for conv/pool layers
        self._conv_channels_vec = self._gen_hparam_vec_for_conv(self._conv_channels, "conv_channels", 
            check_auto=True, init_for_auto=self.input_shape[0], powers_of_two_if_auto=True, direction_if_auto="up")
        self._conv_kernel_size_vec = self._gen_hparam_vec_for_conv(self._conv_kernel_size, "conv_kernel_size")
        self._pool_kernel_size_vec = self._gen_hparam_vec_for_conv(self._pool_kernel_size, 'pool_kernel_size')
        self._conv_padding_vec = self._gen_hparam_vec_for_conv(self._conv_padding, 'conv_padding')
        self._pool_padding_vec = self._gen_hparam_vec_for_conv(self._pool_padding, 'pool_padding')
        self._conv_stride_vec = self._gen_hparam_vec_for_conv(self._conv_stride, 'conv_stride')
        self._pool_stride_vec = self._gen_hparam_vec_for_conv(self._pool_stride, 'pool_stride')
        self._conv_dilation_vec = self._gen_hparam_vec_for_conv(self._conv_dilation, 'conv_dilation')
        self._pool_dilation_vec = self._gen_hparam_vec_for_conv(self._pool_dilation, 'pool_dilation')
        self._conv_activation_vec = self._gen_hparam_vec_for_conv(self._conv_activation, 'conv_activation')
        self._conv_activation_params_vec = self._gen_hparam_vec_for_conv(self._conv_activation_params, 'conv_activation_params')
        self._pool_type_vec = self._gen_hparam_vec_for_conv(self._pool_type, 'pool_type')
        self._pool_params_vec = self._gen_hparam_vec_for_conv(self._pool_params, 'pool_params')
        self._conv_params_vec = self._gen_hparam_vec_for_conv(self._conv_params, 'conv_params')
        self._adaptive_pool_output_size_vec = self._gen_hparam_vec_for_conv(self._adaptive_pool_output_size, 'adaptive_pool_output_size')
        self._conv_norm_layer_type_vec = self._gen_hparam_vec_for_conv(self._conv_norm_layer_type, 'conv_norm_layer_type')
        self._conv_norm_layer_params_vec = self._gen_hparam_vec_for_conv(self._conv_norm_layer_params, 'conv_norm_layer_params')
        self._conv_norm_layer_position_vec = self._gen_hparam_vec_for_conv(self._conv_norm_layer_position, 'conv_norm_layer_position')
        self._conv_dropout_vec = self._gen_hparam_vec_for_conv(self._conv_dropout, 'conv_dropout')
        
        # Constructing the encoder (convolutional blocks)
        # print("input_shape: ", self.input_shape)
        in_channels = self.input_shape[0]
        input_image = list(self.input_shape[1:])
        for i in range(self._num_conv_blocks):
            out_channels = self._conv_channels_vec[i]
            # print("in_channels: ", in_channels)
            # print("out_channels: ", out_channels)
            # print("input_image: ", input_image)
            block = Conv_Block(in_channels, out_channels, self._conv_dim, input_image, self._conv_kernel_size_vec[i], self._conv_padding_vec[i], self._conv_stride_vec[i], 
                 self._conv_dilation_vec[i], self._conv_params_vec[i], self._conv_activation_vec[i], self._conv_activation_params_vec[i], self._conv_norm_layer_position_vec[i], 
                 self._conv_norm_layer_type_vec[i],  self._conv_norm_layer_params_vec[i], self._pool_type_vec[i], self._pool_kernel_size_vec[i], 
                 self._pool_padding_vec[i], self._pool_stride_vec[i], self._pool_dilation_vec[i], self._pool_params_vec[i], self._adaptive_pool_output_size_vec[i], 
                 self._conv_dropout_vec[i], self._min_image_size)
            modules_list.append(block)
            output_image = block.output_image
            self.size_list.append([out_channels]+output_image)
            in_channels = out_channels
            input_image = output_image
            
        # Flattening (Image embedding)
        modules_list.append(nn.Flatten())
        self._dense_input_size = np.prod(output_image) * out_channels
        self.size_list.append([self._dense_input_size])
        
        # Dense layers hyperparameters
        self._dense_width = hparams["dense_width"]
        self._dense_depth = hparams["dense_depth"]
        self._dense_activation = hparams["dense_activation"] if hparams.get("dense_activation") else "ReLU"
        self._dense_activation_params = hparams.get("dense_activation_params")
        self._output_activation = hparams.get("output_activation") if hparams.get("output_activation") else None
        self._output_activation_params = hparams.get("output_activation_params")
        self._dense_norm_layer_type = hparams.get("dense_norm_layer_type")
        self._dense_norm_layer_params = hparams.get("dense_norm_layer_params")
        self._dense_norm_layer_position = hparams.get("dense_norm_layer_position")
        self._dense_dropout = hparams.get("dense_dropout")
        
        # Generate lists of hyperparameters for the dense layers
        self._dense_width_vec = self._gen_hparam_vec_for_dense(self._dense_width, 'dense_width',
            check_auto=True, init_for_auto=self._dense_input_size, powers_of_two_if_auto=True, direction_if_auto="down")
        self._dense_activation_vec = self._gen_hparam_vec_for_dense(self._dense_activation, 'dense_activation')
        self._dense_activation_params_vec = self._gen_hparam_vec_for_dense(self._dense_activation_params, 'dense_activation_params')
        self._dense_norm_layer_type_vec = self._gen_hparam_vec_for_dense(self._dense_norm_layer_type, 'dense_norm_layer_type')
        self._dense_norm_layer_params_vec = self._gen_hparam_vec_for_dense(self._dense_norm_layer_params, 'dense_norm_layer_params')
        self._dense_norm_layer_position_vec = self._gen_hparam_vec_for_dense(self._dense_norm_layer_position, 'dense_norm_layer_position')
        self._dense_dropout_vec = self._gen_hparam_vec_for_dense(self._dense_dropout, 'dense_dropout')
        
        # Construct the dense layers
        in_size = self._dense_input_size
        for i in range(self._dense_depth):
            out_size = self._dense_width_vec[i]
            temp_dropout_rate = self._dense_dropout_vec[i] if (i != self._dense_depth-1) else None # The hidden layer just before the output layer rarely has Dropout.
            modules_list.append(Dense_Block(in_size, out_size, self._dense_activation_vec[i], self._dense_activation_params_vec[i], 
                                            self._dense_norm_layer_type_vec[i], self._dense_norm_layer_position_vec[i], self._dense_norm_layer_params_vec[i], temp_dropout_rate))
            in_size = out_size
            self.size_list.append([out_size])
        
        # Output layer
        modules_list.append(nn.Linear(in_size, self.output_shape[-1]))
        if self._output_activation:
            if self._output_activation_params:
                modules_list.append(getattr(nn, self._output_activation)(**self._output_activation_params))
            else:
                modules_list.append(getattr(nn, self._output_activation)())
        
        # Building Sequential Model
        self.net = nn.Sequential(*modules_list)

    
    def _gen_hparam_vec_for_conv(self, hparam, hparam_name, **kwargs):
        return generate_array_for_hparam(hparam, self._num_conv_blocks, 
                hparam_name=hparam_name, count_if_not_list_name='num_conv_blocks', **kwargs)
    
    def _gen_hparam_vec_for_dense(self, hparam, hparam_name, **kwargs):
        return generate_array_for_hparam(
            hparam, self._dense_depth, hparam_name=hparam_name, count_if_not_list_name='dense_depth', **kwargs)
    
    def forward(self, inputs):
        return self.net(inputs)


