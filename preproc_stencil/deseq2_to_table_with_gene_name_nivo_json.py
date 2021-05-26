import argparse
import csv
import json 

class Gene_Info:
    def __init__ (self):
        self.id  = None 
        self.name = None 


class Nivo_Deseq2_Table_Col:
    def __init__ (self, name):
        self.name = name
        self.label = name # can be different than name
        self.options = { 'filter': False , 'sort': True} 


class Nivo_Deseq2_Table_Row:
    def __init__ (self, deseq2_table_data):
        self.gene_id = int(deseq2_table_data[0])
        self.base_mean = change_to_float_if_possible(deseq2_table_data[1])
        self.log2fc = change_to_float_if_possible(deseq2_table_data[2])
        self.stderr = change_to_float_if_possible(deseq2_table_data[3])
        self.wald_stats = change_to_float_if_possible(deseq2_table_data[4])
        self.p_value = change_to_float_if_possible(deseq2_table_data[5])
        self.p_adj = change_to_float_if_possible(deseq2_table_data[6])
        self.gene_name = deseq2_table_data[7]

def change_to_float_if_possible(value):
    if value != 'NA':
        return float(value)
    else:
        return (value)
        


def Extract_features_gff(parsed_gff_tabular):
    features= []
    for line in parsed_gff_tabular:
        if (line[0][0] == '#'):
            print ('line start with # so it is ignored. The line is')
            print (line)  
            continue      
        try:
            feature  =    (str(line[2]))
            if feature not in features:
                print ('A feature name in ggf file is %s' %feature)
                features.append(feature)
        except:
            print ('Warning: line does not have feature. The line is %s' %line)
    return (features)


def Extract_attributes_gff(parsed_gff_tabular):
    attributes= []
    for line in parsed_gff_tabular:
        if (line[0][0] == '#'):
            print ('Line start with # so it is ignored. The line is %s' %line)
            continue      
        try:
            attribute = (str(line[8]))
            attributes.append(attribute)
        except:
            print ('Warning: line does not have attribute. the line is %s' %line)
            continue
    return (attributes)


def Extract_gene_id_and_gene_name_gff(attributes):
    ## get out of attributes column, "GeneID" subelement and "Name" subelement if exist in the column
    gene_info_list = []
    for attribute in attributes:
        if "GeneID:" in attribute and "Name=" in attribute:
            gene_info = Gene_Info()
            attribute_subelements = attribute.split(';')
            for attribute_subelement in attribute_subelements:
                if "GeneID:" in attribute_subelement:
                   gene_info.id = attribute_subelement
                if "Name=" in attribute_subelement:
                   gene_info.name = attribute_subelement
                
            gene_info_list.append(gene_info)
            
    # parse the gene id located in front of "GeneID:" and before "," and 
    # parse the gene name located in front of "Name="
    for gene_info in gene_info_list:
        start_index = gene_info.id.index('GeneID:') + len('GeneID:')
        gene_info.id = gene_info.id [start_index:]
        sum_char = ""
        for a_char in gene_info.id:
            if (a_char == ','):
                break
            sum_char = sum_char + a_char
        gene_info.id = int (sum_char)
    
        start_index = gene_info.name.index('Name=') + len('Name=')
        gene_info.name = gene_info.name[start_index:]

    # make GeneID and gene Name a dictionary to be easily accessible
    # one GeneID can have multiple Names which is given as list
    gene_id_name_dic = {}
    last_gene_id = None
    last_gene_name = None
    sum_skipped_lines = 0
    for gene_info in gene_info_list:
        if (gene_info.id != last_gene_id) and (gene_info.name != last_gene_name):
            gene_id_name_dic[int(gene_info.id)] = [gene_info.name]
            last_gene_id = gene_info.id
            last_gene_name = gene_info.name  
        
        elif (gene_info.id == last_gene_id) and (gene_info.name != last_gene_name):
            gene_id_name_dic[int(gene_info.id)].append(gene_info.name)
            last_gene_name = gene_info.name  
        
        elif (gene_info.id != last_gene_id) and (gene_info.name == last_gene_name):
            
            gene_id_name_dic[int(gene_info.id)] = [gene_info.name]
            print ("Warning: same names for GeneID: %s and %s. The names is %s" %(gene_info.id, last_gene_id, gene_info.name)) 
            last_gene_id = gene_info.id
            #raise Exception (" there are genes with different ids but the same gene name")
        
        else :
            sum_skipped_lines += 1 
        
    print ('number of lines skipped, becasue no geneID and Gene Name is available, is: %s' %sum_skipped_lines) 
    return (gene_id_name_dic)


def Parse_tabular_file(file_name, num_skipped_rows):
    with open(file_name) as data:                                                                                          
        data_reader = csv.reader(data, delimiter='\t')
        
        if (num_skipped_rows > 0):
            for i in range(num_skipped_rows):
                next(data_reader)
        
        raw_data = list (data_reader)

    return raw_data


def Parse_tabular_file_v2(file_name):
    with open(file_name) as data:                                                                                          
        data_reader = csv.reader(data, delimiter='\t')
        raw_data = list (data_reader)
    return raw_data


def Write_data_dic(mydic,output_file):
    with open(output_file, 'w') as f:

        f.write ('# GeneID	GeneName \n')
        for key, value in mydic.items():
            f.write(str(key) + '\t')
            for i in range (len (value)-1):
                f.write(str(value[i]) + '\t')
            f.write(str(value[-1]) + '\n')


def Write_data_dic_plus_tabular(mydic,mytabular,output_file):
    sum_found = 0
    sum_not_found = 0
    with open(output_file, 'w') as f:
        f.write ('# GeneID	Base mean	log2(FC)	StdErr	Wald-Stats	P-value	P-adj	GeneName \n')
        for line in mytabular:
            f.write(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" +line[3] +
            "\t" +line[4]+ "\t" + line[5]+ "\t" + line[6] + "\t")
            try:
                f.write(mydic[int(line[0])][0] + '\n')
                #print ( 'for gene %s gene name found \n' %line[0])
                sum_found += 1 
            except:
                print ( 'for gene %s gene name not found \n' %line[0])
                f.write('not-found' + '\n')
                sum_not_found += 1 
    
    print ( 'percentage of sucess to assign gene name to gene ID is %s' % float(sum_found/(sum_found + sum_not_found)))

def Write_data_dic_plus_tabular(mydic,mytabular,output_file):
    mytabular_plus_gene_name= []
    sum_found = 0
    sum_not_found = 0
    with open(output_file, 'w') as f:
        #f.write ('# GeneID	Base mean	log2(FC)	StdErr	Wald-Stats	P-value	P-adj	GeneName \n')
        for line in mytabular:
            #f.write(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" +line[3] +
            #"\t" +line[4]+ "\t" + line[5]+ "\t" + line[6] + "\t")
            try:
             #   f.write(mydic[int(line[0])][0] + '\n')
                #print ( 'for gene %s gene name found \n' %line[0])
                sum_found += 1
                line.append (mydic[int(line[0])][0])
            except:
                print ( 'for gene %s gene name not found \n' %line[0])
              #  f.write('not-found' + '\n')
                sum_not_found += 1 
                line.append('not-found') 
            mytabular_plus_gene_name.append(line)
    print ( 'percentage of sucess to assign gene name to gene ID is %s' % float(sum_found/(sum_found + sum_not_found)))
    return (mytabular_plus_gene_name)
   
def Write_json_deseq2_tabular_plus_gene_name(mytabular, col_names, output_file_name):

    columns = []
    for col_name in col_names:
        nivo_deseq2_table_col = Nivo_Deseq2_Table_Col(col_name)
        columns.append (nivo_deseq2_table_col.__dict__)
     
    rows = [] 
    for row in mytabular:
        nivo_deseq2_table_row = Nivo_Deseq2_Table_Row (row)
        rows.append(nivo_deseq2_table_row.__dict__)
    
    nivo_table = {}
    nivo_table['columns'] = columns
    nivo_table['rows'] = rows

    #fileM = open(output_file_name,'w')
    with open(output_file_name, 'w') as fileM:
        json.dump(nivo_table, fileM) 




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--annotation' , dest='gff_tabular', required=True, help='Name of the gff annotation file')
    parser.add_argument('--deseq' , dest='deseq_tabular', required=True, help='Name of deseq2 output file')
    parser.add_argument('--output' , dest='output_file', required=True, help='Name of the output file')
    args = parser.parse_args()


    deseq2_col_names = ['gene_id', 'base_mean','log2fc','stderr','wald_stats','p_value','p_adj','gene_name']
    parsed_gff_tabular = Parse_tabular_file_v2(args.gff_tabular)
    parsed_deseq_tabular = Parse_tabular_file_v2(args.deseq_tabular)
    print ("parsed tabular files")

    features = Extract_features_gff(parsed_gff_tabular)
    attributes = Extract_attributes_gff(parsed_gff_tabular)
    gene_id_name_dic = Extract_gene_id_and_gene_name_gff(attributes)
    print ("gene id and name extracted from gff file")
    Write_data_dic(gene_id_name_dic,'gene_id_name_pair_in_gff.txt')
    deseq2_tabular_plus_gene_name = Write_data_dic_plus_tabular(gene_id_name_dic,parsed_deseq_tabular,args.output_file)
    Write_json_deseq2_tabular_plus_gene_name(deseq2_tabular_plus_gene_name, deseq2_col_names, args.output_file)
    print ("finished")


if __name__ == "__main__":
    main()
