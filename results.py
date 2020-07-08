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

    with open(filename, newline='') as rfile, open('newresults.txt', mode='w') as new_file:

        reader = list(csv.reader(rfile, delimiter='\t', lineterminator='\n'))
        out_writer = csv.writer(new_file, delimiter='\t', lineterminator='\n', quotechar='/')

        out_writer.writerow(['target', 'prediction'])

        for line in reader[1:]:
            # print(line)
            newline = [sentence.split()[:sentence.split().index('<eos>')] if '<eos>' in sentence.split() else sentence.split() for sentence in line[1:]]
            out_writer.writerow([' '.join(newline[0]), ' '.join(newline[1])])

def results():

    with open("newresults.txt", 'r') as results_file, open("pos_neg.txt", 'w') as neg_file, open("pos_pos.txt", 'w') as pos_file:
        
        results_reader = list(csv.reader(results_file, delimiter='\t'))
        neg_writer = csv.writer(neg_file, delimiter='\t', lineterminator='\n', quotechar='/')
        pos_writer = csv.writer(pos_file, delimiter='\t', lineterminator='\n', quotechar='/')

        neg_writer.writerow(["target" , "prediction"])
        pos_writer.writerow(["target", "prediction"])

        len_list = [len(line[0].split()) for line in results_reader[1:]]
        max_len = max(len_list)

        template = {length + 1:0 for length in list(range(max_len))}
        pcorrect_dict, ncorrect_dict, ptotal_dict, ntotal_dict = dict(template), dict(template), dict(template), dict(template)

        total_dict = {length + 1:len_list.count(length + 1) for length in list(range(max_len))}

        for target, prediction in results_reader[1:]:
            linelen = len(target.split())

            if target == prediction:
                if 'not' in target:
                    ncorrect_dict[linelen] += 1
                    ntotal_dict[linelen] += 1
                else:
                    pcorrect_dict[linelen] += 1
                    ptotal_dict[linelen] += 1

            if target != prediction:                
                # pos -> neg transforms
                if 'not' in target:
                    neg_writer.writerow([target, prediction])
                    ntotal_dict[linelen] += 1
                # pos -> pos transforms
                if 'not' not in target:
                    pos_writer.writerow([target, prediction])
                    ptotal_dict[linelen] += 1

        return max_len, pcorrect_dict, ncorrect_dict, ptotal_dict, ntotal_dict, total_dict
  
# from nltk.draw.tree import draw_trees
  
def make_trees(filename):

    with open(filename, 'r') as seqfile, open("no-parses.csv", 'w') as npfile:
        npwriter = csv.writer(npfile, delimiter='\t', lineterminator='\n', quotechar='/')
        parser = BottomUpLeftCornerChartParser(not_grammar)
 
        seq_list = list(csv.reader(seqfile, delimiter='\t'))
        seq_list = seq_list[1:]

        # get each sentence
        targlist = [line[0].split() for line in seq_list]
        predlist = [line[1].split() for line in seq_list]

        # return list of generators for parses
        targ_parses = [parser.parse(targ) for targ in targlist]
        pred_parses = [parser.parse(pred) for pred in predlist]

        # returns number of parses in each generator
        len_predparses = [len(list(parser.parse(pred))) for pred in predlist]

        targtreelist = []
        predtreelist = []

        targsentlist = []
        predsentlist = []

        npwriter.writerow(['target', 'prediction'])
        for i in range(len(pred_parses)):
            if len_predparses[i] == 0: 
                npwriter.writerow(['target', 'prediction'])
                npwriter.writerow(['targ', 'pred'])
                npwriter.writerow(' '.join(predlist[i]))
                npwriter.writerow(['targ', 'pred'])
                print(npfile.closed)
                print([' '.join(targlist[i]), ' '.join(predlist[i])])
            else:
                targtreelist.append(next(targ_parses[i]))
                predtreelist.append(next(pred_parses[i]))

                targsentlist.append(' '.join(targlist[i]))
                predsentlist.append(' '.join(predlist[i]))
    
        return targtreelist, predtreelist, targsentlist, predsentlist

def equal_structs(targtrees, predtrees):
    
    boolList = []
    length = range(len(targtrees))
    for tree in length:
        if len(targtrees[tree].leaves()) != len(predtrees[tree].leaves()):
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
        for subtree in predtrees[tree].subtrees(filter=lambda t: t.label() == 'S'):
            subtree
        if 'not' in subtree.leaves():
            boolList.append(1)
        else:
            boolList.append(0)
    
    return boolList

def negate_target(targtrees, predtrees):
    boolList = []

    listlen = range(len(targtrees))
    for i in listlen:
        targsent = targtrees[i].leaves()

        not_index = targsent.index('not')
        targverb = targsent[not_index + 1]

        pred_sent = predtrees[i].leaves()

        if 'not' in pred_sent and targverb in pred_sent:
            verb_index = pred_sent.index(targverb)
            if pred_sent[verb_index - 1] == 'not':
                boolList.append(1)
            else: 
                boolList.append(0)
        else:
            boolList.append(0)
        
    return boolList

def pos_csv_writer(filename, PPtargsents, PPpredsents, bool0, bool1):

    with open(filename + 'BOOLS.csv', 'w') as writefile:
        writer = csv.writer(writefile, delimiter='\t', lineterminator='\n', quotechar='/')
        writer.writerow(['target', 'prediction', 'equal structures', 'equal S, AdvP, and RelP clauses'])
        length = range(len(PPtargsents))
        for i in length:
            writer.writerow([PPtargsents[i], PPpredsents[i], bool0[i], bool1[i]])

def neg_csv_writer(filename, PNtargsents, PNpredsents, bool0, bool1, bool2, bool3):
    with open(filename + 'BOOLS.csv', 'w') as writefile:
        writer = csv.writer(writefile, delimiter='\t', lineterminator='\n', quotechar='/')
        writer.writerow(['target', 'prediction', 'equal structures', 'equal S, AdvP, and RelP clauses', 'negates main clause', 'negates target verb'])
        length = range(len(PNtargsents))
        for i in length:
            writer.writerow([PNtargsents[i], PNpredsents[i], bool0[i], bool1[i], bool2[i], bool3[i]])

def make_dicts(max_len, pcorrect_dict, ncorrect_dict, ptotal_dict, ntotal_dict, total_dict, possents, negsents, PPequal_structsBOOL, PPclausalBOOL, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL, PNnegate_targetBOOL):
    
    # STRING COMPARISON DICTS

    avg_dict, posavg_dict, negavg_dict = {}, {}, {}
    
    for i in range(max_len):
        avg_dict[i + 1] = round((pcorrect_dict[i + 1] + ncorrect_dict[i + 1]) / total_dict[i + 1], 3) if total_dict[i + 1] != 0 else 'N/A'
        posavg_dict[i + 1] = round(pcorrect_dict[i + 1] / ptotal_dict[i + 1], 3) if ptotal_dict[i + 1] != 0 else 'N/A'
        negavg_dict[i + 1] = round(ncorrect_dict[i + 1] / ntotal_dict[i + 1], 3) if ntotal_dict[i + 1] != 0 else 'N/A'

    # TREE COMPARISON DICTS

    PPesAvg, PPclausalAvg, PNesAvg, PNclausalAvg, PNnmAvg, PNntAvg = {}, {}, {}, {}, {}, {}

    # pos -> pos dicts
    poslen_list = [len(line.split()) for line in possents[0]] 
    if len(poslen_list) > 0:
        posmax_len = max(poslen_list)

        pos_template = {length + 1:0 for length in list(range(posmax_len))}
        PPequal_structsDICT, PPclausalDICT = dict(pos_template), dict(pos_template)
        postotal_dict = {length + 1:poslen_list.count(length + 1) for length in list(range(posmax_len))}

        poslen = range(len(possents))

        for i in poslen:
            targlen = len(possents[0][i].split())

            PPequal_structsDICT[targlen] += PPequal_structsBOOL[i]
            PPclausalDICT[targlen] += PPclausalBOOL[i]
        
        for i in range(posmax_len):
            PPesAvg[i + 1] = round(PPequal_structsDICT[i + 1] / postotal_dict[i + 1], 3) if postotal_dict[i + 1] != 0 else 'N/A'
            PPclausalAvg[i + 1] = round(PPclausalDICT[i + 1] / postotal_dict[i + 1], 3) if postotal_dict[i + 1] != 0 else 'N/A'

    
    # pos -> neg dicts

    neglen_list = [len(line.split()) for line in negsents[0]]
    print(negsents)
    exit()
    if len(neglen_list) > 0:
        negmax_len = max(neglen_list)
        
        neg_template = {length + 1:0 for length in list(range(negmax_len))}
        PNequal_structsDICT, PNclausalDICT, PNnegate_mainDICT, PNnegate_targetDICT = dict(neg_template), dict(neg_template), dict(neg_template), dict(neg_template)
        negtotal_dict = {length + 1:neglen_list.count(length + 1) for length in list(range(negmax_len))}
        
        neglen = range(len(negsents))

        for i in neglen:
            targlen = len(negsents[0][i].split())

            PNequal_structsDICT[targlen] += PNequal_structsBOOL[i]
            PNclausalDICT[targlen] += PNclausalBOOL[i]
            PNnegate_mainDICT[targlen] += PNnegate_mainBOOL[i]
            PNnegate_targetDICT[targlen] += PNnegate_targetBOOL[i]
        
        for i in range(negmax_len):
            PNesAvg[i + 1] = round(PNequal_structsDICT[i + 1] / negtotal_dict[i + 1], 3) if negtotal_dict[i + 1] != 0 else 'N/A'
            PNclausalAvg[i + 1] = round(PNclausalDICT[i + 1] / negtotal_dict[i + 1], 3) if negtotal_dict[i + 1] != 0 else 'N/A'
            PNnmAvg[i + 1] = round(PNnegate_mainDICT[i + 1] / negtotal_dict[i + 1], 3) if negtotal_dict[i + 1] != 0 else 'N/A'
            PNntAvg[i + 1] = round(PNnegate_targetDICT[i + 1] / negtotal_dict[i + 1], 3) if negtotal_dict[i + 1] != 0 else 'N/A'

    return avg_dict, posavg_dict, negavg_dict, PPesAvg, PPclausalAvg, PNesAvg, PNclausalAvg, PNnmAvg, PNntAvg
    # return avg_dict, pcorrectDICT, ncorrectDICT, PPequal_structsDICT, PPclausalDICT, PNequal_structsDICT, PNclausalDICT, PNnegate_mainDICT, PNnegate_targetDICT
        
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

    read_file(argv[1]) # Reads raw results, turns it into new results by taking off <eos> token (using helper function)
 
    max_len, pcorrect_dict, ncorrect_dict, ptotal_dict, ntotal_dict, total_dict = results() # pos_neg.txt, pos_pos.txt, dictionaries

    PPtargtrees, PPpredtrees, PPtargsents, PPpredsents = make_trees('pos_pos.txt') # create trees for pos -> pos transformations
    PNtargtrees, PNpredtrees, PNtargsents, PNpredsents = make_trees('pos_neg.txt') # create trees for pos -> neg transformations

    PPequal_structsBOOL = equal_structs(PPtargtrees, PPpredtrees) # returns list of booleans for whether the structure of the sentence is equal for pos -> neg
    PNequal_structsBOOL = equal_structs(PNtargtrees, PNpredtrees) # returns list of booleans for whether the structure of the sentence is equal for pos -> neg

    PPclausalBOOL = clausal(PPtargtrees, PPpredtrees) # returns a list of booleans for preserving target clausal units: AdvP, S, RelP
    PNclausalBOOL = clausal(PNtargtrees, PNpredtrees) # returns a list of booleans for preserving target clausal units: AdvP, S, RelP

    PNnegate_mainBOOL = negate_main(PNpredtrees) # returns a list of booleans for negating the main clause
    PNnegate_targetBOOL = negate_target(PNtargtrees, PNpredtrees) # returns a list of booleans for negating the target verb

    pos_csv_writer('pos_pos', PPtargsents, PPpredsents, PPequal_structsBOOL, PPclausalBOOL) # writes into a new CSV with 4 columns: targ, pred, boolean values
    neg_csv_writer('pos_neg', PNtargsents, PNpredsents, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL, PNnegate_targetBOOL) # writes into a new CSV with 5 columns: targ, pred, boolean values

    # Creates dictionaries, key: sen length, value: bools
    avg_dict, posavg_dict, negavg_dict, PPesAvg, PPclausalAvg, PNesAvg, PNclausalAvg, PNnmAvg, PNntAvg = make_dicts(max_len, pcorrect_dict, ncorrect_dict, ptotal_dict, ntotal_dict, total_dict, [PPtargsents, PPpredtrees], [PNtargsents, PNpredsents], PPequal_structsBOOL, PPclausalBOOL, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL, PNnegate_targetBOOL)
    
    # list of all dictionaries
    dictlist = [avg_dict, posavg_dict, negavg_dict, PPesAvg, PPclausalAvg, PNesAvg, PNclausalAvg, PNnmAvg, PNntAvg]
    
    # dictionary names
    dictnames = ['Total Correct', 'Correct Pos Transforms', 'Correct Neg Transforms', 'Equal Structures (PP)', 'Preserves S, AdvP, RelP Structs (PP)', 'Equal Structures (PN)', 'Preserves S, AdvP, RelP Structs (PN)', 'Negates Main Clause (PN)', 'Negates Target Verb (PN)']
    
    # write dictionaries to files
    write_dicts(dictlist, dictnames, max_len)

main()
