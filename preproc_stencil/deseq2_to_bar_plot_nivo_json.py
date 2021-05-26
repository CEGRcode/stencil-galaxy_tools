## Takes deseq2 tabular file as input and provides Nivo JSON format data for bar plot as output.
#To do:
# 1- although looks like the column of p_values are sorted. It is better to be sorted.

import numpy as np
import argparse
import time
import pandas as pd

import preproc_util_stencil 


def nivo_extract_bar_plot(num_bins, sorted_column, name_index, name_keys):
    print (sorted_column) 
    bar_width = (max(sorted_column) - min(sorted_column))/float(num_bins)
    safety_margin = 0.01 * bar_width
    bar_height = 0
    counter = 0 
    bars_info = []
    for element in sorted_column:
           
        counter = counter + 1
        ## check for bar position AND make sure it is not the last element in the column
        if (element < ((bar_width*(len(bars_info) + 1)) + safety_margin) and  counter != (len(sorted_column) -1 ) ):
            bar_height = bar_height + 1
        else: ## move to new bar, or handle the last element.
            bar_info = {}
            bar_info[name_index] ="{:.2f}".format(min(sorted_column) + 0.5 * bar_width + bar_width*(len(bars_info)))  
            ## the second term on the right hand side is to account for the last element in the lis 
            bar_info[name_keys[0]] = bar_height + int ((counter == (len(sorted_column) - 1) ))
            bars_info.append(bar_info)
            bar_height = 0 + 1  ## zero for resetting and one for counting the first element in the new bar
    
    return (bars_info)


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
   
    num_bins = 50
    name_index = 'p_values'
    name_keys = ['freq']

    print (" process started ..." )
    parsed_deseq2_tabular = preproc_util_stencil.Parse_tabular_file(args.tabular_file, num_skipped_rows = 0)
    print ("deseq2 tabular file parsed" )
    p_values = Extract_p_values(parsed_deseq2_tabular)   
    #sorted_column= extract_sorted_column(extracted_deseq2_tabular_rows_bar_plot)
    sorted_column= p_values #extract_sorted_column(extracted_deseq2_tabular_rows_bar_plot)
    nivo_bar_plot = nivo_extract_bar_plot(num_bins, sorted_column, name_index, name_keys)
    nivo_bar_plot_options = preproc_util_stencil.Nivo_Bar_Plot_Options(name_index, name_keys) 
    preproc_util_stencil.Nivo_plot_write_json(nivo_bar_plot, nivo_bar_plot_options, args.output_file)

   
############################################################################################################

def Extract_p_values(parsed_deseq2_tabular):
    na_counter = 0 ## to count the lines which are not parsed because have "NA" value. 
    p_values = [] 
    for line in parsed_deseq2_tabular:
        if (line[5] =='NA'):
            na_counter += 1 
            continue
        p_values.append (float(str(line[5])))
    print ('Number of lines skipped because of NA parameter in p_value is:')
    print (na_counter)
    return(sorted(p_values))


if __name__ == "__main__":
    main()
