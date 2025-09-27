
import os
import networkx as nx
import matplotlib.pyplot as plt

def visualize_topology(topo, outfile="output/topology.png"):
    """
    Draws routers and links (and optional LAN stubs) using networkx + matplotlib.
    """
    G = nx.Graph()

    # Add router nodes
    for rname in topo["routers"].keys():
        G.add_node(rname, type="router")

    # Add links between routers
    for link in topo["links"]:
        ep = link["endpoints"]
        a = ep[0]["router"]
        b = ep[1]["router"]
        label = link["subnet"]
        if G.has_edge(a, b):
            # If multiple subnets between same pair, append label
            G[a][b]["label"] += f" | {label}"
        else:
            G.add_edge(a, b, label=label)

    # Add LAN nodes as clouds
    for lan in topo["lans"]:
        lan_node = f"LAN:{lan['subnet']}"
        G.add_node(lan_node, type="lan")
        G.add_edge(lan["router"], lan_node)

    pos = nx.spring_layout(G, seed=42)  # deterministic layout
    router_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "router"]
    lan_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "lan"]

    plt.figure(figsize=(10, 7))

    nx.draw_networkx_nodes(G, pos, nodelist=router_nodes, node_shape='s', node_size=1800)
    nx.draw_networkx_labels(G, pos, labels={n:n for n in router_nodes})

    if lan_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=lan_nodes, node_shape='o', node_size=1000)
        nx.draw_networkx_labels(G, pos, labels={n:n.replace('LAN:', '') for n in lan_nodes})

    nx.draw_networkx_edges(G, pos)
    # Draw edge labels (subnets)
    edge_labels = {(u, v): d.get("label","") for u, v, d in G.edges(data=True) if d.get("label")}
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    plt.tight_layout()
    plt.savefig(outfile)
    plt.close()
