import pandas as pd
iso_data=pd.read_csv("d://Desktop//forest1//ForestEagleEye//dataset//树木覆盖的全球位置//treecover_extent_2010_by_region__ha.csv").fillna(0)
iso_meta=pd.read_csv("d://Desktop//forest1//ForestEagleEye//dataset//树木覆盖的全球位置//iso_metadata.csv").fillna(0)
mergedata=pd.merge(iso_data,iso_meta,on='iso')
