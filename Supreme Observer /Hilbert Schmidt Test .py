def hilbert_schmidt_test(U, Vconj):
    assert U.num_qubits == Vconj.num_qubits

    # ENTER CODE BELOW
    num_qubits = U.num_qubits

    # Construct Hilbert-Schmidt Test circuit
    qr = QuantumRegister(num_qubits * 2)
    cr = ClassicalRegister(num_qubits * 2)
    A = [qr[i] for i in range(num_qubits)]
    B = [qr[i] for i in range(num_qubits, num_qubits * 2)]

    qc = QuantumCircuit(qr, cr, name="HST")
    qc.h(A)
    qc.cx(A, B)
    qc.append(U, A)
    qc.append(Vconj, B)
    qc.cx(A, B)
    qc.h(A)
    qc.measure(qr, cr)
   
    # ENTER CODE ABOVE

    return qc

qc = hilbert_schmidt_test(bh, bh)
qc.draw('mpl')
