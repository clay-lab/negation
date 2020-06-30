# code adapted from Bob Frank's grammars.py
from nltk import CFG, Tree
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

not_grammar = CFG.fromstring("""
    S -> NP MP | AdvP S | S AdvP
    NP -> Det N | PN | Pron
    MP -> M VP | M Neg VP
    VP -> VInTr | VPTr | VPTr RelP
    AdvP -> Adv NP MP
    VPTr -> VTr NPTr
    RelP -> RP NP M VTr | RP NP M Neg Vtr
    NPTr -> Det NTr | PlDet PlNTr
    Det -> 'the' | 'a' 
    N -> 'student' | 'professor' | 'wizard' | 'witch'
    PN -> 'harry'   | 'ginny'   | 'hermione'  | 'ron'   | 'fred'   | 'george'   | 'petunia'   | 'vernon'   | 'lily'   | 'hagrid'   | 'james'   | 'neville'   | 'snape'   | 'dobby'   | 'mcgonagall'   | 'lupin'   | 'draco'   | 'voldemort'   | 'sirius'   | 'albus'  
    Pron -> 'he'   | 'she'  
    M -> 'can'   | 'may'   | 'must'   | 'should'   
    VInTr -> 'hiccup'   | 'party'  | 'wiggle'   | 'laugh'   | 'smile'   | 'giggle'   | 'jump'   | 'run'   | 'walk'   | 'swim'  
    VTr -> 'prepare'   | 'make'   | 'eat'   | 'sprinkle'   | 'arrange'   | 'chew'   | 'gobble'   | 'assemble'   | 'create'   | 'hide'  
    NTr -> 'cookie'   | 'cake'   | 'chocolate'   | 'pancake'   | 'souffle'   | 'eclaire'   | 'croissant'   | 'strudel'   | 'baklava'   | 'doughnut'  
    PlDet -> 'the'   | 'many'   
    PlNTr -> 'cookies'   | 'cakes'   | 'chocolates'   | 'pancakes'   | 'souffles'   | 'eclaires'   | 'croissants'   | 'strudels'   | 'baklava'   | 'doughnuts'  
    RP -> 'that'   | 'which'   
    NTand -> 'and'  
    Adv -> 'because'   | 'since'     
    Neg -> 'not'  
    
""")
