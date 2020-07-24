library(ggplot2)
library(scales)
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
ggplot(data3, aes(x = Dictionary.Name)) + 
  labs(title="Correct Output  (Full Sequence Accuracy)", x = "Sentence Length", y = "Correct Output (Full Sequence Accuracy)") +
  geom_line(aes(y = avgPPtrans, color = 'Pos->Pos'), size = 1) + 
  geom_point(aes(y = avgPPtrans, color = 'Pos->Pos')) +
  geom_line(aes(y = avgPNtrans, color = 'Pos->Neg'), size = 1) + 
  geom_point(aes(y = avgPNtrans, color = 'Pos->Neg')) +
  theme_bw() + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  scale_color_discrete(name = 'Transformation Type') +
  scale_x_continuous(breaks = seq(3,30,2)) +
  scale_y_continuous(breaks = seq(0,1,0.1), labels = percent)

ggplot(data3, aes(x = Dictionary.Name)) +
  labs(title="Pos -> Pos Transformations", x = "Sentence Length", y = "Correct") +
  geom_line(aes(y = avgPPparseable, color = "Parseable Sentences"), size = 1) +
  geom_point(aes(y = avgPPparseable, color = "Parseable Sentences")) +
  geom_line(aes(y = avgPPtreestruct, color = "Preserves Tree Structure"), size = 1) +
  geom_point(aes(y = avgPPtreestruct, color = "Preserves Tree Structure")) +
  geom_line(aes(y = avgPPclauses, color = "Preserves Significant Clauses \n (S, AdvP, RelP)"), size = 1) + 
  geom_point(aes(y = avgPPclauses, color = "Preserves Significant Clauses \n (S, AdvP, RelP)")) +
  theme_bw() + 
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_color_discrete(name = 'Task') +
  scale_x_continuous(breaks = seq(3,30,2)) +
  scale_y_continuous(breaks = seq(0,1,0.1), limits = c(0, 1), labels=percent)

ggplot(data3, aes(x = Dictionary.Name)) + 
  labs(title="Pos -> Neg Transformations", x = "Sentence Length", y = "Correct") + 
  geom_line(aes(y = avgPNparseable, color = "Parseable Sentences"), size = 1) + 
  geom_point(aes(y = avgPNparseable, color = "Parseable Sentences")) +
  geom_line(aes(y = avgPNtreestruct, color = "Preserves Tree Structures"), size = 1) + 
  geom_point(aes(y = avgPNtreestruct, color = "Preserves Tree Structures")) + 
  geom_line(aes(y = avgPNclauses, color = "Preserves Significant Clauses \n (S, AdvP, RelP)"), size = 1) + 
  geom_point(aes(y = avgPNclauses, color = "Preserves Significant Clauses \n (S, AdvP, RelP)")) + 
  theme_bw() + 
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_color_discrete(name = 'Task') +
  scale_x_continuous(breaks = seq(3,30,2)) +
  scale_y_continuous(breaks = seq(0,1,0.1), limits = c(0, 1), labels = percent)

ggplot(data3, aes(x = Dictionary.Name)) +
  labs(title="Negation Placement", x = "Sentence Length", y = "Correct") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_color_discrete(name = 'Task') +
  scale_x_continuous(breaks = seq(3,30,2)) +
  scale_y_continuous(breaks = (seq(0,1, 0.1)), limits = c(0, 1), labels = percent) +
  geom_line(aes(y = avgNegMain, colour = "Negates Main"), size = 1) + 
  geom_point(aes(y = avgNegMain, colour = "Negates Main")) +
  geom_line(aes(y = avgNegTarg, color = 'Negates Target'), size = 1) + 
  geom_point(aes(y = avgNegTarg, color = 'Negates Target')) 

TokenPosPosFM <- 2 * data$Pos..pos.token.precision * 
  data$Pos..pos.token.recall / 
  (data$Pos..pos.token.precision + data$Pos..pos.token.recall)

CategoryPosPosFM <- 2 * 
  data$Pos..Pos.category.precision * 
  data$Pos..pos.category.recall /
  (data$Pos..pos.token.precision + data$Pos..pos.category.recall)

TokenPosNegFM <- 2 *
  data$Pos..neg.token.precision *
  data$Pos..neg.token.recall /
  (data$Pos..neg.token.precision + data$Pos..neg.token.recall)

CategoryPosNegFM <- 2 *
  data$Pos..neg.category.precision *
  data$Pos..Neg.category.recall /
  (data$Pos..neg.category.precision + data$Pos..Neg.category.recall)

ggplot(data, aes(x = Dictionary.Name)) + 
  labs(title="Token Accuracy (F-measure) for Pos->Pos Transformations", x = "Sentence Length", y = "F-measure") +
  geom_line(aes(y = TokenPosPosFM, color = 'Token'), size = 1) +
  geom_point(aes(y = TokenPosPosFM, color = 'Token')) +
  geom_line(aes(y = CategoryPosPosFM, color = 'Grammatical category'), size = 1) +
  geom_point(aes(y = CategoryPosPosFM, color = 'Grammatical category')) +
  theme_bw() + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  scale_color_discrete(name = 'Metric') +
  scale_x_continuous(breaks = seq(3,30,2)) +
  scale_y_continuous(breaks = seq(0,1,0.1), labels=percent)

ggplot(data, aes(x = Dictionary.Name)) + 
  labs(title="Token Accuracy (F-measure) for Pos->Neg Transformations", x = "Sentence Length", y = "F-measure") +
  geom_line(aes(y = TokenPosNegFM, color = 'Token'), size = 1) +
  geom_point(aes(y = TokenPosNegFM, color = 'Token')) +
  geom_line(aes(y = CategoryPosNegFM, color = 'Grammatical category'), size = 1) +
  geom_point(aes(y = CategoryPosNegFM, color = 'Grammatical category')) +
  theme_bw() + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  scale_color_discrete(name = 'Metric') +
  scale_x_continuous(breaks = seq(3,30,2)) +
  scale_y_continuous(breaks = seq(0,1,0.1), limits = c(0.8,1), labels=percent)




 
