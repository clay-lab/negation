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

def read_file(filename, directory):
    path = os.getcwd()
    print(path)
    posfile = os.path.join(directory, "pos_pos.csv")
    negfile = os.path.join(directory, "pos_neg.csv")
    with open(filename, newline='') as rfile, open(posfile, 'w') as pos_file, open(negfile, 'w') as neg_file:

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

        return posfile, negfile, boolLIST
 
# def incorrect_files(pos_pos, pos_neg):

    # with open(pos_pos, 'r') as pos_posfile, open(pos_neg, 'r') as pos_negfile, open("neg_incorrect.csv", 'w') as neg_file, open("pos_incorrect.csv", 'w') as pos_file:
        
    #     pos_reader = csv.reader(pos_posfile, delimiter=',')
    #     neg_reader = csv.reader(pos_negfile, delimiter=',')
    #     neg_writer = csv.writer(neg_file, delimiter=',', lineterminator='\n', quotechar='/')
    #     pos_writer = csv.writer(pos_file, delimiter=',', lineterminator='\n', quotechar='/')

    #     for row in pos_reader:
    #         if row[0] == 'target':
    #             pos_writer.writerow(row)
    #         else:
    #             if row[0] != row[1]:             
    #                 pos_writer.writerow(row)
    #     for row in neg_reader:
    #         if row[0] == 'target':
    #             neg_writer.writerow(row)
    #         else:
    #             if row[0] != row[1]:
    #                 neg_writer.writerow(row)
                
    #     return 'pos_incorrect.csv', 'neg_incorrect.csv'

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
                    if predsent[predsent.index('not')  + 1] == targverb:
                        boolList.append([sourcelen, targlen, predlen, 1])
                    else: 
                        boolList.append([sourcelen, targlen, predlen, 0])
                else:
                    boolList.append([sourcelen, targlen, predlen, 0])

        return boolList

def token_acc(pos_pos, pos_neg):
    with open(pos_pos, 'r') as pos_file, open(pos_neg, 'r') as neg_file:

        pos_reader = list(csv.reader(pos_file, delimiter=','))[1:]
        neg_reader = list(csv.reader(neg_file, delimiter=','))[1:]
        readerlist = [pos_reader, neg_reader]
        token_precisionlist, token_recallList = [], []
        category_precisionlist, category_recallList = [], []

        prod_dict = {production.rhs()[0]: []  if isinstance(production.rhs()[0], str) else None for production in not_grammar.productions()}
        for production in not_grammar.productions():
            if isinstance(production.rhs()[0], str):
                prod_dict[production.rhs()[0]].append(production.lhs())

        for i in range(len(readerlist)):
            sourcelens = [int(line[2]) for line in readerlist[i]]
            targlens = [int(line[3]) for line in readerlist[i]]
            predlens = [int(line[4]) for line in readerlist[i]]
            max_len = range(max(sourcelens))

            source_token_template = {length + 1: (sourcelens.count(length + 1) * (length + 1)) if sourcelens.count(length + 1) > 0 else 'N/A' for length in max_len}
            token_template = {length + 1:0  if source_token_template[length + 1] != 'N/A' else 'N/A' for length in max_len}
            targ_tokens, pred_tokens, category_template = dict(token_template), dict(token_template), dict(token_template)

            counter = 0
            for j in range(len(sourcelens)):
                pred_tokens[sourcelens[j]] += predlens[j]
            for j in range(len(sourcelens)):
                targ_tokens[sourcelens[j]] += targlens[j]

            total_token_correct = 0
            total_category_correct = 0
            for line in readerlist[i]:
                sourcelen = int(line[2])
                targlen = int(line[3])
                predlen = int(line[4])
                if targlen > predlen:
                    cuttarg = line[0].split()[0:predlen]
                    cutpred = line[1].split()
                    length = predlen
                else:
                    cuttarg = line[0].split()
                    cutpred = line[1].split()[0:targlen]
                    length = targlen
                token_correct = [1 if cuttarg[i] == cutpred[i] else 0 for i in range(length)]
                category_correct = [1 if prod_dict[cuttarg[i]] == prod_dict[cutpred[i]] else 0 for i in range(length)]

                # total_token_correct += sum(token_correct)
                token_template[sourcelen] += sum(token_correct)
                # total_category_correct += sum(category_correct)
                category_template[sourcelen] += sum(category_correct)

            token_precisionlist.append({j + 1: str(round((token_template[j + 1] / pred_tokens[j + 1]) * 100, 2)) + '%' if pred_tokens[j + 1] != 'N/A' else 'N/A'  for j in max_len})
            token_recallList.append({j + 1: str(round((token_template[j + 1] / targ_tokens[j + 1]) * 100, 2)) + '%' if targ_tokens[j + 1] != 'N/A' else 'N/A' for j in max_len})

            category_precisionlist.append({j + 1: str(round((category_template[j + 1] / pred_tokens[j + 1]) * 100, 2)) + '%' if pred_tokens[j + 1] != 'N/A' else 'N/A'  for j in max_len})
            category_recallList.append({j + 1: str(round((category_template[j + 1] / targ_tokens[j + 1]) * 100, 2)) + '%' if targ_tokens[j + 1] != 'N/A' else 'N/A' for j in max_len})

        token_list = [source_token_template, pred_tokens, targ_tokens, token_precisionlist[0], token_precisionlist[1], token_recallList[0], token_recallList[1], category_precisionlist[0], category_precisionlist[1], category_recallList[0], category_recallList[1]]
        token_names = ['Total source tokens', 'total prediction tokens per source', 'total target tokens per source', 'Pos->pos token precision', 'Pos->neg token precision', 'Pos->pos token recall', 'Pos->neg token recall', 'Pos->Pos category precision', 'Pos->neg category precision', 'Pos->pos category recall', 'Pos->Neg category recall']
        return token_list, token_names
      
#TODO: resolve ambiguity with 'the'
# def preserve_category(posfile, negfile):

    # with open(posfile, 'r') as pos_read, open(negfile, 'r') as neg_read:
    #     pos_reader = list(csv.reader(pos_read, delimiter=','))[1:]
    #     neg_reader = list(csv.reader(neg_read, delimiter=','))[1:]

    #     prod_dict = {}
    #     posBOOL, negBOOL = [], []

    #     for production in not_grammar.productions():
    #         if isinstance(production.rhs()[0], str):
    #             prod_dict.update({production.rhs()[0]: production.lhs()})


    #     for line in pos_reader:
    #         targ = line[0].split()
    #         pred = line[1].split()
    #         targ_gram = [prod_dict[word] for word in targ]
    #         pred_gram = [prod_dict[word] for word in pred]
    #         if targ_gram == pred_gram:
    #             posBOOL.append(1)
    #         else:
    #             posBOOL.append(0)

    #     for line in neg_reader:
    #         targ = line[0].split()
    #         pred = line[1].split()
    #         targ_gram = [prod_dict[word] for word in targ]
    #         pred_gram = [prod_dict[word] for word in pred]
    #         if targ_gram == pred_gram:
    #             negBOOL.append(1)
    #         else:
    #             negBOOL.append(0)

    # return posBOOL, negBOOL
  
def make_trees(pos_file, neg_file):

    noparses = os.path.join(argv[2], "no-parses.csv")
    with open(pos_file, 'r') as pos_read, open(neg_file, 'r') as neg_read, open(noparses, 'w') as npfile:
        npwriter = csv.writer(npfile, delimiter=',', lineterminator='\n', quotechar='/')
        parser = BottomUpLeftCornerChartParser(not_grammar)
 
        pos_reader = list(csv.reader(pos_read, delimiter=','))[1:]
        neg_reader = list(csv.reader(neg_read, delimiter=','))[1:]
        readerlist = [pos_reader, neg_reader]
        postrees = [[], []]
        negtrees = [[], []]
        treeslist = [postrees, negtrees]

        boolList = [[], []]
        for i in range(len(readerlist)):
            # get each sentence
            targlist = [line[0].split() for line in readerlist[i]]
            predlist = [line[1].split() for line in readerlist[i]]
            sourcelen = [int(line[2]) for line in readerlist[i]]
            targlen = [int(line[3]) for line in readerlist[i]]
            predlen = [int(line[4]) for line in readerlist[i]]
            correctlist = [int(line[5]) for line in readerlist[i]]

            # return list of generators for parses
            targ_parses = [list(parser.parse(targlist[j])) if correctlist[j] != 1 else "correct" for j in range(len(targlist))]
            pred_parses = [list(parser.parse(predlist[j])) if correctlist[j] != 1 else "correct" for j in range(len(predlist))]

            # returns number of parses in each generator 
            npwriter.writerow(['Target', 'Prediction', 'Source Length'])
            for j in range(len(pred_parses)):
                if pred_parses[j] == "correct":
                    treeslist[i][0].append([sourcelen[j], targlen[j], "correct"])
                    treeslist[i][1].append([sourcelen[j], predlen[j], "correct"])
                    boolList[i].append([sourcelen[j], targlen[j], predlen[j], 1])
                else:
                    if len(pred_parses[j]) == 0: 
                        npwriter.writerow([' '.join(targlist[j]), ' '.join(predlist[j]), sourcelen[j]])
                        treeslist[i][0].append([sourcelen[j], targlen[j], 'N/A'])
                        treeslist[i][1].append([sourcelen[j], predlen[j], 'N/A'])
                        boolList[i].append([sourcelen[j], targlen[j], predlen[j], 0])
                    else:
                            # append target tree, append pred parses GENERATOR not tree
                            treeslist[i][0].append([sourcelen[j], targlen[j], targ_parses[j]])
                            treeslist[i][1].append([sourcelen[j], predlen[j], pred_parses[j]])
                            boolList[i].append([sourcelen[j], targlen[j], predlen[j], 1])

        return treeslist[0][0], treeslist[0][1], treeslist[1][0], treeslist[1][1], boolList[0], boolList[1]

def equal_structs(targtrees, predtrees):
    
    boolList1, boolList2 = [], []
    length = range(len(targtrees))
    for i in length:
        sourcelen = targtrees[i][0]
        targlen = targtrees[i][1]
        predlen = predtrees[i][1]
        if targtrees[i][2] == 'correct':
            boolList1.append([sourcelen, targlen, predlen, 1])
            boolList2.append([sourcelen, targlen, predlen, 1])
        elif targtrees[i][2] == 'N/A':
            boolList1.append([sourcelen, targlen, predlen, 'N/A'])
            boolList2.append([sourcelen, targlen, predlen, 'N/A'])
        elif (targlen != predlen):
            boolList1.append([sourcelen, targlen, predlen, 0])
            boolList2.append([sourcelen, targlen, predlen, 0])
        else:
            targprods = [tree.productions() for tree in targtrees[i][2]]
            predprods = [tree.productions() for tree in predtrees[i][2]]
            targNodes, predNodes, targclauses, predclauses = [], [], [], []
            structlist, clauselist = [], []
            for j in range(len(targprods)):
                targNodes.append([production.lhs() for production in targprods[j]])
                targclauses.append([str(nodes) for nodes in targNodes[j] if (str(nodes) == 'S' or str(nodes) == 'AdvP' or str(nodes) == 'RelP')])
            for j in range(len(predprods)):
                predNodes.append([production.lhs() for production in predprods[j]])
                predclauses.append([str(nodes) for nodes in predNodes[j] if (str(nodes) == 'S' or str(nodes) == 'AdvP' or str(nodes) == 'RelP')])
            for j in range(len(targNodes)):
                for k in range(len(predNodes)):
                    structlist.append(targNodes[j] == predNodes[k])
                    clauselist.append(targclauses[j] == predclauses[k])
            if True in structlist:
                boolList1.append([sourcelen, targlen, predlen, 1])
            else:
                boolList1.append([sourcelen, targlen, predlen, 0])
            if True in clauselist:
                boolList2.append([sourcelen, targlen, predlen, 1])
            else:
                boolList2.append([sourcelen, targlen, predlen, 0])

    return boolList1, boolList2

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
            treeslist = []
            for trees in predtrees[tree][2]:
                for subtree in trees.subtrees(filter=lambda t: t.label() == 'S'):
                    subtree
                if len(subtree) == 2 and subtree[1][1].leaves()[0] == 'not':
                    treeslist.append(1)
                else:
                    treeslist.append(0)
            if 1 in treeslist:
                boolList.append([sourcelen, targlen, predlen, 1])
                    # print(subtree.leaves())
            else:
                boolList.append([sourcelen, targlen, predlen, 0])
                
    
    return boolList

def pos_csv_writer(pos_file, structsBOOL, clausalBOOL, pos_parsedBOOL):
    posbools = os.path.join(argv[2], 'pos_posBOOLS.csv')
    with open(pos_file, 'r') as read_file, open(posbools, 'w') as boolsfile:

        reader = list(csv.reader(read_file, delimiter=','))
        writer = csv.writer(boolsfile, delimiter=',', lineterminator='\n')

        reader[0].extend(["Preserves Tree Structure", "Preserves Significant Clauses", "Parseable"])
        writer.writerow(reader[0])

        reader = reader[1:]
        lenreader = range(len(reader))

        for i in lenreader:
            reader[i].extend([structsBOOL[i][3], clausalBOOL[i][3], pos_parsedBOOL[i][3]])
            writer.writerow(reader[i])
    
    return posbools

def neg_csv_writer(neg_file, structsBOOL, clausalBOOL, neg_mainBOOL, neg_targBOOL, neg_parsedBOOL):
    negbools = os.path.join(argv[2], "pos_negBOOLS.csv")
    with open(neg_file, 'r') as read_file, open(negbools, 'w') as boolsfile:

        reader = list(csv.reader(read_file, delimiter=','))
        writer = csv.writer(boolsfile, delimiter=',', lineterminator='\n')

        reader[0].extend(["Preserves Tree Structure", "Preserves Significant Clauses", "Negates Main Verb", "Negates Target Verb", "Parseable"])
        writer.writerow(reader[0])

        reader = reader[1:]
        length = range(len(reader))
        for i in length:
            reader[i].extend([structsBOOL[i][3], clausalBOOL[i][3], neg_mainBOOL[i][3], neg_targBOOL[i][3], neg_parsedBOOL[i][3]])
            writer.writerow(reader[i])
    
    return negbools

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
    pos_structsDICT, pos_clausalDICT, pos_parseableDICT = dict(templatelist[0]), dict(templatelist[0]), dict(templatelist[0])
    pos_dicts = [pos_structsDICT, pos_clausalDICT, pos_parseableDICT]

    neg_structsDICT, neg_clausalDICT, negates_mainDICT, negates_targDICT, neg_parseableDICT = dict(templatelist[1]), dict(templatelist[1]), dict(templatelist[1]), dict(templatelist[1]), dict(templatelist[1])
    neg_dicts = [neg_structsDICT, neg_clausalDICT, negates_mainDICT, negates_targDICT, neg_parseableDICT]

    pos_correctDICT, neg_correctDICT, total_correctDICT = dict(templatelist[0]), dict(templatelist[1]), dict(templatelist[2])
    correct_dicts = [pos_correctDICT, neg_correctDICT, total_correctDICT]

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
            total_correctDICT[sourcelen] += 1
        elif correctBOOL[i][4] == 0 and correct == 1:
            neg_correctDICT[sourcelen] += 1
            total_correctDICT[sourcelen] += 1
    
    # Positive Average Dictionaries
    pos_averages = []
    for i in range(len(pos_dicts)):
        pos_averages.append({j + 1: (str(round((pos_dicts[i][j + 1] / totaltemplatelist[0][j + 1]) * 100, 2))) + '%' if  totaltemplatelist[0][j + 1] != 'N/A' else 'N/A' for j in list(range(max_len))})
    # Negative Average Dictionaries
    neg_averages = []
    for i in range(len(neg_dicts)):
        neg_averages.append({j + 1: (str(round((neg_dicts[i][j + 1] / totaltemplatelist[1][j + 1]) * 100, 2))) + '%' if totaltemplatelist[1][j + 1] != 'N/A' else 'N/A' for j in list(range(max_len))})
    # Total Average Dict
    averages = []
    for i in range(len(correct_dicts)):
        averages.append({j + 1: (str(round((correct_dicts[i][j + 1] / totaltemplatelist[i][j + 1]) * 100, 2))) + '%' if totaltemplatelist[i][j + 1] != 'N/A' else 'N/A' for j in list(range(max_len))})
    
    # Total, pos total, pos correct, neg total, neg correct, total correct, pos structs, pos clausal, neg structs, neg clausal,  neg main, neg targ
    dictlist = [totaltemplatelist[2], total_correctDICT,
    totaltemplatelist[0], 
    pos_correctDICT, 
    totaltemplatelist[1], 
    neg_correctDICT,  
    averages[0], 
    averages[1], 
    averages[2], 
    pos_parseableDICT,
    pos_averages[2], 
    pos_averages[0], 
    pos_averages[1],
    neg_parseableDICT, 
    neg_averages[4], 
    neg_averages[0], 
    neg_averages[1], 
    neg_averages[2], 
    neg_averages[3]]
    dictnames = ["Total Sentences per Length", 
    "Total Correct Sentences per Length", 
    "Total pos->pos sents per len", 
    "Correct pos->pos sents per len", 
    "Total pos->neg sents per len", 
    "Correct pos->neg sents per len", 
    'Correct Pos->Pos Transformations', 
    'correct Pos->Neg Transformations', 
    'Total correct per len', 
    'Total parseable sentences (pos->pos)', 
    'Parseable sentences (pos->pos)', 
    'Preserve tree structures (pos->pos)', 
    'Preserve significant clauses (pos->pos)', 
    'Total parseable sentences pos->neg', 
    'Parseable Sentences (pos->neg)', 
    'Preserve tree structures (pos->neg)', 
    'Preserve significant clauses (pos->neg)', 
    'Negates main clause (pos->neg)', 
    'Negates target (pos->neg)']
    
    return max_len, dictlist, dictnames

def write_dicts(dictlist, dictnames, max_len):
    dicts = os.path.join(argv[2], 'dicts.csv')
    with open(dicts, 'w') as dictfile:

        newdicts = [{'Dictionary Name':dictname} for dictname in dictnames]
        
        for i in range(len(newdicts)):
            newdicts[i].update(dictlist[i])
        
        lenlist = list(range(max_len + 1))
        lenlist[0] = 'Dictionary Name'

        fieldnames = lenlist

        writer = csv.DictWriter(dictfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
        writer.writeheader()
        writer.writerows(newdicts)

        
# Main function
def main():

    # Files
    pos_pos, pos_neg, correctBOOL = read_file(argv[1], argv[2]) # Reads raw results, turns it into new results by taking off <eos> token

    # Strings
    neg_targetBOOL = negate_target(pos_neg) # returns a list of booleans for negating the target verb
    tokenList, token_names = token_acc(pos_pos, pos_neg) # returns proportion of correct tokens (pos, neg)
    # Trees
    pos_targTREES, pos_predTREES, neg_targTREES, neg_predTREES, pos_parsedBOOL, neg_parsedBOOL = make_trees(pos_pos, pos_neg) # create trees for all transformations
    pos_structsBOOL, pos_clausalBOOL = equal_structs(pos_targTREES, pos_predTREES) # [sourcelen, targlen, predlen, BOOL]
    neg_structsBOOL, neg_clausalBOOL = equal_structs(neg_targTREES, neg_predTREES)
    neg_mainBOOL = negate_main(neg_targTREES, neg_predTREES) # [sourcelen, targlen, predlen, BOOL]
    posBOOLS = pos_csv_writer(pos_pos, pos_structsBOOL, pos_clausalBOOL,pos_parsedBOOL)
    negBOOLS = neg_csv_writer(pos_neg, neg_structsBOOL, neg_clausalBOOL, neg_mainBOOL, neg_targetBOOL, neg_parsedBOOL)  # writes into a new CSV with columns: targ, pred, boolean values
    
    # Dictionaries
    pos_boolLIST, neg_boolLIST = [pos_structsBOOL, pos_clausalBOOL, pos_parsedBOOL], [neg_structsBOOL, neg_clausalBOOL, neg_mainBOOL, neg_targetBOOL, neg_parsedBOOL]
    max_len, dictlist, dictnames = make_dicts(pos_boolLIST, neg_boolLIST, correctBOOL)
    dictlist.extend(tokenList)
    dictnames.extend(token_names)
    write_dicts(dictlist, dictnames, max_len)

def parses():
    with open('no-parses.csv', 'r') as npfile:
        reader = csv.reader(npfile)
        for line in reader:
            print(len(line[0].split()))
main()
# parses()
