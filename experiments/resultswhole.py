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
import statistics
import argparse

def read_file(filename):
    with open(filename, newline='') as rfile:
        reader = list(csv.reader(rfile, delimiter='\t', lineterminator='\n'))
        neg_list, pos_list = [], []
        poscorrectTOTAL = 0
        negcorrectTOTAL = 0
        for line in reader[1:]:
            newline = [sentence.split()[:sentence.split().index('<eos>')] if '<eos>' in sentence.split() else sentence.split() for sentence in line]
            sourcelen, targlen, predlen = len(newline[0]), len(newline[1]), len(newline[2])
            correct = 1 if newline[1] == newline[2] else 0
            if 'not' in newline[1]:
                pos = 0
                neg_list.append([' '.join(newline[1]), ' '.join(newline[2]), sourcelen, targlen, predlen, correct])
                negcorrectTOTAL += correct
            else:
                pos_list.append([' '.join(newline[1]), ' '.join(newline[2]), sourcelen, targlen, predlen, correct])
                poscorrectTOTAL += correct

    return pos_list, neg_list, poscorrectTOTAL, negcorrectTOTAL

def negate_target(neg_list):
    has_targetTOTAL, negates_targTOTAL = 0, 0
    for i in range(len(neg_list)):
        sourcelen = neg_list[i][2]
        correct = neg_list[i][5]
        if correct == 1:
            has_targetTOTAL += 1
            negates_targTOTAL += 1
            neg_list[i].extend([1, 1])
        else:
            targsent = neg_list[i][0].split()
            predsent = neg_list[i][1].split()
            not_index = targsent.index('not') 
            targverb = targsent[not_index + 1]
            if targverb in predsent:
                has_targetTOTAL += 1
                neg_list[i].extend([1])
                if 'not' in predsent:
                    verb_index = predsent.index(targverb)
                    if predsent[predsent.index('not') + 1] == targverb:
                        negates_targTOTAL += 1
                        neg_list[i].extend([1])
                    else:
                        neg_list[1].extend([0])
            else:
                neg_list[i].extend([0, 0])
    return has_targetTOTAL, negates_targTOTAL

def token_acc(pos_list, neg_list):
        sentlist = [pos_list, neg_list]
        token_precisionlist, token_recallList = [], []
        category_precisionlist, category_recallList = [], []

        prod_dict = {production.rhs()[0]: []  if isinstance(production.rhs()[0], str) else None for production in not_grammar.productions()}
        for production in not_grammar.productions():
            if isinstance(production.rhs()[0], str):
                prod_dict[production.rhs()[0]].append(production.lhs())
        
        for i in range(len(sentlist)):
            token_correctTOTAL, category_correctTOTAL = 0, 0
            targlenLIST = [sentlist[i][j][3] for j in range(len(sentlist[i]))]
            predlenLIST = [sentlist[i][j][4] for j in range(len(sentlist[i]))]

            pred_tokensTOTAL, targ_tokensTOTAL = 0, 0
            pred_tokensTOTAL += sum(predlenLIST)
            targ_tokensTOTAL += sum(targlenLIST)

            total_token_correct = 0
            total_category_correct = 0
            for j in range(len(sentlist[i])):
                targlen = targlenLIST[j]
                predlen = predlenLIST[j]
                if targlen > predlen:
                    cuttarg = sentlist[i][j][0].split()[0:predlen]
                    cutpred = sentlist[i][j][1].split()
                    length = predlen
                else:
                    cuttarg = sentlist[i][j][0].split()
                    cutpred = sentlist[i][j][1].split()[0:targlen]
                    length = targlen
                token_correct = [1 if cuttarg[i] == cutpred[i] else 0 for i in range(length)]
                category_correct = [1 if prod_dict[cuttarg[i]] == prod_dict[cutpred[i]] else 0 for i in range(length)]

                # total_token_correct += sum(token_correct)
                token_correctTOTAL += sum(token_correct)
                # total_category_correct += sum(category_correct)
                category_correctTOTAL += sum(category_correct)
            
            token_precisionlist.append((token_correctTOTAL/ pred_tokensTOTAL))
            token_recallList.append((token_correctTOTAL / targ_tokensTOTAL))

            category_precisionlist.append((category_correctTOTAL / pred_tokensTOTAL))
            category_recallList.append((category_correctTOTAL / targ_tokensTOTAL))

        return token_precisionlist, token_recallList, category_precisionlist, category_recallList
  
def make_trees(pos_list, neg_list, outfolder):

    noparses = os.path.join(outfolder, "no-parses.csv")
    with open(noparses, 'w', newline='') as npfile:
        npwriter = csv.writer(npfile, delimiter=',', lineterminator='\n', quotechar='/')
        parser = BottomUpLeftCornerChartParser(not_grammar)
        sentlist = [pos_list, neg_list]
        postrees, negtrees = [[], []], [[], []]
        treeslist = [postrees, negtrees]
        parseables = [0, 0]

        for i in range(len(sentlist)):
            # pos_list: target sent, pred sent, sourcelen, targlen, predlen, correctBOOL
            # return list of generators for parses
            targ_parses = [list(parser.parse(sentlist[i][j][0].split())) if sentlist[i][j][5] != 1 else "correct" for j in range(len(sentlist[i]))]
            pred_parses = [list(parser.parse(sentlist[i][j][1].split())) if sentlist[i][j][5] != 1 else "correct" for j in range(len(sentlist[i]))]

            # returns number of parses in each generator 
            npwriter.writerow(['Target', 'Prediction', 'Source Length'])
            for j in range(len(pred_parses)):
                if pred_parses[j] == "correct":
                    treeslist[i][0].append([sentlist[i][j][2], sentlist[i][j][3], "correct"])
                    treeslist[i][1].append([sentlist[i][j][2], sentlist[i][j][4], "correct"])
                    parseables[i] += 1
                    sentlist[i][j].extend([1])
                else:
                    if len(pred_parses[j]) == 0:
                        npwriter.writerow([sentlist[i][j][0], sentlist[i][j][1], sentlist[i][j][2]])
                        treeslist[i][0].append([sentlist[i][j][2], sentlist[i][j][3], 'N/A'])
                        treeslist[i][1].append([sentlist[i][j][2], sentlist[i][j][4], 'N/A'])
                        sentlist[i][j].extend([0])
                    else:
                        treeslist[i][0].append([sentlist[i][j][2], sentlist[i][j][3], targ_parses[j]])
                        treeslist[i][1].append([sentlist[i][j][2], sentlist[i][j][4], pred_parses[j]])
                        parseables[i] += 1
                        sentlist[i][j].extend([1])

    return treeslist, parseables[0], parseables[1], sum(parseables)

def equal_structs(pos_list, neg_list, treeslist):
    #treeslist: [[postarg, pospred], [negtarg, negpred]]
    # totals = [[pos structs, pos clausal], [neg structs, neg clausal]]
    totals = [[0, 0], [0, 0]]
    lists = [pos_list, neg_list]
    for i in range(len(treeslist)): # pos, neg
        length = range(len(treeslist[i][0]))
        for j in length:
            sourcelen = treeslist[i][0][j][0]
            targlen = treeslist[i][0][j][1]
            predlen = treeslist[i][1][j][1]
            if treeslist[i][0][j][2] == 'correct':
                lists[i][j].extend([1, 1])
                totals[i][0] += 1
                totals[i][1] += 1
            elif treeslist[i][0][j][2] == 'N/A':
                lists[i][j].extend(['N/A', 'N/A'])
            elif (targlen != predlen):
                lists[i][j].extend([0, 0])
            else:
                targNodes = [production.lhs() for production in treeslist[i][0][j][2][0].productions()]
                targclauses = [str(nodes) for nodes in targNodes if (str(nodes) == 'S' or str(nodes) == 'AdvP' or str(nodes) == 'RelP')]
                
                predNodes = [production.lhs() for production in treeslist[i][1][j][2][0].productions()]
                predclauses = [str(nodes) for nodes in predNodes if (str(nodes) == 'S' or str(nodes) == 'AdvP' or str(nodes) == 'RelP')]
                
                structbool = 1 if targNodes == predNodes else 0
                clausebool = 1 if targclauses == predclauses else 0

                lists[i][j].extend([structbool, clausebool])
                if structbool == 1:
                    totals[i][0] += 1
                if clausebool == 1:
                    totals[i][1] += 1

    return totals[0][0], totals[0][1], totals[1][0], totals[1][1]

def negate_main(neg_list, targtrees, predtrees):
    # extend(has main clause, negates main clause, negates outside of main clause)
    length = range(len(predtrees))
    mainclauseTOTAL, negatesmainTOTAL, negatesoutsideTOTAL, nomainTOTAL = 0, 0, 0, 0
    for i in length:
        sourcelen = targtrees[i][0]
        if predtrees[i][2] == 'correct':
            neg_list[i].extend([1, 1, 1])
            mainclauseTOTAL += 1
            negatesmainTOTAL += 1
        elif predtrees[i][2] == 'N/A':
            neg_list[i].extend([0, 0, 0])
        else:
            targlen, predlen = targtrees[i][1], predtrees[i][1]
            targsent, predsent = targtrees[i][2][0].leaves(), predtrees[i][2][0].leaves()
            not_index = targsent.index('not') 
            targverb = targsent[not_index + 1]
            # check if there's a main clause
            if 'S2' in [str(prod.lhs()) for prod in predtrees[i][2][0].productions()]:
                mainclauseTOTAL += 1
                neg_list[i].extend([1])
                # if there is a main clause then check if it's negated
                # do stuff with main clauses
                for subtree in predtrees[i][2][0].subtrees(filter=lambda t: t.label() == 'S2'):
                    subtree
                if subtree[1][1].label() == 'Neg':
                    negatesmainTOTAL += 1
                    neg_list[i].extend([1])
                else:
                    if 'not' in predsent:
                        negatesoutsideTOTAL += 1
                        neg_list[i].extend([1])
            else:
                nomainTOTAL += 1
                negbool = 1 if 'not' in predsent else 0
                neg_list[i].extend([0, 0, negbool])

    return mainclauseTOTAL, negatesmainTOTAL, negatesoutsideTOTAL, nomainTOTAL

def noAdvp(neg_list, targtrees, predtrees):
    negateone = 0
    negatefirst = 0
    negateselsewhere = 0
    oneclause = 0
    moreclauses = 0
    for i in range(len(neg_list)):
        if predtrees[i][2] != 'N/A' and predtrees[i][2] != 'correct': 
            predNodes = [str(production.lhs()) for production in predtrees[i][2][0].productions()]
            if predNodes.count('S') == 2 and 'not' in predtrees[i][2][0][0].leaves():
                negateone += 1
                oneclause += 1
            elif predNodes.count('S') > 2 and 'not' in predtrees[i][2][0][0].leaves():
                negatefirst += 1
                moreclauses += 1
            elif predNodes.count('S') > 2 and 'not' in predtrees[i][2][0].leaves() and 'not' not in predtrees[i][2][0][0].leaves():
                negateelsewhere += 1
                moreclauses += 1
    return negateone, negatefirst, negateselsewhere, oneclause, moreclauses

def pos_csv_writer(pos_list, outfolder):
    posbools = os.path.join(outfolder, 'pos_pos.csv')
    with open(posbools, 'w') as boolsfile:
        writer = csv.writer(boolsfile, delimiter=',', lineterminator='\n')
        writer.writerow(["Target Sentence",
                        "Predicted Sentence",
                        "Source Length",
                        "Target Length",
                        "Prediction Length",
                        "Correct Transformation",
                        "Parseable",
                        "Preserves Identical Tree Structure",
                        "Preserves Significant Clauses (S, AdvP, RelP)"])

        for i in range(len(pos_list)):
            writer.writerow(pos_list[i])
    
def neg_csv_writer(neg_list, outfolder):
    negbools = os.path.join(outfolder, "pos_neg.csv")
    with open(negbools, 'w') as boolsfile:
        writer = csv.writer(boolsfile, delimiter=',', lineterminator='\n')
        writer.writerow(["Target Sentence",
                        "Predicted Sentence",
                        "Source Length",
                        "Target Length",
                        "Prediction Length",
                        "Correct Transformation",
                        "Parseable",
                        "Preserves Identical Tree Structure",
                        "Preserves Significant Clauses (S, AdvP, RelP)",
                        "Negates Main Clause",
                        "Has Main Clause",
                        "Negates Main Clause",
                        "Negates Outside of Main Clause",
                        "Has Target Verb",
                        "Negates Target Verb"])

        for i in range(len(neg_list)):
            writer.writerow(neg_list[i])

def write_table(tablelist, tablenames, outfolder):
    tables = os.path.join(outfolder[:-8], '{0}-tables.csv'.format(argv[2]))
    with open(tables, 'w') as tablefile:
        tablewriter = csv.writer(tablefile, delimiter=',', lineterminator='\n')
        tablewriter.writerow(['Task', 'Model 1', 'Model 2', 'Model 3', 'Model 4', 'Model 5', 'Mean'])
        for i in range(len(tablelist[0])):
            average = statistics.mean([tablelist[0][i], tablelist[1][i], tablelist[2][i], tablelist[3][i], tablelist[4][i]])
            tablewriter.writerow([tablenames[i], tablelist[0][i], tablelist[1][i], tablelist[2][i], tablelist[3][i], tablelist[4][i], average])
# Main function
def main(resultsfile, outfolder):
    # pos_list: target sent, pred sent, sourcelen, targlen, predlen, correctBOOL
    # templates: total transformations (templateDICT is blank)
    pos_list, neg_list, poscorrectTOTAL, negcorrectTOTAL = read_file(resultsfile)
    token_precisionlist, token_recallList, category_precisionlist, category_recallList = token_acc(pos_list, neg_list) # returns proportion of correct tokens (pos, neg)
    treeslist, posparseables, negparseables, allparseables = make_trees(pos_list, neg_list, outfolder) # create trees for all transformations    
    posstructs, posclausal, negstructs, negclausal = equal_structs(pos_list, neg_list, treeslist) # [srcelen, targlen, predlen, BOOL]    
    mainclauseTOTAL, negatesmainTOTAL, negatesoutsideTOTAL, nomainTOTAL = negate_main(neg_list, treeslist[1][0], treeslist[1][1]) # [sourcelen, targlen, predlen, BOOL]
    has_targetTOTAL, negates_targTOTAL = negate_target(neg_list) # returns a list of booleans for negating the target verb
    if 'noadvp' in argv[1].lower():
        negateone, negatefirst, negateselsewhere, oneclause, moreclauses = noAdvp(neg_list, treeslist[1][0], treeslist[1][1])

    pos_csv_writer(pos_list, outfolder)
    neg_csv_writer(neg_list, outfolder)  # writes into a new CSV with columns: targ, pred, boolean values
    # Dictionaries
    tablelist = [len(pos_list), len(neg_list), poscorrectTOTAL, negcorrectTOTAL, round(token_precisionlist[0], 2),
            round(token_precisionlist[1], 2), round(token_recallList[0], 2), round(token_recallList[1], 2), round(category_precisionlist[0], 2),
            round(category_precisionlist[1], 2), round(category_recallList[0], 2), round(category_recallList[1], 2), posparseables,
            negparseables, allparseables, posstructs, posclausal, negstructs, negclausal, mainclauseTOTAL,
            negatesmainTOTAL, negatesoutsideTOTAL, nomainTOTAL, has_targetTOTAL,negates_targTOTAL]
    tablenames = ['Total Pos->Pos', 'Total Pos->Neg', 'Pos->Pos Correct', 'Pos->Neg Correct', 'Pos Token Precision',
                'Neg Token Precision', 'Pos Token Recall', 'Neg Token Recall', 'Pos Category Precision',
                'Neg Category Precision', 'Pos Category Recall', 'Neg Category Recall', 'Parseable Pos->Pos',
                'Parseable Pos->Neg', 'All Parseable Sentences', 'Equal Structures Pos->Pos', 'Preserves Clauses Pos->Pos', 'Equal Structures Pos->Neg', 'Preserves Clauses Pos->Neg', 'Has Main Clause',
                'Negates Main', 'Negates Outside Main', 'No Main Clause', 'Has Target Verb', 'Negates Target Verb']
    if 'noadvp' in argv[1].lower():
        tablelist.extend([negateone, negatefirst, negateselsewhere, oneclause, moreclauses])
        tablenames.extend(['Negates the One Adv Clause', 'Negates the First Adv Clause', 'Negates Elsewhere', 'Has one Adv Clause', 'Has more than one Adv Clause'])
    return tablelist, tablenames


tablelist = []
for i in range(5):
    task = argv[1]
    attention = argv[2]
    directory = argv[3]
    resultsfile = os.path.join(directory, task, 'models', 'GRU-GRU-{0}'.format(attention), 'model-{0}'.format(i + 1), 'results', '{0}.tsv'.format(task))
    outfolder = os.path.join(directory, task, '{0}-results'.format(attention), 'model-{0}'.format(i + 1))
    tablenums, tablenames = main(resultsfile, outfolder)
    tablelist.append(tablenums)
    print('Evaluated Model {0}'.format(i + 1))
print('Writing Results to File')
write_table(tablelist, tablenames, outfolder)



