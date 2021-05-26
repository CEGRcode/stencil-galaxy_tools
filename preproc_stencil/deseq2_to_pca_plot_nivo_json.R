args<-print(commandArgs(trailingOnly=TRUE))
deseq2_normalized_counts_output<-read.table(args[1], header = TRUE, row.names = 1)

#write.table(deseq2_normalized_counts_output, file = args[2], sep = "\t",
#            row.names = FALSE, col.names = TRUE)

library (matrixStats)
library(ggplot2)
library(jsonlite)
ntop = 500
deseq2_counts<-read.table(args[1], header = TRUE, row.names = 1)
#head (deseq2_counts)
names_col <- (names (deseq2_counts))
#group_name <- c ('HepG2','HepG2','HepG2','HepG2','k562','k562','k562','k562')
deseq2_counts_matrix = data.matrix(deseq2_counts)
rv <- rowVars(deseq2_counts_matrix)
select <- order(rv, decreasing=TRUE)[seq_len(min(ntop, length(rv)))]
pca <- prcomp(t(deseq2_counts_matrix[select,]))
percentVar <- pca$sdev^2 / sum( pca$sdev^2 )
#d <- data.frame(PC1=pca$x[,1], PC2=pca$x[,2] , name=names_col, group = group_name)
d_simple <- data.frame(PC1=pca$x[,1], PC2=pca$x[,2], names_col)
#p<-ggplot(data=d, aes_string(x="PC1", y="PC2", color="group")) + geom_point(size=3) + 
#  xlab(paste0("PC1: ",round(percentVar[1] * 100),"% variance")) +
#  ylab(paste0("PC2: ",round(percentVar[2] * 100),"% variance")) +
#  coord_fixed()
colnames(d_simple) <- c("x", "y", "id")
rownames(d_simple) <- c()
d_json <-toJSON(d_simple, pretty=TRUE)

#write('[ {  "id": "group A", "data": ', args[2], append = FALSE)
write(d_json, args[2], append = FALSE)
#write(' } ]', args[2], append = TRUE)

