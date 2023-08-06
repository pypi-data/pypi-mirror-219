if __package__=="eznet_torch.models":
    from ..utils import *
else:
    import os, sys
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(parent_dir)
    from utils import *

class PyTorchSmartModule(nn.Module):
    
    sample_hparams = {
        'model_name': 'dummy_Pytorch_Smart_Module',
        'l2_reg': 0.0001,
        'batch_size': 16,
        'epochs': 2,
        'validation_data': 0.1,
        'validation_tolerance_epochs': 10,
        'learning_rate': 0.0001,
        'learning_rate_decay_gamma': 0.99,
        'loss_function': 'MSELoss',
        'loss_function_params': None,
        'optimizer': 'Adam',
        'optimizer_params': {'eps': 1e-07}
    }
    
    def __init__(self, hparams:dict=None):
        """
        Base class for smart, trainable pytorch modules. All hyperparameters are contained within the `hparams`
        dictionary. Some training-related hyperparameters are common across almost all kinds of PyTorch modules,
        which can be overloaded by the child class. The module includes functions for training, evaluation, and
        prediction. These functions cane be modified or overloaded by any child subclass.

        ### Usage

        `net = PyTorchSmartModule(hparams)` where `hparams` is dictionary of hyperparameters containing the following:
            - `model_name` (str): Name of the model.
            - `batch_size` (int): Minibatch size, the expected input size of the network.
            - `learning_rate` (float): Initial learning rate of training.
            - `learning_rate_decay_gamma` (float): Exponential decay rate gamma for learning rate, if any.
            - `optimizer` (str): Optimizer. Examples are "Adam", "SGD", "RMSprop", "Adagrad", etc.
            - `optimizer_params` (dict): Additional parameters of the optimizer, if any.
            - `epochs` (int): Maximum number of epochs for training.
            - `validation_tolerance_epochs` (int): Epochs to tolerate unimproved val loss, before early stopping.
            - `l2_reg` (float): L2 regularization parameter.
            - `loss_function` (str): Loss function. Examples: "MSELoss", "CrossEntropyLoss", "NLLLoss", etc.
            - `loss_function_params` (dict): Additional parameters for the loss function, if any.

        ### Returns

        Returns a `torch.nn.Module` object that can be trained and used accordingly.
        Run `print(net)` afterwards to see what you have inside the network.
        
        ### Notes:
        - The `self.batch_input_shape` attribute must be set in the `__init__` method.
        - The `self.batch_output_shape` attribute must be set in the `__init__` method.
        """
        super(PyTorchSmartModule, self).__init__()
        if not hparams: hparams = self.sample_hparams
        self.hparams = hparams
        self._batch_size = int(hparams["batch_size"])
        self._loss_function = hparams.get("loss_function")
        self._loss_function_params = hparams.get("loss_function_params")
        self._optimizer = hparams.get("optimizer")
        self._optimizer_params = hparams.get("optimizer_params")
        self._validation_tolerance_epochs = hparams.get("validation_tolerance_epochs")
        self._learning_rate = hparams.get("learning_rate")
        self._learning_rate_decay_gamma = hparams.get("learning_rate_decay_gamma")
        self._validation_data = hparams.get("validation_data")
        self._epochs = hparams.get("epochs")
        self._l2_reg = hparams.get("l2_reg") if hparams.get("l2_reg") else 0.0
        self.history = None
        self.batch_input_shape = (self._batch_size, 1)
        self.batch_output_shape = (self._batch_size, 1)
        if self._l2_reg > 0.0:
            if self._optimizer_params is not None:
                self._optimizer_params["weight_decay"] = self._l2_reg
            else:
                self._optimizer_params = {"weight_decay": self._l2_reg}
    
    def train_model(self, dataset, verbose:bool=True, script_before_save:bool=False, saveto:str=None, **kwargs):
        self.history = train_pytorch_model(self, dataset, self._batch_size, self._loss_function, self._optimizer, self._optimizer_params, self._loss_function_params, 
        self._learning_rate, self._learning_rate_decay_gamma, self._epochs, self._validation_tolerance_epochs, self._validation_data, verbose, script_before_save, saveto, **kwargs)
        return self.history
    
    def evaluate_model(self, dataset, verbose:bool=True, **kwargs):
        return evaluate_pytorch_model(self, 
            dataset, loss_str=self._loss_function, loss_function_params=self._loss_function_params, batch_size=self._batch_size, verbose=verbose, **kwargs)
    
    def predict_model(self, dataset, 
        return_in_batches:bool=True, return_inputs:bool=False, return_raw_predictions:bool=False, verbose:bool=True, **kwargs):
        return predict_pytorch_model(self, dataset, self._loss_function, self._batch_size, return_in_batches=return_in_batches, return_inputs=return_inputs, 
            return_raw_predictions=return_raw_predictions, verbose=verbose, **kwargs)

