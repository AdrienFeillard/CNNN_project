import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

############################################ Exercice 0 ############################################
def generate_balanced_random_patterns(N, M):
    return np.array(np.random.choice([-1, 1], (M, N)),dtype=float)


def update_state(S, W, beta=4):
    h = np.dot(W, S)
    return (np.tanh(beta * h))

#Ex 0.2
def flip_bits(pattern, c):
    flip_indices = np.random.choice(len(pattern), size=int(len(pattern) * c), replace=False)
    pattern_flipped = pattern.copy()
    pattern_flipped[flip_indices] *= -1
    
    return pattern_flipped


def compute_overlap(state, patterns):
    return np.dot(patterns, state) / len(state)

def run_standard_hopfield_network(N, M, T):
    patterns = generate_balanced_random_patterns(N, M)
    W = 1/N * np.dot(patterns.T, patterns)
 
    # Set initial state close to the first pattern
    initial_state = flip_bits(patterns[0], c=0.05)
    # Let the network evolve
    state = initial_state
    for t in range(T):  # Simulate for 20 time steps
            state = update_state(state, W)
            overlaps = compute_overlap(state, patterns)
            #print(f"Time step {t}, Overlaps: {overlaps}")
    
    return state, patterns

def plot_standard_hopfield_network_results(M, state, patterns):
    fig, ax = plt.subplots(nrows=M, ncols=2, figsize=(5, 5))
    # Display the original pattern
    for i in range(M):
        ax[i, 0].imshow(patterns[i].reshape(10, 10), cmap='binary', vmin=-1, vmax=1)
        ax[i, 0].set_title(f'Original Pattern {i+1}')
        ax[i, 0].axis('off')  # Hide grid lines and ticks for clarity
        # Display the retrieved pattern
        ax[i, 1].imshow(state.reshape(10, 10), cmap='binary', vmin=-1, vmax=1)
        ax[i, 1].set_title(f'Retrieved Pattern {i+1}')
        ax[i, 1].axis('off')  # Hide grid lines and ticks for clarity
    plt.suptitle("Comparison of Original and Retrieved Patterns")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("Ex0.2_pattern_retrieval.png", )
    plt.show()


#################################### Exercice 1 #######################################
##############################################Ex1.1

def update_state_with_overlaps(state,patterns,N, beta=4):
    #h = np.zeros_like(S, dtype=float)
    #for i in range(N):
        #h[i] = np.sum(m * patterns[:, i])
    m= np.dot(patterns, state) / N
    h=np.dot(m,patterns)
    
    return np.tanh(beta * h)

def run_standard_hopfield_network_with_overlaps(N, M, T):
    patterns = generate_balanced_random_patterns(N, M)
    

    #W = 1/N * np.dot(patterns.T, patterns)
    # Set initial state close to the first pattern
    initial_state = flip_bits(patterns[0], c=0.05)
    # Let the network evolve
    state = initial_state
    
    for t in range(T):  # Simulate for 20 time steps
        state = update_state_with_overlaps(state,patterns,N,beta=4)


    return state, patterns


#################################################Ex1.2
def hamming_distance(P1, P2):
    return (len(P1) - np.dot(P1, P2)) / (2 * len(P1))

################################################Ex1.3

def run_standard_hopfield_network_with_hamming_distance(N,M,T):
    patterns = generate_balanced_random_patterns(N, M)
    patterns =np.array(patterns,dtype=float)
    initial_state = flip_bits(patterns[0], c=0.15)
    state = initial_state
    distances = []


  
    # Simulate the network
    for t in range(T):
        
        state = update_state_with_overlaps(state,patterns,N)  # Example overlap
        print(state)
        distances.append([hamming_distance(state, p) for p in patterns])
        overlaps = compute_overlap(state, patterns)
        print(f"Time step {t}, Overlaps: {overlaps}")
    
    return np.array(distances,dtype=float), state, patterns

def plot_patterns_state_comparison_hamming_distances(distances,M, state,patterns):

    fig, ax = plt.subplots(nrows=M, ncols=2, figsize=(12, 12))
    
    for i in range(M):
        # Display the original pattern
        ax[i, 0].imshow(patterns[i].reshape(15, 20), cmap='binary', vmin=-1, vmax=1)
        ax[i, 0].set_title(f'Original Pattern {i+1}')
        ax[i, 0].axis('off')  # Hide grid lines and ticks for clarity
    
        # Display the retrieved pattern (assuming final state resembles the first pattern)
        ax[i, 1].imshow(state.reshape(15, 20), cmap='binary', vmin=-1, vmax=1)
        ax[i, 1].set_title(f'Retrieved Pattern {i+1}')
        ax[i, 1].axis('off')  # Hide grid lines and ticks for clarity
    
    # Add a super title and show the plot for patterns
    plt.suptitle('Comparison of Original and Retrieved Patterns')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
    
    # Plot Hamming distances
    plt.figure(figsize=(10, 5))
    for i in range(M):
        plt.plot(distances[:, i], label=f'Pattern {i+1}')
    plt.xlabel('Time step')
    plt.ylabel('Hamming distance')
    plt.title('Evolution of Hamming Distances Over Time')
    plt.legend()
    plt.show()

##############################################Ex1.4
def pattern_retrieval_error_and_count(patterns, N, T=50, beta=4):
    retrieval_errors = []
    retrieval_counts = []
    for pattern in patterns:
        initial_state = flip_bits(pattern, c=0.05)
        state = initial_state
        
        for t in range(T):
            state = update_state_with_overlaps(state,patterns, beta)
        retrieval_errors.append(hamming_distance(pattern, state))
        retrieval_counts.append(hamming_distance(pattern, state) <= 0.05)
    return np.mean(retrieval_errors), np.std(retrieval_errors), np.sum(retrieval_counts)

# Run simulations for different dictionary initializations
def run_simulation_dictionary(M, N=300, iterations=5,beta=4):
    mean_errors = []
    std_errors = []
    pattern_counts = []
    for _ in range(iterations):
        patterns = generate_balanced_random_patterns(N, M)
        mean_error, std_error, count = pattern_retrieval_error_and_count(patterns, N, beta=beta)
        mean_errors.append(mean_error)
        std_errors.append(std_error)
        pattern_counts.append(count)
    return np.mean(mean_errors), np.mean(std_errors), np.mean(pattern_counts)

#####################################Ex1.7
def capacity_study(N_values, loading_values, trials=10):
    """Study the capacity of Hopfield networks across different sizes and loadings."""
    results = {N: [] for N in N_values}

    for N in N_values:
        print(N)
        for L in loading_values:
            M = int(L * N)
            retrieval_rates = [run_simulation_dictionary(M, N) for _ in range(trials)]
            mean_retrieval_rate = np.mean(retrieval_rates)
            std_retrieval_rate = np.std(retrieval_rates)
            results[N].append((mean_retrieval_rate, std_retrieval_rate))

    # Plotting the results
    plt.figure(figsize=(10, 8))
    for N in N_values:
        means, stds = zip(*results[N])
        plt.errorbar(loading_values, means, yerr=stds, label=f'N={N}')

    plt.xlabel('Loading L = M/N')
    plt.ylabel('Average Retrieved Patterns / N')
    plt.title('Network Capacity vs Network Size')
    plt.legend()
    plt.grid(True)
    plt.show()

##########################################Ex1.8

def plot_beta_impact(N, M, beta_values):
    """ Plot the impact of beta on network retrieval capacity. """
    
    retrieval_rates = [run_simulation_dictionary(N, M, beta=beta) for beta in beta_values]

    plt.figure(figsize=(8, 5))
    plt.plot(beta_values, retrieval_rates, marker='o')
    plt.xlabel('Inverse Temperature Beta')
    plt.ylabel('Retrieval Rate')
    plt.title('Impact of Beta on Memory Retrieval')
    plt.grid(True)
    plt.show()


############################################# Exercice 2 ##############################################
#########################################Ex2.2
def generate_low_activity_patterns(N, M, activity):
    """
    Generate M low-activity patterns with N neurons each,
    where each neuron has a probability 'activity' of being 1.
    """
    return np.random.choice([0, 1], (M, N), p=[1-activity, activity]).astype(float)
def compute_weight_matrix(pattern,N,a,b):
    pattern_a=pattern-np.full((pattern.shape),a)
    pattern_b=pattern-np.full((pattern.shape),b)
    
    c= 2/(a*(1-a))
    
    return c/N* np.dot(pattern_b.T, pattern_a)
"""
def hamming_distance_(P, Q):
    
    Compute the Hamming distance between two patterns.
    
    return np.sum(P != Q) / len(P)
"""

def stochastic_spike_variable(S):
    """
    Generate a stochastic spike variable for each neuron based on its state S.
    Probability is derived from the neuron's continuous value.
    """
    return np.random.binomial(1, 0.5 * (S + 1))

def compute_overlaps(patterns, S, a):
    """
    Compute the overlaps m_mu for each pattern.
    """
    overlaps= np.dot((patterns-np.full((patterns.shape),a)),S)
   
    return overlaps

def update_states_with_overlaps(patterns, overlaps,theta, beta,b):
    """
    Update the states of the network based on overlaps and pattern influence.
    """
    H= np.dot(overlaps,(patterns-np.full((patterns.shape),b))) 
    H-=theta
    return np.tanh(beta * H)

def run_simulation_low_activity(N, M, a, b, theta_values, beta, T, c=2):
    """
    Run the simulation for multiple theta values and plot the retrieval accuracy.
    """
    patterns = generate_low_activity_patterns(N, M, a)
    initial_state = patterns[0].copy()  # Initialize the state close to the first pattern
    hamming_distances = []
    for theta in theta_values:
            S = initial_state.copy()
            for t in range(T):
                overlaps = compute_overlaps(patterns, S, a)
                S = update_states_with_overlaps(patterns, overlaps,theta, beta,b)
                S = np.array([stochastic_spike_variable(si) for si in S])
            # Evaluate performance after the last update
            distances = [hamming_distance(S, p) for p in patterns]
            mean_distance = np.mean(distances)
            hamming_distances.append(mean_distance)

    return theta_values, hamming_distances


##########################################Ex2.3
def run_simulation_and_plot(N, M_values, a, b, theta_values, beta, T, c=2):
    """
    Run the simulation for multiple theta values and plot the retrieval accuracy.
    """
    retrieval_rates = np.zeros((len(M_values), len(theta_values)))

    for i, M in enumerate(M_values):
        print(M)
        patterns = generate_low_activity_patterns(N, M, a)

        for j, theta in enumerate(theta_values):
            retrieval_count=0
            for pattern in patterns:
                # Initialize the state close to the pattern with some bits flipped
                initial_state = pattern.copy()
                initial_state = flip_bits(initial_state,0.05)  # Flip the bits
                S = initial_state.copy()
                for _ in range(T):
                    overlaps = compute_overlaps(patterns, S, a)
                    S = update_states_with_overlaps(patterns, overlaps, theta, beta, b)
                    S = np.array([stochastic_spike_variable(si) for si in S])
                # Evaluate performance after the last update
                if hamming_distance(S, pattern) <= 0.05:
                    retrieval_count += 1
    
            retrieval_rate = retrieval_count / M
            retrieval_rates[i, j] = retrieval_rate

    # Plotting the results
    plt.figure(figsize=(10, 8))
    for j, theta in enumerate(theta_values):
        plt.plot(M_values, retrieval_rates[:, j], label=f'Theta = {theta:.2f}', marker='o')

    plt.xlabel('Number of Patterns (M)')
    plt.ylabel('Retrieval Rate (Fraction of Patterns Retrieved)')
    plt.title('Network Capacity vs Number of Patterns and Theta')
    plt.legend()
    plt.grid(True)
    plt.show()

#Ex2.6

def simulate_capacity(N, M, activity, theta, beta=4, iterations=100):
    patterns = generate_low_activity_patterns(N, M, activity)
    retrieved_patterns = 0

    for _ in range(iterations):
        initial_state = np.random.choice([0, 1], N, p=[1-activity, activity])
        state = initial_state

        for t in range(20):  # Run for a certain number of time steps
            overlaps= compute_overlaps(patterns, state, activity)
            state = update_states_with_overlaps(patterns,overlaps,[theta], beta,activity)

        # Check if the first pattern is retrieved
        if hamming_distance(state, patterns[0]) <= 0.05:
            retrieved_patterns += 1

    return retrieved_patterns / iterations


###################################################### Exercice 3 ################################################################