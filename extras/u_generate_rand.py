import random

with open('train.txt', 'r+') as outFile:
    for i in range (700):
        num= random.randint(0, 10000000000)
        outFile.write(str(num)+"\n")