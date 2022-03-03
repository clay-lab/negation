from nltk import PCFG, Tree
from nltk import nonterminals, Nonterminal, Production

import random
from generator import generate
from generator import create_file

# Create some nonterminals
# S, # Sentence
# S2, # Sentence 2: follows and Advp
# NP, # Noun Phrase
# MP, # Modal Phrase
# AdvP, # Adverb Phrase
# VPTr, # Verb Phrase with a Transitive Verb
# RelP, # Relative Phrase
# NPTr, # Noun Phrase following a VPTr 
# VP, # Verb Phrase: occurs at the end of a RelP
# Det, # Determiner
# N, # Noun
# PN, # Proper Noun
# Pron, # Pronoun
# M, # Modal
# VInTr, # Intransitive Verb
# VTr, # Transitive Verb
# NTr, # Noun Following a VPTr
# PlDet, # Plural Determiner
# PlNTr, # Plural Noun following a VPTr
# RP, # Relative Pronoun
# V, # Verb that occurs at the end of an AdvP
# NTand, # Nonterminal and: only occurs in an S2
# Adv, # Adverb
# comma #comma: for ease in reading clauses 
S, S2, NP, MP, AdvP, VPTr, RelP, NPTr, VP, Det, N, PN, Pron, M, VInTr, VTr, NTr, PlDet,PlNTr, RP, V, NTand, Adv, comma = nonterminals('S, S2, NP, MP, AdvP, VPTr, RelP, NPTr, VP, Det, N, PN, Pron, M, VInTr, VTr, NTr, PlDet,PlNTr, RP, V, NTand, Adv, comma')

neg_grammar = PCFG.fromstring("""
    S -> NP MP [0.33] | NP M VPTr RelP [0.33] | AdvP S2 [0.34]
    S2 -> NP MP [0.33] | NP M VPTr RelP [0.33] | NTand AdvP S2 [0.34]
    NP -> Det N [0.2] | PN [0.6] | Pron [0.2]
    MP -> M VInTr [0.5] | M VPTr [0.5]
    AdvP -> Adv NP MP comma [1.0]
    VPTr -> VTr NPTr  [1.0]
    RelP -> RP VP [1.0]
    NPTr -> Det NTr [0.5] | PlDet PlNTr [0.5]
    VP -> NP V [1.0]
    Det -> 'the' [0.5] | 'a' [0.5]
    N -> 'student' [0.3] | 'professor' [0.3] | 'wizard' [0.2] | 'witch' [0.2]
    PN -> 'Harry' [0.1] | 'Hermione' [0.1] | 'Ron' [0.1] | 'Petunia' [0.05] | 'Vernon' [0.05] | 'Lily' [0.1] | 'James' [0.1] | 'Snape' [0.1] | 'McGonagall' [0.1] | 'Draco' [0.05] | 'Tom' [0.05] | 'Albus' [0.1] 
    Pron -> 'he' [0.5] | 'she' [0.5]
    M -> 'can' [0.2] | 'may' [0.2] | 'must' [0.3] | 'should' [0.3] 
    VInTr -> 'hiccup' [0.2] | 'party'[0.2] | 'wiggle' [0.1] | 'laugh' [0.1] | 'smile' [0.1] | 'giggle' [0.1] | 'jump' [0.1] | 'run' [0.1]
    VTr -> 'prepare' [0.4] | 'make' [0.3] | 'eat' [0.2] | 'sprinkle' [0.1]
    NTr -> 'cookie' [0.2] | 'cake' [0.2] | 'chocolate' [0.2] | 'pancake' [0.2] | 'souffle' [0.2]
    PlDet -> 'the' [0.8] | 'some' [0.2]
    PlNTr -> 'cookies' [0.2] | 'cakes' [0.2] | 'chocolates' [0.2] | 'pancakes' [0.2] | 'souffles' [0.2]
    RP -> 'that' [0.6] | 'which' [0.4]
    V -> 'loves' [0.2] | 'wants' [0.2] | 'hates' [0.2] | 'likes' [0.2] | 'eats' [0.2]
    NTand -> 'and' [1.0]
    Adv -> 'because' [0.5] | 'since' [0.5]
    comma -> ',' [1.0]   
""")

def negation(grammar):
    pos_tree = generate(grammar)
    pos = ' '.join(pos_tree.leaves())
    neg_tree = negate(pos_tree)
    neg = ' '.join(neg_tree.leaves())
    source = pos
    target = neg
    (pos) = 'POS: '
    (neg) = 'NEG: '
    return (pos), source, (neg), target
 


# 3 cases: t[1] can be an M, MP, or an S2
# to form the tree, I use recursion. The base case is M or MP and the recursive call happens in the case of S2
def negate(t):
    symbol = t[1].label().symbol()
    # base case 1
    if symbol == 'M':
        modal = t[1,0]
        modal = modal + ' not'
        t[1,0] = modal
    # base case 2
    elif symbol == 'MP':
        modal = t[1,0]
        modal = modal[-1]
        modal = modal + ' not'
        t[1,0] = modal
    # recursive call
    else:
        if t[1].label().symbol() == 'AdvP':
            negate(t[2])
        else:
            negate(t[1])  
    return t

create_file("test_file", neg_grammar, negation)