# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 05:42:16 2020

@author: admin
"""
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar,Dropdown, Select,HoverTool,Panel, Tabs
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
import geopandas as gpd
import json
import sys

#reading geodata
sectionsgpd=gpd.read_file(join(dirname(__file__),"data","combined","v0_sec_data.shp"))
sectionsgpd.set_geometry('geometry')
communesgpd=gpd.read_file(join(dirname(__file__),"data","combined","v0_com_data.shp"))
communesgpd.set_geometry('geometry')
departementsgpd=gpd.read_file(join(dirname(__file__),"data","combined","v0_dep_data.shp"))
departementsgpd.set_geometry('geometry')


def getDataset(geodata, name, adm_division):
    #name: name of the adm division
    #adm_division: type of adm division
    v=geodata.copy()
    v.set_index(adm_division,inplace=True)
    x=v.loc[name].copy()
    x.reset_index(inplace=True)
    print(x.columns)
    print(x.shape)
    return x

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
communesgpd=communesgpd.astype({"ADM1_FR":'category'})
sectionsgpd=sectionsgpd.astype({"ADM1_FR":'category',"ADM2_FR":'category'})
#indicators selection
selectA=Select(title="Indicator", options=departementsgpd.columns.tolist(), value="Population") 
selectB=Select(title="Indicator", options=communesgpd.columns.tolist(), value="Population") 
selectC=Select(title="Indicator", options=sectionsgpd.columns.tolist(), value="Population")   

artibonite=communesgpd[communesgpd["ADM1_FR"]=="Artibonite"]
dessalines=sectionsgpd[sectionsgpd['ADM2_FR']=="Dessalines"]


select1 = Select(title='Departements', options=communesgpd["ADM1_FR"].cat.categories.tolist(), value='Artibonite')
select2 = Select(title='Communes', options=sectionsgpd[sectionsgpd['ADM1_FR']=="Artibonite"]['ADM2_FR'].cat.categories.tolist(), value="Dessalines")
indicators_list=["hop", "Dispensair","hop"]
select3=Select(title='Indicators', options=indicators_list, value='hop')


deptool=[("Nom","@ADM1_FR"),
                ("Population","@IHSI_UNFPA"),
                ("qte dispensaires","@Dispensair")
                ]
comtool=[("Nom","@ADM2_FR"),
                ("Population","@IHSI_UNFPA"),
                ("qte dispensaires","@Dispensair")
                ]
sectiontool=[("Nom","@ADM3_FR"),
                ("Population","@IHSI_UNFPA"),
                ("qte dispensaires","@Dispensair")
                ]


p1=plot_map(departementsgpd,column="hop",title=" Hopital par departement",tooltip=deptool )
"""
Try to uncomment lines 85,86, 98, 99, 102 to 104 you will get OverflowError: Maximum recursion level reached, can you help me with that
I need them because the user should e able to select departement, commune, etc
"""

p2=plot_map(artibonite,column="hop",title="Hop par com",tooltip=comtool )
p3=plot_map(dessalines,column="hop",title="Hop par section",tooltip=sectiontool )   

def dep_update(attr, old,new):
    data=getDataset(communesgpd, select1.value, "ADM1_FR")
    print(select1.value)
    p2.source=plot_map(data,column="hop",title=select1.value )

def com_update(attr, old,new):
    data=getDataset(sectionsgpd, new, "ADM2_FR")
    p3=plot_map(data,column="hop",title="Hop par com" )

    

select1.on_change('value', dep_update)
select2.on_change('value', com_update)

one=column(selectA)
two=column(select1, selectB)
#two=column(select1, p2)
three=column(select2,selectC)
#layout= row(one,two,three)
layout1=row(one, p1)
layout2=row(two, p2)
layout3=row(three,p3)
tab1=Panel(child=layout1,title="Country")
tab2=Panel(child=layout2,title="Departement")
tab3=Panel(child=layout3,title="Commune")
tabs = Tabs(tabs=[ tab1, tab2,tab3 ])
layout=column(tabs)
curdoc().add_root(layout)