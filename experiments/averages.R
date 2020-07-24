data1 <- read.csv("C:/Users/shayn/Documents/GitHub/negation/experiments/negation/location-results/dicts1.csv")
data2<- read.csv("C:/Users/shayn/Documents/GitHub/negation/experiments/negation/location-results/dicts2.csv")
data3 <- read.csv("C:/Users/shayn/Documents/GitHub/negation/experiments/negation/location-results/dicts3.csv")
data4 <- read.csv("C:/Users/shayn/Documents/GitHub/negation/experiments/negation/location-results/dicts4.csv")
data5 <- read.csv("C:/Users/shayn/Documents/GitHub/negation/experiments/negation/location-results/dicts5.csv")

avgPPtrans <- (data1$Correct.Pos..Pos.Transformations + 
                 data2$Correct.Pos..Pos.Transformations + 
                 data3$Correct.Pos..Pos.Transformations + 
                 data4$Correct.Pos..Pos.Transformations + 
                 data5$Correct.Pos..Pos.Transformations) / 5

avgPNtrans <- (data1$correct.Pos..Neg.Transformations + 
                 data2$correct.Pos..Neg.Transformations + 
                 data3$correct.Pos..Neg.Transformations + 
                 data4$correct.Pos..Neg.Transformations + 
                 data5$correct.Pos..Neg.Transformations) / 5

avgPPparseable <- (data2$Parseable.sentences..pos..pos. + 
                     data1$Parseable.sentences..pos..pos. + 
                     data3$Parseable.sentences..pos..pos. + 
                     data4$Parseable.sentences..pos..pos. + 
                     data5$Parseable.sentences..pos..pos.) / 5

aavgPPtreestruct <- (data1$Preserve.tree.structures..pos..pos. + 
                       data2$Preserve.tree.structures..pos..pos. + 
                       data3$Preserve.tree.structures..pos..pos. + 
                       data4$Preserve.tree.structures..pos..pos. + 
                       data5$Preserve.tree.structures..pos..pos.) / 5

avgPPclauses <- (data1$Preserve.significant.clauses..pos..pos. + 
                   data2$Preserve.significant.clauses..pos..pos. + 
                   data3$Preserve.significant.clauses..pos..pos. + 
                   data4$Preserve.significant.clauses..pos..pos. + 
                   data5$Preserve.significant.clauses..pos..pos.) / 5

avgPNparseable <- (data1$Parseable.Sentences..pos..neg. + 
                     data2$Parseable.Sentences..pos..neg. + 
                     data3$Parseable.Sentences..pos..neg. + 
                     data4$Parseable.Sentences..pos..neg. + 
                     data5$Parseable.Sentences..pos..neg.) / 5

avgPNtreestruct <- (data1$Preserve.tree.structures..pos..neg. + 
                      data2$Preserve.tree.structures..pos..neg. + 
                      data3$Preserve.tree.structures..pos..neg. + 
                      data4$Preserve.tree.structures..pos..neg. + 
                      data5$Preserve.tree.structures..pos..neg.) / 5

avgPNclauses <- (data1$Preserve.significant.clauses..pos..neg. + 
                   data2$Preserve.significant.clauses..pos..neg. + 
                   data3$Preserve.significant.clauses..pos..neg. + 
                   data4$Preserve.significant.clauses..pos..neg. + 
                   data5$Preserve.significant.clauses..pos..neg.) / 5

avgNegMain <- (data1$Negates.main.clause..pos..neg. + 
                 data2$Negates.main.clause..pos..neg. + 
                 data3$Negates.main.clause..pos..neg. + 
                 data4$Negates.main.clause..pos..neg. + 
                 data5$Negates.main.clause..pos..neg.) / 5

avgNegTarg <- (data1$Negates.target..pos..neg. + 
                 data2$Negates.target..pos..neg. + 
                 data3$Negates.target..pos..neg. + 
                 data4$Negates.target..pos..neg. + 
                 data5$Negates.target..pos..neg.) / 5

avgtokenprecPP <- (data1$Pos..pos.token.precision +
                     data2$Pos..pos.token.precision +
                     data3$Pos..pos.token.precision + 
                     data4$Pos..pos.token.precision +
                     data5$Pos..pos.token.precision) / 5

avgtokenrecallPP <- (data1$Pos..pos.token.recall +
                       data2$Pos..pos.token.recall +
                       data3$Pos..pos.token.recall + 
                       data4$Pos..pos.token.recall +
                       data5$Pos..pos.token.recall) / 5

avgtokenprecPN <- (data1$Pos..neg.token.precision +
                     data2$Pos..neg.token.precision +
                     data3$Pos..neg.token.precision + 
                     data4$Pos..neg.token.precision +
                     data5$Pos..neg.token.precision) / 5

avgtokenrecallPN <- (data1$Pos..neg.token.recall +
                       data2$Pos..neg.token.recall +
                       data3$Pos..neg.token.recall + 
                       data4$Pos..neg.token.recall +
                       data5$Pos..neg.token.recall) / 5

avgcatprecPP <- (data1$Pos..Pos.category.precision +
                   data2$Pos..Pos.category.precision +
                   data3$Pos..Pos.category.precision + 
                   data4$Pos..Pos.category.precision +
                   data5$Pos..Pos.category.precision) / 5

avgcatrecallPP <- (data1$Pos..pos.category.recall +
                     data2$Pos..pos.category.recall +
                     data3$Pos..pos.category.recall + 
                     data4$Pos..pos.category.recall +
                     data5$Pos..pos.category.recall) / 5

avgcatprecPN <- (data1$Pos..neg.category.precision +
                   data2$Pos..neg.category.precision +
                   data3$Pos..neg.category.precision + 
                   data4$Pos..neg.category.precision +
                   data5$Pos..neg.category.precision) / 5

avgcatrecallPN <- (data1$Pos..Neg.category.recall +
                     data2$Pos..Neg.category.recall +
                     data3$Pos..Neg.category.recall + 
                     data4$Pos..Neg.category.recall +
                     data5$Pos..Neg.category.recall) / 5