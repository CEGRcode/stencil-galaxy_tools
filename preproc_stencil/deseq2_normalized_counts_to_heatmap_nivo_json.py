import numpy as np
import colorsys
import argparse
import pandas as pd
from numpy.linalg import norm

import preproc_util_stencil

def Number_matrix_to_hsl_matrix(matrix_a, base_color):
    max_matrix = matrix_a.max()
    min_matrix = matrix_a.min()
    hsl_matrix = [[0 for x in range(len(matrix_a))] for y in range(len(matrix_a))] 
    
    for i in range(len(matrix_a)):
        for j in range(len(matrix_a[i])):
            single_color_code = (1.0/(max_matrix - min_matrix)) * (matrix_a[i][j] - min_matrix)
            if (base_color == 'red'):
                element = 1 
            if (base_color == 'green'):
                element = 1 
            if (base_color == 'blue'):
                hls_tuple = colorsys.rgb_to_hls(1, 1, single_color_code)
                hsl_matrix[i][j] = (hls_tuple[0]*360, hls_tuple[2]*100, hls_tuple[1]*100) 
    
    return hsl_matrix
        
def Matrices_data_to_heatmap_nivo_json(number_matrix, conditions, hsl_matrix = None):
    nivo_heatmap_plot_groups = []
    for i in range(len(conditions)):
        nivo_heatmap_plot_group = {}
        nivo_heatmap_plot_group["samples"] = str(conditions[i])
        for j in range(len(conditions)):
            nivo_heatmap_plot_group[ str(conditions[j])] = round(float(number_matrix[i][j]),3)
            if hsl_matrix is not None: 
                nivo_heatmap_plot_group[ str(conditions[j]+'Color')] = "hsl(" + str(hsl_matrix[i][j][0]) + ", "+ str(hsl_matrix[i][j][1]) +"%, "+ str(hsl_matrix[i][j][2]) + "%)"
        nivo_heatmap_plot_groups.append(nivo_heatmap_plot_group)
    
    return nivo_heatmap_plot_groups        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input' , dest='deseq2_tabular', required=True, help='Name of the .tabular file which is output of deseq2')
    parser.add_argument('--output' , dest='output_file', required=True, help='Desired name of output file')
    parser.add_argument('--color_code' , dest='color_code_needed', required=True, help='color code needed in json file. Enter yes or no')
 
    args = parser.parse_args()
    raw_data = pd.read_table(args.deseq2_tabular, index_col=0)
    conditions = list (raw_data.columns)
    number_matrix = np.full((len(raw_data.columns),len(raw_data.columns)), None)
    
    i = -1
    for column1 in raw_data:
        i = i + 1
        j = -1 
        for column2 in raw_data:
            j = j + 1
            number_matrix[i][j] = norm(raw_data[column1] - raw_data[column2])
    
    if (args.color_code_needed == 'yes' or args.color_code_needed == 'Yes'):
        base_color = 'blue'
        hsl_matrix = Number_matrix_to_hsl_matrix(number_matrix, base_color)
        nivo_heatmap_plot_groups = Matrices_data_to_heatmap_nivo_json(number_matrix, conditions, hsl_matrix)
    else:
        nivo_heatmap_plot_groups = Matrices_data_to_heatmap_nivo_json(number_matrix, conditions)


    nivo_heatmap_plot_options = preproc_util_stencil.Nivo_Heatmap_Plot_Options(conditions) 
    preproc_util_stencil.Nivo_plot_write_json(nivo_heatmap_plot_groups, nivo_heatmap_plot_options, args.output_file)


if __name__ == "__main__":
    main()
