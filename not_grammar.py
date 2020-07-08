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

# not_grammar = CFG.fromstring("""
#     S -> NP MP | AdvP S | S AdvP
#     NP -> Det N | PN | Pron
#     MP -> M VP | M Neg VP
#     VP -> VInTr | VPTr | VPTr RelP
#     AdvP -> Adv NP MP
#     VPTr -> VTr NPTr
#     RelP -> RP NP M VTr | RP NP M Neg Vtr
#     NPTr -> Det NTr | PlDet PlNTr
#     Det -> 'the' | 'a' 
#     N -> 'student' | 'professor' | 'wizard' | 'witch'
#     PN -> 'harry'   | 'ginny'   | 'hermione'  | 'ron'   | 'fred'   | 'george'   | 'petunia'   | 'vernon'   | 'lily'   | 'hagrid'   | 'james'   | 'neville'   | 'snape'   | 'dobby'   | 'mcgonagall'   | 'lupin'   | 'draco'   | 'voldemort'   | 'sirius'   | 'albus'  
#     Pron -> 'he'   | 'she'  
#     M -> 'can'   | 'may'   | 'must'   | 'should'   
#     VInTr -> 'hiccup'   | 'party'  | 'wiggle'   | 'laugh'   | 'smile'   | 'giggle'   | 'jump'   | 'run'   | 'walk'   | 'swim'  
#     VTr -> 'prepare'   | 'make'   | 'eat'   | 'sprinkle'   | 'arrange'   | 'chew'   | 'gobble'   | 'assemble'   | 'create'   | 'hide'  
#     NTr -> 'cookie'   | 'cake'   | 'chocolate'   | 'pancake'   | 'souffle'   | 'eclaire'   | 'croissant'   | 'strudel'   | 'baklava'   | 'doughnut'  
#     PlDet -> 'the'   | 'many'   
#     PlNTr -> 'cookies'   | 'cakes'   | 'chocolates'   | 'pancakes'   | 'souffles'   | 'eclaires'   | 'croissants'   | 'strudels'   | 'baklava'   | 'doughnuts'  
#     RP -> 'that'   | 'which'   
#     NTand -> 'and'  
#     Adv -> 'because'   | 'since'     
#     Neg -> 'not'  
    
# """)

not_grammar = PCFG.fromstring("""
    S -> NP MP [0.6] | AdvP S [0.2] | S AdvP [0.2]
    NP -> Det N [0.2] | PN [0.7] | Pron [0.1] 
    MP -> M VP [0.5] | M Neg VP [0.5]
    VP -> VInTr [0.2] | VPTr [0.4] | VPTr RelP [0.4] 
    AdvP -> Adv NP MP [1.0] 
    VPTr -> VTr NPTr  [1.0]
    RelP -> RP NP M VTr [1.0]
    NPTr -> Det NTr [0.5] | PlDet PlNTr [0.5] 
    Det -> 'the' [0.5] | 'a' [0.5]
    N -> 'student' [0.3] | 'professor' [0.3] | 'wizard' [0.2] | 'witch' [0.2]
    PN -> 'harry' [0.05] | 'ginny' [0.05] | 'hermione' [0.05] | 'ron' [0.05] | 'fred' [0.05] | 'george' [0.05] | 'petunia' [0.05] | 'vernon' [0.05] | 'lily' [0.05] | 'hagrid' [0.05] | 'james' [0.05] | 'neville' [0.05] | 'snape' [0.05] | 'dobby' [0.05] | 'mcgonagall' [0.05] | 'lupin' [0.05] | 'draco' [0.05] | 'voldemort' [0.05] | 'sirius' [0.05] | 'albus' [0.05]
    Pron -> 'he' [0.5] | 'she' [0.5]
    M -> 'can' [0.2] | 'may' [0.2] | 'must' [0.3] | 'should' [0.3] 
    VInTr -> 'hiccup' [0.1] | 'party'[0.1] | 'wiggle' [0.1] | 'laugh' [0.1] | 'smile' [0.1] | 'giggle' [0.1] | 'jump' [0.1] | 'run' [0.1] | 'walk' [0.1] | 'swim' [0.1]
    VTr -> 'prepare' [0.1] | 'make' [0.1] | 'eat' [0.1] | 'sprinkle' [0.1] | 'arrange' [0.1] | 'chew' [0.1] | 'gobble' [0.1] | 'assemble' [0.1] | 'create' [0.1] | 'hide' [0.1]
    NTr -> 'cookie' [0.1] | 'cake' [0.1] | 'chocolate' [0.1] | 'pancake' [0.1] | 'souffle' [0.1] | 'eclaire' [0.1] | 'croissant' [0.1] | 'strudel' [0.1] | 'baklava' [0.1] | 'doughnut' [0.1]
    PlDet -> 'the' [0.8] | 'many' [0.2] 
    PlNTr -> 'cookies' [0.1] | 'cakes' [0.1] | 'chocolates' [0.1] | 'pancakes' [0.1] | 'souffles' [0.1] | 'eclaires' [0.1] | 'croissants' [0.1] | 'strudels' [0.1] | 'baklava' [0.1] | 'doughnuts' [0.1]
    RP -> 'that' [0.6] | 'which' [0.4] 
    NTand -> 'and' [1.0]
    Adv -> 'because' [0.5] | 'since' [0.5]   
    Neg -> 'not' [1.0]
    
""")
