dm = DensityMatrix.from_instruction(bh)

# ENTER CODE BELOW
bh_hr_purity = dm.purity()
# Number of qubits in the black hole subsystem
num_black_hole_qubits = 1  # Adjust this based on your system

# Partial trace to obtain the density matrix of the Hawking radiation subsystem
hr_density_matrix = partial_trace(dm, range(num_black_hole_qubits, dm.num_qubits))

hr_purity = hr_purity = hr_density_matrix.purity()
# ENTER CODE ABOVE

print(f"Purity of the whole system: {bh_hr_purity:.3f}")
print(f"Purity of the Hawking radiation subsystem: {hr_purity:.3f}")
