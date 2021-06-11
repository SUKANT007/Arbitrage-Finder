# Arbitrage Finder

Program that detects arbitrage opportunities in the foreign exchange market using Bellman-Ford algorithm.

Given as input a list of currencies, the program:

- Gathers currency pairs through forex-python and organizes them in a matrix data structure.
- Abstracts the exchange market creating a graph model with currency as nodes and exchange rates as edges.
- Finds negative cycles in the graph using Bellman-Ford algorithm, that correspond to an arbitrage opportunity.
- Computes the possible profit given by the concatenation of the negative cycle.
- Displays the graph with the negative cycle highlighted using the networkx library.

## Requirements

```bash
pip3 install numpy
pip3 install matplotlib.pyplot
pip3 install networkx
pip3 install pandas_datareader
pip3 install forex-python


```

## Screenshots

[![Graph.png](https://i.postimg.cc/J4G19XYR/Graph.png)](https://postimg.cc/VdPQtJch)
