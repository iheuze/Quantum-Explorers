def cost_function(theta, hst, sampler):
    # calculate the cost of Hilbert-Schmidt test based on the parameters theta
    qc = hst.assign_parameters(theta)
    result = sampler.run(qc).result()
    
    try:
        print('Hilbert-Schmidt distance:', result.quasi_dists[0][0], 'cost:', 1-result.quasi_dists[0][0])
        return 1-result.quasi_dists[0][0]
    except KeyError:
        return 1
    
def param_shift_gradient(theta, qc, sampler, theta_index=None):
    grad = []

    shifted_theta_list = []
    if theta_index is None:
        theta_index = range(len(theta))
    for i in theta_index:
        _theta = theta.copy()
        _theta[i] += np.pi/2
        shifted_theta_list.append(_theta)

        _theta = theta.copy()
        _theta[i] -= np.pi/2
        shifted_theta_list.append(_theta)

    result = sampler.run([qc]*len(shifted_theta_list), 
                         shifted_theta_list).result()

    for i in theta_index:
        grad_param = 0
        if 0 in result.quasi_dists[2*i].keys():
            grad_param += 0.5*result.quasi_dists[2*i][0]
        if 0 in result.quasi_dists[2*i+1].keys():
            grad_param -= 0.5*result.quasi_dists[2*i+1][0]
        grad.append(grad_param)

    return grad

from qiskit.circuit.library import TwoLocal
from qiskit import QuantumCircuit
import numpy as np
from scipy.optimize import minimize
# ENTER CODE BELOW
ansatz = TwoLocal(3, ['ry','rz'], 'cz', 'full', reps=5) 
# ENTER CODE ABOVE
ansatz.draw('mpl')

# ENTER CODE BELOW
# Define relevant variables
theta_initial = np.random.uniform(-np.pi, np.pi, ansatz.num_parameters)
hst_circuit = hilbert_schmidt_test(bh, ansatz)
sampler = Sampler()

# Optimize the parameters with scipy.optimize.minimize
opt_result = minimize(cost_function, theta_initial, args=(hst_circuit, sampler), method='COBYLA', options={'maxiter': 3000})

# ENTER CODE ABOVE
assert opt_result.success and opt_result.fun < 1e-6

# Assign optimized parameters to the ansatz
bh_conj = ansatz.assign_parameters(opt_result.x)
bh_conj.name = 'scrambing_U^*' 
