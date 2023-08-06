if __package__=="eznet_torch.models":
    from ..utils import *
else:
    import os, sys
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(parent_dir)
    from utils import *
import warnings

class Conv_Block(nn.Module):
    def __init__(self, in_channels:int, out_channels:int=None, conv_dim:int=1, input_image:list=[30], conv_kernel_size=3, conv_padding='valid', conv_stride=1, conv_dilation=1, 
                 conv_params:dict=None, conv_activation:str='ReLU', conv_activation_params:dict=None, norm_layer_position:str=None, norm_layer_type:str=None, 
                 norm_layer_params:dict=None, pool_type:str=None, pool_kernel_size=2, pool_padding:int=0, pool_stride=1, pool_dilation=1, pool_params:dict=None, 
                 adaptive_pool_output_size=None, dropout:float=None, min_image_dim:int=1):
        """Convolutional block, containing one convolution layer, followed optionally by a normalization layer,
        an activation layer, a pooling layer and a dropout layer. The convolution layer is mandatory, but the other ones
        are optional. The convolution layer can be 1D, 2D or 3D. The normalization layer can be any such layer defined
        in PyTorch. The activation layer can also be anything, and the pooling layer can be any of the pooling layers
        defined for PyTorch. The dropout layer is a standard dropout layer. The dimension of any existing batch-norm and
        dropout layer will match the dimension of the convolution layer. For Conv1d, BatchNorm1d and Dropout1d will be
        used, if desired.
        
        This module is meant to be used as a building block for arger modules available here.

        ### Args:
        
        - `in_channels` (int): Channels of input image.
        - `out_channels` (int, optional): Number of convolution filters. Defaults to the input channels size.
        - `conv_dim` (int, optional): Dimension of the convolution. Defaults to 1. 1 means Conv1d, 2 means Conv2d etc.
        - `input_image` (list, optional): Size of the input image. Defaults to [30]. This must be a list/tuple of integers, with legth equal to `conv_dim`.
        - `conv_kernel_size` (int, optional): Convolution kernel size. Defaults to 3. It is strongly recommended to provide a list of integers, with length equal to `conv_dim`.
        - `conv_padding` (str, optional): Convolution padding. Defaults to 'same'. Arrays are recommended over integers.
        - `conv_stride` (int, optional): Convolution stride. Defaults to 1.
        - `conv_dilation` (int, optional): Convolution dilation. Defaults to 1.
        - `conv_params` (dict, optional): Additional dictionary of kwargs for Conv?d module. Defaults to None.
        - `conv_activation` (str, optional): String representing activation function. Defaults to 'ReLU'. Examples: 'LeakyReLU', 'Sigmoid', 'Tanh' etc.
        - `conv_activation_params` (dict, optional): kwargs dictionary for activation function. Defaults to None.
        - `norm_layer_position` (str, optional): Position of the normalization layer relative to activation. Defaults to None. It should be 'before' or 'after' or None.
        - `norm_layer_type` (str, optional): Type of the normalization layer. Defaults to None. Examples: 'BatchNorm', 'LayerNorm', etc.
        - `norm_layer_params` (dict, optional): kwargs dictionary for normalization layer. Defaults to None.
        - `pool_type` (str, optional): Type of pooling layer, if any. Defaults to None. For example, 'Max', 'Avg', 'AdaptiveMax', 'AdaptiveAvg' etc.
        - `pool_kernel_size` (int, optional): Pooling kernel size. Defaults to 2. Arrays are recommended over integers.
        - `pool_padding` (int, optional): Padding for pooling layer. Defaults to 0. 'same' is NOT an option here.
        - `pool_stride` (int, optional): Pooling stride. Defaults to 1.
        - `pool_dilation` (int, optional): Pooling dilation. Defaults to 1.
        - `pool_params` (dict, optional): kwargs dictionary for pooling layer module. Defaults to None.
        - `adaptive_pool_output_size` (list, optional): Output size for adaptive pooling, if any. Defaults to None.
        - `dropout` (float, optional): Dropout rate, if any. Defaults to None. for Conv?d, Dropout?d is used.
        - `min_image_dim` (int, optional): Minimum image dimension. Defaults to 1. This is used for preventing the image dimension from becoming too small. 
            It can automatically adjust padding and stride for convolution and pooling layers to keep the image dimensions larger than this argument.
        
        ### Returns:
        A `torch.nn.Module` instance representing a single convolutional block.
        
        ### Attributes:
        `self.output_image` (list): Size of the output image.
        `self.net` (torch.nn.Module): The actual network, a `torch.nn.Sequential` instance.
        """
        super(Conv_Block, self).__init__()
        # Input channels check
        assert isinstance(in_channels,int) and in_channels>0, "`in_channels` must be a positive integer, not {} which has type {}.".format(in_channels, str(type(in_channels)))
        self._in_channels = in_channels
        # Output channels check
        if isinstance(out_channels,int) and out_channels > 0:
            self._out_channels = out_channels
        else:
            warnings.warn("Invalid value out_channels={}. Using value {} equal to in_channels.".format(out_channels,in_channels), UserWarning)
            self._out_channels = in_channels
        # Convolution dimension check    
        assert isinstance(conv_dim, int) and conv_dim in [1,2,3], "`conv_dim` must be an integer among [1,2,3], not {} which has type {}.".format(conv_dim, str(type(conv_dim)))
        self._conv_dim = conv_dim
        # Determine convolution module used
        self._conv_module = convdict_pytorch["conv{}d".format(self._conv_dim)]
        # Iniput imager size check
        assert isinstance(input_image, (list,tuple)) and len(input_image)==self._conv_dim, \
            "`input_image` must be a list or tuple of length equal to `conv_dim`, not {} which has type {}.".format(input_image, str(type(input_image)))
        self._input_image = input_image
        # Store convolution parameters as class attributes
        self._conv_kernel_size = conv_kernel_size
        self._conv_padding = conv_padding
        self._conv_stride = conv_stride
        self._conv_dilation = conv_dilation
        self._conv_params = conv_params
        self._conv_activation = conv_activation
        # Check activation function and module
        self._conv_activation_module = getattr(nn, self._conv_activation) if self._conv_activation else None
        self._conv_activation_params = conv_activation_params
        # Check position, type and parameters of normalization layer
        if norm_layer_position in ['before', 'after', None]:
            self._norm_layer_position = norm_layer_position
        else:
            warnings.warn(("Invalid value {} for `norm_layer_position`: It can only be 'before' (before activation), 'after' (after activation) or None. "+
                          "Using default value of None. There will be no normalization.").format(norm_layer_position), UserWarning)
            self._norm_layer_position = None
        self._norm_layer_type = norm_layer_type
        if self._norm_layer_position is None: self._norm_layer_type = None
        if self._norm_layer_type is None: self._norm_layer_position = None
        self._norm_layer_params = norm_layer_params
        if self._norm_layer_type:
            self._norm_layer_module = getattr(nn, 'BatchNorm{}d'.format(self._conv_dim)) if 'BatchNorm' in self._norm_layer_type else getattr(nn, self._norm_layer_type)
        else:
            self._norm_layer_module = None
        # Check pooling layer type, module and parameters
        self._pool_type = pool_type
        self._pool_module = getattr(nn, "{}Pool{}d".format(self._pool_type, self._conv_dim)) if self._pool_type else None
        self._pool_kernel_size = pool_kernel_size
        self._pool_padding = pool_padding
        self._pool_stride = pool_stride
        self._pool_dilation = pool_dilation
        self._pool_params = pool_params
        self._adaptive_pool_output_size = adaptive_pool_output_size
        # Check Dropout parameters
        self._dropout = dropout if dropout else None
        self._dropout_module = getattr(nn, 'Dropout{}d'.format(self._conv_dim)) if self._dropout else None
        # Store minimum desired image size
        self._min_image_dim = min_image_dim if min_image_dim>0 else 1
        # Initialize vector of layers, and image size
        layers_vec = []
        img_size = self._input_image
        # -----------------------------------------------------------------------------        
        # Check if output image size is smaller than min_image_dim, and adjust parameters if necessary
        temp_img_size = calc_image_size(img_size, kernel_size=self._conv_kernel_size, stride=self._conv_stride, padding=self._conv_padding, dilation=self._conv_dilation)
        if min(temp_img_size) < self._min_image_dim:
            warnings.warn(
                "Output image is smaller in one or more dimensions than min_image_dim={} for Conv_Block. ".format(self._min_image_dim)+ 
                "Using padding='same' and stride=1 instead of padding={} and stride={}".format(self._conv_padding, self._conv_stride), UserWarning)
            self._conv_padding = 'same'
            self._conv_stride = 1
        # Construct convolutional layer
        if self._conv_params:
            layers_vec.append(self._conv_module(in_channels, out_channels, kernel_size=self._conv_kernel_size, 
            stride=self._conv_stride, padding=self._conv_padding, dilation=self._conv_dilation, **self._conv_params))
        else:
            layers_vec.append(self._conv_module(in_channels, out_channels, kernel_size=self._conv_kernel_size, 
            stride=self._conv_stride, padding=self._conv_padding, dilation=self._conv_dilation))
        # Calculate output image size
        img_size = calc_image_size(img_size, kernel_size=self._conv_kernel_size, stride=self._conv_stride, padding=self._conv_padding, dilation=self._conv_dilation)
        # ---------------------------------------------------------------------------
        # Construct normalization layer, if it should be here.
        if self._norm_layer_position=='before':
            if self._norm_layer_params:
                layers_vec.append(self._norm_layer_module(out_channels, **self._norm_layer_params))
            else:
                layers_vec.append(self._norm_layer_module(out_channels))
        # Construct activation layer
        if self._conv_activation:
            if self._conv_activation_params:
                layers_vec.append(self._conv_activation_module(**self._conv_activation_params))
            else:
                layers_vec.append(self._conv_activation_module())
        # Construct normalization layer, if it should be here.
        if self._norm_layer_position=='after':
            if self._norm_layer_params:
                layers_vec.append(self._norm_layer_module(out_channels, **self._norm_layer_params))
            else:
                layers_vec.append(self._norm_layer_module(out_channels))
        # ---------------------------------------------------------------------------
        # Check type and parameters of the pooling layer, and calculate output image size
        if self._pool_type is not None and 'adaptive' in self._pool_type.lower():
            assert self._adaptive_pool_output_size is not None, "adaptive_pool_output_size must be specified for adaptive pooling."
            if self._pool_params:
                layers_vec.append(self._pool_module(output_size=self._adaptive_pool_output_size, **self._pool_params))
            else:
                layers_vec.append(self._pool_module(output_size=self._adaptive_pool_output_size))
            img_size = list(self._adaptive_pool_output_size)
        elif self._pool_type is not None:
            temp_img_size = calc_image_size(img_size, kernel_size=self._pool_kernel_size, stride=self._pool_stride, padding=self._pool_padding, dilation=self._pool_dilation)
            if min(temp_img_size) < self._min_image_dim:
                warnings.warn(
                    "Output image is smaller in one or more dimensions than min_image_dim={} for Conv_Block. ".format(self._min_image_dim)+ 
                    "Using padding={} and stride=1 instead of padding={} and stride={}".format(self._pool_kernel_size//2, self._pool_padding, self._pool_stride), UserWarning)
                self._pool_padding = self._pool_kernel_size//2
                self._pool_stride = 1
            if self._pool_params:
                layers_vec.append(self._pool_module(kernel_size=self._pool_kernel_size, stride=self._pool_stride, padding=self._pool_padding, dilation=self._pool_dilation,
                                      **self._pool_params))
            else:
                layers_vec.append(self._pool_module(kernel_size=self._pool_kernel_size, stride=self._pool_stride, padding=self._pool_padding, dilation=self._pool_dilation))
            img_size = calc_image_size(img_size, kernel_size=self._pool_kernel_size, stride=self._pool_stride, padding=self._pool_padding, dilation=self._pool_dilation)
        # ---------------------------------------------------------------------------
        # Construct Dropout layer    
        if self._dropout: layers_vec.append(self._dropout_module(self._dropout))
        # Store output image size as attribute    
        self.output_image = img_size
        # Construct Sequential module
        self.net = nn.Sequential(*layers_vec)

    def forward(self, x):
        return self.net(x)
        