import math
import numpy as np
import pandas_datareader as pd
import networkx as nx
import matplotlib.pyplot as plt
from forex_python.converter import CurrencyRates


class Graph:

    def __init__(self, num, labels):
        self.vertices = num
        self.arches = []
        self.tickers = labels
        self.currency_matrix = np.zeros((num, num))

    def define_arches(self, s, e, v):  # s=start, e=end, v=value
        self.arches.append([s, e, v])

    # Building a matrix data structure and appending edges to graph
    def build_graph(self):
        c = CurrencyRates()
        for i in range(self.vertices):
            for j in range(self.vertices):
                if i == j:
                    # The diagonal is always equal to 1
                    data = 1
                else:
                    # Concatenating --> ex. "USDEUR=X"
                    aux = str(self.tickers[i] + self.tickers[j] + '=X')

                    # Live exchange rate in adj close column
                    # data = round(pd.get_data_yahoo(aux).iat[-1, -1], 5)
                    data = round(float(c.get_rate(
                        self.tickers[i], self.tickers[j])), 5)

                    print(aux, data)

                # Keeping track of exchange rates
                self.currency_matrix[i][j] = data
                self.define_arches(i, j, round(-math.log(data, 10), 5))

    def Bellman_Ford(self):

        # 1° Creating graph
        print('\nCollecting data, computing Bellman Ford algorithm, searching for arbitrage opportunity...')
        self.build_graph()

        # 2° Initializing distances between vertices
        dist = [float("Inf")] * self.vertices
        path = [float("Inf")] * self.vertices
        dist[0] = 0
        path[0] = 0
        profit = 1

        # 3° Relaxing all edges and checking for short distance with nested loops
        for _ in range(self.vertices - 1):
            for s, e, v in self.arches:
                if dist[s] != float("Inf") and dist[s] + v < dist[e]:
                    dist[e] = dist[s] + v
                    path[e] = s

        # 4° Detecting negative cycles
        Neg_cycles = self.Negative_Cycle(dist, path)

        # 5° Results, if there is a negative cycle --> computing possible profit
        if not Neg_cycles:
            print("\nNo arbitrage opportunity.")
            self.Display_Graph(path, 0, 0)

        else:

            for neg_cycle in Neg_cycles:
                print("\nFound negative cycle:")
                print('  ' + " --> ".join([self.tickers[i]
                                           for i in neg_cycle[::-1]]))
                prec = neg_cycle[-1]
                for i in neg_cycle[-2::-1]:
                    profit *= self.currency_matrix[prec][i]
                    prec = i
                profit = round(profit, 4)
                print("  Profit: ", profit)
                self.Display_Graph(neg_cycle, profit, 1)

    def Negative_Cycle(self, dist, path):
        Neg_cycles = []
        flag = False
        for s, e, v in self.arches:
            # Verifying distance after the algo has converged
            if dist[s] + v < dist[e] and dist[s] != float("Inf"):
                neg_cycle = [e, s]
                aux = s  # auxiliary variable

                while path[aux] not in neg_cycle:  # Going backwards in original path
                    neg_cycle.append(path[aux])
                    aux = path[aux]
                neg_cycle.append(path[aux])

                # Selecting valid cycle
                if neg_cycle[0] == neg_cycle[-1] and len(neg_cycle) > 3:
                    Neg_cycles.append(neg_cycle)
                    flag = True

        if(flag):
            return Neg_cycles
        else:
            return False

    def Display_Graph(self, path, profit, flag):

        path_edges = []
        graph_view = nx.MultiDiGraph()

        for s, e, v in self.arches:
            graph_view.add_edge(s, e, weight=round(10**(-v), 4))

        pos = nx.circular_layout(graph_view)

        if flag == 0:

            plt.title('NO Arbitrage Opportunity, NO Negative Cycle', fontsize=20)

        else:

            # Colouring the negative cycle
            for i in range(len(path)-1):
                path_edges.append((path[i+1], path[i]))

            plt.text(-1.3, -1.3, "Found Negative Cycle: \n\n" + '  ' + " --> ".join([self.tickers[i] for i in path[::-1]])
                     + "\n\nProfit: " + str(profit),
                     bbox=dict(boxstyle="square", facecolor="white"), size=12.5)
            plt.title('ARBITRAGE OPPORTUNITY', fontsize=20)

        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in graph_view.edges(data=True)])
        edge_colors = [
            'black' if not edge in path_edges else 'red' for edge in graph_view.edges()]
        node_colors = ['green' for path in graph_view.nodes()]

        labels = {}
        for i in range(len(self.tickers)):
            labels[i] = self.tickers[i]

        nx.draw_networkx_edge_labels(
            graph_view, pos, label_pos=0.28, edge_labels=edge_labels)
        nx.draw(graph_view, pos, node_size=1500, node_color=node_colors, edge_color=edge_colors, with_labels=False,
                connectionstyle='arc3, rad = 0.1')
        nx.draw_networkx_labels(graph_view, pos, labels,
                                font_size=16, font_color='black')

        plt.show()


if __name__ == "__main__":

    tickers = []

    print('Insert number of currencies: ')
    numV = int(input())

    print('Insert tickers of currencies (3-letter symbols): ')

    for x in range(numV):
        tickers.append(str(input()))

    g = Graph(numV, tickers)
    g.Bellman_Ford()
