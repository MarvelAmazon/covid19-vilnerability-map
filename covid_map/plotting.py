# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 07:28:55 2020

@author: Treudsky L.H. Antoine
"""
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar,HoverTool
from bokeh.palettes import brewer
import json


#Pass a geodataframe to get GeoJSONDatatsource
def getGeoSource(gdf):
    merged_json=json.loads(gdf.to_json())
    json_data = json.dumps(merged_json)
    return GeoJSONDataSource(geojson = json_data)

def plot_map(gdf, column=None, title='',tooltip=None):
    #code from https://github.com/dmnfarrell/teaching/blob/master/geo/maps_python.ipynb
    geosource=getGeoSource(gdf)
    palette = brewer['OrRd'][8]
    palette = palette[::-1]
    vals = gdf[column]
    
       #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = vals.min(), high = vals.max())
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20, 
                         location=(0,0), orientation='horizontal')
    p1 = figure(title=title)
    p1.axis.visible = False
    p1.xgrid.visible = False
    p1.ygrid.visible = False
    p1.patches('xs','ys',source=geosource, line_color = "black", line_width = 0.25, fill_alpha = 1,
               fill_color={'field' :column , 'transform': color_mapper})
    TOOLTIPS = tooltip
    p1.add_tools(HoverTool(tooltips=TOOLTIPS))
    p1.add_layout(color_bar, 'below')
    return p1