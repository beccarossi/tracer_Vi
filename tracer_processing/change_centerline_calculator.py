# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 13:06:58 2020

@author: Rebecca Rossi
"""

import fiona
from shapely.geometry import shape
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import LineString
from shapely.ops import nearest_points
import numpy as np

df = pd.read_excel(r"F:\PhD_research\ROSSI_compiled_PEL_tracer_distances.xlsx")

old_line = r"F:\Radio_Rocks_Matlab_RYAN\plot_in_Q\PEL_centerline_line.shp"
new_line = r"F:\PhD_research\amethyst_brook_hecras_calib1\gis\river4.shp"
old_points = r"F:\PhD_research\GIS\change_centerline\Dietrich_centerline_pts.shp"
new_points = r"F:\PhD_research\GIS\change_centerline\hecras_centerline_pts2.shp"


gdf = gpd.read_file(new_points)
a = gdf.geometry.unary_union



ls_new = LineString(a)

old_shp = fiona.open(old_line)
first = old_shp.next()
old_geom = shape(first['geometry'])

old_points = fiona.open(old_points)

new_shp = fiona.open(new_line)
first = new_shp.next()
new_geom = shape(first['geometry'])


df.columns = df.columns.astype(str)
#160308_161117 calculations
tmp = df[['160308_161117']].dropna()
tmp.loc[:,'Distance_160308_161117'] = tmp.apply(lambda x: ls_new.length*(1-ls_new.project(nearest_points( old_geom.interpolate(x),a)[0], normalized=True)), axis=1)

#151211 calculations
tmp1 = df[['151211']].dropna()
tmp1.loc[:,'Distance_151211'] = tmp1.apply(lambda x: ls_new.length*(1-ls_new.project(nearest_points( old_geom.interpolate(x),a)[0], normalized=True)), axis=1)


dist = np.round(df.loc[1,'160308_161117'],1)




#merge calculated values back to df
df = df.merge(tmp[['Distance_160308_161117']], left_index=True, right_index=True)
df = df.merge(tmp1[['Distance_151211']], left_index=True, right_index=True)
df = df.drop('151211_cor', axis=1)
df = df.drop('160308_161117_cor', axis=1)

df.to_excel(r"F:\PhD_research\GIS\change_centerline\new_centerline_disances_tabulated.xlsx", index=False)




