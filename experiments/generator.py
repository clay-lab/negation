from nltk import PCFG, Tree

from nltk import nonterminals, Nonterminal, Production

import itertools

import sys

import random

import csv

from typing import Callable, List

import json





def generate(grammar, start=None, depth=None):

    """

    Generates an iterator of all sentences from a CFG.



    :param grammar: The Grammar used to generate sentences.

    :param start: The Nonterminal from which to start generate sentences.

    :param depth: The maximal depth of the generated tree.

    :param n: The maximum number of sentences to return.

    :return: An iterator of lists of terminal tokens.

    """

    if not start:

        start = grammar.start()

    if depth is None:

        depth = sys.maxsize



    items = [start]

    tree = _generate(grammar,items, depth)

    return tree[0]



def _generate(grammar,items,depth=None):

    if depth > 0:

        result = []

        for i in items:

            p = random.random()

            total_rule_prob = 0.

            if isinstance(i, Nonterminal):

                for prod in grammar.productions(lhs=i):

                    total_rule_prob += prod.prob()

                    if p < total_rule_prob:

                        expansion = _generate(grammar, prod.rhs(), depth - 1)

                        result += [Tree(i, expansion)]

                        break

            else:

                result += [i]  

                break              

        return result



def create_file (filename, grammar, ex_generator, n=10):

    with open("test_file.csv", mode='w') as output_file:

        output_writer = csv.writer(output_file, delimiter=',', quotechar=' ')

#        output_writer.writerow({'SRC', 'TRANSFORM', 'TRG'})

        output_writer.writerow(['SRC', 'TRG'])

        for _ in range(n):

            # src, trans, targ = ex_generator(grammar)

            (pos), src, (neg), targ = ex_generator(grammar)

            # output_writer.writerow([src + ' ' + trans, targ])

            output_writer.writerow([(pos) + src + ' ' + (neg) + targ])


def create_dataset_json(grammar: PCFG, ex_generator: Callable, 
                        file_prefix: str = '', **splits: dict[str,int]) -> None:
    """
    Create a dataset json file that can be read using the datasets module's dataset loader.
    params: grammar: PCFG: a PCFG object
            ex_generator: function: a function that creates a pair of sentences and associated tags
                          from the grammar
            file_prefix: str: an identifier to add to the beginning of the output file names
            splits: a dictionary mapping a string identifying a set label to the number of examples to generate
                    for the file with that label
                    ex: train = 10000, dev = 1000, test = 10000
    output: a file for each argument in splits that contains the specified number of example pairs
    """
    file_prefix = file_prefix + '_' if file_prefix else ''
    
    for name, n_examples in splits.items():
        l = []
        for n in range(n_examples):
            source, pfx, target = ex_generator(grammar)
            l += [{'translation': {'src': source, 'prefix': neg, 'tgt': target}}]
        
        if l:
            with open(file_prefix + name + '.json', 'w') as f:
                for ex in l:
                    json.dump(ex, f, ensure_ascii=False)
                    f.write('\n')
            
# def demo(N=5):

#     for _ in range(N):

#         sent = generate(grammars)

#         print(" ".join(sent.leaves()))



# if __name__ == "__main__":

#     demo()