from flask import Flask, render_template, redirect, url_for, request

import wordrootmodels.models as test
import wordrootmodels.fwr2 as fwr2
import wordrootmodels.rootwordcombine as rootwordcombine
import wordrootmodels.meaningOfRoots as meaningOfRoots
import wordrootmodels.familyOfRoots as familyOfRoots



app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        inputword = request.values.get('Inputword').lower()
        wordrootPredict = ('no result')
        esleroots = ''
        inputroot = inputword
        pre_result = ''
        aff_result = ''
        suf_result = ''
        pre = ''
        aff = ''
        suf = ''
        pre_family = ''
        aff_family = ''
        suf_family = ''



        print(request.values.get('Inputword'))
        print(request.values.get('Togglemodel1'))
        if request.values.get('Togglemodel1') == 'on':
            try:
                fwr=fwr2.wordrootPredict(inputword)
                wordrootPredict = fwr[0][0]
                pre = wordrootPredict[0]
                aff = wordrootPredict[1]
                suf = wordrootPredict[2]
                inputroot=' '.join(wordrootPredict)
                k = []
                for item in fwr[1:5]:
                    print(item)
                    k.append(item[0])
                esleroots=k
            except:
                wordrootPredict = ('no result')

        if request.values.get('Togglemodel2') == 'on':
            print(pre)

            if pre != '':
                pre_result = meaningOfRoots.meaningOfRoots(pre, 0)[1]
            if aff!='':
                aff_result = meaningOfRoots.meaningOfRoots(aff, 1)[1]
            if suf!='':
                suf_result = meaningOfRoots.meaningOfRoots(suf, 2)[1]
                
        if request.values.get('Togglemodel3') == 'on':
            print(pre)

            if pre != '':
                pre_family = familyOfRoots.familyOfRoots(pre)
            if aff!='':
                aff_family = familyOfRoots.familyOfRoots(aff)
            if suf!='':
                suf_family = familyOfRoots.familyOfRoots(suf)

        if request.values.get('Togglemodel1') == None and request.values.get('Togglemodel2') == None and request.values.get('Togglemodel3') == None and request.values.get('Togglemodel4') == 'on':
            inputroot = inputword
        
        root_suggest = rootwordcombine.rootwordcombine(inputroot)
        root_suggest_inputconbine=root_suggest[0]
        root_suggest_suggest=root_suggest[1]
        root_suggest_lemma=root_suggest[2]
        root_suggest_crawl=root_suggest[3]


        return render_template("index.html", title="ISLab　NLP　Final",inputword=inputword,wordrootPredict=wordrootPredict,esleroots=esleroots,inputroot=inputroot,root_suggest_inputconbine=root_suggest_inputconbine,root_suggest_suggest=root_suggest_suggest,root_suggest_lemma=root_suggest_lemma,root_suggest_crawl=root_suggest_crawl,pre_result=pre_result,suf_result=suf_result,aff_result=aff_result,pre=pre,aff=aff,suf=suf,pre_family=pre_family,aff_family=aff_family,suf_family=suf_family)
    return render_template("index.html", title="ISLab　NLP　Final")
 

if __name__=='__main__':
    app.run(host='127.0.0.1', port=42968, debug=True)
