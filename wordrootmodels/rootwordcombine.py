import requests
from bs4 import BeautifulSoup as soup

def crawl_parse(query):
    data_dict = {
        'url': '',
        'title': '',
        'foreigns': [],
        'references': [],
        'text': ''
        }

    url = 'https://www.etymonline.com/search?q='+query # 目標 url
    response = requests.get(url) # 使用 GET 送出 request
    if response.status_code == 200:  # 「200 OK」代表請求成功被處理
        text = response.text  # 把 response 內容取出
        html = soup(text, "html.parser")  # 使用 bs4 生成 bs object
        beautiful_html = html.prettify()  # 縮排過後的html source code
        count = html.select_one('.searchList__pageCount--2jQdB').text
        print(count)
        if count == '0 entry found':
            return None
        first_block=html.select_one('div object')
        #url
        url = first_block.select_one('a')['href']
        #print(url)
        data_dict['url']='https://www.etymonline.com'+url
        #title
        title = first_block.select_one('a').text
        #print(title)
        data_dict['title']=title

        #foreigns
        foreigns = first_block.select('.foreign')
        #print(foreigns)
        for item in foreigns:
            data_dict['foreigns'].append(item.text)
        #references
        references = first_block.select('.crossreference')
        #print(references)
        for item in references:
            data_dict['references'].append(item.text)
        #text
        text = first_block.select_one('section').text
        #print(text)
        data_dict['text']=text
    else:
        print('Failed', response.status_code)
        return None

    return data_dict



from collections import Counter, defaultdict
import math, re
import kenlm
import operator
import itertools

model = kenlm.Model('bnc.prune.arpa')


def words(text): return re.findall(r'\w+|[,.?]', text.lower())


WORDS = Counter(words(open('big.txt').read()))


def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return float(WORDS[word] / N)


def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def suggest(word):
    '''return top 5 words as suggestion, original_word as top1 when original_word is correct'''
    print(word)
    print(word[-3:])

    if word[-3:] == 'ing':
        word = word[:-3]+'y'
        print(word)
    suggest_P = {}
    edits_set = edits1(word).union(set(edits2(word)))
    for candidate in known(edits_set):
        suggest_P[candidate] = P(candidate)
    if word in WORDS:
        suggest_P[word] = 1
    suggest_can = sorted(suggest_P, key=suggest_P.get, reverse=True)[:5]
    
    return suggest_can



if __name__ == "__main__":

    # target = ['quering','acquir']
    # for item in target:
    #     print(item + ':\n')
    #     result= crawl_parse(item)
    #     print(crawl_parse(item))
    #     print('\n')
    #     if (result == None):
    #         sug_word=suggest(item)
    #         print(sug_word)
    #         try:
    #             crawl_parse(sug_word[0])
    #         except Exception as e:
    #             print(e)


    testlist = ['definit', 'ion', 's']


    
    print(testlist[-1:])
    if testlist[-1:] == ['s']:
        testlist=testlist[:-1]
    testword="".join(testlist)
    sug_word=suggest(testword)
    print(sug_word)
    result= crawl_parse(testword)
    print(result)
