def yoshida_kitaev_decoder(alice, U, Uconj):
    A = QuantumRegister(1, 'A')
    BH = QuantumRegister(2, 'BH')
    QM = QuantumRegister(2, 'QM')
    B = QuantumRegister(2, 'B')

    BSM = ClassicalRegister(2, 'BSM')
    T = ClassicalRegister(1, 'T')

    qc = QuantumCircuit(A, BH, QM, B, BSM, T)

    # ENTER CODE BELOW
    qc.append(alice.to_instruction(), [A[0]])
    qc.barrier()
      # Apply Bell State for BH_0 and QM_1
    qc.h(BH[0])
    qc.cx(BH[0], QM[1])

    # Apply Bell State for B_0 and B_1
    qc.h(B[0])
    qc.cx(B[0], B[1])

    # Apply Bell State for BH_1 and QM_0
    qc.h(BH[1])
    qc.cx(BH[1], QM[0])

    qc.barrier()

    # Scrambling_U for A, BH_0, BH_1
    qc.append(U.to_instruction(), [A[0], BH[0], BH[1]])

    # Scrambling_U* for QM_0, QM_1, B_0
    qc.append(Uconj.to_instruction(), [QM[0], QM[1], B[0]])

    qc.barrier()

    # Apply Bell Dagger for BH_1 and QM_0
    qc.cx(BH[1], QM[0])
    qc.h(BH[1])
    # ENTER CODE ABOVE

    return qc

qc_list = []
for alice in alice_states:
    qc = yoshida_kitaev_decoder(alice, bh, bh_conj)
    
    # measure decoded result
    qc.barrier()
    qc.measure(qc.qubits[-1], qc.clbits[-1])
    
    qc_list.append(qc)

qc_list[-1].draw(output='mpl')


def add_swap_test(alice, decoder):
    aux = QuantumRegister(2, 'aux')
    qc = decoder.copy()

    # ENTER CODE BELOW
    qc.add_register(aux)
    qc.barrier()
    # Apply Hadamard gate on the first ancilla 
    qc.h(aux[0])
    # Apply SWAP gate 
    qc.cswap(aux[0],0,5)
    # Apply Hadamard gate on the first ancilla 
    qc.h(aux[0])
    qc.barrier()
    qc.measure(aux[0], 2)
    # ENTER CODE ABOVE

    return qc


qc_list = []
for alice in alice_states:
    qc = yoshida_kitaev_decoder(alice, bh, bh_conj)
    qc = add_swap_test(alice, qc)
    qc_list.append(qc)

qc_list[-1].draw(output='mpl')

sampler = AerSampler()
result = sampler.run(circuits=qc_list).result()

post_select_dists = post_select_EPR(result)
plot_distribution(post_select_dists, legend=[f"$|{b}\\rangle$" for b in bases], title="SWAP test")
