# Do not edit this code. Use this circuit in your answers.
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)
qc.x(1)
qc.cx(0,1)
qc.measure_all()
qc.draw()

from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options, Sampler
from qiskit.providers.fake_provider import FakeManila
from qiskit_aer.noise import NoiseModel

# Save the Runtime account credentials if you have not done so already
# If you need to overwrite the account info, please add `overwrite=True`
# QiskitRuntimeService.save_account(channel='ibm_quantum', token='my_token', overwrite=True)

service = QiskitRuntimeService(channel='ibm_quantum')
backend = service.get_backend('ibmq_qasm_simulator')
print(backend)

# Obtaining the noise model we will apply to the backend we obtained above
fake_backend = FakeManila()
noise_model = NoiseModel.from_backend(fake_backend)

# Use this when defining the simulator in your options instances
sim = {
    "noise_model": noise_model,
    "seed_simulator": 42, # Do not change this value. Doing so may result in your answer being marked as incorrect.
}

####### build your code below #########

options = Options(resilience_level=0) # options with no error mitigation
options.simulator = {
    "noise_model": noise_model,
    "seed_simulator": 42
}

options_with_m3 =  Options(resilience_level=1) # options with M3 error mitigation
options_with_m3.simulator = {
    "noise_model": noise_model,
    "seed_simulator": 42
}

with Session(service=service, backend=backend):
    # no error mitigation
    sampler = Sampler(options=options)
    job = sampler.run(qc)
    results_no_em = job.result()
    quasi_dist_no_em = results_no_em.quasi_dists[0]
    
    # apply M3 error mitigation
    sampler = Sampler(options=options_with_m3)
    job = sampler.run(qc)
    results_with_m3 = job.result()
    quasi_dist_with_m3 = results_with_m3.quasi_dists[0]

####### build your code above #########

print("Running your session, please be patient...")
print(f"Quasi-distribution with no error mitigation: {quasi_dist_no_em}")
print(f"Quasi-distribution with error mitigation: {quasi_dist_with_m3}")

# Visualize your results

from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram

# Convert integers to binary strings 
binary_prob_dist_no_em = quasi_dist_no_em.binary_probabilities()
binary_prob_dist_with_m3 = quasi_dist_with_m3.binary_probabilities()

# Theoretical results
qc.remove_final_measurements()
theory_probabilities = Statevector(qc).probabilities_dict()
qc.measure_all()

# Plot all the results
legends = ["No error mitigation", "Error mitigation applied", "Theory"]
plot_histogram([binary_prob_dist_no_em, binary_prob_dist_with_m3, theory_probabilities], legend=legends)
