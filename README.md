# negation
The data in this repo has been trained on the neural network model developed in the [CLAY lab Transductions repository](https://github.com/clay-lab/transductions) using the following hyperparameters:

The negation data is trained on the following hyperparameters:

Encoder type: `` GRU ``

Decoder type: `` GRU ``

Attention: varies. See folder names

Learning Rate: `` 0.01 ``

Hidden Layers: `` 1 ``

Batch Size: `` 5 ``

For more information on the data analysis in this repository, visit this [this link](https://docs.google.com/document/d/107KZ1vDLfGgx0bMNxNhf7bz_ejVvmiSrCKTB4VKA5hU/edit?usp=sharing)

## Experiments
There are currently two experiments in this repository: 'negation' and 'noAdvp'. 

Negation: train, val, and test data contains sentences with adverbial phrases before and after the main clause.

NoAdvp: train and val datasets contain pos->neg transformations without adverbial phrases before the main clause. Test dataset contains only transformations with at least one adverbial phrase before the main clause.

Each experiment has a number of subdirectories and files.
1) ``data``: this directory contains the necessary test dataset that was used to test the models

2) ``models``: this directory contains all models trained and tested in this repo

3) ``results``: the models are divided by types of attention used during training: location, multiplicative, and additive. the results directories include files related to the performance of each model

4) ``tables.csv`` files: these files contain tables that provide information on the performance of each model and the mean across the models.

### Results Directories
Each model contains three files that detail their performance on various tasks.
``no-parses.csv`` contains all non-parseable sentences using the [BottomUpLeftCornerChartParser](https://www.nltk.org/_modules/nltk/parse/chart.html)

``pos_neg.csv`` contains all positive to negative transformations in the test data

``pos_pos.csv`` contains all postive to positive transformations in the test data


#### Tasks
The following tasks are evaluated for each model:
``Correct Transformation``: evaluates whether the model's transformation is exactly the same as the target transformation

``Parseable``: evaluates whether the sentence is parseable using the [BottomUpLeftCornerChartParser](https://www.nltk.org/_modules/nltk/parse/chart.html)

``Preserves Identical Tree Structure``: evaluates whether the predicted sentence preserves the identical tree structure of the target sentence.

``Preserves Significant Clauses (S, AdvP, RelP)``: evaluates whether the predicted sentence preserves the following significant clauses: sentence clauses, adverbial phrases, and relative clauses.

``Negates Main Clause``: evaluates whether the predicted sentence negates the main clause

``Has Main Clause``: evaluates whether the predicted sentence contains a main clause

``Negates Outside of Main Clause``: evaluates whether the predicted sentence negates outside the main clause

``Has Target Verb``: evaluates whether the predicted sentence has the verb that was negated in the target sentence

``Negates Target Verb``: evaluates whether the predicted sentence negates the same verb that was negated in the target sentence

## Replicate The Results In this Repository

``resultswhole.py``  runs per each type of attention and will run through models 1-5. The program takes in the following three arguments:

``Task Name``: the directory that will hold all information about the experiment

``Attention Type``: the attention used for that particular model

``Directory``: the directory that contains the experiment being run (i.e the directory that holds that task name argument)

Models are analyzed with the following commands:

``python resultswhole.py {task name} {attention-type} {directory}``

The structure of this repo is designed for replication of results. Please use the configuration of these files when running the program.
