from qiskit import QuantumCircuit
from qiskit.visualization import plot_state_qsphere
from qiskit.quantum_info import Statevector

####### build your code below #########

circuit =  QuantumCircuit(4)
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(0, 2) 
circuit.cx(0, 3)
circuit.x(1)
 
state = Statevector(circuit)
plot_state_qsphere(state)


####### build your code above #########

display(plot_state_qsphere(circuit))
display(circuit.draw('mpl'))
