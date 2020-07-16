from sys import argv
import csv
import pandas as pd
from os import mkdir
import os
from not_grammar import not_grammar
from nltk import BottomUpLeftCornerChartParser, Nonterminal, nonterminals
from nltk.draw.tree import draw_trees
from nltk.tree import ParentedTree
import nltk

def read_file(filename):
    path = os.getcwd()
    print(path)
    with open(filename, newline='') as rfile, open("pos_pos.csv", 'w') as pos_file, open("pos_neg.csv", 'w') as neg_file:

        boolLIST = []

        reader = list(csv.reader(rfile, delimiter='\t', lineterminator='\n'))
        neg_writer = csv.writer(neg_file, delimiter=',', lineterminator='\n', quotechar='/')
        pos_writer = csv.writer(pos_file, delimiter=',', lineterminator='\n', quotechar='/')

        neg_writer.writerow(['target', 'prediction', 'source length', 'target length', 'prediction length', 'correct'])
        pos_writer.writerow(['target', 'prediction', 'source length', 'target length', 'prediction length', 'correct'])

        for line in reader[1:]:
            newline = [sentence.split()[:sentence.split().index('<eos>')] if '<eos>' in sentence.split() else sentence.split() for sentence in line]
            sourcelen = len(newline[0])
            targlen = len(newline[1])
            predlen = len(newline[2])
            correct = 1 if newline[1] == newline[2] else 0
            if 'not' in newline[1]:
                neg_writer.writerow([' '.join(newline[1]), ' '.join(newline[2]), sourcelen, targlen, predlen, correct])
                pos = 0
            else:
                pos_writer.writerow([' '.join(newline[1]), ' '.join(newline[2]), sourcelen, targlen, predlen, correct])
                pos = 1
            boolLIST.append([sourcelen, targlen, predlen, correct, pos])

        return "pos_pos.csv", "pos_neg.csv", boolLIST
 
# def incorrect_files(pos_pos, pos_neg):

    with open(pos_pos, 'r') as pos_posfile, open(pos_neg, 'r') as pos_negfile, open("neg_incorrect.csv", 'w') as neg_file, open("pos_incorrect.csv", 'w') as pos_file:
        
        pos_reader = csv.reader(pos_posfile, delimiter=',')
        neg_reader = csv.reader(pos_negfile, delimiter=',')
        neg_writer = csv.writer(neg_file, delimiter=',', lineterminator='\n', quotechar='/')
        pos_writer = csv.writer(pos_file, delimiter=',', lineterminator='\n', quotechar='/')

        for row in pos_reader:
            if row[0] == 'target':
                pos_writer.writerow(row)
            else:
                if row[0] != row[1]:             
                    pos_writer.writerow(row)
        for row in neg_reader:
            if row[0] == 'target':
                neg_writer.writerow(row)
            else:
                if row[0] != row[1]:
                    neg_writer.writerow(row)
                
        return 'pos_incorrect.csv', 'neg_incorrect.csv'

def negate_target(neg_file):
    with open(neg_file, 'r') as neg_read:

        neg_reader = list(csv.reader(neg_read, delimiter=','))[1:]
        boolList = []

        for line in neg_reader:
            correct = int(line[5])
            targlen = int(line[3])
            predlen = int(line[4])
            sourcelen = int(line[2])
            if correct == 1:
                boolList.append([sourcelen, targlen, predlen, 1])
            else:
                targsent = line[0].split()
                predsent = line[1].split()
                

                # print(targsent)
                not_index = targsent.index('not') 
                targverb = targsent[not_index + 1]

                if 'not' in predsent and targverb in predsent:
                    verb_index = predsent.index(targverb)
                    if predsent[verb_index - 1] == 'not':
                        boolList.append([sourcelen, targlen, predlen, 1])
                    else: 
                        boolList.append([sourcelen, targlen, predlen, 0])
                else:
                    boolList.append([sourcelen, targlen, predlen, 0])

        return boolList
#TODO: resolve ambiguity with 'the'
# def preserve_category(posfile, negfile):

    with open(posfile, 'r') as pos_read, open(negfile, 'r') as neg_read:
        pos_reader = list(csv.reader(pos_read, delimiter=','))[1:]
        neg_reader = list(csv.reader(neg_read, delimiter=','))[1:]

        prod_dict = {}
        posBOOL, negBOOL = [], []

        for production in not_grammar.productions():
            if isinstance(production.rhs()[0], str):
                prod_dict.update({production.rhs()[0]: production.lhs()})


        for line in pos_reader:
            targ = line[0].split()
            pred = line[1].split()
            targ_gram = [prod_dict[word] for word in targ]
            pred_gram = [prod_dict[word] for word in pred]
            if targ_gram == pred_gram:
                posBOOL.append(1)
            else:
                posBOOL.append(0)

        for line in neg_reader:
            targ = line[0].split()
            pred = line[1].split()
            targ_gram = [prod_dict[word] for word in targ]
            pred_gram = [prod_dict[word] for word in pred]
            if targ_gram == pred_gram:
                negBOOL.append(1)
            else:
                negBOOL.append(0)

    return posBOOL, negBOOL
  
def make_trees(pos_file, neg_file):

    with open(pos_file, 'r') as pos_read, open(neg_file, 'r') as neg_read, open("no-parses.csv", 'w') as npfile:
        npwriter = csv.writer(npfile, delimiter=',', lineterminator='\n', quotechar='/')
        parser = BottomUpLeftCornerChartParser(not_grammar)
 
        pos_reader = list(csv.reader(pos_read, delimiter=','))[1:]
        neg_reader = list(csv.reader(neg_read, delimiter=','))[1:]
        readerlist = [pos_reader, neg_reader]
        postrees = [[], []]
        negtrees = [[], []]
        treeslist = [postrees, negtrees]

        for i in range(len(readerlist)):
            # get each sentence
            targlist = [line[0].split() for line in readerlist[i]]
            predlist = [line[1].split() for line in readerlist[i]]
            sourcelen = [int(line[2]) for line in readerlist[i]]
            targlen = [int(line[3]) for line in readerlist[i]]
            predlen = [int(line[4]) for line in readerlist[i]]
            correctlist = [int(line[5]) for line in readerlist[i]]

            # return list of generators for parses
            targ_parses = [parser.parse(targlist[j]) if correctlist[j] != 1 else "correct" for j in range(len(targlist))]
            pred_parses = [parser.parse(predlist[j]) if correctlist[j] != 1 else "correct" for j in range(len(predlist))]

            # returns number of parses in each generator
            len_predparses = [len(list(parser.parse(pred))) for pred in predlist]
 
            npwriter.writerow(['target', 'prediction'])
            for j in range(len(pred_parses)):
                if pred_parses[j] == "correct":
                    treeslist[i][0].append([sourcelen[j], targlen[j], "correct"])
                    treeslist[i][1].append([sourcelen[j], predlen[j], "correct"])
                else:
                    if len_predparses[j] == 0: 
                        npwriter.writerow([' '.join(targlist[j]), ' '.join(predlist[j])])
                        treeslist[i][0].append([sourcelen[j], targlen[j], 'N/A'])
                        treeslist[i][1].append([sourcelen[j], predlen[j], 'N/A'])
                    else:
                            treeslist[i][0].append([sourcelen[j], targlen[j], next(targ_parses[j])])
                            treeslist[i][1].append([sourcelen[j], predlen[j], next(pred_parses[j])])

        return treeslist[0][0], treeslist[0][1], treeslist[1][0], treeslist[1][1]


def equal_structs(targtrees, predtrees):
    
    boolList = []
    length = range(len(targtrees))
    for tree in length:
        sourcelen = targtrees[tree][0]
        targlen = targtrees[tree][1]
        predlen = predtrees[tree][1]
        if targtrees[tree][2] == 'correct':
            boolList.append([sourcelen, targlen, predlen, 1])
        elif targtrees[tree][2] == 'N/A':
            boolList.append([sourcelen, targlen, predlen, 'N/A'])
        elif (targlen != predlen):
            boolList.append([sourcelen, targlen, predlen, 0])
        else:
            targprods = (targtrees[tree][2]).productions()
            predprods = (predtrees[tree][2]).productions()
            targNodes = [production.lhs() for production in targprods]
            predNodes = [production.lhs() for production in predprods]

            if targNodes == predNodes:
                boolList.append([sourcelen, targlen, predlen, 1])
            else:
                boolList.append([sourcelen, targlen, predlen, 0])

    return boolList

def clausal(targtrees, predtrees):

    boolList = []
    length = range(len(targtrees))
    for tree in length:
        sourcelen = targtrees[tree][0]
        targlen = targtrees[tree][1]
        predlen = predtrees[tree][1]
        if targtrees[tree][2] == 'correct':
            boolList.append([sourcelen, targlen, predlen, 1])
        elif targtrees[tree][2] == 'N/A':
            boolList.append([sourcelen, targlen, predlen,'N/A'])
        else:
            targNodes = [prod for prod in targtrees[tree][2].productions() if (str(prod.lhs()) == 'S' or str(prod.lhs()) == 'AdvP' or str(prod.lhs()) == 'RelP') or ('S' in str(prod.rhs()) or 'AdvP' in str(prod.rhs()) or 'RelP' in str(prod.rhs())) or 'VP' in str(prod.rhs())]
            predNodes = [prod for prod in predtrees[tree][2].productions() if (str(prod.lhs()) == 'S' or str(prod.lhs()) == 'AdvP' or str(prod.lhs()) == 'RelP') or ('S' in str(prod.rhs()) or 'AdvP' in str(prod.rhs()) or 'RelP' in str(prod.rhs())) or 'VP' in str(prod.rhs())]

            if targNodes == predNodes:
                boolList.append([sourcelen, targlen, predlen, 1])
            else:
                boolList.append([sourcelen, targlen, predlen, 0])

    return boolList

def negate_main(targtrees, predtrees):
    boolList = []
    length = range(len(predtrees))
    for tree in length:
        sourcelen = targtrees[tree][0]
        targlen = targtrees[tree][1]
        predlen = predtrees[tree][1]
        if predtrees[tree][2] == 'correct':
            boolList.append([sourcelen, targlen, predlen, 1])
        elif predtrees[tree][2] == 'N/A':
            boolList.append([sourcelen, targlen, predlen, 'N/A'])
        else:
            for subtree in predtrees[tree][2].subtrees(filter=lambda t: t.label() == 'S'):
                subtree
            if 'not' in subtree.leaves():
                boolList.append([sourcelen, targlen, predlen, 1])
            else:
                boolList.append([sourcelen, targlen, predlen, 0])
    
    return boolList

def pos_csv_writer(pos_file, structsBOOL, clausalBOOL):

    with open(pos_file, 'r') as read_file, open('pos_posBOOLS.csv', 'w') as boolsfile:

        reader = list(csv.reader(read_file, delimiter=','))
        writer = csv.writer(boolsfile, delimiter=',', lineterminator='\n')

        reader[0].extend(["Preserves Tree Structure", "Preserves Significant Clauses"])
        writer.writerow(reader[0])

        reader = reader[1:]
        lenreader = range(len(reader))

        for i in lenreader:
            reader[i].extend([structsBOOL[i][2], clausalBOOL[i][2]])
            writer.writerow(reader[i])
    
    return 'pos_posBOOLS.csv'

def neg_csv_writer(neg_file, structsBOOL, clausalBOOL, neg_mainBOOL, neg_targBOOL):
    
    with open(neg_file, 'r') as read_file, open('pos_negBOOLS.csv', 'w') as boolsfile:

        reader = list(csv.reader(read_file, delimiter=','))
        writer = csv.writer(boolsfile, delimiter=',', lineterminator='\n')

        reader[0].extend(["Preserves Tree Structure", "Preserves Significant Clauses", "Negates Main Verb", "Negates Target Verb"])
        writer.writerow(reader[0])

        reader = reader[1:]
        length = range(len(reader))
        for i in length:
            reader[i].extend([structsBOOL[i][2], clausalBOOL[i][2], neg_mainBOOL[i][2], neg_targBOOL[i][2]])
            writer.writerow(reader[i])
    
    return 'pos_negBOOLS.csv'

def make_dicts(posBOOLS, negBOOLS, correctBOOL):
    # [sourcelen, targlen, predlen, correct, pos]

    pos_lenlist = [posBOOLS[0][i][0] for i in range(len(posBOOLS[0]))] 
    neg_lenlist = [negBOOLS[0][i][0] for i in range(len(negBOOLS[0]))]
    total_lenlist = [correctBOOL[i][0] for i in range(len(correctBOOL))]
    max_len = max(total_lenlist)
    lenlists = [pos_lenlist, neg_lenlist, total_lenlist]

    # Create Templates
    totaltemplatelist = []
    templatelist = []
    for i in range(len(lenlists)):
        totaltemplatelist.append({length + 1:lenlists[i].count(length + 1) if lenlists[i].count(length + 1) > 0 else 'N/A' for length in list(range(max_len))})
        templatelist.append({length + 1:0  if totaltemplatelist[i][length + 1] != 'N/A' else 'N/A' for length in list(range(max_len))})

    # Initialize pos and neg dicts
    pos_structsDICT, pos_clausalDICT, pos_correctDICT = dict(templatelist[0]), dict(templatelist[0]), dict(templatelist[0])
    pos_dicts = [pos_structsDICT, pos_clausalDICT]

    neg_structsDICT, neg_clausalDICT, negates_mainDICT, negates_targDICT, neg_correctDICT = dict(templatelist[1]), dict(templatelist[1]), dict(templatelist[1]), dict(templatelist[1]), dict(templatelist[1])
    neg_dicts = [neg_structsDICT, neg_clausalDICT, negates_mainDICT, negates_targDICT]

    # Fill dictionaries
    for i in range(len(posBOOLS)):
        for sent in posBOOLS[i]:
            sourcelen = sent[0]
            linebool = 0 if sent[3] == 'N/A' else sent[3]
            pos_dicts[i][sourcelen] += linebool

    for i in range(len(negBOOLS)):
        for sent in negBOOLS[i]:
            sourcelen = sent[0]
            linebool = 0 if sent[3] == 'N/A' else sent[3]
            neg_dicts[i][sourcelen] += linebool

    for i in range(len(correctBOOL)):
        sourcelen = correctBOOL[i][0]
        correct = correctBOOL[i][3]
        templatelist[2][sourcelen] += correct
        if correctBOOL[i][4] == 1 and correct == 1:
            pos_correctDICT[sourcelen] += 1
        elif correctBOOL[i][4] == 0 and correct == 1:
            neg_correctDICT[sourcelen] += 1
        
    pos_structsAVG = {i + 1: (str(round(((pos_structsDICT[i + 1]) / pos_total_template[i + 1]) * 100, 2))) + '%' if pos_total_template[i + 1] != 'N/A' else 'N/A' for i in list(range(max_poslen))}
    pos_clausalAVG = {i + 1: (str(round(((pos_clausalDICT[i + 1]) / pos_total_template[i + 1]) * 100, 2))) + '%' if pos_total_template[i + 1] != 'N/A' else 'N/A' for i in list(range(max_poslen))}

    neg_structsAVG = {i + 1: (str(round(((neg_structsDICT[i + 1]) / neg_total_template[i + 1]) * 100, 2))) + '%' if neg_total_template[i + 1] != 'N/A' else 'N/A' for i in list(range(max_neglen))}
    neg_clausalAVG = {i + 1: (str(round(((neg_clausalDICT[i + 1]) / neg_total_template[i + 1])* 100, 2))) + '%' if neg_total_template[i + 1] != 'N/A' else 'N/A' for i in list(range(max_neglen))}
    neg_mainAVG = {i + 1: (str(round(((negates_mainDICT[i + 1]) / neg_total_template[i + 1])* 100, 2))) + '%' if neg_total_template[i + 1] != 'N/A' else 'N/A' for i in list(range(max_neglen))}
    neg_targAVG = {i + 1: (str(round(((negates_targDICT[i + 1]) / neg_total_template[i + 1]) * 100, 2))) + '%' if neg_total_template[i + 1] != 'N/A' else 'N/A' for i in list(range(max_neglen))}
    
    avg_dict = {i + 1: (str(round((total_correctDICT[i + 1]/ total_template[i + 1]) * 100, 2))) + '%' if total_template[i + 1] != 'N/A' else 'N/A' for i in list(range(max_len))}
    dictlist = [total_template, pos_total_template, pos_correctDICT, neg_total_template, neg_correctDICT, avg_dict, pos_structsAVG, pos_clausalAVG, neg_structsAVG, neg_clausalAVG, neg_mainAVG, neg_targAVG]
    
    return max_len, dictlist

def write_dicts(dictlist, dictnames, max_len):
    with open('dicts.csv', 'w') as dictfile:

        newdicts = [{'Dictionary Name':dictname} for dictname in dictnames]

        for i in range(len(newdicts)):
            newdicts[i].update(dictlist[i])
        
        lenlist = list(range(max_len + 1))
        lenlist[0] = 'Dictionary Name'

        fieldnames = lenlist

        writer = csv.DictWriter(dictfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(newdicts)

        
# Main function
def main():
    ''' 
    PPequal_structsBOOL, PPclausalBOOL - size of pos_pos.csv
    PNnegate_targetBOOL, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL - size of pos_neg.csv

    '''
    # Files
    # Reads raw results, turns it into new results by taking off <eos> token
    pos_pos, pos_neg, correctBOOL = read_file(argv[1])  # [sourcelen, targlen, predlen, correct, pos]
    # pos_incorrect, neg_incorrect = incorrect_files(pos_pos, pos_neg) # pos_neg.txt, pos_pos.txt

    # Strings
    neg_targetBOOL = negate_target(pos_neg) # returns a list of booleans for negating the target verb

    # Trees
    pos_targTREES, pos_predTREES, neg_targTREES, neg_predTREES = make_trees(pos_pos, pos_neg) # create trees for all transformations

    pos_structsBOOL, pos_clausalBOOL = equal_structs(pos_targTREES, pos_predTREES), clausal(pos_targTREES, pos_predTREES) # [targlen, predlen, BOOL]
    neg_structsBOOL, neg_clausalBOOL, neg_mainBOOL = equal_structs(neg_targTREES, neg_predTREES), clausal(neg_targTREES, neg_predTREES), negate_main(neg_targTREES, neg_predTREES) # [targlen, predlen, BOOL]

    posBOOLS = pos_csv_writer(pos_pos, pos_structsBOOL, pos_clausalBOOL)
    negBOOLS = neg_csv_writer(pos_neg, neg_structsBOOL, neg_clausalBOOL, neg_mainBOOL, neg_targetBOOL)  # writes into a new CSV with 5 columns: targ, pred, boolean values
    
    pos_boolLIST = [pos_structsBOOL, pos_clausalBOOL]
    neg_boolLIST = [neg_structsBOOL, neg_clausalBOOL, neg_mainBOOL, neg_targetBOOL]
    # Creates dictionaries, key: sen length, value: bools
    
    # max_len, pos_total_template, neg_total_template, pos_catAVG, pos_structsAVG, pos_clausalAVG, neg_catAVG, neg_structsAVG, neg_clausalAVG, neg_mainAVG, neg_targAVG, avg_dict = make_dicts(posBOOLS, negBOOLS, newresults)
    max_len, dictlist = make_dicts(pos_boolLIST, neg_boolLIST, correctBOOL)

    # dictionary names
    dictnames = ["Total Sentences per Length", "Total pos->pos sents per len", "Correct pos->pos sents per len", "Total pos->neg sents per len", "Correct pos->neg sents per len", 'Total Correct per len', 'Preserve tree structures (pos->pos)', 'Preserve significant clauses (pos->pos)', 'Preserve tree structures (pos->neg)', 'Preserve significant clauses (pos->neg)', 'Negates main clause (pos->neg)', 'Negates target (pos->neg)']
    
    # write dictionaries to files
    write_dicts(dictlist, dictnames, max_len)

main()
