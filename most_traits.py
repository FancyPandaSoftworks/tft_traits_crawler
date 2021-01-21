import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
import operator

###Load the datasets
champion_df = pd.read_csv('champion_traits_df.csv')
traits_df = pd.read_csv('traits_min_df.csv')


class GraphVisualization:

    def __init__(self):
        ###visual is a list which stores all
        ###the set of edges that constitutes a
        ###graph
        self.visual = []

        ###Create graph
        self.G = nx.Graph()

    ###edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    ###class Graph given by networkx G.add_edges_from(visual)
    ###creates a graph with a given list
    ###nx.draw_networkx(G) - plots the graph
    ###plt.show() - displays the graph
    def visualize(self):
        self.G.add_edges_from(self.visual)
        nx.draw_networkx(self.G)
        plt.show()


G = GraphVisualization()


def get_traits(champ_name):
    traits = champion_df[champion_df['champion'] == champ_name].iloc[:, 2:5].values.tolist()

    ###Flatten list
    traits = [item for sublist in traits for item in sublist]

    traits = [item for item in traits if str(item) != 'nan']
    return traits


for i in champion_df['champion'][champion_df['champ_cost'] > 3].values:
    traits = get_traits(i)

    ###Link all the corresponding champion
    linking_champions = champion_df['champion'][
        (champion_df['traits_1'].isin(traits) | champion_df['traits_2'].isin(traits) | champion_df['traits_3'].isin(traits))]
    for j in linking_champions:
        G.addEdge(i, j)

G.visualize()

###Get the shortest path of all the champions that are linked together
def find_paths(G,u,n):
    if n == 0:
        return [[u]]
    paths = [[u]+path for neighbor in G.neighbors(u) for path in find_paths(G, neighbor, n-1) if u not in path]
    return paths


all_paths = []
print('checking all path ... ')
for node in G.G:
    all_paths.extend(find_paths(G.G, node, 7))

print(len(all_paths))
###Get the traits of the paths
champ_traits = []
counter = 0
for pathing in all_paths:
    trait_counter = traits_df.iloc[:, 1:3]
    for champ in pathing:
        champ_trait = get_traits(champ)
        trait_counter['min_requirements'][trait_counter['traits'].isin(champ_trait)] = trait_counter['min_requirements'][trait_counter['traits'].isin(champ_trait)].subtract(1)
    path_trait = trait_counter['traits'][trait_counter['min_requirements'] <= 0].values.tolist()
    ###How many traits of the champ combination?
    traits_length = len(path_trait)

    ###Get the pathing, traits and number of traits in a list
    temp_trait_list = [pathing, path_trait, traits_length]
    champ_traits.append(temp_trait_list)
    counter += 1

champ_traits.sort(key=operator.itemgetter(2), reverse=True)
print(champ_traits[0:5])
