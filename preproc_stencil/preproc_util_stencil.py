import csv 
import json

def Nivo_plot_write_json(nivo_plot_groups, output_file):

    file_name = output_file
    fileM = open(file_name,'w')
    nivo_plot = {}
    nivo_plot['chartData'] = nivo_plot_groups
    #nivo_plot['chartOptions'] = []
    with open(file_name, 'w') as fileM:
        json.dump(nivo_plot, fileM) 

def Parse_tabular_file(file_name, num_skipped_rows):
    with open(file_name) as data:                                                                                          
        data_reader = csv.reader(data, delimiter='\t')
        
        if (num_skipped_rows > 0):
            for i in range(num_skipped_rows):
                next(data_reader)
        
        raw_data = list (data_reader)

    return raw_data


def Xy_convert_format_to_point_dict(x,y):
    point_dict_format = {}
    point_dict_format["x"] = round(float(x),4)
    point_dict_format["y"] = round(float(y),4)
    return (point_dict_format)


