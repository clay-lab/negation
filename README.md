# negation
New Repo to store results analysis from CLAY lab Transductions

The data in this repo has been trained on the neural network model developed in the [CLAY lab Transductions repository] (https://github.com/clay-lab/transductions).
The negation data is trained on the following hyperparameters:

Encoder type: `` GRU ``
Decoder type: `` GRU ``
Attention: varies. See folder names
Learning Rate: `` 0.01 ``
Hidden Layers: `` 1 ``
Batch Size: `` 5 ``

Each folder is named based on the attention used in each run: no attention, additive, location, or multiplicative. 
Subfolders are named based on the run number. There will be 5 runs for each attention type.
In each run, there are 
