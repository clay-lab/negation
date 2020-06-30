from sys import argv
import csv
import pandas as pd
from os import mkdir
# from not_grammar import not_grammar
from nltk import ViterbiParser, ShiftReduceParser, RecursiveDescentParser, BottomUpLeftCornerChartParser


def level_accuracy(targtree, predtree, t_level_dict, p_level_dict, counter=0):

    if len(targtree) == 1 or len(predtree) == 1:
        print(t_level_dict)
        print(p_level_dict)
        exit()
        return level_dict
    else:
        print(len(targtree))
        # print(targtree)
        # print(targtree[0])
        t_level_dict[counter] = targtree[0].label()
        p_level_dict[counter] = predtree[0].label()
        counter += 1
        print(t_level_dict)
        print(p_level_dict)
        level_accuracy(targtree[0], predtree[0], t_level_dict, p_level_dict, counter)
    exit()



        # print("TARG TREE: ", targtree)
        # print("PRED TREE: ", predtree)

def read_file():
    filename = argv[1]
    with open(filename, newline='') as rfile:
        reader = csv.reader(rfile, delimiter='\t', lineterminator='\n')
        newreader = [line for line in reader]
        nreader = []
        nreader.append(["target", "prediction"])
        for line in newreader[1:]:
            newline = []
            for sentence in line:
                splitsent = sentence.split(" ")
                for word in range(len(splitsent)):     
                    if splitsent[word] == '<eos>':
                        splitsent = splitsent[:word]
                        break
                newline.append(splitsent)
            nreader.append(newline[1:])
        return nreader



def write_file():
    filename = argv[1]
    with open("newresults.txt", mode='w') as new_file:
        out_writer = csv.writer(new_file, delimiter='\t', lineterminator='\n', quotechar='/')
        newreader = read_file()
        out_writer.writerow(['target', 'prediction'])
        for newline in newreader[1:]:
            out_writer.writerow([' '.join(newline[0]), ' '.join(newline[1])])

    with open("newresults.txt", 'r') as results_file, open("pos_neg.txt", 'w') as neg_file, open("pos_pos.txt", 'w') as pos_file, open("dicts.txt", 'w') as dict_file:
        results_reader = csv.reader(results_file, delimiter='\t')
        neg_writer = csv.writer(neg_file, delimiter='\t', lineterminator='\n', quotechar='/')
        pos_writer = csv.writer(pos_file, delimiter='\t', lineterminator='\n', quotechar='/')
        dict_writer = csv.writer(dict_file, delimiter='\t', lineterminator='\n', quotechar='/')

        neg_writer.writerow(["target" , "prediction"])
        pos_writer.writerow(["target", "prediction"])


        results_list = [(len(line[0].split(' ')), line[0], line[1]) for line in results_reader]
        len_list = [line[0] for line in results_list[1:]]
        max_len = max(len_list)

        pcorrect_dict = {}
        ncorrect_dict = {}
        total_dict = {}
        neg_dict = {}
        pos_dict = {}
        for i in range(max_len):
            pcorrect_dict[i + 1] = 0
            ncorrect_dict[i + 1] = 0
            neg_dict[i + 1] = 0
            pos_dict[i + 1] = 0
            total_dict[i + 1] = len_list.count(i + 1)

        for linelen, target, prediction in results_list[1:]:

            if target == prediction:
                if 'not' in target:
                    ncorrect_dict[linelen] += 1
                else:
                    pcorrect_dict[linelen] += 1

            if target != prediction:
                # parser = BottomUpLeftCornerChartParser(not_grammar)
                # targlist = target.split()
                # predlist = prediction.split()
                # targ_parses = parser.parse(targlist)
                # pred_parses = parser.parse(predlist)
                # t_level_dict = {}
                # p_level_dict = {}
                # for targtree in targ_parses:
                #     for predtree in pred_parses:
                #         print(targtree)
                #         level_dict = level_accuracy(targtree, predtree, t_level_dict, p_level_dict)
                # exit()
                        # if len(predtree) == 0 or len(targtree) == 0
                        # print(targtree)
                        # print(predtree)

                # targ_tree = [targtree for targtree in targ_parses]
                # pred_tree = [predtree for predtree in pred_parses]
                # print(targ_tree.leaves())
                # exit()
                # print(targlist)
                # print(predlist, "\n")
                # print(targ_tree, "\n")
                # print(pred_tree, "\n")

                # print(targ_tree[0][1].label())
                # print(pred_tree[0][1].label())
                # print(len(targ_tree[0][1]))
                # print(len(pred_tree[0][1]))
                # exit()
                # for tree in targ_parses:
                #     print(len(tree))
                #     print(tree[0].label())
                #     print(tree[1].label())
                #     print(tree)
                #     print(tree.leaves())
                #     print(tree.leaf_treeposition(tree.leaves().index('witch')))

                    
                    # print(tree.draw())
                # exit()
                
                # pos -> neg transforms
                if 'not' in target:
                    neg_writer.writerow([target, prediction])
                    neg_dict[linelen] += 1
                # pos -> pos transforms
                if 'not' not in target:
                    pos_writer.writerow([target, prediction])
                    pos_dict[linelen] += 1

                    # inequality = [(x, y) for x, y in zip(prediction.split(' '), target.split(' ')) if y != x]
                    # print(inequality)

        avg_dict = {}

        for i in range(max_len):
            avg_dict[i + 1] = round((pcorrect_dict[i + 1] + ncorrect_dict[i + 1]) / total_dict[i + 1], 3) if total_dict[i + 1] != 0 else 0

        dict_writer.writerow(["CORRECT POS->POS MAPPING PER LENGTH: ", pcorrect_dict])
        dict_writer.writerow(["CORRECT POS->NEG MAPPING PER LENGTH: ", ncorrect_dict])
        dict_writer.writerow(["TOTAL SENTENCES PER LENGTH: ", total_dict])
        dict_writer.writerow(["AVG: CORRECT: TOTAL: ", avg_dict])
        dict_writer.writerow(["INCORRECT POS -> POS TRANSFORM: ", pos_dict])
        dict_writer.writerow(["INCORRECT POS -> NEG TRANSFORM: ", neg_dict])
        

write_file()
