from flask import Flask, render_template, redirect, url_for, request

import test

app = Flask(__name__)

@app.route('/')
def index():
    ans1=test.test()
    return render_template("index.html", title="ISLab　NLP　Final",ans1=ans1)


if __name__=='__main__':
    app.run(host='127.0.0.1', port=42968, debug=True)
