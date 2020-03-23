# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 12:13:34 2020

@author: admin
"""

from os.path import dirname, join
import geopandas as gpd
import pandas as pd
import h5py

#Read geographical data
sectionsgpd=gpd.read_file(join(dirname(__file__),"data","adm","hti_admbnda_adm3_cnigs_20181129.shp"))
communesgpd=gpd.read_file(join(dirname(__file__),"data","adm","hti_admbnda_adm2_cnigs_20181129.shp"))
departementsgpd=gpd.read_file(join(dirname(__file__),"data","adm","hti_admbnda_adm1_cnigs_20181129.shp"))
sections_population=pd.read_excel(join(dirname(__file__),"data","population","hti_adminboundaries_tabulardata.xlsx"),sheet_name="hti_pop2019_adm3", index_col=["adm3code"])
communes_population=pd.read_excel(join(dirname(__file__),"data","population","hti_adminboundaries_tabulardata.xlsx"),sheet_name="hti_pop2019_adm2", index_col=["adm2code"])
departements_population=pd.read_excel(join(dirname(__file__),"data","population","hti_adminboundaries_tabulardata.xlsx"),sheet_name="hti_pop2019_adm1", index_col=["adm1code"])
#create hdf5 file
hf = h5py.File('data.h5', 'w')
sectionsgpd.to_hdf(join(dirname(__file__),"data.h5"),  key='sections', mode='w')
communesgpd.to_hdf(join(dirname(__file__),"data.h5"), key='communes', mode='w')
departementsgpd.to_hdf(join(dirname(__file__),"data.h5"), key='departements', mode='w')
