import csv 
import json
import math
import numpy as np


class Nivo_General_Plot_Options:
    def __init__ (self):
        self.margin  = {'top':60, 'right':140, 'bottom':70, 'left':90 }
        self.axisTop = {'orient': 'top', 'tickSize': 5, 'tickPadding': 5, 'tickRotation': -90, 'legend': '', 'legendOffset': 36 }
        self.axisRight = {}
        self.axisBottom = {'orient':'bottom', 'tickSize':5, 'tickPadding':5, 'tickPadding':5, 'tickRotation':0, 'legend':'X-Axis', 'legendPosition':'middle', 'legendOffset': 46}
        self.axisLeft =   {'orient':'bottom', 'tickSize':5, 'tickPadding':5, 'tickPadding':5, 'tickRotation':0, 'legend':'Y-Axis', 'legendPosition':'middle', 'legendOffset': -60}

class Nivo_Scatter_Plot_Options(Nivo_General_Plot_Options):
     
    def __init__(self, x_min, x_max, y_min, y_max):
        Nivo_General_Plot_Options.__init__(self)
        x_min_log = Cal_log_scale_limit (x_min)
        x_max_log = Cal_log_scale_limit (x_max)
        y_min_linear = Cal_linear_scale_limit (y_min)
        y_max_linear = Cal_linear_scale_limit (y_max)
        x_log_scale_ticks = Cal_log_scale_ticks (x_min_log, x_max_log)
        y_linear_scale_ticks = Cal_linear_scale_ticks(y_min_linear, y_max_linear)
        self.Update_general_plot_options(x_log_scale_ticks,y_linear_scale_ticks)
        
        self.xScale = {'type': 'log' , 'min':x_min_log, 'max': x_max_log}
        self.yScale = {'type': 'linear' , 'min':y_min_linear , 'max': y_max_linear}
        #xFormat
        #yFormat
        self.blendMode = 'multiply'
        self.colors = {'scheme': 'nivo'}
        self.legends = { 'anchor': 'bottom-right', 'direction': 'column', 'justify': False, 'translateX': 130, 'translateY': 0, 'itemWidth': 100, 'itemHeight': 12, 'itemsSpacing': 5, 'itemDirection': 'left-to-right', 'symbolSize': 12, 'symbolShape': 'circle', 'effects': { 'on': 'hover' , 'style': {'itemOpacity': 1} }}
    
    def Update_general_plot_options(self, x_log_scale_ticks, y_linear_scale_ticks):
        self.axisTop['legend'] = 'MA−plot for Treatment treated vs untreated'
        tmp = x_log_scale_ticks[-1]
        self.axisTop['tickValues'] = [tmp] #tmp.append(1og_scale_ticks[-1])
        self.axisBottom['legend'] = 'Mean of normalized counts'
        self.axisBottom['tickValues'] = x_log_scale_ticks
        self.axisLeft['legend'] = 'Log fold change'
        self.axisLeft['legendOffset'] = -40
        self.axisLeft['tickValues'] = y_linear_scale_ticks
        self.margin  = {'top':40, 'right':60, 'bottom':70, 'left':60 }

    

class Nivo_Bar_Plot_Options:
    def __init__ (self, indexBy, keys):
        Nivo_General_Plot_Options.__init__(self)
        self.Update_general_plot_options()
        self.padding = 0.3
        self.indexBy = indexBy
        self.keys = keys  ## it can be more than one value
        self.valueScale = {'type': 'linear'}
        self.indexScale = {'type': 'band', 'round': True}
        self.colors = {'scheme': 'nivo'}
        self.defs = [ {'id': 'dots', 'type': 'patternDots', 'background': 'inherit', 'color': '#38bcb2', 'size': 4, 'padding': 1, 'stagger': True } ]
        self.fill = [{ 'match': {'id': keys[0]}, 'id': 'dots' }] 
        self.borderRadius = 12
        self.borderColor = 'black' ## it can be more complicated than a simple color. Please see nivo website
        self.labelSkipWidth = 12 
        self.labelSkipHeight = 12
        self.labelTextColor = 'black' ## it can be more complicated than a simple color. Please see nivo website
        self.animate = True
        self.motionStiffness = 90
        self.motionDamping = 15
        self.legends = { 'dataFrom': 'keys', 'anchor': 'bottom-right', 'direction': 'column', 'justify': False, 'translateX': 120, 'translateY': 0, 'itemWidth': 100, 'itemHeight': 20, 'itemsSpacing': 2, 'itemDirection': 'left-to-right', 'itemOpacity': 0.85, 'symbolSize': 20, 'effects': { 'on': 'hover' , 'style': {'itemOpacity': 1} }}

    def Update_general_plot_options(self):
        self.margin  = {'top':50, 'right':130, 'bottom':50, 'left':60}
        self.axisTop = {}
        self.axisBottom['legendOffset'] = 32
        self.axisLeft['legendOffset'] =  -60



class Nivo_Line_Plot_Options(Nivo_General_Plot_Options):

    def __init__ (self):
        Nivo_General_Plot_Options.__init__(self)
        self.Update_general_plot_options()
        self.xScale = {'type': 'point'}
        self.yScale = {'type': 'linear', 'min': 'auto', 'max': 'auto', 'stacked': True, 'reverse': False  }
        self.yFormat = ">-.2f"
        self.lineWidth = 2
        self.pointSize = 10
        self.pointColor = {'theme': 'background'}
        self.pointBorderWidth = 2
        self.pointBorderColor = 'black' ## Other options available. Pleae check Nivo website.
        self.pointLabelYOffset = -12
        self.useMesh = True
        self.legends = { 'anchor': 'bottom-right', 'direction': 'column', 'justify': False, 'translateX': 100, 'translateY': 0, 'itemWidth': 80, 'itemHeight': 20, 'itemsSpacing': 0, 'itemDirection': 'left-to-right', 'itemOpacity': 0.75,  'symbolSize': 12, 'symbolShape': 'circle', 'symbolBorderColor': 'rgba(0, 0, 0, .5)', 'effects': { 'on': 'hover' , 'style': {'itemBackground': 'rgba(0, 0, 0, .03)', 'itemOpacity': 1} }}

    def Update_general_plot_options(self):
        self.margin['top'] = 50
        self.margin['right'] = 110
        self.margin['bottom'] = 50
        self.margin['left'] = 60
        self.axisLeft['orient'] = 'left'
        self.axisLeft['legendOffset'] = -40
        self.axisTop = {}
        self.axisBottom['legendOffset'] =  36


class Nivo_Heatmap_Plot_Options(Nivo_General_Plot_Options):
    def __init__ (self, conditions):
        Nivo_General_Plot_Options.__init__(self)
        self.Update_general_plot_options()
        self.keys = conditions   
        self.indexBy = 'samples'
        self.cellOpacity = 1
        self.cellBorderColor = {'theme': 'background'}
        self.labelTextColor =  {'theme': 'background'}
        self.defs = [{'id': 'lines', 'type': 'patternLines', 'background': 'inheret', 'color': 'rgba(0, 0, 0, 0.1)', 'rotation': -45, 'lineWidth': 4, 'spacing': 7}] 
        self.fill = [{'id': 'lines'}]
        self.animate = True
        self.motionConfig = "wobbly"
        self.motionStiffness = 80
        self.motionDamping = 9
        self.hoverTarget = "cell"
        self.cellHoverOthersOpacity = 0.25

    def Update_general_plot_options(self):
        self.margin['top'] = 100
        self.margin['right'] = 60
        self.margin['bottom'] = 60
        self.margin['left'] = 60
        self.axisBottom = {}
        self.axisLeft['orient'] = 'left'
        self.axisLeft['tickRotation'] = 0
        self.axisLeft['legend'] = 'samples'
        self.axisLeft['legendOffset'] = -40

def Cal_log_scale_limit(x_limit):
    if (x_limit > 1):
        x_limit_log_digits = int(math.log(x_limit, 10)) + 1 
    else:
        x_limit_log_digits = int(math.log(x_limit, 10)) - 1
        
    return(pow(10, x_limit_log_digits))

def Cal_linear_scale_limit(x_limit):
    if (x_limit >= 0):
        return(int(x_limit) + int(1)) 
    else:
        return(int(x_limit) - int(1))



def Cal_log_scale_ticks (x_min_log, x_max_log):
    log_scale_ticks= [x_min_log]
    while True:
        log_scale_ticks.append(log_scale_ticks[-1]*10)
        if (log_scale_ticks[-1]*10> x_max_log + 1):
            break
    
    print (log_scale_ticks)
    return (log_scale_ticks)


def Cal_linear_scale_ticks (x_min_linear, x_max_linear):
    linear_scale_ticks= [x_min_linear]
    while True:
        linear_scale_ticks.append(linear_scale_ticks[-1] + int(1))
        if (linear_scale_ticks[-1] == x_max_linear):
            break
    
    print (linear_scale_ticks)
    return (linear_scale_ticks)



def Nivo_plot_write_json(nivo_plot_groups, nivo_plot_options, output_file):
    file_name = output_file
    fileM = open(file_name,'w')
    nivo_plot = {}
    nivo_plot['chartData'] = nivo_plot_groups
    nivo_plot['chartOptions'] = nivo_plot_options.__dict__
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


