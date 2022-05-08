import pandas as pd
import spicy
import networkx as nx
import matplotlib.pyplot as plt

# Change the path to csv file that stores the Sentiment Analysis of followers' tweets about M1
# Read in csv the data
tweetsResult = pd.read_csv('./All_M1_Tweets_Results.csv')

# Number of followers' tweets about M1
print("Number of followers' tweets about M1 ", tweetsResult.shape[0])

# tweetsResult.columns:
# ['Unnamed: 0', 'text', 'polarity', 'user_id', 'user_name']

# Mapping the user_id to an opinion
follower_ids = tweetsResult['user_id']
follower_opinions = tweetsResult['polarity']
ids_ops = dict(zip(follower_ids, follower_opinions))


neg_count = 0
pos_count = 0

for op in follower_opinions:
    if op == 'negative':
        neg_count = neg_count + 1
    elif op == 'positive':
        pos_count = pos_count + 1

print("Number of influencer's followers holding positive opinion toward M1", pos_count)
print("Number of influencer's followers holding negative opinion toward M1", neg_count)


# Initialize this with the uer_id of the influencer
influencer = 0

# Plot a graph
G = nx.Graph()
G.add_edges_from([(follower, influencer) for follower in follower_ids])
color_map = []


for node in G:
    if node == 0:
        color_map.append('blue')
    else:
        if ids_ops[node] == 'negative':
            color_map.append('red')
        elif ids_ops[node] == 'positive':
            color_map.append('green')


nx.draw(G, node_color=color_map, with_labels=False)
plt.show()