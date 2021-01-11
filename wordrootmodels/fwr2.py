import json
from collections import Counter
import os
import math

prefix_freq=Counter()
affix_freq=Counter()    
suffix_freq=Counter()
            
def segment(word):
	# TODO: split a word into pieces
    spilt_list=[]
    for i in range(len(word)):
        for j in range(len(word)):
            if j>=i and i >0:
                spilt_list.append((word[:i],word[i:j],word[j:]))
    
    return spilt_list



def Calculation(spilt_list):
    global prefix_freq
    global affix_freq
    global suffix_freq

    new_list=[]
    prefix_sum=sum(prefix_freq.values())
    affix_sum=sum(affix_freq.values())
    suffix_sum=sum(suffix_freq.values())
    for item in spilt_list:
        pre_text=item[0]
        aff_text=item[1]
        suf_text=item[2]
        p1=prefix_freq[pre_text]/prefix_sum
        p2=affix_freq[aff_text]/affix_sum
        p3=suffix_freq[suf_text]/suffix_sum
        if p1==0:
            p1=1/(prefix_sum*10**len(pre_text))
        if p2==0:
            p2=1/(affix_sum*10**len(aff_text))
        if p3==0:
            p3=1/(suffix_sum*10**len(suf_text))

        if(aff_text)=='':
            ans=math.log(p1)+math.log(p3)
        else:
            ans=math.log(p1)+math.log(p2)+math.log(p3)
        new_list.append((item, round(ans, 3)))
        new_list.sort(key=lambda tup: tup[1] , reverse=True)
    return new_list[:10]

def wordrootPredict(inpurword):
        
    global prefix_freq
    global affix_freq
    global suffix_freq
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'etym.entries.v1.format.json')
    
    with open(path , 'r') as reader:
        jf = json.loads(reader.read())

    for i in range(jf['count']):
        for w in jf['results'][i]['foreigns']:
            if len(w)>1:
                if w[0]!='*' :
                        if w[0]=='-' and w[-1]!='-' :
                            suffix_freq[w[1:]]+= 1
                        elif w[0]!='-' and w[-1]=='-' :
                            prefix_freq[w[:-1]] += 1
                        elif(w[0]!='-' and w[-1]!='-'):
                            affix_freq[w] += 1

    for i in range(jf['count']):
        for w in jf['results'][i]['cross-references']:
            if '*' not in w :
                if len(w)>1:
                    if w[0]=='-' and w[-1]!='-' :
                        suffix_freq[w[1:]]+= 1
                    elif w[-1]=='-' and w[0]!='-' :
                        prefix_freq[w[:-1]] += 1
                    elif(w[0]!='-' and w[-1]!='-'):
                        affix_freq[w] += 1

    scholarship=segment(inpurword)
    ansList = Calculation(scholarship)
    return ansList

if __name__ == "__main__":
    print(wordrootPredict('Literature')[0][0])
