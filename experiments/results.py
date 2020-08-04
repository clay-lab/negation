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
    with open(filename, newline='') as rfile:
        reader = list(csv.reader(rfile, delimiter='\t', lineterminator='\n'))
        neg_list, pos_list = [], []
        for line in reader[1:]:
            newline = [sentence.split()[:sentence.split().index('<eos>')] if '<eos>' in sentence.split() else sentence.split() for sentence in line]
            sourcelen, targlen, predlen = len(newline[0]), len(newline[1]), len(newline[2])
            correct = 1 if newline[1] == newline[2] else 0
            if 'not' in newline[1]:
                pos = 0
                neg_list.append([' '.join(newline[1]), ' '.join(newline[2]), sourcelen, targlen, predlen, correct])
            else:
                pos_list.append([' '.join(newline[1]), ' '.join(newline[2]), sourcelen, targlen, predlen, correct])
    # len lists
    pos_lenlist, neg_lenlist = [pos_list[i][2] for i in range(len(pos_list))] , [neg_list[i][2] for i in range(len(neg_list))]
    max_len, min_len = max(max(pos_lenlist), max(neg_lenlist)), min(min(pos_lenlist), min(neg_lenlist))
    len_range = list(range(min_len - 1, max_len))

    # Create Templates
    pos_template = {length + 1:pos_lenlist.count(length + 1) for length in len_range}
    neg_template = {length + 1:neg_lenlist.count(length + 1) for length in len_range}
    total_template = {length + 1:pos_template[length + 1] + neg_template[length + 1] for length in len_range}
    templateDICT = {length + 1:0 for length in len_range}
    # Fill dictionaries
    pos_correctDICT, neg_correctDICT, total_correctDICT = dict(templateDICT), dict(templateDICT), dict(templateDICT)
    for i in range(len(pos_list)):
        sourcelen = pos_list[i][2]
        pos_correctDICT[sourcelen] += pos_list[i][5]
        total_correctDICT[sourcelen] += pos_list[i][5]
    for i in range(len(neg_list)):
        sourcelen = neg_list[i][2]
        neg_correctDICT[sourcelen] += neg_list[i][5]
        total_correctDICT[sourcelen] += neg_list[i][5]
    
    #Average dicts
    avgDICT = {length + 1: str(round((total_correctDICT[length + 1] / total_template[length + 1]) * 100, 2)) + '%' for length in len_range}
    avgposDICT = {length + 1: str(round((pos_correctDICT[length + 1] / pos_template[length + 1]) * 100, 2)) + '%' for length in len_range}
    avgnegDICT = {length + 1: str(round((neg_correctDICT[length + 1] / neg_template[length + 1]) * 100, 2)) + '%' for length in len_range}

    dictlist = [total_template, total_correctDICT, pos_template, pos_correctDICT, neg_template, neg_correctDICT, avgposDICT, avgnegDICT, avgDICT]
    dictnames = ["Total Sentences (#)", 
                "Total Correct Transformations (#)",
                "Total Pos->Pos Transformations (#)",
                "Correct Pos->Pos Transformations (#)",
                "Total Pos->Neg Transformations (#)",
                "Correct Pos->Neg Transformations (#)",
                "Correct Pos->Pos Transformations (%)",
                "Correct Pos->Neg Transformations (%)",
                "Total Correct Transformations (%)"]
    avgdictlist = [dictlist[6], dictlist[7], dictlist[8]]
    avgdictnames = [dictnames[6], dictnames[7], dictnames[8]]


    return pos_list, neg_list, dict(pos_template), dict(neg_template), dict(templateDICT), dictlist, dictnames, len_range, avgdictlist, avgdictnames

def negate_target(neg_list, neg_templateDICT, templateDICT, len_range):
    # dicts: has the target verb, negates the target verb
    has_targetDICT, negates_targDICT = dict(templateDICT), dict(templateDICT)
    for i in range(len(neg_list)):
        sourcelen = neg_list[i][2]
        correct = neg_list[i][5]
        if correct == 1:
            has_targetDICT[sourcelen] += 1
            negates_targDICT[sourcelen] += 1
            neg_list[i].extend([1, 1])
        else:
            targsent = neg_list[i][0].split()
            predsent = neg_list[i][1].split()
            not_index = targsent.index('not') 
            targverb = targsent[not_index + 1]
            if targverb in predsent:
                has_targetDICT[sourcelen] += 1
                neg_list[i].extend([1])
                if 'not' in predsent:
                    verb_index = predsent.index(targverb)
                    if predsent[predsent.index('not') + 1] == targverb:
                        negates_targDICT[sourcelen] += 1
                        neg_list[i].extend([1])
                    else:
                        neg_list[1].extend([0])
            else:
                neg_list[i].extend([0, 0])
    avgnegates_targDICT = {length + 1: str(round((negates_targDICT[length + 1] / neg_templateDICT[length + 1]) * 100, 2)) + '%' for length in len_range}
    avgnegates_targ1DICT = {length + 1: str(round((negates_targDICT[length + 1] / has_targetDICT[length + 1]) * 100, 2)) + '%' if has_targetDICT[length + 1] != 0 else 0 for length in len_range}
    avghas_targDICT = {length + 1: str(round((has_targetDICT[length + 1] / neg_templateDICT[length + 1]) * 100, 2)) + '%' for length in len_range}
    dictlist = [avghas_targDICT, avgnegates_targDICT, avgnegates_targ1DICT]
    dictnames = ["Pos->Neg Predictions Containing the Target Verb (%)",
                "Pos->Neg Predictions Negating the Target Verb (Denominator: all pos->neg sentences)",
                "Pos->Neg Predictions Negating the Target Verb (Denominator: pos->neg with target verb)"
                ]
    avgdictlist = dictlist 
    avgdictnames = dictnames
    return dictlist, dictnames, avgdictlist, avgdictnames

def token_acc(pos_list, neg_list, templateDICT, len_range):
        sentlist = [pos_list, neg_list]
        token_precisionlist, token_recallList = [], []
        category_precisionlist, category_recallList = [], []

        prod_dict = {production.rhs()[0]: []  if isinstance(production.rhs()[0], str) else None for production in not_grammar.productions()}
        for production in not_grammar.productions():
            if isinstance(production.rhs()[0], str):
                prod_dict[production.rhs()[0]].append(production.lhs())
        for i in range(len(sentlist)):
            sourcelenLIST = [sentlist[i][j][2] for j in range(len(sentlist[i]))]
            targlenLIST = [sentlist[i][j][3] for j in range(len(sentlist[i]))]
            predlenLIST = [sentlist[i][j][4] for j in range(len(sentlist[i]))]

            max_len = max(sourcelenLIST)
            min_len = min(sourcelenLIST)

            source_token_template = {length + 1: (sourcelenLIST.count(length + 1) * (length + 1)) for length in len_range}
            token_template = dict(templateDICT)
            targ_tokens, pred_tokens, category_template = dict(templateDICT), dict(templateDICT), dict(templateDICT)

            for j in range(len(sentlist[i])):
                pred_tokens[sourcelenLIST[j]] += predlenLIST[j]
            for j in range(len(sourcelenLIST)):
                targ_tokens[sourcelenLIST[j]] += targlenLIST[j]

            total_token_correct = 0
            total_category_correct = 0
            for j in range(len(sentlist[i])):
                sourcelen = sourcelenLIST[j]
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
                token_template[sourcelen] += sum(token_correct)
                # total_category_correct += sum(category_correct)
                category_template[sourcelen] += sum(category_correct)

            token_precisionlist.append({j + 1: str(round((token_template[j + 1] / pred_tokens[j + 1]) * 100, 2)) + '%'for j in len_range})
            token_recallList.append({j + 1: str(round((token_template[j + 1] / targ_tokens[j + 1]) * 100, 2)) + '%' for j in len_range})

            category_precisionlist.append({j + 1: str(round((category_template[j + 1] / pred_tokens[j + 1]) * 100, 2)) + '%' for j in len_range})
            category_recallList.append({j + 1: str(round((category_template[j + 1] / targ_tokens[j + 1]) * 100, 2)) + '%'for j in len_range})

        token_dicts = [source_token_template, pred_tokens, targ_tokens, token_precisionlist[0], token_precisionlist[1], token_recallList[0], token_recallList[1], category_precisionlist[0], category_precisionlist[1], category_recallList[0], category_recallList[1]]
        token_names = ['Total source tokens', 
        'Total Prediction Tokens per Source', 
        'Total Target Tokens per Source', 
        'Pos->Pos Token Precision (%)', 
        'Pos->Neg Token Precision (%)', 
        'Pos->Pos Token Recall (%)', 
        'Pos->Neg Token Recall (%)', 
        'Pos->Pos Category Precision (%)', 
        'Pos->Neg Category Precision (%)', 
        'Pos->Pos Category Recall (%)', 
        'Pos->Neg Category Recall (%)']

        avgdictlist = token_dicts[3:]
        avgdictnames = token_names[3:]
        return token_dicts, token_names, avgdictlist, avgdictnames
  
def make_trees(pos_list, neg_list, templateDICT, pos_template, neg_template, len_range):

    noparses = os.path.join(argv[2], "no-parses.csv")
    with open(noparses, 'w', newline='') as npfile:
        npwriter = csv.writer(npfile, delimiter=',', lineterminator='\n', quotechar='/')
        parser = BottomUpLeftCornerChartParser(not_grammar)
        sentlist = [pos_list, neg_list]
        postrees, negtrees = [[], []], [[], []]
        treeslist = [postrees, negtrees]
        templatelist = [dict(templateDICT), dict(templateDICT)]

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
                    templatelist[i][sentlist[i][j][2]] += 1
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
                        templatelist[i][sentlist[i][j][2]] += 1
                        sentlist[i][j].extend([1])
            # Dictionaries
            total_parseableDICT = {length + 1: templatelist[0][length + 1] + templatelist[1][length + 1] for length in len_range}
            avgparsesDICT = {length + 1: str(round((total_parseableDICT[length + 1] / (pos_template[length + 1] + neg_template[length + 1])) * 100, 2)) + '%' for length in len_range}
            avgposparsesDICT = {length + 1: str(round((templatelist[0][length + 1] / pos_template[length + 1]) * 100, 2)) + '%' for length in len_range}
            avgnegparsesDICT = {length + 1: str(round((templatelist[1][length + 1] / neg_template[length + 1]) * 100, 2)) + '%' for length in len_range}
            dictlist = [total_parseableDICT, templatelist[0], templatelist[1], avgparsesDICT, avgposparsesDICT, avgnegparsesDICT]
            dictnames = ['Parseable Sentences (#)',
                        'Pos->Pos Parseable Sentences (#)',
                        'Pos->Neg Parseable Sentences (#)',
                        'Parseable Sentences (%)',
                        'Pos->Pos Parseable Sentences (%)',
                        'Pos->Neg Parseable Sentences (%)']
        avgdictlist = dictlist[3]
        avgdictnames = dictnames[3]
        return treeslist, dictlist, dictnames, avgdictlist, avgdictnames

def equal_structs(pos_list, neg_list, treeslist, templateDICT, pos_template, neg_template, totalparseableDICT, parseableDICT, len_range):
    #treeslist: [[postarg, pospred], [negtarg, negpred]]
    pos_structsDICT, pos_clausalDICT, neg_structsDICT, neg_clausalDICT = dict(templateDICT), dict(templateDICT), dict(templateDICT), dict(templateDICT)
    dicts = [[pos_structsDICT, pos_clausalDICT], [neg_structsDICT, neg_clausalDICT]]
    lists = [pos_list, neg_list]
    for i in range(len(treeslist)): # pos, neg
        length = range(len(treeslist[i][0]))
        for j in length:
            sourcelen = treeslist[i][0][j][0]
            targlen = treeslist[i][0][j][1]
            predlen = treeslist[i][1][j][1]
            if treeslist[i][0][j][2] == 'correct':
                lists[i][j].extend([1, 1])
                dicts[i][0][sourcelen] += 1
                dicts[i][1][sourcelen] += 1
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
                    dicts[i][0][sourcelen] += 1
                if clausebool == 1:
                    dicts[i][1][sourcelen] += 1


    avgposstructsDICT = {length + 1: str(round((dicts[0][0][length + 1] / pos_template[length + 1]) * 100, 2)) + '%' for length in len_range}
    avgposclausesDICT = {length + 1: str(round((dicts[0][1][length + 1] / pos_template[length + 1]) * 100, 2)) + '%' for length in len_range}
    avgnegstructsDICT = {length + 1: str(round((dicts[1][0][length + 1] / neg_template[length + 1]) * 100, 2)) + '%' for length in len_range}
    avgnegclausesDICT = {length + 1: str(round((dicts[1][1][length + 1] / neg_template[length + 1]) * 100, 2)) + '%' for length in len_range}
    
    dictlist = [avgposstructsDICT, avgposclausesDICT, avgnegstructsDICT, avgnegclausesDICT]
    dictnames = ["Pos->Pos Preseve Tree Structures (%)",
                "Pos->Pos Preserve Significant Clauses (%)",
                "Pos->Neg Preseve Tree Structures (%)",
                "Pos->Neg Preserve Significant Clauses (%)"]
    
    avgdictlist = dictlist
    avgdictnames = dictnames
    return dictlist, dictnames, avgdictlist, avgdictnames

def negate_main(neg_list, targtrees, predtrees, templateDICT, neg_template, neg_parsesDICT, len_range):
    # extend(has main clause, negates main clause, negates outside of main clause)
    main_clauseDICT, negates_mainDICT, negates_outsideDICT, no_mainDICT = dict(templateDICT), dict(templateDICT), dict(templateDICT), dict(templateDICT)
    length = range(len(predtrees))
    for i in length:
        sourcelen = targtrees[i][0]
        if predtrees[i][2] == 'correct':
            neg_list[i].extend([1, 1, 1])
            main_clauseDICT[sourcelen] += 1
            negates_mainDICT[sourcelen] += 1
        elif predtrees[i][2] == 'N/A':
            neg_list[i].extend([0, 0, 0])
        else:
            targlen, predlen = targtrees[i][1], predtrees[i][1]
            targsent, predsent = targtrees[i][2][0].leaves(), predtrees[i][2][0].leaves()
            not_index = targsent.index('not') 
            targverb = targsent[not_index + 1]
            # check if there's a main clause
            if 'S2' in [str(prod.lhs()) for prod in predtrees[i][2][0].productions()]:
                main_clauseDICT[sourcelen] += 1
                neg_list[i].extend([1])
                # if there is a main clause then check if it's negated
                # do stuff with main clauses
                for subtree in predtrees[i][2][0].subtrees(filter=lambda t: t.label() == 'S2'):
                    subtree
                if subtree[1][1].label() == 'Neg':
                    negates_mainDICT[sourcelen] += 1
                    neg_list[i].extend([1])
                else:
                    if 'not' in predsent:
                        negates_outsideDICT[sourcelen] += 1
                        neg_list[i].extend([1])
            else:
                no_mainDICT[sourcelen] += 1
                negbool = 1 if 'not' in predsent else 0
                neg_list[i].extend([0, 0, negbool])

    avgnegmainDICT = {length + 1: str(round((negates_mainDICT[length + 1] / neg_template[length + 1]) * 100, 2)) + '%' for length in len_range}
    avgnegmainonlymainDICT = {length + 1: str(round((negates_mainDICT[length + 1] / main_clauseDICT[length + 1]) * 100, 2)) + '%' for length in len_range}
    avghasmainDICT = {length + 1: str(round((main_clauseDICT[length + 1] / neg_template[length + 1]) * 100, 2)) + '%' for length in len_range}
    avgnegatesoutsideDICT = {length + 1: str(round((negates_outsideDICT[length + 1] / main_clauseDICT[length + 1]) * 100, 2)) + '%' for length in len_range}

    dictlist = [main_clauseDICT, negates_mainDICT, negates_outsideDICT, avgnegatesoutsideDICT, no_mainDICT, avgnegmainDICT, avgnegmainonlymainDICT, avghasmainDICT]
    dictnames = ["Pos->Neg Predictions with Main Clause (#)",
                "Pos->Neg Predictions that Negate Main Clause (#)",
                "Pos->Neg Predictions that Negate Outside Main Clause (#)",
                "Pos->Neg Predictions that Negate Outside Main Clause (%)",
                "Pos->Neg Predictions without Main Clause (#)",
                "Pos->Neg Predictions that Negate Main Clause (Denominator: all Pos->Neg sentences)",
                "Pos->Neg Predictions that Negate Main Clause (Denominator: only Pos->Neg sentences with main clauses)",
                "Pos->Neg Predictions with Main Clause (%)"]
    avgdictlist = [dictlist[3], dictlist[5], dictlist[6], dictlist[7]]
    avgdictnames = [dictnames[3], dictnames[5], dictnames[6], dictnames[7]]

    return dictlist, dictnames, avgdictlist, avgdictnames

def pos_csv_writer(pos_list):
    posbools = os.path.join(argv[2], 'pos_pos.csv')
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
            writer.writerow([pos_list[i]])
    
def neg_csv_writer(neg_list):
    negbools = os.path.join(argv[2], "pos_neg.csv")
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
            writer.writerow([neg_list[i]])

def write_dicts(dictlist, dictnames, avgdictlist, avgdictnames, len_range):
    dicts = os.path.join(argv[2], 'dicts.csv')
    with open(dicts, 'w') as dictfile:
        newdicts = [{'Dictionary Name':dictname} for dictname in dictnames]
        
        for i in range(len(newdicts)):
            newdicts[i].update(dictlist[i])
        
        len_range[0] = 'Dictionary Name'
        len_range.append(23)
        fieldnames = len_range

        writer = csv.DictWriter(dictfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
        writer.writeheader()
        writer.writerows(newdicts)

        
# Main function
def main():
    # pos_list: target sent, pred sent, sourcelen, targlen, predlen, correctBOOL
    # templates: total transformations (templateDICT is blank)
    pos_list, neg_list, pos_template, neg_template, templateDICT, dictlist, dictnames, len_range, avgdictlist, avgdictnames = read_file(argv[1])
    tokenDICTS, tokenNAMES, avgtokenlist, avgtokennames = token_acc(pos_list, neg_list, templateDICT, len_range) # returns proportion of correct tokens (pos, neg)
    dictlist.extend(tokenDICTS), dictnames.extend(tokenNAMES)
    avgdictlist.extend(avgtokenlist), avgdictnames.extend(avgtokennames)
    
    treeslist, parseDICTS, parseNAMES, avgparselist, avgparsenames = make_trees(pos_list, neg_list, templateDICT, pos_template, neg_template, len_range) # create trees for all transformations
    dictlist.extend(parseDICTS), dictnames.extend(parseNAMES)
    avgdictlist.extend(avgparselist), avgdictnames.extend(avgparsenames)
   
    structDICTS, structNAMES, avgstructlist, avgstructnames = equal_structs(pos_list, neg_list, treeslist, templateDICT, pos_template, neg_template, parseDICTS[0], parseDICTS[1], len_range) # [sourcelen, targlen, predlen, BOOL]
    dictlist.extend(structDICTS), dictnames.extend(structNAMES)
    avgdictlist.extend(avgstructlist), avgdictnames.extend(avgstructnames)
    
    negmainDICTS, negmainNAMES, avgmainlist, avgmainnames = negate_main(neg_list, treeslist[1][0], treeslist[1][1], templateDICT, neg_template, parseDICTS[2], len_range) # [sourcelen, targlen, predlen, BOOL]
    dictlist.extend(negmainDICTS), dictnames.extend(negmainNAMES)
    avgdictlist.extend(avgmainlist), avgdictnames.extend(avgmainnames)
    
    targDICTS, targNAMES, avgtarglist, avgtargnames = negate_target(neg_list, neg_template, templateDICT, len_range) # returns a list of booleans for negating the target verb
    dictlist.extend(targDICTS), dictnames.extend(targNAMES)
    avgdictlist.extend(avgtarglist), avgdictnames.extend(avgtargnames)
    
    pos_csv_writer(pos_list)
    neg_csv_writer(neg_list)  # writes into a new CSV with columns: targ, pred, boolean values
    # Dictionaries
    write_dicts(dictlist, dictnames, avgdictlist, avgdictnames, len_range)
main()