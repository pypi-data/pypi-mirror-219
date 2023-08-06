# ezNet-torch

PyTorch implementation of **ezNet** ("easy net"), a package containing "easy" implementation of a collection of basic and widely-used deep learning models.  
This implementation is for PyTorch. See [here](https://github.com/pniaz20/eznet_keras) for an identical Keras (TensorFlow) implementation.

Author: Pouya P. Niaz (<pniaz20@ku.edu.tr> , <pouya.p.niaz@gmail.com>)  
Version: 0.0.1  
Last Update: July 15, 2023

Install with:

```bash
pip install eznet-torch
```

-----------------------------------

## 1- Intro

You can build, train and evaluate all manner of PyTorch models using the utilities in this package, similar to torch-lightning, but with additional functionality, and easier.
Furthermore, there is a collection of basic and widely-used deep learning models ready to be used immediately.
This package also offers `PyTorchSmartModule`, a sublass of `nn.Module` that has built-in functions for manipulating its hyperparameters,
training, evaluation, testing, storing, etc.

Note that for all the functions and classes described briefly here, the docstrings provide much more detailed information.

Also note that even though most of the functionality here exists in torch-lightning, there is additional functionality here, and it is easy to use.
Furthermore, inspecting the code can be useful for educational purposes.

### 1-1- Implementation notes

Unlike, e.g., PyTorch, you may not be able to just import everything together as in `import eznet_torch` and then use dot indexing to access everything underneath
(I would love to do that, I haven't yet quite figured out how to. I am a newbie.)

Instead, import the specific module, class or function, e.g.,

```python
from eznet_torch.models import ANN
# or 
from eznet_torch.utils import calc_image_size
```

-----------------------------------

## 2- Applications

### 2-1- Smart Model for Convenient DL Training and Deployment

The `PyTorchSmartModule` class enables you to write any kind of PyTorch model, and it has built-in functions for training, testing, evaluaiton, saving, etc.

```python
from eznet_torch.models import PyTorchSmartModule

class MyModel(PyTorchSmartModule):
    def __init__(self, hparams:dict=None):
        super(MyModel, self).__init__(hparams)
        #
        # Some code here
        #
    
    def forward(self, x):
        # something or another

sample_hparams = {
    'model_name': 'PyTorchSmartModule',   # Name of the model. Arbitrary.
    'l2_reg': 0.0001,                     # L2 regularization parameter
    'batch_size': 16,                     # Mini-batch size
    'epochs': 2,                          # Maximum training epochs
    'validation_data': [0.05,'trainset'], # Portion of train set used for validation (if necessary)
    'validation_tolerance_epochs': 10,    # Validation patience for early stopping
    'learning_rate': 0.0001,              # (Initial) Learning rate
    'learning_rate_decay_gamma': 0.99,    # Learning rate exponential decay gamma
    'loss_function': 'CrossEntropyLoss',  # Loss function string (name of class)
    'loss_function_params': None,         # Dictionary of parameters to pass to the loss function
    'optimizer': 'Adam',                  # Optimizer string (name of class)
    'optimizer_params': None              # Dictionary of parameters to pass to the optimizer constructor
}

model = MyModel(sample_hparams)

trainset = ... # some torch.utils.data.Dataset
valset = ...   # some torch.utils.data.Dataset
testset = ...  # some torch.utils.data.Dataset

model.train_model([trainset, valset], verbose=1, script_before_save=True, saveto="mymodel.pt", num_workers=0)
results = model.evaluate_model(testset, verbose=1)
```

A few implementation notes:

- Whatever hyperparameters you have for the model itself, can be included in the hparams dictionary.
- The `__init__` method must always calculate the lists `self.batch_input_shape` and `batch_output_shape`.
- The `__init__` method of the `PyTorchSmartModule` class will create attributes with the same name as the hyperparameters shown above.
- Tha `__init__` method of the class may alter some of its attributes if the input hyperparameters don't exist or don't make sense.
- The `self.history` attribute is `None` at the beginning, but is updated after training, to hold losses, accuracies, and learning rates during training.
- The `script_before_save` argument tells whether the model should be converted to torchscript before saving.
  Comes in handy when you frequently deploy deep learning models on robotic/mechatronic hardware that use C++ (therefore libtorch),
  in which case you MUST convert the model to torchscript before saving it, so it can be imported using libtorch in C++.
- We have coded the `train_model` function (and some others) so it automatically recognizes if the loss is a classification or regression loss,
  in both of which cases metrics are chosen to be either **accuracy**, or **r2_score**, respectively. Metrics are reported for every epoch.
  (hence why scikit-learn is a dependency. It is not used elsewhere. This is unnecessary dependency just for a calculation, and will be removed in a future version).

### 2-2- Utility Functions for Manipulating PyTorch Models

In `eznet_torch.utils`, there are some functions for manipulating PyTorch models, that come in handy if you frequently work with custom DL models.

- `make_path(path)` creates a path for a folder or file, if some folders in the path don't exist.
  Anywhere you want to save something, instead of `path/to/foo.bar` you can just use `make_path("path/to/foo.bar")` so if `path` or `to` directories
  don't exist they will be created.
- `autoname(name)` gets a string as a name, and appends the current time stamp to it. Comes in handy when trying to time stamp the multiple training runs you'll do.
- `calc_image_size(size_in, kernel_size, padding, stride, dilation)` gets the input image dimension (1D, 2D or 3D), along with the
  parameters of a convolution or pooling operation, and returns the output image dimensions. Comes in handy when you want to check to see if your
  CNN layers are not shrinking the image too much.
- `generate_geometric_array()` gets an initial count and returns an array where the count doubles or halves along the array.
  Comes in handy when you want to automatically assign number of filters/channels or hidden sizes in ANNs and CNNs.
- `generate_array_for_hparam()` gets the value of a hyperparameter specified by the user (e.g. ANN width), computes whether the hyperparameter needs to be an array
  (e.g. the user input an integer but ANN width should be an array with length equal to ANN depth), and then returns an array that properly holds the hyperparameter values.
- `generate_sample_batch(model)` gets `model.batch_input_shape` and `model.batch_output_shape` and returns random input and output batches.
- `train_pytorch_model(model, dataset=[trainset, valset], **kwargs)` trains any `nn.Module` instance given some parameters, and optionally, scripts and saves it afterward.
  The function gets dataset and automatically generates dataloaders from that.
- `save_pytorch_model(model, saveto, **kwargs)` scripts the model first if requested, and then saves it.
- `evaluate_pytorch_model(model, dataset, **kwargs)` evaluates a model on a dataset, reporting such metrics as accuracy, r2_score, etc.
- `predict_pytorch_model(model, dataset, **kwargs)` predicts the model on all batches of a dataset and returns the predictions.

### 2-3- Functions and Classes for Adding and Manipulating Modular Dense Blocks and Conv Blocks

This package also has classes and functions that can be used to create entire Dense blocks and Conv blocks.

```python
class eznet_torch.models.DenseBlock(nn.Module)
```

Gets some arguments to the constructor and returns a module that holds
a **Dense** layer, followed optionally by a **normlization** layer, an **activation** layer, and a **dropout** layer. The arguments to the constructor are
sufficient to build any kind of modular `DenseBlock`, stacking it on top of other layers in your model.
I created this class becasue Dense blocks almost always have a widely-used format: dense, norm, activation, dropout.

```python
class eznet_torch.models.ConvBlock(nn.Module)
```

Gets some arguments to the constructor and returns a module that contains a **convolution** layer, followed optionally
by a **normalization** layer, an **activation** layer, a **pooling** layer, and a **dropout** layer.
Again, the inputs are fully sufficient to make any kind of `ConvBlock` and stack it on top of other layers in your CNN.
Similar to the previous case, I created this class becasue it has easy-to-use modular capabilities to build widely-used CNN blocks
that have these kinds of layers in them.

### 2-4- Easy to Use Famous Deep Learning Models for Convenience

This package also holds some widely-used and basic deep learning models as in MLP, CNN, RNN, etc. that can get a dictionary of
well-defined hyperparameters, and return a `PyTorchSmartModule` instance that can be easily trained, evaluated, stored and deployed.

All of the following models reside in the `eznet_torch.models` submodule.

**NOTE** To see a list of all hyperparameters that each of the following classes use, simply invoke the `class.sample_hparams` class attribute.
Also, you can simply call the `help(class)` function to read the docstrings.
For `ANN`, for instance,

```python
from eznet_torch.models import ANN

print(ANN.sample_hparams)

help(ANN)
```

- `ANN` is a multi-layer perceptron containing many `DenseBlock`s, stacked together. For all hyperparameters such as width,
  you can specify an integer to be used for all hidden layers (i.e., all blocks), or an array of different values for each hidden layer (i.e., block).
  For every hyperparameter such as normalization layer type, use `None` in its place in the array to indicate that the corresponding
  Dense block in that place does not have any normalization layers at all. The same goes for many other hyperparameters.
- `Conv_Network` is a CNN where you not only choose the dimensionality (1D, 2D or 3D convolutions) but also all the other hyperparameters of all
  Convolution blocks and Dense blocks residing in the network. This network is some Convulution blocks, followed by some Dense blocks.
  You get to choose which Conv block has what kind of Conv, Norm (if any), Activation, Pooling (if any), or Dropout (if any) layer.
  You also get to choose custom parametrers (**kwargs) for Conv, Pooling, Norm, Activation and Dense layer constructors, so that you can add additional parameters,
  or overwrite the ones used by the class itself. You have full freedom.
- `Recurrent_Network` is an RNN containing some RNN layers (RNN, GRU, LSTM, etc.) followed by some Dense blocks. Again, the whole thing is fully modular and you have full freedom.
- `LanguageModel` is an RNN model that gets a sequence of characters and predicts the next character. It is a character-level language model.

More model varieties with modular and easy-to-use functionality will be added in time.

-----------------------------------

## 3- License

This package itself has MIT license, but PyTorch has different licenses, which need to be accounted for when using this package.

-----------------------------------

## 4- Credits

PyTorch  
<https://pytorch.org/>  
<https://github.com/pytorch/pytorch>

-----------------------------------
