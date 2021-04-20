import argparse
import time

import preproc_util_stencil

class Tagpileup_Tabular_Info:
    def __init__ (self):
        self.x = []
        self.sense = [] 
        self.antisense = [] 
        self.x_info_extracted = False 
        self.sense_info_extracted = False
        self.antisense_info_extracted = False

class Nivo_Line_Plot_Group:
    def __init__ (self, group_id, hsl_color):
        self.id = group_id
        self.data = []
        self.color = hsl_color

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input' , dest='tagpileup_tabular', required=True, help='Name of the .tabular file which is output of Tagpileup')
    parser.add_argument('--output' , dest='output_file', required=True, help='Desired name of output file')
    args = parser.parse_args()
    print (" process started ..." )
    parsed_tagpileup_tabular = preproc_util_stencil.Parse_tabular_file(args.tagpileup_tabular)
    extracted_tagpileup_tabular_info = Extract_tagpileup_tabular_info(parsed_tagpileup_tabular)

    nivo_line_plot_groups_dict = []
    nivo_line_plot_groups_dict.append(nivo_line_plot_group_maker(extracted_tagpileup_tabular_info, 'sense', "hsl(240,100%,50%)"))
    nivo_line_plot_groups_dict.append(nivo_line_plot_group_maker(extracted_tagpileup_tabular_info, 'antisense', "hsl(0, 100%, 50%)"))
    preproc_util_stencil.Nivo_plot_write_json(nivo_line_plot_groups_dict, args.output_file)

def Extract_tagpileup_tabular_info(parsed_tagpileup_tabular):
    
    tagpileup_tabular_info = Tagpileup_Tabular_Info()
    for line in parsed_tagpileup_tabular:
        
        if not tagpileup_tabular_info.x_info_extracted: 
            for i in range(len(line)-1):
                tagpileup_tabular_info.x.append(line[i + 1])
            tagpileup_tabular_info.x_info_extracted = True
            print ('I am finished with x coordinate')
            print (str(i))
            continue 
        
        if not tagpileup_tabular_info.sense_info_extracted: 
            for i in range(len(line)-1):
                tagpileup_tabular_info.sense.append(line[i + 1])
            tagpileup_tabular_info.sense_info_extracted = True
            print ('I am finished with sense coordinate')
            print (str(i))
            continue 
        
        if not tagpileup_tabular_info.antisense_info_extracted: 
            for i in range(len(line)-1):
                tagpileup_tabular_info.antisense.append(line[i + 1])
            tagpileup_tabular_info.antisense_info_extracted = True
            print ('I am finished with antisense coordinate')
            print (str(i))
            continue 

    return (tagpileup_tabular_info)

def nivo_line_plot_group_maker(tagpileup_tabular_info, group_id, group_color):
    nivo_line_plot_group = Nivo_Line_Plot_Group(group_id, group_color)
    if (group_id == 'sense'):
        for i in range(len(tagpileup_tabular_info.x)): 
            nivo_line_plot_group.data.append(preproc_util_stencil.Xy_convert_format_to_point_dict(tagpileup_tabular_info.x[i],tagpileup_tabular_info.sense[i]))
    elif (group_id == 'antisense'):
        for i in range(len(tagpileup_tabular_info.x)): 
           nivo_line_plot_group.data.append(preproc_util_stencil.Xy_convert_format_to_point_dict(tagpileup_tabular_info.x[i],tagpileup_tabular_info.antisense[i]))
    else:
        print (' this code is just for sense and antisense group id ')
    
    nivo_line_plot_group_dict = {}
    nivo_line_plot_group_dict["id"] = nivo_line_plot_group.id
    nivo_line_plot_group_dict["color"] = nivo_line_plot_group.color
    nivo_line_plot_group_dict["data"] = nivo_line_plot_group.data

    return(nivo_line_plot_group_dict)



if __name__ == "__main__":
    main()
