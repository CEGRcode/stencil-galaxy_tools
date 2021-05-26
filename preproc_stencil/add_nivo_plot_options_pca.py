import json
import argparse

import preproc_util_stencil 

def raw_json_to_nivo_json(raw_json):
    nivo_json_list =[]
    for i in range(len(raw_json)):
        nivo_json = {}
        nivo_json['id'] = raw_json[i]['id']

        nivo_json['data'] = []
        nivo_json['data'].append({ 'x': raw_json[i]['x'], 'y': raw_json[i]['y'] })
        nivo_json_list.append(nivo_json)
    return (nivo_json_list)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input' , dest='plot_data_json', required=True, help='Name of the nivo plot data in json format')

    #parser.add_argument('--plottype' , dest='plottype', required=True, help='Type of the plot, options: scatter_plot_pca, scatter_plot_ma')
    parser.add_argument('--output' , dest='output_file', required=True, help='Desired name of output file')
    args = parser.parse_args()
    print (" process started ..." )
    f = open (args.plot_data_json)
    f_json = json.load (f)

    x_min = x_max = f_json[0]['x'] # just a possible guess to start with
    for i in range (len(f_json)):
        if (f_json[i]['x'] < x_min):
            x_min = f_json[i]['x']
    
    for i in range (len(f_json)):
        if (f_json[i]['x'] > x_max):
            x_max = f_json[i]['x']
    
    y_min = y_max = f_json[0]['y']
    for i in range (len(f_json)):
        if (f_json[i]['y'] < y_min):
            y_min = f_json[i]['y']
    
    for i in range (len(f_json)):
        if (f_json[i]['y'] > y_max):
            y_max = f_json[i]['y']

    print ("extremes found")
    nivo_scatter_plot_options = preproc_util_stencil.Nivo_Scatter_Plot_Options_Pca(x_min, x_max, y_min, y_max) 
    print ("nivo scatter plot options generated")
    
    f_nivo_json = raw_json_to_nivo_json(f_json)
    preproc_util_stencil.Nivo_plot_write_json(f_nivo_json, nivo_scatter_plot_options, args.output_file)
    print ("deseq2 tabular rows written" )
    
    f.close()

if __name__ == "__main__":
    main()
