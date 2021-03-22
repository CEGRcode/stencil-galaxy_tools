## Takes deseq2 tabular file as input and provides JSON format data as output.
## The output is tailored for nivo visualizer software used by Stencil website.
## The tool currently can provide MA plot which is a sacatter plot and distribution of Adjusted P Values as bar plot.

import csv 
import argparse
import time
import json

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


       

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input' , dest='deseq2_tabular', required=True, help='Name of the .tabular file which is output of deseq2')
    parser.add_argument('--plottype' , dest='plottype', required=True, help='Type of the plot, options: scatter_plot, bar_plot')
    parser.add_argument('--output' , dest='output_file', required=True, help='Desired name of output file')
    args = parser.parse_args()
    print (" process started ..." )
    parsed_deseq2_tabular = Parse_tabular_file(args.deseq2_tabular)
    print ("deseq2 tabular file parsed" )
    extracted_deseq2_tabular_rows= Extract_deseq2_tabular_rows(parsed_deseq2_tabular)
    print ("deseq2 tabular rows extracted" )

    if (args.plottype == 'scatter_plot'):
        
        nivo_scatter_plot_num_groups = 1
        data = nivo_scatter_plot_data_maker(extracted_deseq2_tabular_rows)
        print ("deseq2 tabular rows written" )
        nivo_scatter_plot_groups = []
        for i in range(nivo_scatter_plot_num_groups):
            nivo_scatter_plot_groups.append(nivo_scatter_plot_group_maker(data, i))  
        
        nivo_plot_write_json(nivo_scatter_plot_groups, args.output_file)
        print ("deseq2 tabular rows written" )

    elif (args.plottype == 'bar_plot'):
        
        num_bins = 50
        name_column = 'p_adj_value'
        sorted_column= extract_sorted_column(extracted_deseq2_tabular_rows)
        nivo_bar_plot = nivo_extract_bar_plot(num_bins, sorted_column, name_column)
        nivo_plot_write_json(nivo_bar_plot, args.output_file)

    else:
        print ('please enter valid plot type')

def Parse_tabular_file(file_name):
    with open(file_name) as data:                                                                                          
        data_reader = csv.reader(data, delimiter='\t')
        raw_data = list (data_reader)
    return raw_data


def Extract_deseq2_tabular_rows(parsed_deseq2_tabular):
    na_counter = 0 ## to count the lines which are not parsed because have "NA" value. 
    deseq2_tabular_rows = [] 
    for line in parsed_deseq2_tabular:
        if ('NA' in line):
            na_counter += 1 
            continue
        deseq2_tabular_row = Deseq2_Tabular_Row()
        deseq2_tabular_row.gene_id     =     (str(line[0]))
        deseq2_tabular_row.base_mean   = float((str(line[1])))  
        deseq2_tabular_row.log2_fc    = float((str(line[2]))) 
        deseq2_tabular_row.wald_stats      = float(   line[4])
        deseq2_tabular_row.p_value =     float(str(line[5]))
        deseq2_tabular_row.p_adj_value    = float((str(line[6])))
        deseq2_tabular_rows.append (deseq2_tabular_row)
    print ('Number of lines skipped because of NA parameter, is:')
    print (na_counter)
    return (deseq2_tabular_rows)



def xy_convert_format_to_point_dict(x,y):
    point_dict_format = {}
    point_dict_format["x"] = x
    point_dict_format["y"] = y
    return (point_dict_format)




def nivo_plot_write_json(nivo_scatter_plot_groups, output_file):

    file_name = output_file
    fileM = open(file_name,'w')
    with open(file_name, 'w') as fileM:
        json.dump(nivo_scatter_plot_groups, fileM)   



def nivo_scatter_plot_data_maker(deseq2_tabular_rows):
    data=[]
    for deseq2_tabular_row in deseq2_tabular_rows: 
        data.append(xy_convert_format_to_point_dict(deseq2_tabular_row.base_mean,deseq2_tabular_row.log2_fc))
    return(data)


def nivo_scatter_plot_group_maker(data, nivo_group_id):
    nivo_scatter_plot_group = {}
    nivo_scatter_plot_group["id"] = 'group ' + str(nivo_group_id)
    nivo_scatter_plot_group["data"] = data
    return(nivo_scatter_plot_group)


def nivo_extract_bar_plot(num_bins, sorted_column, name):
    
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
            bar_info[name] ="{:.2f}".format(min(sorted_column) + 0.5 * bar_width + bar_width*(len(bars_info)))  
            ## the second term on the right hand side is to account for the last element in the lis 
            bar_info["freq"] = bar_height + int ((counter == (len(sorted_column) - 1) ))
            print ('element for switch is: ')
            print(element)
            bars_info.append(bar_info)
            bar_height = 0 + 1  ## zero for resetting and one for counting the first element in the new bar
    
    return (bars_info)


def extract_sorted_column(rows):
    sorted_column = []
    for row in rows:
        sorted_column.append(row.p_adj_value)
    return (sorted_column)
        


if __name__ == "__main__":
    main()
