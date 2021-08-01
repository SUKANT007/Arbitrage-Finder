import ForexArbitrage

# v1 = 5
# # Major Currency Pairs (Us Dollar, Euro, Pound Sterling, Swiss Franc, Canadian Dollar)
# tickers1 = ['USD', 'EUR', 'GBP', 'CHF', 'CAD']

# g = ForexArbitrage.Graph(v1, tickers1)
# g.Bellman_Ford()

# v2 = 4
# # Exotic Currency Pairs (Turkish Lira, Mexican Peso, Hungarian Forint, Thai Baht)
# tickers2 = ['TRY', 'MXN', 'HUF', 'THB']

# g = ForexArbitrage.Graph(v2, tickers2)
# g.Bellman_Ford()

v3 = 6
tickers3 = ['EUR', 'USD', 'HUF', 'MXN', 'TRY', 'CAD']   # Mixed Currencies

g = ForexArbitrage.Graph(v3, tickers3)
g.Bellman_Ford()


# v4 = 9
# tickers4 = ['EUR', 'AUD', 'USD', 'CNY', 'NZD', 'HUF', 'MXN', 'CAD', 'TRY']
# g = ForexArbitrage.Graph(v4, tickers4)
# g.Bellman_Ford()
