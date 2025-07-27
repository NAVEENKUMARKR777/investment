import networkx as nx
import matplotlib.pyplot as plt

# Create directed graph
G = nx.DiGraph()

# Define nodes
proposers = ["P0", "P1"]
acceptors = ["A0", "A1", "A2"]
learners = ["L0", "L1"]

# Add nodes with roles
G.add_nodes_from(proposers, role="proposer")
G.add_nodes_from(acceptors, role="acceptor")
G.add_nodes_from(learners, role="learner")

# Proposal details
proposal_number = 1
proposal_value = "X"

# Add edges with labels
for p in proposers:
    for a in acceptors:
        G.add_edge(p, a, label=f"accept(n={proposal_number}, v={proposal_value})")

for a in acceptors:
    for l in learners:
        G.add_edge(a, l, label=f"learn(n={proposal_number}, v={proposal_value})")

# Improved manual layout with spacing
pos = {
    "P0": (-2, 3),
    "P1": (2, 3),
    "A0": (-3, 1.5),
    "A1": (0, 1.5),
    "A2": (3, 1.5),
    "L0": (-1.5, 0),
    "L1": (1.5, 0),
}

# Color roles
node_colors = []
for node in G.nodes(data=True):
    role = node[1]["role"]
    if role == "proposer":
        node_colors.append("lightblue")
    elif role == "acceptor":
        node_colors.append("lightgreen")
    elif role == "learner":
        node_colors.append("lightyellow")

# Draw diagram
plt.figure(figsize=(14, 8))
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500)
nx.draw_networkx_labels(G, pos, font_weight="bold", font_size=12)

# Edges with curved lines for clarity
nx.draw_networkx_edges(
    G, pos, arrows=True, arrowstyle='-|>', connectionstyle='arc3,rad=0.2'
)

# Add edge labels above curves
edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_size=9, label_pos=0.6
)

# Final touches
plt.title("Paxos Consensus Visualization – Clean & Readable", fontsize=16)
plt.axis("off")
plt.tight_layout()
plt.show()
