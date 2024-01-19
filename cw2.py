"""
Coursework 2 for COMP.SEC.220:
Security Protocols - Helping Alice and Bob to share secrets

Author: Paavo Peltopihko
Studentnumber: XXXXXX
Email: paavo.peltopihko@tuni.fi

This code is for Assignment 1 implementation which is based on the paper:
Private Lives Matter: A Differential Private Functional Encryption Scheme

"""
from mife.single.ddh import FeDDH
import numpy as np
import time


def generate_tree(array:list, n_value:int):
    """
    Function is used to generate the tree out from the given array.
    
    Splits the given array to n_value number of slices and calculates the 
    amount of numbers in each slice. Stores those to another array that is 
    returned.
    """
    leaf_amount = 2**n_value
    
    # Calc values that are in each 1/leaf_amount slice of the range from 0-100.  
    leaf = 1
    sum_of_numbers = 0
    binary_tree_leafs = []
    for number in array:
        if number <= leaf*100/leaf_amount: 
            sum_of_numbers += 1
        else:
            binary_tree_leafs.append(sum_of_numbers)
            sum_of_numbers = 0
            leaf += 1
            if number <= leaf*100/leaf_amount: 
                sum_of_numbers += 1
            else:
                while number > leaf*100/leaf_amount:
                    binary_tree_leafs.append(sum_of_numbers)
                    leaf += 1
                sum_of_numbers += 1
    # Adding the last sum to the binary tree.
    binary_tree_leafs.append(sum_of_numbers)
    while len(binary_tree_leafs) < leaf_amount:
        binary_tree_leafs.append(0)

    return binary_tree_leafs


def create_data(data_size:int):
    """
    Creates an numpy array of data exual the number in the parameter.

    Stores the used dataset to files for using it again in expirements.
    Returns sorted numpy array. 
    """
    # Range of values is [0.0, 100.0)
    array = np.random.randint(low=0, high=100, size=data_size)
    filename = str(data_size) + ".txt"
    np.savetxt(filename, array, fmt='%10.5f')

    # Return sorted copy of the created array
    return np.sort(array)


def read_data_from_file(filename):
    """
    Use this to read the test data from a file and don't generate new data

    Returns sorted numpy array
    """
    array = np.loadtxt(filename)

    return np.sort(array)


def perf_setup(datapoints:int, n_value:int):
    """
    This is the performance counter for running the data generation and 
    treegeneration 50 times in a row.
    """

    start_treegeneration = time.perf_counter()
    
    for i in range(50):
    # Generate data for 100 numbers and create the tree 50 times, calc mean time
        array = create_data(datapoints)
        binary_tree = generate_tree(array, n_value)
    
    stop_treegeneration = time.perf_counter()

    whole_time_ms = (stop_treegeneration - start_treegeneration)*1000
    average_time_ms = whole_time_ms/50

    print(f"Dataset size: {datapoints}, n: {n_value} and number of leafs: {2**n_value}")
    print(f"Time for the whole 50 rounds: {whole_time_ms:.2f} ms")
    print(f"Average time per round: {average_time_ms:.2f} ms")


# This function is from teachers:
def add_laplace_noise(original_value, scale_parameter, size=1): 
    """ 
    Add Laplace noise to a given value. 
   
    Parameters: 
    - original_value: The original value to which noise will be added. 
    - scale_parameter: The scale parameter of the Laplace distribution. 
    - size: The number of samples to generate. 
    
    Returns: 
    - A NumPy array containing the original value with added Laplace noise. 
    """ 
    
    noise = np.random.laplace(loc=0.0, scale=scale_parameter, size=size) 
    
    return original_value + noise 

# Example usage: original_value = 10.0 scale_parameter = 1.0 size = 1 
# 
# 
# You can adjust the size based on how many samples you want 
# noisy_value = add_laplace_noise(original_value, scale_parameter, size) 
# print("Original Value:", original_value) print("Noisy Value:", noisy_value)


def add_noise(array:list):
    """
    Adds noise to each element in the given list. 

    Returns a new array with added noise to each element.
    """
    for i in range(len(array)):
        original_value = array[i]
        noisy_value = add_laplace_noise(original_value, 1.0)
        array[i] = int(noisy_value[0])  # Sadly we must use integers as the 
                                        # PyMIFE encryption requires integers
    return array


def perf_noise(array:list, n_value):
    """
    This is the performance counter for running the noise generation 50 times 
    in a row.
    """
    
    # Get the mean performance running 50 rounds:
    start_noisetimer = time.perf_counter()
    
    for i in range(50):
        bin_tree_noise = add_noise(array)
    
    stop_noisetimer = time.perf_counter()
    whole_time_ms = (stop_noisetimer-start_noisetimer)*1000
    mean_time_ms = whole_time_ms/50
    print(f"Time to add noise in {2**n_value} leaves 50 times: {whole_time_ms:.2f} ms")        
    print(f"The mean time to add noise to {2**n_value} leaves: {mean_time_ms:.2f} ms")


def generate_keys(number_of_leaves:int):
    """
    Generates key for the amount of leaves given

    returns a object that is the key.
    """
    key = FeDDH.generate(number_of_leaves)
    return key


def perf_keygeneration(number_of_leaves:int):
    """
    Performance test to generate keys, runs 50 times.
    """
    # Get the mean performance running 50 rounds:
    start_keytimer = time.perf_counter()
    
    for i in range(50):
        key = generate_keys(number_of_leaves)
    
    stop_keytimer = time.perf_counter()
    whole_time_ms = (stop_keytimer-start_keytimer)*1000
    mean_time_ms = whole_time_ms/50
    print(f"Time to generate keys for {number_of_leaves} leaves 50 times: {whole_time_ms:.2f} ms")        
    print(f"The mean time to generate keys for {number_of_leaves} leaves: {mean_time_ms:.2f} ms")


def encryption(key, array:list):
    """
    Encryption function for FeDDH-scheme.

    returns the ciphertext
    """

    cipher_text = FeDDH.encrypt(array, key)
    return cipher_text


def perf_encryption(key, array:list):
    """
    Performance function to encrypt data, this runs 50 times.
    """
    # Get the mean performance running 50 rounds:
    start_enctimer = time.perf_counter()
    
    for i in range(50):
        ciphertext = encryption(key, array)
    
    stop_enctimer = time.perf_counter()
    whole_time_ms = (stop_enctimer-start_enctimer)*1000
    mean_time_ms = whole_time_ms/50
    print(f"Time to encrypt data for {len(array)} elements 50 times: {whole_time_ms:.2f} ms")        
    print(f"The mean time to encrypt data for {len(array)} elements: {mean_time_ms:.2f} ms")


def decryption_key_generation(start:int, end:int, data_size:int, key):
    """
    Creates a decryption key for calculating the sum from our encrypted data.
    Takes as parameter a range of indices from start to end.
    Returns the decryption key
    """

    # Create the Y-vector for calculating sum from given datasize:
    y = []
    for i in range(data_size):
        if i >= start and i <= end:
            y.append(1)
        else:
            y.append(0)

    # Create the decryption key:
    dec_key = FeDDH.keygen(y, key)

    return dec_key


def perf_decryption_best_case(data_size: int, key, ciphertext):
    """
    This does the best case calculation for the data which is to retrieve the 
    sum for whole data set.
    """
    # Get the mean performance running 50 rounds:
    start_dectimer = time.perf_counter()
    
    for i in range(50):
        dec_key = decryption_key_generation(0, data_size, data_size, key)
        plaintext = FeDDH.decrypt(ciphertext, key.get_public_key(), dec_key, (0, 10000))
    
    stop_dectimer = time.perf_counter()
    whole_time_ms = (stop_dectimer-start_dectimer)*1000
    mean_time_ms = whole_time_ms/50
    print(f"Time to decrypt data for {data_size} elements 50 times: {whole_time_ms:.2f} ms")        
    print(f"The mean time to derypt data for {data_size} elements: {mean_time_ms:.2f} ms")


def pert_decryption_worst_case(data_size: int, key, ciphertext):
    """
    This does the worst case calculation for decryption which a query to get 
    every leaf value separatelly.
    """
    # Get the mean performance running 50 rounds:
    start_dectimer = time.perf_counter()

    # create an identity matrix from numpy to quicken the calculation:
    identity_matrix = np.identity(data_size, dtype=int)    

    # 50 rounds of calculations:
    for round in range(50):
        plaintext_vector = []
        for i in range(data_size):
            # Generate a decryption key for each element in the data
            y = identity_matrix[i]
            dec_key = FeDDH.keygen(y, key)
            plaintext = FeDDH.decrypt(ciphertext, key.get_public_key(), dec_key, (0,10000000))
            plaintext_vector.append(plaintext)


    stop_dectimer = time.perf_counter()
    whole_time_ms = (stop_dectimer-start_dectimer)*1000
    mean_time_ms = whole_time_ms/50
    print(f"Time to decrypt worst case for {data_size} elements 50 times: {whole_time_ms:.2f} ms")        
    print(f"The mean time to derypt worst case for {data_size} elements: {mean_time_ms:.2f} ms")

def main():
    datapoint_amounts = [100, 500, 1000, 10000]
    n_values = [5, 6, 7, 8, 9, 10]

    ####### You can use this function to read predetermined data:
    # filename = input("Input the name for the data file:")
    # array_from_file = read_data_from_file(filename)
    # treesize = int(input("Give the n value of your tree 2^n: "))
    # binary_tree_from_file = generate_tree(array_from_file, treesize)

    # Do the performance test for creating dataset and tree leaves:
    for datapoint_amount in datapoint_amounts:
        for n_value in n_values:
            perf_setup(datapoint_amount, n_value)


    # Get the actual tree for the project:
    array_10000 = read_data_from_file("10000.txt")

    # One tree for each amount of leaves:
    binary_tree_10000_5 = generate_tree(array_10000, 5)
    binary_tree_10000_6 = generate_tree(array_10000, 6)
    binary_tree_10000_7 = generate_tree(array_10000, 7)
    binary_tree_10000_8 = generate_tree(array_10000, 8)
    binary_tree_10000_9 = generate_tree(array_10000, 9)
    binary_tree_10000_10 = generate_tree(array_10000, 10)

    print()
    
    # Adding noise to each leaf in the trees performance test:
    perf_noise(binary_tree_10000_5, 5)
    perf_noise(binary_tree_10000_6, 6)
    perf_noise(binary_tree_10000_7, 7)
    perf_noise(binary_tree_10000_8, 8)
    perf_noise(binary_tree_10000_9, 9)
    perf_noise(binary_tree_10000_10, 10)
    
    # Getting the real data for each size binary tree to use in encryption:
    bin_tree_10000_5_noise = add_noise(binary_tree_10000_5)
    bin_tree_10000_6_noise = add_noise(binary_tree_10000_6)
    bin_tree_10000_7_noise = add_noise(binary_tree_10000_7)
    bin_tree_10000_8_noise = add_noise(binary_tree_10000_8)
    bin_tree_10000_9_noise = add_noise(binary_tree_10000_9)
    bin_tree_10000_10_noise = add_noise(binary_tree_10000_10)
    
    print()
    # Performance test for key generation using PyMIFE library:
    for n_value in n_values:
        number_of_leaves = 2**n_value
        perf_keygeneration(number_of_leaves)
    
    # Generate key for encryption for rest of the program:
    key_32 = generate_keys(32)
    key_64 = generate_keys(64)
    key_128 = generate_keys(128)
    key_256 = generate_keys(256)
    key_512 = generate_keys(512)
    key_1024 = generate_keys(1024)

    print()
   
    # Test the performance of the encryption:
    perf_encryption(key_32, bin_tree_10000_5_noise)
    perf_encryption(key_64, bin_tree_10000_6_noise)
    perf_encryption(key_128, bin_tree_10000_7_noise)
    perf_encryption(key_256, bin_tree_10000_8_noise)
    perf_encryption(key_512, bin_tree_10000_9_noise)
    perf_encryption(key_1024, bin_tree_10000_10_noise)

    # Real encryption of data:
    ciphertext_32 = encryption(key_32, bin_tree_10000_5_noise)
    ciphertext_64 = encryption(key_64, bin_tree_10000_6_noise)
    ciphertext_128 = encryption(key_128, bin_tree_10000_7_noise)
    ciphertext_256 = encryption(key_256, bin_tree_10000_8_noise)
    ciphertext_512 = encryption(key_512, bin_tree_10000_9_noise)
    ciphertext_1024 = encryption(key_1024, bin_tree_10000_10_noise)

    print()
    # Decryption key generation and decryption phase:
    # Doing the best case first:
    perf_decryption_best_case(1024, key_1024,ciphertext_1024) 
    print()

    # This will run forever or fail if run with the 1024 leafs, so using only 
    # 64 here to demonstrate the problem.
    pert_decryption_worst_case(64,key_64,ciphertext_64)


main()

