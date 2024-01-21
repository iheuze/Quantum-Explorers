# Helper functions to draw and visualize graph solution

import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(G, colors, pos):
    default_axes = plt.axes(frameon=True)
    nx.draw_networkx(G, node_color=colors, node_size=600, alpha=0.8, ax=default_axes, pos=pos, node_shape="o")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    
def draw_tsp_solution(G, order, colors, pos):
    G2 = nx.DiGraph()
    G2.add_nodes_from(G)
    n = len(order)
    for i in range(n):
        j = (i + 1) % n
        G2.add_edge(order[i], order[j], weight=G[order[i]][order[j]]["weight"])
    default_axes = plt.axes(frameon=True)
    nx.draw_networkx(
        G2, node_color=colors, edge_color="b", node_size=600, alpha=0.8, ax=default_axes, pos=pos
    )
    edge_labels = nx.get_edge_attributes(G2, "weight")
    nx.draw_networkx_edge_labels(G2, pos, font_color="b", edge_labels=edge_labels)

from qiskit_optimization.applications import Tsp

tsp = Tsp.create_random_instance(4, seed=43)
adj_matrix = nx.to_numpy_array(tsp.graph)
print("distance\n", adj_matrix)

colors = ["r"] * len(tsp.graph.nodes)
pos = [tsp.graph.nodes[node]["pos"] for node in tsp.graph.nodes]
draw_graph(tsp.graph, colors, pos)

from qiskit_optimization.converters import QuadraticProgramToQubo

qp = tsp.to_quadratic_program()
qp2qubo = QuadraticProgramToQubo()  # instatiate qp to qubo class
qubo = qp2qubo.convert(qp)  # convert quadratic program to qubo
qubitOp, offset = qubo.to_ising()  # convert qubo to ising

from qiskit.algorithms.minimum_eigensolvers import SamplingVQE
from qiskit.algorithms.optimizers import NFT
from qiskit.circuit.library import TwoLocal
from qiskit_aer.primitives import Sampler as AerSampler
from qiskit.utils import algorithm_globals
algorithm_globals.random_seed = 123

optimizer = NFT(maxiter=100)
ry = TwoLocal(qubitOp.num_qubits, "ry", "cz", reps=2, entanglement="linear")

####### build your code below #########

vqe = SamplingVQE(ansatz=ry,
                  optimizer=optimizer,
                  sampler=AerSampler())

####### build your code above #########

result = vqe.compute_minimum_eigenvalue(qubitOp)

print("energy:", result.eigenvalue.real)
print("time:", result.optimizer_time)
x = tsp.sample_most_likely(result.eigenstate)
print("feasible:", qubo.is_feasible(x))
z = tsp.interpret(x)
print("solution:", z)
print("solution objective:", tsp.tsp_value(z, adj_matrix))
draw_tsp_solution(tsp.graph, z, colors, pos)
