import json
import requests
from math import log
from pprint import pprint
from collections import Counter
from bs4 import BeautifulSoup as soup

def segment(word):
    output = []
    for i in range(1, len(word)):
        for j in range(i, len(word)):
            output.append((word[:i], word[i:j], word[j:len(word)]))
    return output

def calculate(word):
    output = []
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

def familyOfRoots(root):
    url = f'https://www.etymonline.com/search?q={root}'
    response = requests.get(url)
    anslist=[]
    if response.status_code == 200:
        text = response.text
        html = soup(text, "html.parser")

        label = html.select('div object a')
        for i in label:
            if '.' not in i.text:
                continue
            if root not in i.text:
                continue
            anslist.append(i.text)
        if len(anslist) == 0:
            anslist.append('查無資料')
        
        result=',  '.join(anslist)

        return(result)
    else:
        print('Failed', response.status_code)
        return '查無資料'


# demo = ['international', 'scholarship', 'university', 'education', 'programme']



if __name__ == "__main__":
    with open('etym.entries.v1.format.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    prefix_freq = Counter()
    affix_freq = Counter()
    suffix_freq = Counter()

    for i in data['results']:
        for j in i['foreigns'] + i['cross-references']:
            if j == '' or j[0] == '*' or j[0] == j[-1] == '-':
                continue
            elif j[-1] == '-':
                prefix_freq[j[:-1]] += 1
            elif j[0] == '-':
                suffix_freq[j[1:]] += 1
            else:
                affix_freq[j] += 1

    x = calculate('international')
    for i in x:
        familyOfRoots(i)
        print()    
