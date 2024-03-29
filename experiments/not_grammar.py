# code adapted from Bob Frank's grammars.py
from nltk import CFG, Tree, PCFG
from nltk import nonterminals, Nonterminal, Production

import random
# from generator import generate
# from generator import create_file

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
# Adv, # Adverb

#TODO: ADD NEG
S, NP, MP, VP, AdvP, VPTr, RelP, NPTr, Det, N, PN, Pron, M, VInTr, VTr, NTr, PlDet,PlNTr, RP, NTand, Adv, Neg = nonterminals('S, NP, MP, VP, AdvP, VPTr, RelP, NPTr, Det, N, PN, Pron, M, VInTr, VTr, NTr, PlDet,PlNTr, RP, NTand, Adv, Neg')

not_grammar = PCFG.fromstring("""
    S -> AdvP S [0.2] | AdvP [0.2] | S1 [0.6]
    S1 -> S1 AdvP [0.2] | S2 [0.8]
    S2 -> NP MP [1.0]
    NP -> Det N [0.2] | PN [0.7] | Pron [0.1] 
    MP -> M VP [0.5] | M Neg VP [0.5]
    VP -> VTr [0.2] | VPTr [0.4] | VPTr RelP [0.4] 
    AdvP -> Adv NP MP [1.0] 
    VPTr -> VTr NPTr  [1.0]
    RelP -> RP NP M VTr [0.5] | RP NP M Neg Vtr [0.5]
    NPTr -> Det NTr [0.5] | Det PlNTr [0.5] 
    Det -> 'the' [0.5] | 'a' [0.25] | 'many' [0.25]
    N -> 'student' [0.3] | 'professor' [0.3] | 'wizard' [0.2] | 'witch' [0.2]
    PN -> 'harry' [0.05] | 'ginny' [0.05] | 'hermione' [0.05] | 'ron' [0.05] | 'fred' [0.05] | 'george' [0.05] | 'petunia' [0.05] | 'vernon' [0.05] | 'lily' [0.05] | 'hagrid' [0.05] | 'james' [0.05] | 'neville' [0.05] | 'snape' [0.05] | 'dobby' [0.05] | 'mcgonagall' [0.05] | 'lupin' [0.05] | 'draco' [0.05] | 'voldemort' [0.05] | 'sirius' [0.05] | 'albus' [0.05]
    Pron -> 'he' [0.5] | 'she' [0.5]
    M -> 'can' [0.2] | 'may' [0.2] | 'must' [0.3] | 'should' [0.3] 
    VTr -> 'hiccup' [0.05] | 'party'[0.05] | 'wiggle' [0.05] | 'laugh' [0.05] | 'smile' [0.05] | 'giggle' [0.05] | 'jump' [0.05] | 'run' [0.05] | 'walk' [0.05] | 'swim' [0.05]
    VTr -> 'prepare' [0.05] | 'make' [0.05] | 'eat' [0.05] | 'sprinkle' [0.05] | 'arrange' [0.05] | 'chew' [0.05] | 'gobble' [0.05] | 'assemble' [0.05] | 'create' [0.05] | 'hide' [0.05]
    NTr -> 'cookie' [0.05] | 'cake' [0.05] | 'chocolate' [0.05] | 'pancake' [0.05] | 'souffle' [0.05] | 'eclaire' [0.05] | 'croissant' [0.05] | 'strudel' [0.05] | 'baklava' [0.05] | 'doughnut' [0.05]
    NTr -> 'cookies' [0.05] | 'cakes' [0.05] | 'chocolates' [0.05] | 'pancakes' [0.05] | 'souffles' [0.05] | 'eclaires' [0.05] | 'croissants' [0.05] | 'strudels' [0.05] | 'baklava' [0.05] | 'doughnuts' [0.05]
    RP -> 'that' [0.6] | 'which' [0.4] 
    NTand -> 'and' [1.0]
    Adv -> 'because' [0.5] | 'since' [0.5]   
    Neg -> 'not' [1.0]
    
""")
