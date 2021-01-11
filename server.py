from flask import Flask, render_template, redirect, url_for, request

import wordrootmodels.models as test
import wordrootmodels.fwr2 as fwr2

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        inputword = request.values.get('Inputword').lower()
        wordrootPredict = ('no result')
        esleroots = ''
        inputroot=inputword

        print(request.values.get('Inputword'))
        print(request.values.get('Togglemodel1'))
        if request.values.get('Togglemodel1') == 'on':
            try:
                fwr=fwr2.wordrootPredict(inputword)
                wordrootPredict = fwr[0][0]
                inputroot=' '.join(wordrootPredict)
                k = []
                for item in fwr[1:5]:
                    print(item)
                    k.append(item[0])
                esleroots=k
            except:
                wordrootPredict = ('no result')

        if request.values.get('Togglemodel1') == None and request.values.get('Togglemodel2') == None and request.values.get('Togglemodel3') == None and request.values.get('Togglemodel4') == 'on':
            inputroot = inputword
        
        root_suggest()
        return render_template("index.html", title="ISLab　NLP　Final",inputword=inputword,wordrootPredict=wordrootPredict,esleroots=esleroots,inputroot=inputroot,root_suggest=root_suggest)
    return render_template("index.html", title="ISLab　NLP　Final")
 

if __name__=='__main__':
    app.run(host='127.0.0.1', port=42968, debug=True)
