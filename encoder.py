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
def randomize(arr, n):
    # Start from the last element and swap one by one. We don't
    # need to run for the first element that's why i > 0
    for i in range(n - 1, 0, -1):
        # Pick a random index from 0 to i
        j = random.randint(0, i)

        # Swap arr[i] with the element at random index
        arr[i], arr[j] = arr[j], arr[i]
    return arr


message = "this message is encrypted"
message = message.replace(" ", "")
message = message.lower()
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]

randomize(primes, len(primes))

prime_message = []

for c in message:
    prime_message.append(primes[alphabet.index(c)])

print(prime_message)
path = r"C:\Users\radem\PycharmProjects\PrimeSteg\test2.jpg"
img = Image.open(path)

ary = np.array(img)

#print(ary.shape)
#print(ary)

rows = ary.shape[0]
cols = ary.shape[1]
depth = ary.shape[2]


for i in range(0, rows):
    for j in range(0, cols):
        for k in range(0, depth):
            if ary[i, j, k] < 102:
                if ary[i, j, k] == 2 or ary[i, j, k] == 3:
                    ary[i, j, k] = 4
                else:
                    if is_prime(ary[i, j, k]):
                        ary[i, j, k] = ary[i, j, k] - 1


total_cells = rows*cols
insertion_interval = total_cells/len(prime_message)
insertion_interval = math.floor(insertion_interval)
#print(total_cells)
#print(insertion_interval)

ary.resize(total_cells, 3)
#print(ary)

for i in range(0, len(prime_message)):
    value = prime_message[i]
    closest_value = ary[i, 0]
    closest_index = [i, 0]
    for j in range((i*insertion_interval), ((i*insertion_interval)+insertion_interval)):
        for k in range(0, 3):
            if np.abs(value - closest_value) > np.abs(value - ary[j, k]):
                closest_value = ary[j, k]
                closest_index = [j, k]
    ary[closest_index[0], closest_index[1]] = value

#print(ary)

ary.resize(rows, cols, 3)
for i in range(0, rows):
    for j in range(0, cols):
        for k in range(0, depth):
            if ary[i, j, k] < 102:
                if is_prime(ary[i, j, k]):
                        print(ary[i, j, k])

hidden_image = Image.fromarray(ary, 'RGB')

hidden_image.save("new.png")
