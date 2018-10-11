from PIL import Image
import numpy as np
from pycipher import SimpleSubstitution as SimpleSub
import random
import re
from ngram_score import ngram_score
fitness = ngram_score('quadgrams.txt')


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


path = r"C:\Users\radem\PycharmProjects\PrimeSteg\test3_ENCRYPTED.png"
img = Image.open(path)

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]

ary = np.array(img)
rows = ary.shape[0]
cols = ary.shape[1]
depth = ary.shape[2]

hidden_message = []

for i in range(0, rows):
    for j in range(0, cols):
        for k in range(0, depth):
            if ary[i, j, k] < 102:
                if is_prime(ary[i, j, k]):
                        hidden_message.append(ary[i, j, k])

print(hidden_message)
encrypted_message = ""

for prime in hidden_message:
    print(primes.index(prime))
    encrypted_message += (alphabet[primes.index(prime)])

print(encrypted_message)

ctext=encrypted_message
ctext = re.sub('[^A-Z]','',ctext.upper())

maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
maxscore = -99e9
parentscore,parentkey = maxscore,maxkey[:]

# keep going until we are killed by the user
i = 0
while 1:
    i = i+1
    random.shuffle(parentkey)
    deciphered = SimpleSub(parentkey).decipher(ctext)
    parentscore = fitness.score(deciphered)
    count = 0
    while count < 1000:
        a = random.randint(0,25)
        b = random.randint(0,25)
        child = parentkey[:]
        # swap two characters in the child
        child[a],child[b] = child[b],child[a]
        deciphered = SimpleSub(child).decipher(ctext)
        score = fitness.score(deciphered)
        # if the child was better, replace the parent with it
        if score > parentscore:
            parentscore = score
            parentkey = child[:]
            count = 0
        count = count+1
    # keep track of best score seen so far
    if parentscore>maxscore:
        maxscore,maxkey = parentscore,parentkey[:]
        print('\nbest score so far:',maxscore,'on iteration',i)
        ss = SimpleSub(maxkey)
        print('    best key: '+''.join(maxkey))
        print('    plaintext: '+ss.decipher(ctext))