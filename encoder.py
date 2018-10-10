from PIL import Image
import numpy as np
import random


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
substitute_alphabet = randomize(alphabet, alphabet.size)
path = r"C:\Users\radem\PycharmProjects\PrimeSteg\test1.jpg"
img = Image.open(path)

ary = np.array(img)

print(ary.shape)

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
