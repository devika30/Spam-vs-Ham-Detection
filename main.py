from flask import Flask, render_template, request
import os
import pickle as p
import os
from sklearn import *
from collections import Counter
import pickle 


def load(clf_file):
    with open(clf_file,"rb") as fp:
        clf = p.load(fp)
    return clf



def make_dict():
    direc = "emails/"
    files = os.listdir(direc)
    emails = [direc + email for email in files]
    words = []
    c = len(emails)

    for email in emails:
        f = open(email,"r",encoding="utf8", errors='ignore')
        blob = f.read()
        words += blob.split()


    for i in range(len(words)):
        if not words[i].isalpha():
            words[i] = ""

    dictionary = Counter(words)
    del dictionary[""]
    return dictionary.most_common(3000)



def predict_with_text(text):
    print("============================")
    print(text)
    print("============================")
    features = []
    inp = text.split()
    for word in d:
        features.append(inp.count(word[0]))
    res = clf.predict([features])
    print(res)
    resdir = {"0":"Ham","1":"Spam"}

    return resdir.get(str(res[0]))


clf = load("text-classifier.mdl")
print("model loaded")
d = make_dict()


app = Flask(__name__)
IMAGE_FOLDER = os.path.join('static', 'images')
@app.route('/sms')
def showtemplate():
   return render_template('sms.html',imageurl = os.path.join(IMAGE_FOLDER,'bg.jpg'))
	
@app.route('/predict', methods = ['POST','GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files.get('file',None)
        print(request.files)
        if f:
            d = predict_with_text(f.read().decode())
            print(d)
            return render_template('sms.html',imageurl = os.path.join(IMAGE_FOLDER,'bg.jpg'),prediction = d.lower())
        return render_template('sms.html',imageurl = os.path.join(IMAGE_FOLDER,'bg.jpg'))
    if request.method == 'GET' :
        return render_template('sms.html',imageurl = os.path.join(IMAGE_FOLDER,'bg.jpg'))
		
if __name__ == '__main__':
   app.run(debug = True)