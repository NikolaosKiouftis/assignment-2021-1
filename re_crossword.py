import argparse
import string
import sre_yield
import csv

# add arguments
parser = argparse.ArgumentParser(description="solves a crossword")
parser.add_argument("crossword_file", help="name of a file.csv", type=argparse.FileType("r"))
parser.add_argument("words_file", help="name of a file.txt", type=argparse.FileType("r"))
args = parser.parse_args()

c = {}
letters = {}
indexes = {}
content = []
bank = []
# read a csv file
with args.crossword_file as crossword:
    reader = csv.reader(crossword, delimiter=",")
    for line in reader:
        nodes = [x for x in line]
        # initialize dict to represent crossword
        if int(nodes[0]) not in c:
            c[int(nodes[0])] = []
        i = 2
        while i < len(nodes):
            c[int(nodes[0])].append(int(nodes[i]))
            i += 2
        # initialize dict to represent the missing words
        if int(nodes[0]) not in letters:
            letters[int(nodes[0])] = []
        letters[int(nodes[0])].append(nodes[1])
        # initialize dict to represent the index of the crossed word
        if int(nodes[0]) not in indexes:
            indexes[int(nodes[0])] = []
        i = 2
        while i < len(nodes):
            indexes[int(nodes[0])].append((nodes[i]))
            i += 1
# find lengths from missing words
for v, n in letters.items():
    size = len(n[0])
    content.append(size)

# read a text file with regular expressions
# hold only words with size same with missing words
with args.words_file as words:
    for line in words:
        seed = list(sre_yield.AllStrings(line[:-1], max_count=5, charset=string.ascii_uppercase))
        for i in range(len(seed)):
            if len(seed[i]) in content:
                bank.append(seed[i])
# to avoid duplicates
bank = list(dict.fromkeys(bank))

# apply depth first search
words_found = [False] * len(c)


def dfs(g, node):
    print("Matching", node)
    words_found[node] = True
    for x in c[node]:
        if not words_found[x]:
            dfs(g, x)


dfs(c, 0)
