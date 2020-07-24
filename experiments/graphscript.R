library(ggplot2)
library(scales)
library(ggpubr)

fullsentplot <- ggplot(data3, aes(x = Dictionary.Name)) + 
  labs(title="Correct Output  (Full Sequence Accuracy)", x = "Sentence Length", y = "Correct Output") +
  geom_line(aes(y = avgPPtrans, color = 'Pos->Pos'), size = 1) + 
  geom_point(aes(y = avgPPtrans, color = 'Pos->Pos')) +
  geom_line(aes(y = avgPNtrans, color = 'Pos->Neg'), size = 1) + 
  geom_point(aes(y = avgPNtrans, color = 'Pos->Neg')) +
  theme_bw() + 
  theme(plot.title = element_text(hjust = 0.5)) + 
  scale_color_discrete(name = 'Transformation Type') +
  scale_x_continuous(breaks = seq(3,30,2)) +
  scale_y_continuous(breaks = seq(0,1,0.1), labels = percent)

posplot <- ggplot(data3, aes(x = Dictionary.Name)) +
  labs(title="Pos -> Pos Transformations", x = "Sentence Length", y = "% Preserved") +
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

negplot <- ggplot(data3, aes(x = Dictionary.Name)) + 
  labs(title="Pos -> Neg Transformations", x = "Sentence Length", y = "% Preserved") + 
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

negplacement <- ggplot(data3, aes(x = Dictionary.Name)) +
  labs(title="Negation Placement", x = "Sentence Length", y = "% Negated") +
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_color_discrete(name = 'Task') +
  scale_x_continuous(breaks = seq(3,30,2)) +
  scale_y_continuous(breaks = (seq(0,1, 0.1)), limits = c(0, 1), labels = percent) +
  geom_line(aes(y = avgNegMain, colour = "Negates Main"), size = 1) + 
  geom_point(aes(y = avgNegMain, colour = "Negates Main")) +
  geom_line(aes(y = avgNegTarg, color = 'Negates Target'), size = 1) + 
  geom_point(aes(y = avgNegTarg, color = 'Negates Target')) 

posfmplot <- ggplot(data3, aes(x = Dictionary.Name)) + 
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

negfmplot <- ggplot(data3, aes(x = Dictionary.Name)) + 
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

ggarrange(fullsentplot, negplacement, posplot, negplot, posfmplot, negfmplot,
          ncol = 2, nrow = 3)




 
