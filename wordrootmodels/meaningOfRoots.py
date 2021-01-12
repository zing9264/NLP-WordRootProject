import re
import json
import requests
from math import log
from pprint import pprint
from collections import Counter
from spellchecker import SpellChecker
from bs4 import BeautifulSoup as soup

prefix_freq = Counter()
affix_freq = Counter()
suffix_freq = Counter()

def words(text): return re.findall(r'\w+', text.lower())

def suggest(word):
    spell = SpellChecker()
    # find those words that may be misspelled
    misspelled = spell.unknown( [word])
    for word in misspelled:
        # Get the one `most likely` answer
        mostlikely=spell.correction(word)
        return mostlikely
    return word

def segment(word):
    output = []
    for i in range(1, len(word)):
        for j in range(i, len(word)):
            output.append((word[:i], word[i:j], word[j:len(word)]))
    return output

def calculate(word):
    output = []
    global prefix_freq 
    global affix_freq 
    global suffix_freq

    for i in segment(word):
        if prefix_freq[i[0]] == 0:
            p1 = 1 / (sum(prefix_freq.values()) * 10 ** len(i[0]))
        else:
            p1 = prefix_freq[i[0]] / sum(prefix_freq.values())

        if affix_freq[i[1]] == 0:
            p2 = 1 / (sum(affix_freq.values()) * 10 ** len(i[1]))
        else:
            p2 = affix_freq[i[1]] / sum(affix_freq.values())

        if suffix_freq[i[2]] == 0:
            p3 = 1 / (sum(suffix_freq.values()) * 10 ** len(i[2]))
        else:
            p3 = suffix_freq[i[2]] / sum(suffix_freq.values())
        
        if i[1] == '':
            p = log(p1, 10) + log(p3, 10)
        else:
            p = log(p1, 10) + log(p2, 10) + log(p3, 10)
        
        output.append((i, p))

    output.sort(key = lambda x : x[1], reverse = True)
    # pprint(output[:10])
    return output[0][0]

def search(word):

    url = f'https://www.etymonline.com/search?q={word}'
    response = requests.get(url)

    if response.status_code == 200:
        text = response.text
        html = soup(text, "html.parser")
        # output = {}

        title = html.select_one('div object a')
        content = html.select_one('div object section')
        if title == None:
            return False

        if word in title.text:
            return title.text, content.text
        else:
            return False
    else:
        print('Failed', response.status_code)

def search2(word):

    url = f'https://www.etymonline.com/search?q={word}'
    response = requests.get(url)

    if response.status_code == 200:
        text = response.text
        html = soup(text, "html.parser")
        # output = {}

        title = html.select_one('div object a')
        content = html.select_one('div object section')
        if title == None:
            return False

        if word == words(title.text)[0]:
            return title.text, content.text
        else:
            return False
    else:
        print('Failed', response.status_code)


def meaningOfRoots(root, a):
    if a == 0:
        x = search(root+'-')
    else:
        x = search('-'+root)
    if x:
        print(x[0])
        print(x[1])
    else:
        x = search2(root)
        if x:
            print(x[0])
            print(x[1])
        else:
            x = search2(suggest(root))
            if x:
                print(x[0])
                print(x[1])
    return x

# demo = ['international', 'scholarship', 'university', 'education', 'programme']


if __name__ == "__main__":
    pass

