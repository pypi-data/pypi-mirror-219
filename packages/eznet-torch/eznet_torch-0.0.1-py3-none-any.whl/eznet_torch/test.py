
if __name__=="eznet_torch.test":
    from .utils import *
    from .models import *
else:
    from utils import *
    from models import *



def test_calc_image_size():
    size = calc_image_size(size_in=[28,28,28], kernel_size=3, padding='valid', stride=2, dilation=1)
    print(size)

def test_generate_geometric_array():
    array = generate_geometric_array(init=256, count=4, direction='up', powers_of_two=True)
    print(array)
    
def test_generate_array_for_hparam():
    array = generate_array_for_hparam(
        [1,2], count_if_not_list=4, 
        hparam_name='parameter', count_if_not_list_name='its count',
        check_auto=True, init_for_auto=2, powers_of_two_if_auto=True,
        direction_if_auto='up')
    print(array)

def test_dense_block():
    dense_block = Dense_Block(256, 128, 'ReLU', None, 'BatchNorm1d', 'before', None, 0.1)
    print(dense_block)
    x = torch.randn(32,256)
    y = dense_block(x)
    print("Input shape:  ", x.shape)
    print("Output shape: ", y.shape)

def test_conv_block():
    conv_block = Conv_Block(3, 32, conv_dim=2, input_image=[28,28], conv_kernel_size=3, conv_padding='valid', conv_stride=1, conv_dilation=1, conv_params=None, 
                            conv_activation='ReLU', conv_activation_params=None, norm_layer_position='before', norm_layer_type='BatchNorm', norm_layer_params=None, 
                            pool_type='Max', pool_kernel_size=2, pool_padding=0, pool_stride=1, pool_dilation=1, pool_params=None, adaptive_pool_output_size= None, 
                            dropout=0.1, min_image_dim=8)
    print(conv_block)
    x = torch.randn(32,3,28,28)
    y = conv_block(x)
    print("Input shape:  ", x.shape)
    print("Output shape: ", y.shape)
    
def test_conv_network():
    test_pytorch_model_class(Conv_Network)

def test_recurrent_network():
    test_pytorch_model_class(Recurrent_Network)




if __name__ == '__main__':
    
    # test_calc_image_size()
    # test_generate_geometric_array()
    # test_generate_array_for_hparam()
    # test_dense_block()
    # test_conv_block()
    # test_conv_network()
    # test_recurrent_network()
    
    
    pass