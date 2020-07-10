from sys import argv
import csv
import pandas as pd
from os import mkdir
from not_grammar import not_grammar
from nltk import BottomUpLeftCornerChartParser, Nonterminal, nonterminals
from nltk.draw.tree import draw_trees
from nltk.tree import ParentedTree
import nltk
def read_file(filename):

    with open(filename, newline='') as rfile, open('newresults.csv', mode='w') as new_file:

        reader = list(csv.reader(rfile, delimiter='\t', lineterminator='\n'))
        out_writer = csv.writer(new_file, delimiter=',', lineterminator='\n', quotechar='/')

        out_writer.writerow(['target', 'prediction', 'target length', 'correct'])

        for line in reader[1:]:
            newline = [sentence.split()[:sentence.split().index('<eos>')] if '<eos>' in sentence.split() else sentence.split() for sentence in line[1:]]
            targlen = len(newline[0])
            correct = 1 if newline[0] == newline[1] else 0
            out_writer.writerow([' '.join(newline[0]), ' '.join(newline[1]), targlen, correct])
 
def incorrect_files():

    with open("newresults.csv", 'r') as results_file, open("pos_neg.csv", 'w') as neg_file, open("pos_pos.csv", 'w') as pos_file:
        
        results_reader = csv.reader(results_file, delimiter=',')
        neg_writer = csv.writer(neg_file, delimiter=',', lineterminator='\n', quotechar='/')
        pos_writer = csv.writer(pos_file, delimiter=',', lineterminator='\n', quotechar='/')

        boolList = []
        for row in results_reader:
            if row[0] == 'target':
                neg_writer.writerow(row)
                pos_writer.writerow(row)
            else:
                if row[0] != row[1]:             
                    # pos -> neg transforms
                    if 'not' in row[0]:
                        neg_writer.writerow(row)
                    # pos -> pos transforms
                    elif 'not' not in row[0]:
                        pos_writer.writerow(row)

        return 'pos_pos.csv', 'pos_neg.csv'

def negate_target(neg_file):
    with open(neg_file, 'r') as neg_read:

        neg_reader = list(csv.reader(neg_read, delimiter=','))[1:]
        boolList = []

        for line in neg_reader:
            targsent = line[0].split()
            predsent = line[1].split()

            not_index = targsent.index('not')
            targverb = targsent[not_index + 1]

            if 'not' in predsent and targverb in predsent:
                verb_index = predsent.index(targverb)
                if predsent[verb_index - 1] == 'not':
                    boolList.append(1)
                else: 
                    boolList.append(0)
            else:
                boolList.append(0)

        return boolList

def preserve_category(posfile, negfile):

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

        PPtargtrees, PPpredtrees, PNtargtrees, PNpredtrees = [], [], [], []

        for i in range(len(readerlist)):
            # get each sentence
            targlist = [line[0].split() for line in readerlist[i]]
            predlist = [line[1].split() for line in readerlist[i]]

            # return list of generators for parses
            targ_parses = [parser.parse(targ) for targ in targlist]
            pred_parses = [parser.parse(pred) for pred in predlist]

            # returns number of parses in each generator
            len_predparses = [len(list(parser.parse(pred))) for pred in predlist]

            npwriter.writerow(['target', 'prediction'])
            for j in range(len(pred_parses)):
                if len_predparses[j] == 0: 
                    npwriter.writerow([' '.join(targlist[j]), ' '.join(predlist[j])])
                    if i == 0:
                        PPtargtrees.append('N/A')
                        PPpredtrees.append('N/A')
                    else:
                        PNtargtrees.append('N/A')
                        PNpredtrees.append('N/A')
                else:
                    if i == 0:
                        PPtargtrees.append(next(targ_parses[j]))
                        PPpredtrees.append(next(pred_parses[j]))
                    else:
                        PNtargtrees.append(next(targ_parses[j]))
                        PNpredtrees.append(next(pred_parses[j]))

        return PPtargtrees, PPpredtrees, PNtargtrees, PNpredtrees

def equal_structs(targtrees, predtrees):
    
    boolList = []
    length = range(len(targtrees))
    for tree in length:
        if targtrees[tree] == 'N/A':
            boolList.append('N/A')
        elif len(targtrees[tree].leaves()) != len(predtrees[tree].leaves()):
            boolList.append(0)
        else:
            targprods = targtrees[tree].productions()
            predprods = predtrees[tree].productions()
            targNodes = [production.lhs() for production in targprods]
            predNodes = [production.lhs() for production in predprods]

            if targNodes == predNodes:
                boolList.append(1)
            else:
                boolList.append(0)

    return boolList

def clausal(targtrees, predtrees):

    boolList = []
    length = range(len(targtrees))
    for tree in length:
        if targtrees[tree] == 'N/A':
            boolList.append('N/A')
        else:
            targNodes = [prod for prod in targtrees[tree].productions() if (str(prod.lhs()) == 'S' or str(prod.lhs()) == 'AdvP' or str(prod.lhs()) == 'RelP') or ('S' in str(prod.rhs()) or 'AdvP' in str(prod.rhs()) or 'RelP' in str(prod.rhs())) or 'VP' in str(prod.rhs())]
            predNodes = [prod for prod in predtrees[tree].productions() if (str(prod.lhs()) == 'S' or str(prod.lhs()) == 'AdvP' or str(prod.lhs()) == 'RelP') or ('S' in str(prod.rhs()) or 'AdvP' in str(prod.rhs()) or 'RelP' in str(prod.rhs())) or 'VP' in str(prod.rhs())]

            if targNodes == predNodes:
                boolList.append(1)
            else:
                boolList.append(0)

    return boolList

def negate_main(predtrees):
    boolList = []
    length = range(len(predtrees))
    for tree in length:
        if predtrees[tree] == 'N/A':
            boolList.append('N/A')
        else:
            for subtree in predtrees[tree].subtrees(filter=lambda t: t.label() == 'S'):
                subtree
            if 'not' in subtree.leaves():
                boolList.append(1)
            else:
                boolList.append(0)
    
    return boolList

def pos_csv_writer(pos_file, pos_catBOOL, PPequal_structsBOOL, PPclausalBOOL):

    with open(pos_file, 'r') as read_file, open('pos_posBOOLS.csv', 'w') as boolsfile:

        reader = list(csv.reader(read_file, delimiter=','))
        writer = csv.writer(boolsfile, delimiter=',', lineterminator='\n')

        reader[0].extend(["Preserves grammatical categories", "Preserves Tree Structure", "Preserves Significant Clauses"])
        writer.writerow(reader[0])

        reader = reader[1:]
        lenreader = range(len(reader))

        for i in lenreader:
            reader[i].extend([pos_catBOOL[i], PPequal_structsBOOL[i], PPclausalBOOL[i]])
            writer.writerow(reader[i])
    
    return 'pos_posBOOLS.csv'

def neg_csv_writer(neg_file, neg_catBOOL, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL, PNnegate_targetBOOL):
    
    with open(neg_file, 'r') as read_file, open('pos_negBOOLS.csv', 'w') as boolsfile:

        reader = list(csv.reader(read_file, delimiter=','))
        writer = csv.writer(boolsfile, delimiter=',', lineterminator='\n')

        reader[0].extend(["Preserves grammatical categories", "Preserves Tree Structure", "Preserves Significant Clauses", "Negates Main Verb", "Negates Target Verb"])
        writer.writerow(reader[0])

        reader = reader[1:]
        length = range(len(reader))
        for i in length:
            reader[i].extend([neg_catBOOL[i], PNequal_structsBOOL[i], PNclausalBOOL[i], PNnegate_mainBOOL[i], PNnegate_targetBOOL[i]])
            writer.writerow(reader[i])
    
    return 'pos_negBOOLS.csv'

# def make_dicts(max_len, pcorrect_dict, ncorrect_dict, ptotal_dict, ntotal_dict, total_dict, possents, negsents, PPequal_structsBOOL, PPclausalBOOL, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL, PNnegate_targetBOOL):
    
#     # STRING COMPARISON DICTS

#     avg_dict, posavg_dict, negavg_dict = {}, {}, {}
    
#     for i in range(max_len):
#         avg_dict[i + 1] = round((pcorrect_dict[i + 1] + ncorrect_dict[i + 1]) / total_dict[i + 1], 3) if total_dict[i + 1] != 0 else 'N/A'
#         posavg_dict[i + 1] = round(pcorrect_dict[i + 1] / ptotal_dict[i + 1], 3) if ptotal_dict[i + 1] != 0 else 'N/A'
#         negavg_dict[i + 1] = round(ncorrect_dict[i + 1] / ntotal_dict[i + 1], 3) if ntotal_dict[i + 1] != 0 else 'N/A'

#     # TREE COMPARISON DICTS

#     PPesAvg, PPclausalAvg, PNesAvg, PNclausalAvg, PNnmAvg, PNntAvg = {}, {}, {}, {}, {}, {}

#     # pos -> pos dicts
#     poslen_list = [len(line.split()) for line in possents[0]] 
#     if len(poslen_list) > 0:
#         posmax_len = max(poslen_list)

#         pos_template = {length + 1:0 for length in list(range(posmax_len))}
#         PPequal_structsDICT, PPclausalDICT = dict(pos_template), dict(pos_template)
#         postotal_dict = {length + 1:poslen_list.count(length + 1) for length in list(range(posmax_len))}

#         poslen = range(len(possents))

#         for i in poslen:
#             targlen = len(possents[0][i].split())

#             PPequal_structsDICT[targlen] += PPequal_structsBOOL[i]
#             PPclausalDICT[targlen] += PPclausalBOOL[i]
        
#         for i in range(posmax_len):
#             PPesAvg[i + 1] = round(PPequal_structsDICT[i + 1] / postotal_dict[i + 1], 3) if postotal_dict[i + 1] != 0 else 'N/A'
#             PPclausalAvg[i + 1] = round(PPclausalDICT[i + 1] / postotal_dict[i + 1], 3) if postotal_dict[i + 1] != 0 else 'N/A'

    
#     # pos -> neg dicts

#     neglen_list = [len(line.split()) for line in negsents[0]]
#     if len(neglen_list) > 0:
#         negmax_len = max(neglen_list)
        
#         neg_template = {length + 1:0 for length in list(range(negmax_len))}
#         PNequal_structsDICT, PNclausalDICT, PNnegate_mainDICT, PNnegate_targetDICT = dict(neg_template), dict(neg_template), dict(neg_template), dict(neg_template)
#         negtotal_dict = {length + 1:neglen_list.count(length + 1) for length in list(range(negmax_len))}
        
#         neglen = range(len(negsents))

#         for i in neglen:
#             targlen = len(negsents[0][i].split())

#             PNequal_structsDICT[targlen] += PNequal_structsBOOL[i]
#             PNclausalDICT[targlen] += PNclausalBOOL[i]
#             PNnegate_mainDICT[targlen] += PNnegate_mainBOOL[i]
#             PNnegate_targetDICT[targlen] += PNnegate_targetBOOL[i]
        
#         for i in range(negmax_len):
#             PNesAvg[i + 1] = round(PNequal_structsDICT[i + 1] / negtotal_dict[i + 1], 3) if negtotal_dict[i + 1] != 0 else 'N/A'
#             PNclausalAvg[i + 1] = round(PNclausalDICT[i + 1] / negtotal_dict[i + 1], 3) if negtotal_dict[i + 1] != 0 else 'N/A'
#             PNnmAvg[i + 1] = round(PNnegate_mainDICT[i + 1] / negtotal_dict[i + 1], 3) if negtotal_dict[i + 1] != 0 else 'N/A'
#             PNntAvg[i + 1] = round(PNnegate_targetDICT[i + 1] / negtotal_dict[i + 1], 3) if negtotal_dict[i + 1] != 0 else 'N/A'

#     return avg_dict, posavg_dict, negavg_dict, PPesAvg, PPclausalAvg, PNesAvg, PNclausalAvg, PNnmAvg, PNntAvg
#     # return avg_dict, pcorrectDICT, ncorrectDICT, PPequal_structsDICT, PPclausalDICT, PNequal_structsDICT, PNclausalDICT, PNnegate_mainDICT, PNnegate_targetDICT
def make_dicts(pos_file, neg_file):
    with open(pos_file, 'r') as pos_read, open(neg_file, 'r') as neg_read:
        pos_reader = list(csv.reader(pos_read, delimiter=','))[1:]
        neg_reader = list(csv.reader(neg_read, delimiter=','))[1:]

        pos_lenlist = [int(row[2]) for row in pos_reader]
        neg_lenlist = [int(row[2]) for row in neg_reader]
        
        max_poslen = max(pos_lenlist)
        max_neglen = max(neg_lenlist)

        # Create Templates
        pos_total_template = {length + 1:pos_lenlist.count(length + 1) if pos_lenlist.count(length + 1) > 0 else 'N/A' for length in list(range(max_poslen))}
        pos_template = {length + 1:0  if pos_total_template[length + 1] != 'N/A' else 'N/A' for length in list(range(max_poslen))}

        neg_total_template = {length + 1:neg_lenlist.count(length + 1)  if neg_lenlist.count(length + 1) > 0 else 'N/A' for length in list(range(max_neglen))}
        neg_template = {length + 1:0 if neg_total_template[length + 1] != 'N/A' else 'N/A' for length in list(range(max_neglen))}

        # Initialize pos and neg dicts
        pos_catDICT, pos_structsDICT, pos_clausalDICT = pos_template, pos_template, pos_template
        neg_catDICT, neg_structsDICT, neg_clausalDICT, negates_mainDICT, negates_targDICT = neg_template, neg_template, neg_template, neg_template, neg_template

        # Fill dictionaries
        for row in pos_reader:
            pos_catDICT[row[2]] += row[4]
            pos_structsDICT[row[2]] += row[5]
            pos_clausalDICT[row[2]] += row[6]

        for row in neg_reader:
            neg_catDICT[row[2]] += row[4]
            neg_structsDICT[row[2]] += row[5]
            neg_clausalDICT[row[2]] += row[6]
            negates_mainDICT[row[2]] += row[7]
            negates_targDICT[row[2]] += row[8]




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
    accuracyBOOL - size of results file
    pos_catBOOL, PPequal_structsBOOL, PPclausalBOOL - size of pos_pos.csv
    neg_catBOOL, PNnegate_targetBOOL, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL - size of pos_neg.csv

    '''
    # Files
    read_file(argv[1]) # Reads raw results, turns it into new results by taking off <eos> token
    pos_file, neg_file = incorrect_files() # pos_neg.txt, pos_pos.txt

    # Strings
    PNnegate_targetBOOL = negate_target(neg_file) # returns a list of booleans for negating the target verb
    pos_catBOOL, neg_catBOOL = preserve_category(pos_file, neg_file) # returns a list of booleans for perserving grammatical categories

    # Trees
    PPtargtrees, PPpredtrees, PNtargtrees, PNpredtrees = make_trees(pos_file, neg_file) # create trees for all transformations

    PPequal_structsBOOL, PPclausalBOOL = equal_structs(PPtargtrees, PPpredtrees), clausal(PPtargtrees, PPpredtrees)
    PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL = equal_structs(PNtargtrees, PNpredtrees), clausal(PNtargtrees, PNpredtrees), negate_main(PNpredtrees)

    posBOOLS = pos_csv_writer(pos_file, pos_catBOOL, PPequal_structsBOOL, PPclausalBOOL) # writes into a new CSV with 4 columns: targ, pred, boolean values
    negBOOLS = neg_csv_writer(neg_file, neg_catBOOL, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL, PNnegate_targetBOOL) # writes into a new CSV with 5 columns: targ, pred, boolean values

    # Creates dictionaries, key: sen length, value: bools
    # avg_dict, posavg_dict, negavg_dict, PPesAvg, PPclausalAvg, PNesAvg, PNclausalAvg, PNnmAvg, PNntAvg = make_dicts(max_len, pcorrect_dict, ncorrect_dict, ptotal_dict, ntotal_dict, total_dict, [PPtargsents, PPpredtrees], [PNtargsents, PNpredsents], PPequal_structsBOOL, PPclausalBOOL, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL, PNnegate_targetBOOL)
    something = make_dicts(posBOOLS, negBOOLS)
    # list of all dictionaries
    dictlist = [avg_dict, posavg_dict, negavg_dict, PPesAvg, PPclausalAvg, PNesAvg, PNclausalAvg, PNnmAvg, PNntAvg]
    
    # dictionary names
    dictnames = ['Total Correct', 'Correct Pos Transforms', 'Correct Neg Transforms', 'Equal Structures (PP)', 'Preserves S, AdvP, RelP Structs (PP)', 'Equal Structures (PN)', 'Preserves S, AdvP, RelP Structs (PN)', 'Negates Main Clause (PN)', 'Negates Target Verb (PN)']
    
    # write dictionaries to files
    write_dicts(dictlist, dictnames, max_len)

main()
