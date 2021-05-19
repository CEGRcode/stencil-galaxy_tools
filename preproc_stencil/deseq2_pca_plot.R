args<-print(commandArgs(trailingOnly=TRUE))
#head(mtcars, 6)
deseq2_normalized_counts_output<-read.table(args[1], header = TRUE, row.names = 1)
pca <- prcomp(mtcars[,c(1:7,10,11)], center = TRUE,scale. = TRUE)
percentVar <- pca$sdev^2 / sum( pca$sdev^2 )
str(percentVar)



#write.table(deseq2_normalized_counts_output, file = args[2], sep = "\t",
#            row.names = FALSE, col.names = TRUE)

library (matrixStats)
library(ggplot2)
library(jsonlite)
ntop = 500
deseq2_counts<-read.table(args[1], header = TRUE, row.names = 1)

head (deseq2_counts)
names_col <- (names (deseq2_counts))
names_col <- (names (deseq2_counts))
group_name <- c ('HepG2','HepG2','HepG2','HepG2','k562','k562','k562','k562')
deseq2_counts_matrix = data.matrix(deseq2_counts)
rv <- rowVars(deseq2_counts_matrix)
select <- order(rv, decreasing=TRUE)[seq_len(min(ntop, length(rv)))]
pca <- prcomp(t(deseq2_counts_matrix[select,]))
percentVar <- pca$sdev^2 / sum( pca$sdev^2 )
d <- data.frame(PC1=pca$x[,1], PC2=pca$x[,2] , name=names_col, group = group_name)
d_simple <- data.frame(PC1=pca$x[,1], PC2=pca$x[,2])
p<-ggplot(data=d, aes_string(x="PC1", y="PC2", color="group")) + geom_point(size=3) + 
  xlab(paste0("PC1: ",round(percentVar[1] * 100),"% variance")) +
  ylab(paste0("PC2: ",round(percentVar[2] * 100),"% variance")) +
  coord_fixed()
colnames(d_simple) <- c("x", "y")
rownames(d_simple) <- c()
d_json <-toJSON(d_simple, pretty=TRUE)
#d_json <- gsub ("\\[", " ",d_json )
#d_json <- gsub ("\\]", " ",d_json )
#write_json(d_simple, '/Users/an653/Box/Ali_files/210512_pca_plot_deseq2/pca_nivo_json.txt')

write('[ {  "id": "group A", "data": ', args[2], append = FALSE)
write(d_json, args[2], append = TRUE)
write(' } ]', args[2], append = TRUE)
#write(' }', args[2], append = TRUE)

