
from pathlib import Path
import math
from timeit import default_timer as timer
from datetime import datetime
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split, Dataset, TensorDataset
from torch.nn.init import xavier_uniform_, zeros_, orthogonal_, calculate_gain
# Note: Custom random initializations should NOT be implemented without the gain values from calculate_gain.
from sklearn.metrics import r2_score
import numpy as np
from tqdm import tqdm

########################################################################################################################
# Global variables, functions, and classes
########################################################################################################################

# Set random seed
SEED = 42

def make_path(path:str):
    ''' Make a path if it doesn't exist.'''
    Path.mkdir(Path(path).parent, parents=True, exist_ok=True)
    return path


def autoname(name):
    """
    Genereate a unique name for a file, based on the current time and the given name.
    Gets the `name` as a string and adds the time stamp to the end of it before returning it.
    """
    return name + "_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


actdict_pytorch = {
    'relu':nn.ReLU, 'leakyrelu':nn.LeakyReLU, 'sigmoid':nn.Sigmoid, 'tanh':nn.Tanh, 'softmax':nn.Softmax, 'logsoftmax':nn.LogSoftmax,
    'softplus':nn.Softplus, 'softshrink':nn.Softshrink,'elu':nn.ELU, 'selu':nn.SELU, 'softsign':nn.Softsign, 'softmin':nn.Softmin, 'softmax2d':nn.Softmax2d}

lossdict_pytorch = {
    "mse":nn.MSELoss, "crossentropy":nn.CrossEntropyLoss, "binary_crossentropy":nn.BCELoss, "categorical_crossentropy":nn.CrossEntropyLoss, "nll":nn.NLLLoss, 
    "poisson":nn.PoissonNLLLoss, "kld":nn.KLDivLoss, "hinge":nn.HingeEmbeddingLoss, "l1":nn.L1Loss, "mae": nn.L1Loss, "l2":nn.MSELoss, "smoothl1":nn.SmoothL1Loss, 
    "bce_with_logits":nn.BCEWithLogitsLoss
}

optdict_pytorch = {'adam':optim.Adam, 'sgd':optim.SGD, 'rmsprop':optim.RMSprop}

convdict_pytorch = {'conv1d':nn.Conv1d, 'conv2d':nn.Conv2d, 'conv3d':nn.Conv3d}

pooldict_pytorch = {
    "maxpool1d": nn.MaxPool1d, "avgpool1d": nn.AvgPool1d, "adaptivemaxpool1d": nn.AdaptiveMaxPool1d, "adaptiveavgpool1d": nn.AdaptiveAvgPool1d,
    "maxpool2d": nn.MaxPool2d, "avgpool2d": nn.AvgPool2d, "adaptivemaxpool2d": nn.AdaptiveMaxPool2d, "adaptiveavgpool2d": nn.AdaptiveAvgPool2d,
    "maxpool3d": nn.MaxPool3d, "avgpool3d": nn.AvgPool3d, "adaptivemaxpool3d": nn.AdaptiveMaxPool3d, "adaptiveavgpool3d": nn.AdaptiveAvgPool3d}

normdict_pytorch = {
    "batchnorm1d": nn.BatchNorm1d, "batchnorm2d": nn.BatchNorm2d, "batchnorm3d": nn.BatchNorm3d, "instancenorm1d": nn.InstanceNorm1d, "instancenorm2d": nn.InstanceNorm2d, 
    "instancenorm3d": nn.InstanceNorm3d, "layernorm": nn.LayerNorm, "groupnorm": nn.GroupNorm, "localresponsenorm": nn.LocalResponseNorm,
}

dropoutdict_pytorch = {"dropout1d": nn.Dropout1d, "dropout2d": nn.Dropout2d, "dropout3d": nn.Dropout3d}



def calc_image_size(size_in:int, kernel_size:int, padding:int, stride:int, dilation:int):
    if padding == 'same':
        return size_in
    else:
        if padding == 'valid':
            padding = 0
        if isinstance(size_in, (list, tuple)):
            if isinstance(padding, int): padding = [padding]*len(size_in)
            if isinstance(kernel_size, int): kernel_size = [kernel_size]*len(size_in)
            if isinstance(stride, int): stride = [stride]*len(size_in)
            if isinstance(dilation, int): dilation = [dilation]*len(size_in)
            return [math.floor((size_in[i] + 2*padding[i] - dilation[i]*(kernel_size[i]-1) - 1)/stride[i] + 1) for i in range(len(size_in))]
        else:
            assert isinstance(size_in, int), "size_in must be an integer or a list/tuple of integers."
            assert isinstance(padding, int), "padding must be an integer or a list/tuple of integers."
            assert isinstance(kernel_size, int), "kernel_size must be an integer or a list/tuple of integers."
            assert isinstance(stride, int), "stride must be an integer or a list/tuple of integers."
            assert isinstance(dilation, int), "dilation must be an integer or a list/tuple of integers."
            return math.floor((size_in + 2*padding - dilation*(kernel_size-1) - 1)/stride + 1)


def generate_geometric_array(init, count, direction, powers_of_two=True):
    """Generate array filled with incrementally doubling/halving values, optionally with powers of two.

    ### Args:
        `init` (int): The first value to begin.
        `count` (int): Number of elements to generate.
        `direction` (str): Direction of the array. Can be either 'up' or 'down', i.e. increasing or decreasing.
        `powers_of_two` (bool, optional): Generate numbers that are powers of two. Defaults to True.

    ### Returns:
        list: List containing elements
    """
    lst = []
    old = int(2**math.ceil(math.log2(init))) if powers_of_two else init
    new = old
    for _ in range(count):
        lst.append(new)
        old = new
        new = (old * 2) if direction == 'up' else (old // 2)
    return lst


def generate_array_for_hparam(
    hparam, count_if_not_list:int, 
    hparam_name:str='parameter', count_if_not_list_name:str='its count',
    check_auto:bool=False, init_for_auto:int=2, powers_of_two_if_auto:bool=True,
    direction_if_auto:str=None):
    """Generate array for a hyperparameter, regardless of if it is a list or not. This function is for use in APIs
    that generate models with hyperparameters as inputs, which can be lists, a single item, or "auto".
    Examples include width of a neural network's hidden layers, channels of conv layers, etc.
    For these hyperparameters, the user is typically free to specify an array-like, a single item to be repeated,
    or "auto" for automatic calculation of the parameter.
    This function is meant to be used in the body of the code of class constructors and other functions in the API.

    ### Args:
        `hparam` (var): A specific hyperparameter, e.g., input by user to your network's constructor.
        `count_if_not_list` (int): Number of elements to generate if `hparam` is not an array-like.
        `hparam_name` (str, optional): Name of the hyperparameter. Defaults to 'parameter'.
        `count_if_not_list_name` (str, optional): Name of the "count" that must be provided. Defaults to 'its count'.
        `check_auto` (bool, optional): Check for the "auto" case. Defaults to False.
        `init_for_auto` (int, optional): Initial value in case of "auto". Defaults to 2.
        `powers_of_two_if_auto` (bool, optional): Generate powers of two in case of "auto". Defaults to True.
        `direction_if_auto` (str, optional): Direction of geometric increment in case of "auto". Defaults to None.
        This can be "up" or "down". If check_for_auto is True, then this argument must be specified.

    ### Returns:
        list: List containing elements
    """
    assert count_if_not_list is not None, \
        "Since %s may not be a list/tuple, %s must always be specified."%(hparam_name, count_if_not_list_name)
    if isinstance(hparam, (list,tuple)) and len(hparam) == count_if_not_list:
        lst = hparam
    elif hparam == "auto" and check_auto:
        assert init_for_auto is not None, \
            "If %s is 'auto', then %s must be specified."%(hparam_name, "init_for_auto")
        assert direction_if_auto in ['up','down'], \
            "If %s is 'auto', then %s must be specified as 'up' or 'down'."%(hparam_name, "direction_if_auto")
        lst = generate_geometric_array(init_for_auto, count_if_not_list, direction_if_auto, powers_of_two_if_auto)
    else:
        lst = [hparam]*count_if_not_list
    return lst




def generate_sample_batch(model):
    x = np.random.rand(*model.batch_input_shape).astype(np.float32)
    y = np.random.rand(*model.batch_output_shape).astype(np.float32)
    if model.hparams['loss_function'] in ['CrossEntroplyLoss', 'NLLLoss']:
        y = np.argmax(y, axis=1)
    return (x,y)


def test_pytorch_model_class(model_class):
    print("Constructing model...\n")
    model = model_class()
    print("Summary of model:")
    print(model)
    if model._loss_function in ['NLLLoss','CrossEntropyLoss','BCELoss']:
        classification = True
    print("\nGenerating random dataset...\n")
    (x_train, y_train) = generate_sample_batch(model)
    (x_val, y_val) = generate_sample_batch(model)
    x_train_t = torch.from_numpy(x_train)
    y_train_t = torch.from_numpy(y_train)
    x_val_t = torch.from_numpy(x_val)
    y_val_t = torch.from_numpy(y_val)
    # if classification:
    #     y_train_t = y_train_t.int()
    #     y_val_t = y_val_t.int()
    trainset = TensorDataset(x_train_t, y_train_t)
    validset = TensorDataset(x_val_t, y_val_t)
    dataset = (trainset, validset)
    print("\nTraining model...\n")
    model.train_model(dataset, verbose=1)
    print("\nEvaluating model...\n")
    print("Done.")
    

def _update_metrics_for_batch(
    predictions:torch.Tensor, targets:torch.Tensor, loss_str:str, classification:bool, regression:bool, 
    verbose:int, batch_num:int, epoch:int, metric:float, num_logits:int):
    if loss_str == "BCELoss":
        # Output layer already includes sigmoid.
        class_predictions = (predictions > 0.5).int()
    elif loss_str == "BCEWithLogitsLoss":
        # Output layer does not include sigmoid. Sigmoid is a part of the loss function.
        class_predictions = (torch.sigmoid(predictions) > 0.5).int()
    elif loss_str in ["NLLLoss", "CrossEntropyLoss"]:
        # nll -> Output layer already includes log_softmax.
        # crossentropy -> Output layer has no log_softmax. It's implemented as a part of the loss function.
        class_predictions = torch.argmax(predictions, dim=1)
        if predictions.shape == targets.shape: # Targets are one-hot encoded probabilities
            target_predictions = torch.argmax(targets, dim=1)
        else: # Targets are class indices
            target_predictions = targets

    if classification:
        if verbose>=2 and batch_num==0 and epoch ==0: 
            print("Shape of model outputs:     ", predictions.shape)
            print("Shape of class predictions: ", class_predictions.shape)
            print("Shape of targets:           ", targets.shape)
        # Calculate accuracy
        correct = (class_predictions == target_predictions).int().sum().item()
        num_logits += target_predictions.numel()
        metric += correct
        if verbose==3 and epoch==0: 
            print("Number of correct answers (this batch - total): %10d - %10d"%(correct, metric))
        # Calculate F1 score
        # f1 = f1_score(targets.cpu().numpy(), class_predictions.cpu().numpy(), average="macro")
    elif regression:
        if verbose==3 and batch_num==0 and epoch==0: 
            print("Shape of predictions: ", predictions.shape)
            print("Shape of targets:     ", targets.shape)
        # Calculate r2_score
        metric += r2_score(targets.cpu().numpy(), predictions.cpu().numpy())
    
    return metric, num_logits



def _test_shapes(predictions:torch.Tensor, targets:torch.Tensor, classification:bool):
    if classification:
        assert predictions.shape[0] == targets.shape[0], "Batch size of targets and predictions must be the same.\n"+\
            "Target shape: %s, Prediction shape: %s\n"%(str(targets.shape), str(predictions.shape))
        if len(predictions.shape) == 1:
            assert targets.shape == predictions.shape, "For 1D predictions, the targets must also be 1D.\n"+\
                "Predictions shape: %s, Targets shape: %s\n"%(str(predictions.shape), str(targets.shape))
        if len(predictions.shape) == 2:
            assert len(targets.shape)==1 or targets.shape == predictions.shape, \
                "For 2D predictions, the targets must be 1D class indices are 2D [N x K] one-hot encoded array, with the same shape as the predictions.\n"+\
                "Predictions shape: %s, Targets shape: %s\n"%(str(predictions.shape), str(targets.shape))
        if len(predictions.shape) > 2:
            assert len(predictions.shape)==len(targets.shape) or len(predictions.shape)==len(targets.shape)+1, \
                "Target dimensionality must be equal to or one less than the prediction dimensionality.\n"+\
                "Target shape: %s, Prediction shape: %s\n"%(str(targets.shape), str(predictions.shape))+\
                "If targets are class indices, they must be of shape (N,), or (N, d1, ..., dm). "+\
                "Otherwise, they must be (N, K) or (N, K, d1, ..., dm) arrays of one-hot encoded probabilities. "+\
                "Predictions must in any case be (N, K) or (N, K, d1, ..., dm).\n"+\
                "N is batch size, K is number of classes and d1 to dm are other dimensionalities of classification, if any."
            if len(predictions.shape) == len(targets.shape):
                assert predictions.shape == targets.shape, "If predictions and targets have the same dimensionality, they must be the same shape.\n"+\
                    "Target shape: %s, Prediction shape: %s\n"%(str(targets.shape), str(predictions.shape))
            else:
                assert predictions.shape[2:] == targets.shape[1:], \
                    "If predictions have shape (N, K, d1, ..., dm) then targets must either have the same shape, or (N, d1, ..., dm).\n"+\
                    "Target shape: %s, Prediction shape: %s\n"%(str(targets.shape), str(predictions.shape))
    else:
        assert predictions.shape == targets.shape, \
            "Target shape must be equal to the prediction shape.\n"+\
            "Target shape: %s, Prediction shape: %s\n"%(str(targets.shape), str(predictions.shape))




def _calculate_epoch_loss_and_metrics(
    cumulative_epoch_loss:float, num_batches:int, verbose:int, epoch:int, 
    hist_loss:dict, hist_metric:dict, display_metrics:bool, cumulative_metric:float, metric_denominator:int):
    # Calculate training epoch loss
    epoch_loss = cumulative_epoch_loss / num_batches
    if verbose==3 and epoch==0: print("Epoch loss (training): %.5f"%epoch_loss)
    if hist_loss is not None: hist_loss.append(epoch_loss)
    # Calculate training epoch metric (accuracy or r2-score)
    if display_metrics:
        epoch_metric = cumulative_metric / metric_denominator
        if verbose==3 and epoch==0: print("Epoch metric: %.5f"%epoch_metric)
        if hist_metric is not None: hist_metric.append(epoch_metric)
    return epoch_loss, epoch_metric, hist_loss, hist_metric



def save_pytorch_model(model:torch.nn.Module, saveto:str, dataloader=None, script_before_save:bool=True, verbose:int=1):
    try:
        if verbose > 0: print("Saving model...")
        if script_before_save:
            example,_ = next(iter(dataloader))
            example = example[0,:].unsqueeze(0)
            model.cpu()
            with torch.no_grad():
                traced = torch.jit.trace(model, example)
                traced.save(saveto)
        else:
            with torch.no_grad():
                torch.save(model, saveto)
    except Exception as e:
        if verbose > 0:
            print(e)
            print("Failed to save the model.")
    if verbose > 0: print("Done Saving.")
    
    
    

def train_pytorch_model(model, dataset, batch_size:int, loss_str:str, optimizer_str:str, optimizer_params:dict=None, loss_function_params:dict=None, learnrate:float=0.001, 
    learnrate_decay_gamma:float=None, epochs:int=10, validation_patience:int=10000, validation_data:float=0.1, verbose:int=1, script_before_save:bool=True, saveto:str=None, 
    num_workers=0):
    """Train a Pytorch model, given some hyperparameters.

    ### Args:
        - `model` (`torch.nn`): A torch.nn model
        - `dataset` (`torch.utils.data.Dataset`): Dataset object to be used
        - `batch_size` (int): Batch size
        - `loss_str` (str): Loss function to be used. Examples: "CrossEntropyLoss", "BCELoss", "BCEWithLogitsLoss", "MSELoss", etc.
        - `optimizer_str` (str): Optimizer to be used. Examples: "Adam", "SGD", "RMSprop", etc.
        - `optimizer_params` (dict, optional): Parameters for the optimizer.
        - `loss_function_params` (dict, optional): Parameters for the loss function.
        - `learnrate` (float, optional): Learning rate. Defaults to 0.001.
        - `learnrate_decay_gamma` (float, optional): Learning rate exponential decay rate. Defaults to None.
        - `epochs` (int, optional): Number of epochs. Defaults to 10.
        - `validation_patience` (int, optional): Number of epochs to wait before stopping training. Defaults to 10000.
        - `validation_data` (float, optional): Fraction of the dataset to be used for validation. Defaults to 0.1.
        - `verbose` (int, optional): Logging the progress. Defaults to 1. 0 prints nothing, 2 prints everything.
        - `script_before_save` (bool, optional): Use TorchScript for serializing the model. Defaults to True.
        - `saveto` (str, optional): Save PyTorch model in path. Defaults to None.
        - `num_workers` (int, optional): Number of workers for the dataloader. Defaults to 0.
        
    ### Returns:
        - `model`: Trained PyTorch-compatible model
        - `history`: PyTorch model history dictionary, containing the following keys:
            - `training_loss`: List containing training loss values of epochs.
            - `validation_loss`: List containing validation loss values of epochs.
            - `learning_rate`: List containing learning rate values of epochs.
            - `training_metrics`: List containing training metric values of epochs.
            - `validation_metrics`: List containing validation metric values of epochs.
    """
    # Initialize necessary lists
    hist_training_loss = []
    hist_validation_loss = []
    hist_learning_rate = []
    hist_trn_metric = []
    hist_val_metric = []
    
    # Empty CUDA cache
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    
    # Check if validation data is provided or not, and calculate number of training and validation data
    if isinstance(dataset, (list, tuple)):
        assert len(dataset)==2, "If dataset is a tuple, it must have only two elements, the training dataset and the validation dataset."
        trainset, valset = dataset
        num_val_data = int(len(valset))
        num_train_data = int(len(trainset))
        num_all_data = num_train_data + num_val_data
    else:
        num_all_data = len(dataset)
        num_val_data = int(validation_data*num_all_data)
        num_train_data = num_all_data - num_val_data
        (trainset, valset) = random_split(dataset, (num_train_data, num_val_data), generator=torch.Generator().manual_seed(SEED))

    if verbose > 0:
        print("Total number of data points:      %d"%num_all_data)
        print("Number of training data points:   %d"%num_train_data)
        print("Number of validation data points: %d"%num_val_data)
    
    # Generate training and validation dataloaders    
    trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    validloader = DataLoader(valset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    
    if verbose > 0:
        print("Number of training batches:    %d"%len(trainloader))
        print("Number of validation batches:  %d"%len(validloader))
        print("Batch size:                    %d"%batch_size)
        for x,y in trainloader:
            print("Shape of training input from the dataloader:  ", x.shape)
            print("Shape of training output from the dataloader: ", y.shape)
            break
        for x,y in validloader:
            print("Shape of validation input from the dataloader:  ", x.shape)
            print("Shape of validation output from the dataloader: ", y.shape)
            break
    
    # Select the device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    if verbose > 0: print("Selected device: ", device)
    model.to(device)
    
    # Instantiate the loss function
    loss_func = getattr(nn, loss_str)
    criterion = loss_func(**loss_function_params) if loss_function_params else loss_func()
        
    # Instantiate the optimizer
    optimizer_func = getattr(optim, optimizer_str)
    optimizer = optimizer_func(model.parameters(), lr=learnrate, **optimizer_params) if optimizer_params else optimizer_func(model.parameters(), lr=learnrate)
    
    # Defining learning rate scheduling
    if learnrate_decay_gamma:
        if verbose > 0: print("The learning rate has an exponential decay rate of %.5f."%learnrate_decay_gamma)
        scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=learnrate_decay_gamma)
        lr_sch = True
    else:
        lr_sch = False
    
    # Find out if we will display any metric along with the loss.
    display_metrics = True
    classification = False
    regression = False
    if loss_str in ["BCELoss", "BCEWithLogitsLoss", "CrossEntropyLoss", "NLLLoss", "PoissonNLLLoss", "GaussianNLLLoss"]:
        classification = True
        regression = False
        trn_metric_name = "Acc"
        val_metric_name = "Val Acc"
    elif loss_str in ["MSELoss", "L1Loss", "L2Loss", "HuberLoss", "SmoothL1Loss"]:
        classification = False
        regression = True
        trn_metric_name = "R2"
        val_metric_name = "Val R2"
    else:
        classification = False
        regression = False
        display_metrics = False
    if verbose > 0:
        if classification: print("Classification problem detected. We will look at accuracies.")
        elif regression: print("Regression problem detected. We will look at R2 scores.")
        else: print("We have detected neither classification nor regression problem. No metric will be displayed other than loss.")
    
                    
    # Calculating number of training and validation batches
    num_training_batches = len(trainloader)
    num_validation_batches = len(validloader)
    
    # Preparing progress bar
    progress_bar_size = 40
    ch = "█"
    intvl = num_training_batches/progress_bar_size;
    valtol = validation_patience if validation_patience else 100000000
    minvalerr = 10000000000.0
    badvalcount = 0
    
    # Commencing training loop
    tStart = timer()
    loop = tqdm(range(epochs), desc='Training Progress', ncols=100) if verbose==1 else range(epochs)
    for epoch in loop:
        
        # Initialize per-epoch variables
        tEpochStart = timer()
        epoch_loss_training = 0.0
        epoch_loss_validation = 0.0
        newnum = 0
        oldnum = 0
        trn_metric = 0.0
        val_metric = 0.0
        num_train_logits = 0
        num_val_logits = 0
    
        if verbose>=2 and epoch > 0: print("Epoch %3d/%3d ["%(epoch+1, epochs), end="")
        if verbose==3 and epoch ==0: print("First epoch ...")
        
        ##########################################################################
        # Training
        if verbose==3 and epoch==0: print("\nTraining phase ...")
        model.train()
        for i, data in enumerate(trainloader):
            # Fetch data
            seqs, targets = data[0].to(device), data[1].to(device)
            # Forward propagation
            predictions = model(seqs)
            # Test shapes
            _test_shapes(predictions, targets, classification)
            # Loss calculation and accumulation
            loss = criterion(predictions, targets)
            epoch_loss_training += loss.item()
            # Backpropagation and optimizer update
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # Metrics calculation
            if display_metrics:
                with torch.no_grad():
                    trn_metric, num_train_logits = _update_metrics_for_batch(
                        predictions, targets, loss_str, classification, regression, verbose, i, epoch, trn_metric, num_train_logits)
                    
            # Visualization of progressbar within the batch
            if verbose>=2 and epoch > 0:
                newnum = int(i/intvl)
                if newnum > oldnum:
                    print((newnum-oldnum)*ch, end="")
                    oldnum = newnum 
        
        # Update learning rate if necessary
        if lr_sch: scheduler.step()
        
        # Calculate epoch loss and metrics
        epoch_loss_training, trn_metric, hist_training_loss, hist_trn_metric = _calculate_epoch_loss_and_metrics(epoch_loss_training, num_training_batches, verbose, epoch, 
            hist_training_loss, hist_trn_metric, display_metrics, trn_metric, (num_train_logits if classification else num_training_batches))
            
        if verbose>=2 and epoch > 0: print("] ", end="")
        
        ##########################################################################
        # Validation
        if verbose==3 and epoch==0: print("\nValidation phase ...")
        model.eval()
        with torch.no_grad():
            for i, data in enumerate(validloader):
                seqs, targets = data[0].to(device), data[1].to(device)
                predictions = model(seqs)
                loss = criterion(predictions, targets)
                epoch_loss_validation += loss.item()
                # Do prediction for metrics
                if display_metrics:
                    val_metric, num_val_logits = _update_metrics_for_batch(
                        predictions, targets, loss_str, classification, regression, verbose, i, epoch, val_metric, num_val_logits)
        # Calculate epoch loss and metrics
        epoch_loss_validation, val_metric, hist_validation_loss, hist_val_metric = _calculate_epoch_loss_and_metrics(epoch_loss_validation, num_validation_batches, verbose, epoch, 
            hist_validation_loss, hist_val_metric, display_metrics, val_metric, (num_val_logits if classification else num_validation_batches))
        
        # Log the learning rate, if there is any scheduling.
        if lr_sch: hist_learning_rate.append(scheduler.get_last_lr()[0])
        else: hist_learning_rate.append(learnrate)
        
        ##########################################################################
        # Post Processing Training Loop            
        tEpochEnd = timer()
        if verbose>=2:
            if display_metrics:
                print("Loss: %5.4f |Val Loss: %5.4f |%s: %5.4f |%s: %5.4f | %6.3f s" % (
                    epoch_loss_training, epoch_loss_validation, trn_metric_name, trn_metric,val_metric_name, val_metric, tEpochEnd-tEpochStart))
            else:
                print("Loss: %5.4f |Val Loss: %5.4f | %6.3f s" % (epoch_loss_training, epoch_loss_validation, tEpochEnd-tEpochStart))
        
        # Checking for early stopping
        if epoch_loss_validation < minvalerr:
            minvalerr = epoch_loss_validation
            badvalcount = 0
        else:
            badvalcount += 1
            if badvalcount > valtol:
                if verbose > 0:
                    print("Validation loss not improved for more than %d epochs."%badvalcount)
                    print("Early stopping criterion with validation loss has been reached. " + 
                        "Stopping training at %d epochs..."%epoch)
                break
    # End for loop
    model.eval()
    ##########################################################################
    # Epilogue
    tFinish = timer()
    if verbose > 0:        
        print('Finished Training.')
        print("Training process took %.2f seconds."%(tFinish-tStart))
    if saveto:
       save_pytorch_model(model, saveto, trainloader, script_before_save, verbose)
    # Clear CUDA cache    
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    # Generate output dictionaries
    history = {
        'training_loss':hist_training_loss, 
        'validation_loss':hist_validation_loss, 
        'learning_rate':hist_learning_rate}
    if display_metrics:
        history["training_metrics"] = hist_trn_metric
        history["validation_metrics"] = hist_val_metric
    if verbose > 0: print("Done training.")
    
    return history




def evaluate_pytorch_model(model, dataset, loss_str:str, loss_function_params:dict=None, batch_size:int=16, device_str:str="cuda", verbose:bool=True, num_workers:int=0):
    """
    Evaluates a PyTorch model on a dataset.
    
    ### Parameters
    
    `model` (`torch.nn.Module`): The model to evaluate.
    `dataset` (`torch.utils.data.Dataset`): The dataset to evaluate the model on.
    `loss_str` (str): The loss function to use when evaluating the model.
    `loss_function_params` (dict, optional) : Parameters to pass to the loss function.
    `batch_size` (int, optional) : The batch size to use when evaluating the model. Defaults to 16.
    `device_str` (str, optional) : The device to use when evaluating the model. Defaults to "cuda".
    `verbose` (bool, optional) : Whether to print out the evaluation metrics. Defaults to True.
    `num_workers` (int, optional) : The number of workers to use when making dataloader. Defaults to 0.
    
    
    ### Returns
    
    A dictionary containing the evaluation metrics, including "loss" and "metrics" in case any metric is available.
    """
    # Clear CUDA cache
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    
    if verbose: print("Preparing data...")
    testloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    num_batches = len(testloader)
        
    if "cuda" in device_str:
        device = torch.device(device_str if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(device_str)
    
    print("selected device: ", device)
    model.eval()
    model.to(device)
    
    loss_func = getattr(nn, loss_str)
    criterion = loss_func(**loss_function_params) if loss_function_params else loss_func()
    
    display_metrics = True
    classification = False
    regression = False
    if loss_str in ["BCELoss", "BCEWithLogitsLoss", "CrossEntropyLoss", "NLLLoss", "PoissonNLLLoss", "GaussianNLLLoss"]:
        classification = True
        regression = False
        metric_name = "Accuracy"
    elif loss_str in ["MSELoss", "L1Loss", "L2Loss", "HuberLoss", "SmoothL1Loss"]:
        classification = False
        regression = True
        metric_name = "R2-Score"
    else:
        classification = False
        regression = False
        display_metrics = False
        
    progress_bar_size = 40
    ch = "█"
    intvl = num_batches/progress_bar_size;
    if verbose: print("Evaluating model...")
    model.eval()
    newnum = 0
    oldnum = 0
    totloss = 0.0
    if verbose: print("[", end="")
    val_metric = 0.0
    num_val_logits = 0
    with torch.no_grad():
        for i, data in enumerate(testloader):
            inputs, targets = data[0].to(device), data[1].to(device)
            predictions = model(inputs)
            loss = criterion(predictions, targets)
            totloss += loss.item()
            
            # Do prediction for metrics
            if display_metrics:
                val_metric, num_val_logits = _update_metrics_for_batch(
                        predictions, targets, loss_str, classification, regression, verbose, i, 0, val_metric, num_val_logits)
                    
            # Visualization of progressbar
            if verbose:
                newnum = int(i/intvl)
                if newnum > oldnum:
                    print((newnum-oldnum)*ch, end="")
                    oldnum = newnum 
    
    totloss, val_metric, _, _ = _calculate_epoch_loss_and_metrics(
            totloss, num_batches, verbose, 0, None, None, display_metrics, val_metric, (num_val_logits if classification else num_batches))
        
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    if verbose: print("] ", end="") 
    if verbose:
        if display_metrics:
            print("Loss: %5.4f | %s: %5.4f" % (totloss, metric_name, val_metric))
        else:
            print("Loss: %5.4f" % totloss)
            
    if verbose: print("Done.")
    d = {"loss":totloss}
    if display_metrics:
        d["metrics"] = val_metric
    return d
            
            

################################
def predict_pytorch_model(model, dataset, loss_str:str, batch_size:int=16, device_str:str="cuda", return_in_batches:bool=True, return_inputs:bool=False, 
                          return_raw_predictions:bool=False, verbose:bool=True, num_workers:int=0):
    """
    Predicts the output of a pytorch model on a given dataset.

    ### Args:
        - `model` (`torch.nn.Module`): The PyTorch model to use.
        - `dataset` (`torch.utils.data.Dataset`): Dataset containing the input data
        - `loss_str` (str): Loss function used when training. Used only for determining whether a classification or a regression model is used.
        - `batch_size` (int, optional): Batch size to use when evaluating the model. Defaults to 16.
        - `device_str` (str, optional): Device to use when performing inference. Defaults to "cuda".
        - `return_in_batches` (bool, optional): Whether the predictions should be batch-separated. Defaults to True.
        - `return_inputs` (bool, optional): Whether the output should include the inputs as well. Defaults to False.
        - `return_raw_predictions` (bool, optional): Whether raw predictions should also be returned. Defaults to False.
        - `verbose` (bool, optional): Verbosity of the function. Defaults to True.
        - `num_workers` (int, optional): Number of workers to use when making dataloader. Defaults to 0.

    ### Returns:
        List: A List containing the output predictions, and optionally, the inputs and raw predictions.
        
    ### Notes:
        - If `return_in_batches` is True, the output will be a list of lists. output[i] contains the i'th batch.
        - If `return_inputs` is true, the first element of the output information will be the inputs.
        - If `return_raw_predictions` is true, the second element of the output information will be the raw predictions.
            Please note that this is only meaningful for classification problems. Otherwise, predictions will only include raw predictions. For classification problems, 
            if this setting is True, the third element of the output information will be the class predictions.
        - "output information" here is a list containing [input, raw_predictions, class_predictions].
            For non-classification problems, "output information" will only contain [input, raw_predictions].
            If `return_inputs` is False, the first element of the output information will be omitted; [raw_predictions].
            If `return_in_batches` is True, the output will be a list of "output information" for every batch.
            Otherwise, the output will be one "output information" for the whole dataset.
    """
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    if verbose: print("Preparing data...")
    testloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    num_batches = len(testloader)
    if "cuda" in device_str:
        device = torch.device(device_str if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(device_str)
    if verbose: print("selected device: ", device)
    model.to(device)
    if loss_str in ["BCELoss", "BCEWithLogitsLoss", "CrossEntropyLoss", "NLLLoss", "PoissonNLLLoss", "GaussianNLLLoss"]:
        classification = True
    else:
        classification = False
    output_list = []
    progress_bar_size = 40
    ch = "█"
    intvl = num_batches/progress_bar_size;
    if verbose: print("Performing Prediction...")
    model.eval()
    newnum = 0
    oldnum = 0
    if verbose: print("[", end="")
    with torch.no_grad():
        for i, data in enumerate(testloader):
            inputs = data[0].to(device)
            predictions = model(inputs)
            
            # Do prediction
            if classification:
                if loss_str == "BCELoss":
                    # Output layer already includes sigmoid.
                    class_predictions = (predictions > 0.5).float()
                elif loss_str == "BCEWithLogitsLoss":
                    # Output layer does not include sigmoid. Sigmoid is a part of the loss function.
                    class_predictions = (torch.sigmoid(predictions) > 0.5).float()
                else:
                    class_predictions = torch.argmax(predictions, dim=1).float()
            
            # Add batch predictions to output dataset
            obatch = []
            if return_inputs:
                obatch.append(inputs.cpu().numpy())
            if classification:
                if return_raw_predictions:
                    obatch.append(predictions.cpu().numpy())
                obatch.append(class_predictions.cpu().numpy())
            else:
                obatch.append(predictions.cpu().numpy())
                
            if return_in_batches:
                output_list.append(obatch)
            elif i==0:
                output_array = obatch
            else:
                for j in range(len(obatch)):
                    output_array[j] = np.append(output_array[j], obatch[j], axis=0)
            
            # Visualization of progressbar
            if verbose:
                newnum = int(i/intvl)
                if newnum > oldnum:
                    print((newnum-oldnum)*ch, end="")
                    oldnum = newnum 
        
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    if verbose: print("] ")
    if return_in_batches:
        return output_list
    else:
        return output_array
        
