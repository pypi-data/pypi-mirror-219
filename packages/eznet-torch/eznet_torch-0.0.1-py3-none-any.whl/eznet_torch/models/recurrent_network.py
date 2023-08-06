if __package__=="eznet_keras.models":
    from ..utils import *
    from .pytorch_smart_module import *
    from .dense_block import *
else:
    import os, sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    sys.path.append(current_dir)
    from utils import *
    from pytorch_smart_module import *
    from dense_block import *


class Recurrent_Network(PyTorchSmartModule):
    
    sample_hparams = {
        'model_name': 'Recurrent_Network',
        'in_features': 10,
        'out_features': 3,
        'in_seq_len': 13,
        'out_seq_len': 1,
        'rnn_type': 'LSTM',
        'rnn_hidden_sizes': 8,
        'rnn_bidirectional': False,
        'rnn_depth': 2,
        'rnn_dropout': 0.1,
        'rnn_params': None,
        'lstm_proj_size':None,
        'final_rnn_return_sequences': False,
        'apply_dense_for_each_time_step': True,
        'permute_output': False,
        'dense_width': 16,
        'dense_depth': 2,
        'dense_dropout': 0.2,
        'dense_activation': 'ReLU',
        'dense_activation_params': None,
        'output_activation': None,
        'output_activation_params': None,
        'norm_layer_type': 'BatchNorm1d',
        'norm_layer_params': None,
        'norm_layer_position': 'before',
        'l2_reg': 0.0001,
        'batch_size': 16,
        'epochs': 2,
        'validation_data': [0.05,'testset'],
        'validation_tolerance_epochs': 10,
        'learning_rate': 0.0001,
        'learning_rate_decay_gamma': 0.99,
        'loss_function': 'CrossEntropyLoss',
        'loss_function_params': None,
        'optimizer': 'Adam',
        'optimizer_params': {'eps': 1e-07}
    }
    
    def __init__(self, hparams:dict=None):
        """Sequence to Dense network with RNN for time-series classification, regression, and forecasting, as well as NLP applications.
        This network uses any RNN layers as encoders to extract information from input sequences, and fully-connected 
        multilayer perceptrons (Dense) to decode the sequence into an output, which can be class probabilitites 
        (timeseries classification), a continuous number (regression), or an unfolded sequence (forecasting) of a 
        target timeseries.

        ### Usage

        `net = Recurrent_Network(hparams)` where `hparams` is dictionary of hyperparameters containing the following:

            - `rnn_type` (str): RNN type, options are "LSTM", "GRU", "RNN", etc.
            - `in_seq_len` (int): Input sequence length, in number of timesteps
            - `out_seq_len` (int): Output sequence length, in number of timesteps, assuming output is also a sequence. This will affect the output layer in the dense section.
                Use 1 for when the output is not a sequence, or do not supply this key.
            - `in_features` (int): Number of features of the input.
            - `out_features` (int): Number of features of the output.
            - `rnn_hidden_sizes` ("auto"|int): RNN layer hidden size. "auto" decides automatically, and a number sets them all the same. Default is 'auto'.
            - `rnn_bidirectional` (bool): Whether the RNN layers are bidirectional or not. Default is False.
            - `rnn_depth` (int): Number of stacked RNN layers. Default is 1.
            - `rnn_dropout` (float): Dropout rates, if any, of the RNN layers. PyTorch ignores this if there is only one RNN layer.
                Please note that using dropout in RNN layers is generally discouraged, for it decreases determinism during inference.
            - `rnn_params` (dict): Additional parameters for the RNN layer constructor. Default is None.
            - `lstm_proj_size` (int): If the RNN type is LSTM, this is the projection size of the LSTM. Default is None.
            - `final_rnn_return_sequences` (bool): Whether the final RNN layer returns sequences of hidden state. 
                **NOTE** Setting this to True will make the model much, much larger.
            - `apply_dense_for_each_time_step` (bool): Whether to apply the Dense network to each time step of the 
                RNN output. If False, the Dense network is applied to the last time step only if 
                `final_rnn_retrurn_sequences` is False, or applied to a flattened version of the output sequence
                otherwise (the dimensionality of the input feature space to the dense network will be multiplied
                by the sequence length. PLEASE NOTE that this only works if the entered sequence is exactly as long
                as the priorly defined sequence length according to the hyperparameters).
            - `permute_output` (bool): Whether to permute the output sequence to be (N, D*H_out, L_out)
            - `dense_width` (int|list): (list of) Widths of the Dense network. It can be a number (for all) or a list holding width of each hidden layer.
            - `dense_depth` (int): Depth (number of hidden layers) of the Dense network.
            - `dense_activation` (str|list): (list of) Activation functions for hidden layers of the Dense network. Examples: "ReLU", "LeakyReLU", "Sigmoid", "Tanh", etc.
            - `dense_activation_params` (dict|list): (list of) Dictionaries of parameters for the activation func constructors of the Dense network.
            - `output_activation` (str): Activation function for the output layer of the Dense network, if any. Examples: "Softmax", "LogSoftmax", "Sigmoid", etc.
                **NOTE** If the loss function is cross entropy, then no output activation is erquired.
                However, if the loss function is nll (negative loglikelihood), then you must specify an output activation as in "LogSoftmax".
            - `output_activation_params` (dict): Dictionary of parameters for the activation func constructor of the output layer.
            - `norm_layer_type` (str|list): (list of) Types of normalization layers to use in the dense section, if any. Options are "BatchNorm1d", "LayerNorm", etc.
            - `norm_layer_params` (dict|list): (list of) Dictionaries of parameters for the normalization layer constructors.
            - `norm_layer_position` (str|list): (list of) Whether the normalization layer should come before or after the activation of each hidden layer in the dense network.
            - `dense_dropout` (float|list): (list of) Dropout rates (if any) for the hidden layers of the Dense network.
            - `batch_size` (int): Minibatch size, the expected input size of the network.
            - `learning_rate` (float): Initial learning rate of training.
            - `learning_rate_decay_gamma` (float): Exponential decay rate gamma for learning rate, if any.
            - `optimizer` (str): Optimizer. Examples: 'Adam', 'SGD', 'RMSProp', etc.
            - `optimizer_params` (dict): Additional parameters of the optimizer, if any.
            - `epochs` (int): Maximum number of epochs for training.
            - `validation_tolerance_epochs` (int): Epochs to tolerate unimproved val loss, before early stopping.
            - `validation_data` (list): Portion of validation data. Should be a tuple like [validation split, dataset as in 'trainset' or 'testset']
            - `l2_reg` (float): L2 regularization parameter.
            - `loss_function` (str): Loss function. Examples: 'BCELoss', 'CrossEntropyLoss', 'MSELoss', etc.
            - `loss_function_params` (dict): Additional parameters for the loss function, if any.

        ### Returns
        
        Returns a `torch.nn.Module` object that can be trained and used accordingly.
        Run `print(net)` afterwards to see what you have inside the network.
        The returned model is an instance of `PyTorchSmartModule`, which has builkt-in functions for training, evaluation, prediction, etc.
        """
        super(Recurrent_Network, self).__init__(hparams)
        hparams = hparams if hparams is not None else self.sample_hparams
        self._rnn_type = hparams["rnn_type"]
        self._rnn = getattr(nn, self._rnn_type)
        self._denseactivation = hparams["dense_activation"] if hparams.get("dense_activation") else "ReLU"
        self._denseactivation_params = hparams.get("dense_activation_params")
        self._outactivation = hparams.get("output_activation")
        self._outactivation_params = hparams.get("output_activation_params")
        self._normlayer_type = hparams.get("norm_layer_type")
        self._normlayer_params = hparams.get("norm_layer_params")
        self._normlayer_position = hparams.get("norm_layer_position")
        self._infeatures = hparams["in_features"]
        self._outfeatures = hparams["out_features"]
        self._rnnhidsizes = hparams["rnn_hidden_sizes"] if hparams.get("rnn_hidden_sizes") else "auto"
        self._densehidsizes = hparams["dense_width"] if hparams.get("dense_width") else "auto"
        self._densedepth = hparams["dense_depth"] if hparams.get("dense_depth") else 0
        self._rnndepth = hparams["rnn_depth"] if hparams.get("rnn_depth") else 1
        self._bidirectional = True if hparams.get("rnn_bidirectional") else False
        self._rnndropout = hparams["rnn_dropout"] if hparams.get("rnn_dropout") else 0
        self._densedropout = hparams["dense_dropout"] if hparams.get("dense_dropout") else None
        self._final_rnn_return_sequences = True if hparams.get("final_rnn_return_sequences") else False
        self._apply_dense_for_each_timestep = True if hparams.get("apply_dense_for_each_timestep") else False
        self._permute_output = True if hparams.get("permute_output") else False
        self._N = int(hparams["batch_size"])
        self._L_in = int(hparams["in_seq_len"])
        self._L_out = int(hparams["out_seq_len"]) if hparams.get("out_seq_len") else 1
        self._D = int(2 if self._bidirectional else 1)
        self._rnn_params = hparams.get("rnn_params")
        self._lstmprojsize = hparams.get("lstm_proj_size") if hparams.get("lstm_proj_size") else 0
        self._H_in = int(self._infeatures)
        if self._rnnhidsizes == "auto": self._H_cell = int(2**(np.round(math.log2(self._H_in*self._L_in))))
        else: self._H_cell = int(self._rnnhidsizes)
        self._H_out = int(self._lstmprojsize if self._lstmprojsize and self._lstmprojsize > 0 else self._H_cell)
        self.batch_input_shape = (self._N, self._L_in, self._H_in)
        if self._final_rnn_return_sequences and self._apply_dense_for_each_timestep:
            if self._permute_output: self.batch_output_shape = (self._N, self._outfeatures, self._L_out)
            else: self.batch_output_shape = (self._N, self._L_out, self._outfeatures)
        else: self.batch_output_shape = (self._N, self._L_out * self._outfeatures)
        
        # Constructing RNN layers
        if self._rnn_type == "LSTM" and self._lstmprojsize > 0:
            if self._rnn_params:
                self.rnn = nn.LSTM(input_size=self._H_in, hidden_size=self._H_cell, num_layers=self._rnndepth, batch_first=True, dropout=self._rnndropout, 
                    bidirectional=self._bidirectional, proj_size=self._lstmprojsize, **self._rnn_params)
            else:
                self.rnn = nn.LSTM(input_size=self._H_in, hidden_size=self._H_cell, num_layers=self._rnndepth, batch_first=True, dropout=self._rnndropout, 
                    bidirectional=self._bidirectional, proj_size=self._lstmprojsize)
        else:
            if self._rnn_params:
                self.rnn = self._rnn(input_size=self._H_in, hidden_size=self._H_cell, num_layers=self._rnndepth, 
                                    batch_first=True, dropout=self._rnndropout, bidirectional=self._bidirectional, **self._rnn_params)
            else:
                self.rnn = self._rnn(input_size=self._H_in, hidden_size=self._H_cell, num_layers=self._rnndepth, 
                                    batch_first=True, dropout=self._rnndropout, bidirectional=self._bidirectional)
        # for attrib in dir(self.rnn):
        #     if attrib.startswith("weight_ih"): xavier_uniform_(self.rnn.__getattr__(attrib))
        #     elif attrib.startswith("weight_hh"): orthogonal_(self.rnn.__getattr__(attrib))
        #     elif attrib.startswith("bias_"): zeros_(self.rnn.__getattr__(attrib))
        
        # Calculating Dense layers widths
        cf = self._L_in if (self._final_rnn_return_sequences and not self._apply_dense_for_each_timestep) else 1 
        self._dense_input_size = self._H_out * self._D * cf
        if self._final_rnn_return_sequences and not self._apply_dense_for_each_timestep:
            self._dense_output_size = int(self._L_out*self._outfeatures)
        else:
            self._dense_output_size = int(self._outfeatures)
            
        # Generate arrays containing parameters of each Dense Block (Every block contains a linear, normalization, activation, and dropout layer).
        self._dense_width_vec = self._gen_hparam_vec_for_dense(self._densehidsizes, 'dense_width')
        self._dense_activation_vec = self._gen_hparam_vec_for_dense(self._denseactivation, 'dense_activation')
        self._dense_activation_params_vec = self._gen_hparam_vec_for_dense(self._denseactivation_params, 'dense_activation_params')
        self._dense_norm_layer_type_vec = self._gen_hparam_vec_for_dense(self._normlayer_type, 'norm_layer_type')
        self._dense_norm_layer_params_vec = self._gen_hparam_vec_for_dense(self._normlayer_params, 'norm_layer_params')
        self._dense_norm_layer_position_vec = self._gen_hparam_vec_for_dense(self._normlayer_position, 'norm_layer_position')
        self._dense_dropout_vec = self._gen_hparam_vec_for_dense(self._densedropout, 'dense_dropout')
        
        # Construct the dense layers
        in_size = self._dense_input_size
        layers = []
        for i in range(self._densedepth):
            out_size = self._dense_width_vec[i]
            temp_dropout_rate = self._dense_dropout_vec[i] if (i != self._densedepth-1) else None # The hidden layer just before the output layer rarely has Dropout.
            layers.append(Dense_Block(in_size, out_size, self._dense_activation_vec[i], self._dense_activation_params_vec[i], 
                self._dense_norm_layer_type_vec[i], self._dense_norm_layer_position_vec[i], self._dense_norm_layer_params_vec[i], temp_dropout_rate))
            in_size = out_size
        
        # Output layer
        layers.append(nn.Linear(in_size, self._dense_output_size))
        if self._outactivation:
            if self._outactivation_params:
                layers.append(getattr(nn, self._outactivation)(**self._outactivation_params))
            else:
                layers.append(getattr(nn, self._outactivation)())
        
        # Sequentiating the layers
        self.fc = nn.Sequential(*layers)
        
        self.rnn.flatten_parameters()
        
        
    
    def _gen_hparam_vec_for_dense(self, hparam, hparam_name, **kwargs):
        return generate_array_for_hparam(hparam, self._densedepth, hparam_name=hparam_name, count_if_not_list_name='dense_depth', **kwargs)
    
    def forward(self, x):
        self.rnn.flatten_parameters()
        # self._rnn_output, (self._rnn_final_hidden_states, self._lstm_final_cell_states) = self.rnn(x)
        rnn_output, _ = self.rnn(x)
        if self._final_rnn_return_sequences:
            if self._apply_dense_for_each_timestep: rnn_output_flattened = rnn_output
            else: rnn_output_flattened = rnn_output.view(rnn_output.shape[0], -1)
        else:
            # RNN output is of shape  (N, L, D * H_out)
            rnn_output_flattened = rnn_output[:,-1,:]
        out = self.fc(rnn_output_flattened)
        if self._permute_output:
            return out.permute(0,2,1)
        else:
            return out

