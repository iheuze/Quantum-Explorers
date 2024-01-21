def post_select_EPR(result):
    # ENTER CODE BELOW
    post_select_dists = []
    for dist in result.quasi_dists:
        post_select_dists.append({'0': 0, '1': 0})
        for k, v in dist.items():
            # check the (last qubit) first index 
            if f"{k:03b}"[2] == '0':
                if f"{k:03b}"[1:] == '00' or f"{k:03b}"[1:] == '11': 
                    post_select_dists[-1]['0'] += v 
                else:
                    post_select_dists[-1]['1'] += v 

    #ENTER CODE ABOVE

    #returns a list of dictionary in the same format as result.quasi_dists
    return post_select_dists 

def post_select_EPR(result):
    # ENTER CODE BELOW
    post_select_dists = []

    for dist in result.quasi_dists:
        post_select_dists.append({'0': 0, '1': 0})
        total_counts = 0

        for k, v in dist.items():
            # Check if qubits 2 and 3 are in the initial state '00'
            if f"{k:03b}"[1] == '0'and f"{k:03b}"[2] == '0':
                # Increment counts based on the state of qubit 0
                if f"{k:03b}"[0] == '0':
                    post_select_dists[-1]['0'] += v
                    total_counts += v
                else:
                    post_select_dists[-1]['1'] += v
                    total_counts += v

    print(post_select_dists)
    for dic in post_select_dists:
        for key in dic:
            dic[key] = dic[key]/total_counts
    
    print(post_select_dists[-1].items())
    return post_select_dists
    # ENTER CODE ABOVE

    # returns a list of dictionary in the same format as result.quasi_dists

post_select_dists = post_select_EPR(result)

plot_distribution(post_select_dists)
