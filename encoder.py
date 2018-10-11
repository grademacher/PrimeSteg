from PIL import Image
import numpy as np
import random
import math


def is_prime(n):
    # Corner cases
    if (n <= 1):
        return False
    if (n <= 3):
        return True

    # This is checked so that we can skip
    # middle five numbers in below loop
    if (n % 2 == 0 or n % 3 == 0):
        return False

    i = 5
    while (i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0):
            return False
        i = i + 6

    return True


# A function to generate a random permutation of arr[]
def randomize(arr1, arr2, n):
    # Start from the last element and swap one by one. We don't
    # need to run for the first element that's why i > 0
    for i in range(n-1, 0, -1):
        # Pick a random index from 0 to i
        j = random.randint(0, i)

        # Swap arr[i] with the element at random index
        arr1[i], arr1[j] = arr1[j], arr1[i]
        arr2[i], arr2[j] = arr2[j], arr2[i]
    return


def encrypt(message, input_file, output_file, key):
    # Format the message
    message = message.replace(" ", "")
    message_stripped = ''.join(c for c in message if c.isalpha())
    message = message_stripped.lower()

    # Open the image file
    img = Image.open(input_file)
    ary = np.array(img)

    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    key_alphabet = alphabet.copy()

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    key_string = ""

    if len(key) > 0:
        # A key was provided, set this as the encryption scheme
        key_string = key
        key = key.lower()
        for i in range(len(key)):
            alphabet[i] = key[i]

    else:
        # Create the substitution cipher for the prime encoding
        randomize(primes, key_alphabet, len(primes))
        for letter in key_alphabet:
            key_string += letter
        key_string = key_string.upper()

    # Encode the message with the substitution scheme
    prime_message = []
    for c in message:
        prime_message.append(primes[alphabet.index(c)])

    # Record the original dimensions of the image array
    rows = ary.shape[0]
    cols = ary.shape[1]
    depth = ary.shape[2]

    # Strip all first 26 prime numbers from the RGB data
    for i in range(0, rows):
        for j in range(0, cols):
            for k in range(0, depth):
                if ary[i, j, k] < 102:
                    if ary[i, j, k] == 2 or ary[i, j, k] == 3:
                        ary[i, j, k] = 4
                    else:
                        if is_prime(ary[i, j, k]):
                            ary[i, j, k] = ary[i, j, k] - 1

    total_cells = rows * cols
    insertion_interval = total_cells / len(prime_message)
    insertion_interval = math.floor(insertion_interval)

    # Resize the array to be a list of pixels with their RGB values
    ary.resize(total_cells, 3)

    # Hide each letter in its own chunk where the prime is the closest to the original value
    for i in range(0, len(prime_message)):
        value = prime_message[i]
        closest_value = ary[(i*insertion_interval), 0]
        closest_index = [(i*insertion_interval), 0]
        for j in range((i * insertion_interval), ((i * insertion_interval) + insertion_interval)):
            for k in range(0, 3):
                if np.abs(value - closest_value) > np.abs(value - ary[j, k]):
                    closest_value = ary[j, k]
                    closest_index = [j, k]
        ary[closest_index[0], closest_index[1]] = value

    # Resize the array to the dimensions of the original image
    ary.resize(rows, cols, 3)

    # Convert the array back to an image and save it
    hidden_image = Image.fromarray(ary, 'RGB')
    hidden_image.save(output_file)

    # Return encryption statistics to the GUI
    return [message, key_string, output_file]



