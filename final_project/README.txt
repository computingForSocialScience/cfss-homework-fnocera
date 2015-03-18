
This is the README file for fnocera final project cfss Winter 2015

The final project is a little different from what was originally proposed. The project makes dynamic networks in d3 for three companies that are part of a case study I am undertaking for my thesis. 
The networks of Nokia, Apple and Blackberry need to be compared structurally to determine whether the competitive advantage of Apple over Nokia can be seen from patent data.
The networks produced are bipartite networks projected to 1D according to Breiger's Duality of persons and groups. In this network the classes are the nodes with an attribute reflecting the number of patents published by that company in that class. Edges are drawn between classes when a patent has co-presence of both categories within it. Therefore, the most commonly combined knowledge will be seen as not only central to the network but also more heavily tied together. It is an important project for the study of innovation networks. 

The networks seem to represent the knowledge within a company very well and we can see that Nokia's central patent is Telecommunications, while Apple is more focussed on Data Processing and Graphics. 

In the project there are 4 scripts
1) company_data.py which takes the data from the database for the three companies and then uploads it to tables (in a clean format to MySQL)
2) network_project.py actually creates the networks .json file with all its measures such as eigenvector centrality, betweenness etc 
3) distribution_project.py plots a bar chart as a .png for the company patents in their respective classes
4) interface.py creates an app where you can click to see data and the distribution plot for a given company, and then also the dynamic d3 network graph. 
