# negation
New Repo to store results analysis from CLAY lab Transductions

The data in this repo has been trained on the neural network model developed in the [CLAY lab Transductions repository](https://github.com/clay-lab/transductions).

## Hyperparameters

The negation data is trained on the following hyperparameters:

Encoder type: `` GRU ``

Decoder type: `` GRU ``

Attention: varies. See folder names

Learning Rate: `` 0.01 ``

Hidden Layers: `` 1 ``

Batch Size: `` 5 ``

## Folders
Each folder is named based on the attention used in each run: no attention, additive, location, or multiplicative.

### Subfolders
Subfolders are named based on the model number. There will be 5 models for each attention type.

#### Runs
For each run, there are 8 files. Below are descriptions of each file.

``dicts.csv`` contains a table with numerical representations of analysis per sentence length

``no-parses.csv`` contains all non-parseable sentences using the [BottomUpLeftCornerChartParser](https://www.nltk.org/_modules/nltk/parse/chart.html)

``pos_neg.csv`` contains all positive to negative transformations in the test data

``pos_pos.csv`` contains all postive to positive transformations in the test data

``pos_negBOOLS.csv`` contains all of the boolean analysis for each sentence in ``pos_neg.csv`` (displayed in ``dicts.csv``)

``pos_negBOOLS.csv`` contains all of the boolean analysis for each sentence in ``pos_pos.csv`` (displayed in ``dicts.csv``)

