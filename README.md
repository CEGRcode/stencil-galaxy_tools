# galaxy_tools_for_stencil

preprocess tools:

RNA-seq pipeline tools:

1- "deseq2_to_ma_plot_nivo_json" tool generates MA plot in nivo standard json format.

2- "deseq2_to_bar_plot_nivo_json" tool generates Bar plot in nivo standard json format.

2- "deseq2_to_heatmap_plot_nivo_json" generates heatmap of distance between samples based on r-log normalized counts of reads per gene, in nivo standard json format. 

3- "deseq2_to_pca_plot_nivo_json" generates a PCA plot from the rlog-normalized counts of read per gene data coming out of deseq2 tool 

4- "deseq2_to_table_with_gene_name_nivo_json" gets the output of deseq2 in tabular format and gene annotation file in gf format. Adds a gene_name column to the table based on gene_id, finally convert the results to nivo JSON format.
  
ChIP-exo pipeline tools:

1- "tagpileup_tabular_to_nivo_json" tool generates Lineplot in nivo standard json format for two groups of sense strand reads and antisense strand reads.

2- "motif_logo_memexml_to_pngs" tool generates meme logos in png format from memexml file. 

3- "resize_4color_plot" tool resize the 4color plot.

4- "scriptmanager_heatmap_add_label" add labels and annotations to the heatmap plot generated by script manager.


tools for POSTing data to Stencil:

1- "post_static_plot_stencil" POSTs static images in png format to Stencil

2- "post_nivo_table_and_plot_stencil" POSTs json files in nivo table or plot format to Stencil. Supported type of plots are ScatterPlot, LinePlot, BarPlot, Heatmap and Table.
