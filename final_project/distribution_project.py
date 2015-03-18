''' Get distribution of patents in their respective classes, that account for more than 1 percent of the company's patents
file is saved as a .png in static folder so that it can be loaded into interface.py
'''

import operator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def distribution_plot(company_name, nokia_class_dict,nokia_dates_dict):

	class_list = []
	for key in nokia_class_dict:
		values = nokia_class_dict[key]
		for i in range(len(values)):
			value = values[i]
			tupl = (key,value)
			class_list.append(tupl)

	nokia_class_df = pd.DataFrame(class_list, columns=['patent_id', 'class'])
	nokia_dates_df = pd.DataFrame.from_dict(nokia_dates_dict, orient='index', dtype=None)
	nokia_dates_df.columns = ['year']

	nokia = pd.merge(nokia_dates_df, nokia_class_df, how='left', left_on=nokia_dates_df.index.unique(), right_on="patent_id", sort=True)
	pivot_nokia = nokia.pivot_table(values='patent_id', index='class', columns='year',aggfunc = lambda x: len(x.dropna().value_counts()))
	pivot_nokia.sort_index(inplace=True)
	nokia_norm = pivot_nokia/pivot_nokia.sum().astype(np.float64)

	nokia_graph = nokia_norm.ix[:,'1990':'2008'].mean(axis=1)

	plt.figure()
	graph = nokia_graph[nokia_graph>0.01].plot(kind='bar')
	graph.set_title("Percentage of Patents by Class Number")
	#plt.show()

	static = 'static'
	if not os.path.exists(static):
		os.makedirs(static)

	filename = "static/" + company_name + ".png"
	if os.path.exists("/static/file_name"):
		os.remove("/static/file_name")

	plt.savefig(filename)

