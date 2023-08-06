
if __package__=="eznet_torch.models":
    from .recurrent_network import *
else:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from recurrent_network import *

class LanguageModel(Recurrent_Network):
    def __init__(self, hparams:dict=None):
        super(LanguageModel, self).__init__(hparams)
        self.embed_dim = hparams['embedding_dim'] if hparams.get('embedding_dim') else hparams['in_features']
        self.vocab_size = hparams['vocab_size'] if hparams.get('vocab_size') else 27
        assert self.embed_dim == self._infeatures, "Embedding dim (%d) must be equal to input feature dim (%d)."%(self.embed_dim, self._infeatures)
        self.embed_layer = nn.Embedding(self.vocab_size, self.embed_dim)
        self._embed_output = None
        self.permute_output = hparams['permute_output'] if hparams.get('permute_output') else False
        self.batch_input_shape = [hparams['batch_size'], hparams['in_seq_len']]
        if self.permute_output:
            self.batch_output_shape = [hparams['batch_size'], hparams['out_features'], hparams['out_seq_len']]
        else:
            self.batch_output_shape = [hparams['batch_size'], hparams['out_seq_len'], hparams['out_features']]
        
    def forward(self, x):
        # TODO: Transfer the "permute_output" logic to the base class as well.
        # self._rnn_output, (self._rnn_final_hidden_states, self._lstm_final_cell_states) = self.rnn(x)
        # Shape of x should be: [N, L]
        self._embed_output = self.embed_layer(x)    # [N, L, embed_dim]
        self._rnn_output, _ = self.rnn(self._embed_output)
        if self._final_rnn_return_sequences:
            if self._apply_dense_for_each_timestep:
                self._rnn_output_flattened = self._rnn_output
            else:
                self._rnn_output_flattened = self._rnn_output.view(self._rnn_output.shape[0], -1)
        else:
            # RNN output is of shape  (N, L, D * H_out)
            self._rnn_output_flattened = self._rnn_output[:,-1,:]
        out = self.decoder(self._rnn_output_flattened)
        if self.permute_output:
            return out.permute(self.permute_output)
        else:
            return out
    
    def test(self):
        print("------------------------------------------------------------------")
        print("Testing RNN_Language_Network")
        print("Constructing random inputs and outputs ...")
        print("Batch size:              %d"%self._batchsize)
        print("Input sequence length:   %d"%self._L_in)
        print("Output sequence length:  %d"%self._L_out)
        print("Input feature dimension: %d"%self._infeatures)
        print("Construjcting random torch.long tensor for input ...")
        x = torch.randint(0, self.vocab_size, self.batch_input_shape, dtype=torch.long)
        print("Input shape:  %s"%str(x.shape))
        print("Constructing random torch.float tensor for output ...")
        y_true = torch.rand(size=self.batch_output_shape)
        print("Output shape from truth: %s"%str(y_true.shape))
        print("Calling the forward method ...")
        y_pred = self.forward(x)
        print("Output shape from preds: %s"%str(y_pred.shape))
        assert y_true.shape == y_pred.shape, \
            "Output shape (%s) does not match expected shape (%s)"%(str(y_pred.shape), str(y_true.shape))
        print("Testing complete. Output shape matches expected shape.")
        print("------------------------------------------------------------------")
