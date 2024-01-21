A_op = random_unitary(2, seed=42)
A = A_op.to_instruction()
AT = A_op.transpose().to_instruction()
qc_list = []

# ENTER CODE BELOW
# Define the size of the state space
n = 2

# Create the Bell state |𝜙⁺⟩ = (|00⟩ + |11⟩)/sqrt(2)
phi_plus_circuit = QuantumCircuit(2)
phi_plus_circuit.h(0)
phi_plus_circuit.cx(0, 1)

# Circuit for (A ⊗ I)|𝜙⁺⟩ with reversed gate order
circuit_A_tensor_I = QuantumCircuit(2, 2)  # Add Classical Register for 2 bits
circuit_A_tensor_I = circuit_A_tensor_I.compose(phi_plus_circuit)
circuit_A_tensor_I.append(A, [0])
circuit_A_tensor_I.measure([0, 1], [0, 1])  # Measure qubits 0 and 1 to classical bits 0 and 1

# Circuit for (I ⊗ A†)|𝜙⁺⟩ with reversed gate order
circuit_I_tensor_AT = QuantumCircuit(2, 2)  # Add Classical Register for 2 bits
circuit_I_tensor_AT.append(AT, [1])
circuit_I_tensor_AT = phi_plus_circuit.compose(circuit_I_tensor_AT)
circuit_I_tensor_AT.measure([0, 1], [0, 1])  # Measure qubits 0 and 1 to classical bits 0 and 1

# Append the circuits to qc_list
qc_list.append(circuit_A_tensor_I)
qc_list.append(circuit_I_tensor_AT)
# ENTER CODE ABOVE
