import py4cytoscape as p4c
p4c.cytoscape_ping()
p4c.cytoscape_version_info()
import pandas as pd
import json
from pprint import pprint

with open('visualizable_data.json', 'r') as f:
    data = json.load(f)

nodes_data = {}
nodes_data['id'] = []
nodes_data['group'] = []
edges_data = {}
edges_data['source'] = []
edges_data['target'] = []
for node in data['nodes']:
    nodes_data['id'].append(node['name'])
    nodes_data['group'].append(node['name'].rsplit('-')[0])
for link in data['links']:
    edges_data['source'].append(link['source'])
    edges_data['target'].append(link['target'])


nodes = pd.DataFrame(nodes_data)
edges = pd.DataFrame(edges_data)

p4c.create_network_from_data_frames(nodes, edges, title="my first network", collection="DataFrame Example")
p4c.cybrowser_show()