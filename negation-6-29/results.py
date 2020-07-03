from sys import argv
import csv
import pandas as pd
from os import mkdir
from not_grammar import not_grammar
from nltk import BottomUpLeftCornerChartParser, Nonterminal, nonterminals
from nltk.draw.tree import draw_trees
from nltk.tree import ParentedTree

def read_file(filename):

    with open(filename, newline='') as rfile, open('newresults.txt', mode='w') as new_file:

        reader = list(csv.reader(rfile, delimiter='\t', lineterminator='\n'))
        out_writer = csv.writer(new_file, delimiter='\t', lineterminator='\n', quotechar='/')

        out_writer.writerow(['target', 'prediction'])

        for line in reader[1:]:
            newline = [sentence.split()[:sentence.split().index('<eos>')] for sentence in line[1:]]
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

        template = {length + 1:0 for length in list(range(max_len + 1))}
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
  
from nltk.draw.tree import draw_trees
  
def make_trees(filename):

    parser = BottomUpLeftCornerChartParser(not_grammar)

    with open(filename, 'r') as seqfile:
        seq_list = list(csv.reader(seqfile, delimiter='\t'))
        seq_list = seq_list[1:]

        targlist = [line[0].split() for line in seq_list]

        predlist = [line[1].split() for line in seq_list]

        targ_parses = [parser.parse(targ) for targ in targlist]
        pred_parses = [parser.parse(pred) for pred in predlist]

        targtreelist = []
        predtreelist = []

        for parses in targ_parses:
            for tree in parses:
                tree
            targtreelist.append(tree)

        for parses in pred_parses:
            for tree in parses:
                tree
            predtreelist.append(tree)

        # targtreelist = [tree
        #                 for parses in targ_parses
        #                 for tree in parses]
        # predtreelist = [[(tree)
        #                 for tree in parses]
        #                 for parses in pred_parses]

        return targtreelist, predtreelist

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
        if len(targtrees[tree].leaves()) != len(predtrees[tree].leaves()):
            boolList.append(0)
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
        for subtree in predtrees[tree].subtrees(filter=lambda t: t.label() == 'S'):
            subtree
        if 'not' in subtree.leaves():
            boolList.append(1)
        else:
            boolList.append(0)
    
    return boolList

def pos_csv_writer(filename, bool0, bool1):
    with open(filename + '.txt', 'r') as readfile, open(filename + 'BOOLS.txt', 'w') as writefile:

        reader = list(csv.reader(readfile, delimiter='\t'))
        reader = reader[1:]
        writer = csv.writer(writefile, delimiter='\t', lineterminator='\n', quotechar='/')
        writer.writerow(['target', 'prediction', 'equal structures', 'equal S, AdvP, and RelP clauses'])
        length = range(len(reader))
        for i in length:
            writer.writerow([reader[i][0], reader[i][1], bool0[i], bool1[i]])

def neg_csv_writer(filename, bool0, bool1, bool2):
    with open(filename + '.txt', 'r') as readfile, open(filename + 'BOOLS.txt', 'w') as writefile:
        
        reader = list(csv.reader(readfile, delimiter='\t'))
        reader = reader[1:]
        writer = csv.writer(writefile, delimiter='\t', lineterminator='\n', quotechar='/')
        writer.writerow(['target', 'prediction', 'equal structures', 'equal S, AdvP, and RelP clauses', 'negates main clause'])
        length = range(len(reader))
        for i in length:
            writer.writerow([reader[i][0], reader[i][1], bool0[i], bool1[i], bool2[i]])

def make_dicts(max_len, postext, negtext, PPequal_structsBOOL, PPclausalBOOL, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL):
    with open(postext, 'r') as posfile, open(negtext, 'r') as negfile:
        posreader = list(csv.reader(posfile, delimiter='\t'))
        posreader = posreader[1:]
        negreader = list(csv.reader(negfile, delimiter='\t'))
        negreader = negreader[1:]

        template = {length + 1:0 for length in list(range(max_len + 1))}
        PPequal_structsDICT, PPclausalDICT, PNequal_structsDICT, PNclausalDICT, PNnegate_mainDICT = dict(template), dict(template), dict(template), dict(template), dict(template)

        poslen = range(len(posreader))

        for i in poslen:
            targlen = len(posreader[i][0].split())
            PPequal_structsDICT[targlen] += PPequal_structsBOOL[i]
            PPclausalDICT[targlen] += PPclausalBOOL[i]
        
        neglen = range(len(negreader))

        for i in neglen:
            targlen = len(negreader[i][0].split())

            PNequal_structsDICT[targlen] += PNequal_structsBOOL[i]
            PNclausalDICT[targlen] += PNclausalBOOL[i]
            PNnegate_mainDICT[targlen] += PNnegate_mainBOOL[i]
        
        
        
# Main function
def main():

    read_file(argv[1]) # Reads raw results, turns it into new results by taking off <eos> token (using helper function)
 
    max_len, pcorrect_dict, ncorrect_dict, ptotal_dict, ntotal_dict, total_dict = results() #pos_neg.txt, pos_pos.txt, dicts.txt

    # Creates boolean structure for each sentence

    PPtargtrees, PPpredtrees = make_trees('pos_pos.txt') # create trees for pos -> pos transformations
    PNtargtrees, PNpredtrees = make_trees('pos_neg.txt') # create trees for pos -> neg transformations

    PPequal_structsBOOL = equal_structs(PPtargtrees, PPpredtrees) # returns list of booleans for whether the structure of the sentence is equal for pos -> neg
    PNequal_structsBOOL = equal_structs(PNtargtrees, PNpredtrees) # returns list of booleans for whether the structure of the sentence is equal for pos -> neg

    PPclausalBOOL = clausal(PPtargtrees, PPpredtrees) # returns a list of booleans for preserving target clausal units: AdvP, S, RelP
    PNclausalBOOL = clausal(PNtargtrees, PNpredtrees) # returns a list of booleans for preserving target clausal units: AdvP, S, RelP


    PNnegate_mainBOOL = negate_main(PNpredtrees)

    pos_csv_writer('pos_pos', PPequal_structsBOOL, PPclausalBOOL) # writes into a new CSV with 4 columns: targ, pred, boolean values
    neg_csv_writer('pos_neg', PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL) # writes into a new CSV with 5 columns: targ, pred, boolean values

    # Creates 4 dictionaries
    #  Key: sentence length, Values: sentences where equal_structs() == T
    #  Key: sentence length, Values: sentences where clausal() == T
    #  Key: sentence length, Values: sentences where negate_main() == T
    #  Key: sentence length, Values: sentences where negate_targ() == T
    boolDICTS = make_dicts(max_len, 'pos_pos.txt', 'pos_neg.txt', PPequal_structsBOOL, PPclausalBOOL, PNequal_structsBOOL, PNclausalBOOL, PNnegate_mainBOOL)
    
    # use dictwriter to make dicts.txt easier to read
    # import all results to google drive
    # confirm that the functions work correctly
main()
