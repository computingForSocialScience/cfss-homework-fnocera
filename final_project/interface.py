''' Interface maker for interactive website for our networks

'''

from flask import Flask, render_template, request, redirect, url_for
import MySQLdb
import tempfile
import matplotlib.pyplot as plt
import pandas as pd
import random
from network_project import retreive_dicts
from network_project import make_network
from distribution_project import distribution_plot

""" Here I use a database on aws so I cannot put the login on github
"""
dbname="fnocera"
host="klab.c3se0dtaabmj.us-west-2.rds.amazonaws.com"
user=""
passwd=""
db=MySQLdb.connect(db=dbname, host=host, user=user,passwd=passwd)

app = Flask(__name__)

@app.route('/')
def make_index_resp():
    #This function renders templates/index.html when
    #someone goes to http://127.0.0.1:5000/
    #it offers the option of Nokia, Apple or Blackberry
    cur = db.cursor()
    get_companies = "SELECT DISTINCT company FROM dates_project;"
    cur.execute(get_companies)
    company_list = []
    for company in cur.fetchall():
        comp = company[0]
        company_list.append(comp)
    return(render_template('index.html', company_input=company_list))

@app.route('/company_info/<companyName>')
def get_info(companyName):
    #This function serves a page with company name, table of data, a link to the class network for that company
    #and also a graph of patent distribution given their classes.
    #It requires company.html to render and passes companyName, number_of_patents, classes_names and png_file to the template
    company_name=companyName
    dates_dict, classes_dict, class_list = retreive_dicts(company_name)
    patent_count, patentCounts, name_dict, bet_dict, eig_dict= make_network(dates_dict, classes_dict, companyName)
    distribution_plot(companyName, classes_dict, dates_dict)
    number_of_patents = sum(patent_count)
    patent_count_list = sorted(patentCounts.items(), key=lambda x: -x[1])
    top_patents = []
    for i in range(10):
        clas = patent_count_list[i][0]
        name = name_dict[str(clas)]
        name = name[0:50]
        no_patents = patent_count_list[i][1]
        bet = bet_dict[int(clas)]
        bet = round(bet, 3)
        eigen = eig_dict[int(clas)]
        eigen = round(eigen,3)
        tupl = (clas, name, no_patents, bet, eigen)
        top_patents.append(tupl)
    classes_names=top_patents
    png_file = companyName + ".png"
    return render_template('company.html',companyName=company_name, number_of_patents=number_of_patents, classes_names=classes_names, png_file=png_file)

@app.route('/network/<companyName>')
def network(companyName):
    #This function simply passes the file name to patents_graph.html and renders the page
    file_to_load = companyName + ".json"
    return render_template('patent_graph.html', file_to_load=file_to_load)


if __name__ == '__main__':
    app.debug=True
    app.run()
