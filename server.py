from flask import Flask, render_template, redirect, url_for, request

import wordrootmodels.models as test
import wordrootmodels.fwr2 as fwr2

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        inputword = request.values.get('Inputword').lower()
        wordrootPredict=''
        print(request.values.get('Inputword'))
        if request.values.get('Togglemodel1') == 'on':
            wordrootPredict = fwr2.wordrootPredict(inputword)[0][0]
        ans1 = test.test(inputword)
        
        return render_template("index.html", title="ISLab　NLP　Final",wordrootPredict=wordrootPredict)
    return render_template("index.html", title="ISLab　NLP　Final")
 

if __name__=='__main__':
    app.run(host='127.0.0.1', port=42968, debug=True)
