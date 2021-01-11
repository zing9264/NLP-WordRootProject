import requests
from bs4 import BeautifulSoup as soup
from spellchecker import SpellChecker
from nltk.stem import WordNetLemmatizer  
import nltk


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
        


def lemmatize_all(sentence):
    wnl = WordNetLemmatizer()
    for word, tag in nltk.pos_tag(nltk.word_tokenize(sentence)):
        if tag.startswith('NN'):
            yield wnl.lemmatize(word, pos='n')
        elif tag.startswith('VB'):
            yield wnl.lemmatize(word, pos='v')
        elif tag.startswith('JJ'):
            yield wnl.lemmatize(word, pos='a')
        elif tag.startswith('R'):
            yield wnl.lemmatize(word, pos='r')
        else:
            yield word


def suggest(word):
    spell = SpellChecker()
    # find those words that may be misspelled
    misspelled = spell.unknown( [word])
    for word in misspelled:
        # Get the one `most likely` answer
        mostlikely=spell.correction(word)
        print('--mostlikely=' '---')
        print(mostlikely)
        return mostlikely
    print('--word---')
    print(word)
    return word



def rootwordcombine(word):
    newword = "".join(word.split())
    queryword = suggest(newword)
    lemma=''.join(lemmatize_all(queryword))

    crawl = crawl_parse(lemma)
    return (newword, queryword, lemma,crawl)
    
if __name__ == "__main__":
    print(rootwordcombine('com- quering'))
