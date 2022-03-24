# About stencil-galaxy_tools #

This repository contains galaxy tools for preprocessing and posting static and interactive plots and tables from Galaxy to Stencil. Preprocessing tools are mainly developed for deseq2, a popular RNA-seq analysis tool. The Post tools are generic and can be used for different static and interactive plots to Stencil Website.


## preprocess tools: ##

  ### RNA-seq pipeline tools: ###

   1- deseq2_to_ma_plot_nivo_json" tool generates MA plot in nivo standard json format.

   2- deseq2_to_bar_plot_nivo_json" tool generates Bar plot in nivo standard json format.

   3- "deseq2_to_heatmap_plot_nivo_json" generates heatmap of distance between samples based on r-log normalized counts of reads per gene, in nivo standard json format. 

   4- "deseq2_to_pca_plot_nivo_json" generates a PCA plot from the rlog-normalized counts of read per gene data coming out of deseq2 tool 

   5- "deseq2_to_table_with_gene_name_nivo_json" gets the output of deseq2 in tabular format and gene annotation file in gf format. Adds a gene_name column to the table based on gene_id, finally convert the results to nivo JSON format.
  
  ### ChIP-exo pipeline tools: ###

   1- "tagpileup_tabular_to_nivo_json" tool generates Lineplot in nivo standard json format for two groups of sense strand reads and antisense strand reads.


## POST tools to Stencil: ##

   1- "post_static_plot_stencil" POSTs static images in png format to Stencil

   2- "post_nivo_table_and_plot_stencil" POSTs json files in nivo table or plot format to Stencil. Supported type of plots are ScatterPlot, LinePlot, BarPlot, Heatmap and Table.


## Installing Stencil Galaxy tools ##
1. Clone the repository in the local_tools folder
```
cd /mnt/mountpoint/srv/galaxy/local_tools
sudo git clone https://github.com/CEGRcode/stencil-galaxy_tools
```

2. Tell galaxy where to look for `stencil-galaxy_tools` tools by adding the following section to `/mnt/mountpoint/srv/galaxy/config/local_tool_conf.xml` file if it is not already included.

```
<section id="STENCIL" name="STENCIL" >
    <tool file="stencil-galaxy_tools/preproc_stencil/deseq2_to_bar_plot_nivo_json.xml" />
    <tool file="stencil-galaxy_tools/preproc_stencil/deseq2_to_heatmap_plot_nivo_json.xml" />
    <tool file="stencil-galaxy_tools/preproc_stencil/deseq2_to_ma_plot_nivo_json.xml" />
    <tool file="stencil-galaxy_tools/preproc_stencil/deseq2_to_pca_plot_nivo_json.xml" />
    <tool file="stencil-galaxy_tools/preproc_stencil/deseq2_to_table_with_gene_name_nivo_json.xml" />
    <tool file="stencil-galaxy_tools/preproc_stencil/tagpileup_tabular_to_nivo_json.xml" />
    <tool file="stencil-galaxy_tools/post_stencil/post_nivo_table_and_plot_json_stencil.xml" />
    <tool file="stencil-galaxy_tools/post_stencil/post_static_plot_stencil.xml" />
  </section>
```

3. Restart Galaxy

    ```
    sudo systemctl restart galaxy
    ```
 
4. Solve dependencies for local Galaxy tools that have been just added through Galaxy web interface. `Admin -> Manage Dependencies`

For more information about Stencil, please check the following paper.

Sun Q, Nematbakhsh A., Kuntala P., Kellogg G, Pugh B. and Lai W., 2022, STENCIL: A web templating engine for visualizing and sharing life science datasets, PLOS Computational Biology 18(2) e1009859
