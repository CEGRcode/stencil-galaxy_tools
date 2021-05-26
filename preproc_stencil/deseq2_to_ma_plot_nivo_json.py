## Takes deseq2 tabular file as input and provides JSON format data as output.
## The output is tailored for nivo visualizer software used by Stencil website.
## The tool provides MA plot which is a sacatter type plot.

import numpy as np
import argparse
import time
import pandas as pd

import preproc_util_stencil 

class Deseq2_Tabular_Row:
    def __init__ (self):
        self.gene_id = None 
        self.base_mean  = None 
        self.log2_fc = None 
        self.stderr = None  
        self.wald_stats = None 
        self.strand_dir = None  
        self.p_value  = None  
        self.p_adj_value  = None

      
def Extract_deseq2_tabular_rows_scatter_plot(parsed_deseq2_tabular):
    na_counter = 0 ## to count the lines which are not parsed because have "NA" value. 
    deseq2_tabular_rows = [] 
    for line in parsed_deseq2_tabular:
        if (line[1] =='NA' or line[2]=='NA'):
            na_counter += 1 
            continue
        deseq2_tabular_row = Deseq2_Tabular_Row()
        deseq2_tabular_row.gene_id     =     (str(line[0]))
        deseq2_tabular_row.base_mean   = float((str(line[1])))  
        deseq2_tabular_row.log2_fc    = float((str(line[2]))) 
        deseq2_tabular_row.wald_stats      = str(   line[4])
        deseq2_tabular_row.p_value =     str(line[5])
        deseq2_tabular_row.p_adj_value    = str(line[6])
        deseq2_tabular_rows.append (deseq2_tabular_row)
    print ('Number of lines skipped because of NA parameter in base_mean and log2_fc, is:')
    print (na_counter)
    return (deseq2_tabular_rows)


def nivo_scatter_plot_deseq2_data_maker(deseq2_tabular_rows, group_name):
    data=[]
    if (group_name == 'notSignificant'):
        for row in deseq2_tabular_rows: 
            try:
                if ( float(row.p_adj_value) >= 0.1): 
                    data.append(preproc_util_stencil.Xy_convert_format_to_point_dict(row.base_mean, row.log2_fc))
            except:
                data.append(preproc_util_stencil.Xy_convert_format_to_point_dict(row.base_mean, row.log2_fc))
                print (row.p_adj_value)
    if (group_name == 'significant'):
        for row in deseq2_tabular_rows: 
            try:
                if (float(row.p_adj_value) < 0.1): 
                    data.append(preproc_util_stencil.Xy_convert_format_to_point_dict(row.base_mean, row.log2_fc))
            except:
                continue
    return(data)

def nivo_scatter_plot_group_maker(data, group_name):
    nivo_scatter_plot_group = {}
    nivo_scatter_plot_group["id"] = group_name
    nivo_scatter_plot_group["data"] = data
    return(nivo_scatter_plot_group)


def nivo_scatter_plot_group_maker_per_gene(data, gene_id):
    nivo_scatter_plot_group = {}
    nivo_scatter_plot_group["id"] = gene_id
    nivo_scatter_plot_group["data"] = data
    return(nivo_scatter_plot_group)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input' , dest='tabular_file', required=True, help='Name of the .tabular file which is output of deseq2 or cuffdiff')
    parser.add_argument('--output' , dest='output_file', required=True, help='Desired name of output file')
    args = parser.parse_args()
    print (" process started ..." )

    parsed_deseq2_tabular = preproc_util_stencil.Parse_tabular_file(args.tabular_file, num_skipped_rows = 0)
    print ("deseq2 tabular file parsed" )
    extracted_deseq2_tabular_rows_scatter_plot = Extract_deseq2_tabular_rows_scatter_plot(parsed_deseq2_tabular)
    print ("deseq2 tabular rows extracted" )
    group_names = ['notSignificant', 'significant']
    nivo_scatter_plot_groups = []
    for group_name in group_names:
        data = nivo_scatter_plot_deseq2_data_maker(extracted_deseq2_tabular_rows_scatter_plot, group_name)
        nivo_scatter_plot_groups.append(nivo_scatter_plot_group_maker(data, group_name))  
        
    df = pd.read_table(args.tabular_file, header= None, index_col=False)
    df.columns = ['gene_id', 'base_mean', 'log2_fc', 'stderr', 'wald_stats', 'p_value', 'p_adj_value'] 
    df = df[df['base_mean'].notna()] 
    df = df[df['log2_fc'].notna()] 
    base_mean_min = df['base_mean'].min( skipna = False)
    base_mean_max = df['base_mean'].max( skipna = False)
    log2_fc_min = df['log2_fc'].min( skipna = False)
    log2_fc_max = df['log2_fc'].max( skipna = False)
    
    nivo_scatter_plot_options = preproc_util_stencil.Nivo_Scatter_Plot_Options(base_mean_min, base_mean_max, log2_fc_min, log2_fc_max) 
    preproc_util_stencil.Nivo_plot_write_json(nivo_scatter_plot_groups, nivo_scatter_plot_options, args.output_file)
    print ("deseq2 tabular rows written" )


if __name__ == "__main__":
    main()
