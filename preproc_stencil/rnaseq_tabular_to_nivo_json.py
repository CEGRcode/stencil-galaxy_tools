## Takes deseq2 tabular file as input and provides JSON format data as output.
## The output is tailored for nivo visualizer software used by Stencil website.
## The tool currently can provide MA plot which is a sacatter plot and distribution of Adjusted P Values as bar plot.

import argparse
import time

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



       

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input' , dest='tabular_file', required=True, help='Name of the .tabular file which is output of deseq2 or cuffdiff')
    parser.add_argument('--source' , dest='source', required=True, help='source of generated file for input. options: deseq2 or cuffdiff')
    parser.add_argument('--plottype' , dest='plottype', required=True, help='Type of the plot, options: scatter_plot, bar_plot')
    parser.add_argument('--output' , dest='output_file', required=True, help='Desired name of output file')
    args = parser.parse_args()
    print (" process started ..." )

    if (args.source == "deseq2"):
        parsed_deseq2_tabular = preproc_util_stencil.Parse_tabular_file(args.tabular_file, num_skipped_rows = 0)
        print ("deseq2 tabular file parsed" )
        extracted_deseq2_tabular_rows= Extract_deseq2_tabular_rows(parsed_deseq2_tabular)
        print ("deseq2 tabular rows extracted" )
    
    if (args.source == "cuffdiff"):
        parsed_cuffdiff_gene_diff_tabular = preproc_util_stencil.Parse_tabular_file(args.tabular_file, num_skipped_rows = 1)
        print ("cuffdiff gene differention tabular file parsed" )
        extracted_cuffdiff_gene_diff_tabular_rows= Extract_cuffdiff_gene_diff_tabular_rows(parsed_cuffdiff_gene_diff_tabular)
        print ("cuffdiff gene differention tabular file rows extracted" )

    if (args.plottype == 'scatter_plot' and args.source == 'deseq2'):
        
        nivo_scatter_plot_num_groups = 2
        nivo_scatter_plot_groups = []
        
        for i in range(nivo_scatter_plot_num_groups):
            data = nivo_scatter_plot_deseq2_data_maker(extracted_deseq2_tabular_rows, i)
            nivo_scatter_plot_groups.append(nivo_scatter_plot_group_maker(data, i))  
            print ( "group id is" + str (i))  
        preproc_util_stencil.Nivo_plot_write_json(nivo_scatter_plot_groups, args.output_file)
        print ("deseq2 tabular rows written" )

    if (args.plottype == 'bar_plot' and args.source == 'deseq2'):
        
        num_bins = 50
        name_column = 'p_adj_value'
        sorted_column= extract_sorted_column(extracted_deseq2_tabular_rows)
        nivo_bar_plot = nivo_extract_bar_plot(num_bins, sorted_column, name_column)
        preproc_util_stencil.Nivo_plot_write_json(nivo_bar_plot, args.output_file)

    if (args.plottype == 'scatter_plot' and args.source == 'cuffdiff'):
        gene_annotated = True 
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
        
        preproc_util_stencil.Nivo_plot_write_json(nivo_scatter_plot_groups, args.output_file)
        print ("cuffdiff gene differention expression tabular rows written" )

############################################################################################################

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






def nivo_scatter_plot_deseq2_data_maker(deseq2_tabular_rows, group_id):
    data=[]
    if (group_id == 0):
        for row in deseq2_tabular_rows: 
            if ( row.p_adj_value >= 0.1): 
                data.append(preproc_util_stencil.Xy_convert_format_to_point_dict(row.base_mean, row.log2_fc))
    if (group_id == 1):
        for row in deseq2_tabular_rows: 
            if (row.p_adj_value < 0.1): 
                data.append(preproc_util_stencil.Xy_convert_format_to_point_dict(row.base_mean, row.log2_fc))
    
    return(data)

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




def nivo_scatter_plot_group_maker(data, nivo_group_id):
    nivo_scatter_plot_group = {}
    nivo_scatter_plot_group["id"] = 'Group ' + str(nivo_group_id)
    nivo_scatter_plot_group["data"] = data
    return(nivo_scatter_plot_group)

def nivo_scatter_plot_group_maker_per_gene(data, gene_id):
    nivo_scatter_plot_group = {}
    nivo_scatter_plot_group["id"] = gene_id
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
