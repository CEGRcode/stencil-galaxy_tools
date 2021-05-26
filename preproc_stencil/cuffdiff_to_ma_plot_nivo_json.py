## Takes cuffdiff tabular file as input and provides JSON format data for MA plot as output.
## The output is tailored for nivo visualizer software used by Stencil website.

import numpy as np
import argparse
import time
import pandas as pd

import preproc_util_stencil 


class Cuffdiff_Gene_Diff_Tabular_Row:
    def __init__ (self):
        self.gene_id = None
        self.gene = None
        self.locus = None
        self.sample_1 = None
        self.sample_2 = None
        self.value_1  = None 
        self.value_2 = None 
        self.log2_fc = None  


def Extract_cuffdiff_gene_diff_tabular_rows(parsed_cuffdiff_gene_diff_tabular):
    no_data_counter = 0 ## to count the lines which are not parsed because have "NA" value. 
    cuffdiff_gene_diff_tabular_rows  = [] 
    for line in parsed_cuffdiff_gene_diff_tabular:
        if (float(line[7]) < 0.0001 or float(line[8]) <  0.0001 ):   # small number
            no_data_counter = no_data_counter + 1 
            continue

        cuffdiff_gene_diff_tabular_row = Cuffdiff_Gene_Diff_Tabular_Row()
        cuffdiff_gene_diff_tabular_row.gene_id     =     str(line[1])
        cuffdiff_gene_diff_tabular_row.gene        =     str(line[2])  
        cuffdiff_gene_diff_tabular_row.locus        =     str(line[3])  
        cuffdiff_gene_diff_tabular_row.sample_1    =     str(line[4]) 
        cuffdiff_gene_diff_tabular_row.sample_2    =     str(line[5])
        cuffdiff_gene_diff_tabular_row.value_1     =     float(str(line[7]))
        cuffdiff_gene_diff_tabular_row.value_2    = float((str(line[8])))
        cuffdiff_gene_diff_tabular_row.log2_fc    = float((str(line[9])))
        cuffdiff_gene_diff_tabular_rows.append (cuffdiff_gene_diff_tabular_row)
    print ('Number of lines skipped because of 0 FPKM in control or treated sample, is:')
    print (no_data_counter)
    return (cuffdiff_gene_diff_tabular_rows)


def nivo_scatter_plot_cuffdiff_data_maker(cuffdiff_gene_diff_tabular_rows, group_id):
    data=[]
    if (group_id == 0):
        for row in cuffdiff_gene_diff_tabular_rows: 
            data.append(preproc_util_stencil.Xy_convert_format_to_point_dict(0.5*(row.value_1 + row.value_2) , row.log2_fc))
    return(data)


def nivo_scatter_plot_cuffdiff_data_maker_per_gene(row):
    data=[]
    data.append(preproc_util_stencil.Xy_convert_format_to_point_dict(0.5*(row.value_1 + row.value_2), row.log2_fc))
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


def extract_sorted_column(rows):
    sorted_column = []
    for row in rows:
        sorted_column.append(float(row.p_value))
    return (sorted_column)
      

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input' , dest='tabular_file', required=True, help='Name of the .tabular file which is output of deseq2 or cuffdiff')
    parser.add_argument('--output' , dest='output_file', required=True, help='Desired name of output file')
    args = parser.parse_args()
   
   gene_annotated = True 
   print (" process started ..." )

   parsed_cuffdiff_gene_diff_tabular = preproc_util_stencil.Parse_tabular_file(args.tabular_file, num_skipped_rows = 1)
   print ("cuffdiff gene differention tabular file parsed" )
   extracted_cuffdiff_gene_diff_tabular_rows= Extract_cuffdiff_gene_diff_tabular_rows(parsed_cuffdiff_gene_diff_tabular)
   print ("cuffdiff gene differention tabular file rows extracted" )

   nivo_scatter_plot_groups = []
   if (gene_annotated == False):       
       nivo_scatter_plot_num_groups = 1
       for i in range(nivo_scatter_plot_num_groups):
           data = nivo_scatter_plot_cuffdiff_data_maker(extracted_cuffdiff_gene_diff_tabular_rows, i)
           nivo_scatter_plot_groups.append(nivo_scatter_plot_group_maker(data, i))  
           print ( "group id is" + str (i))  
   else:
       for row in extracted_cuffdiff_gene_diff_tabular_rows:
           data = nivo_scatter_plot_cuffdiff_data_maker_per_gene(row)
           nivo_scatter_plot_groups.append(nivo_scatter_plot_group_maker_per_gene(data, row.gene_id))  
       nivo_scatter_plot_options = preproc_util_stencil.Nivo_Scatter_Plot_Options() 
   
   preproc_util_stencil.Nivo_plot_write_json(nivo_scatter_plot_groups, nivo_scatter_plot_options, args.output_file)
   print ("cuffdiff gene differention expression tabular rows written" )


if __name__ == "__main__":
    main()
