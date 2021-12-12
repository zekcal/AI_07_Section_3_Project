# ml 모델 관련 import
from flask.wrappers import Request
import joblib

# flask 관련 import
from flask import Flask, render_template, request
import numpy as np

# 모델 로드

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        model = joblib.load('./knn_model.pkl')
        gold_left = float(request.form['gold_left'])
        traits_count = float(request.form['traits_count'])
        total_damage_to_players = float(request.form['total_damage_to_players'])
        Set6_Academy = float(request.form['Set6_Academy'])
        Set6_Arcanist = float(request.form['Set6_Arcanist'])
        Set6_Assassin = float(request.form['Set6_Assassin'])
        Set6_Bodyguard = float(request.form['Set6_Bodyguard'])
        Set6_Bruiser = float(request.form['Set6_Bruiser'])
        Set6_Challenger = float(request.form['Set6_Challenger'])
        Set6_Chemtech = float(request.form['Set6_Chemtech'])
        Set6_Colossus = float(request.form['Set6_Colossus'])
        Set6_Clockwork = float(request.form['Set6_Clockwork'])
        Set6_Cuddly = float(request.form['Set6_Cuddly'])
        Set6_Enchanter = float(request.form['Set6_Enchanter'])
        Set6_Enforcer = float(request.form['Set6_Enforcer'])
        Set6_Glutton = float(request.form['Set6_Glutton'])
        Set6_Imperial = float(request.form['Set6_Imperial'])
        Set6_Innovator = float(request.form['Set6_Innovator'])
        Set6_Mercenary = float(request.form['Set6_Mercenary'])
        Set6_Mutant = float(request.form['Set6_Mutant'])
        Set6_Protector = float(request.form['Set6_Protector'])
        Set6_Scholar = float(request.form['Set6_Scholar'])
        Set6_Scrap = float(request.form['Set6_Scrap'])
        Set6_Sister = float(request.form['Set6_Sister'])
        Set6_Sniper = float(request.form['Set6_Sniper'])
        Set6_Socialite = float(request.form['Set6_Socialite'])
        Set6_Syndicate = float(request.form['Set6_Syndicate'])
        Set6_Transformer = float(request.form['Set6_Transformer'])
        Set6_Twinshot = float(request.form['Set6_Twinshot'])
        Set6_Yordle = float(request.form['Set6_Yordle'])

        data = ((gold_left, traits_count, total_damage_to_players, Set6_Academy, Set6_Arcanist, Set6_Assassin, Set6_Bodyguard, Set6_Bruiser, Set6_Challenger, Set6_Chemtech, Set6_Colossus, Set6_Clockwork, Set6_Cuddly, Set6_Enchanter, Set6_Enforcer, Set6_Glutton, Set6_Imperial, Set6_Innovator, Set6_Mercenary, Set6_Mutant, Set6_Protector, Set6_Scholar, Set6_Scrap, Set6_Sister, Set6_Sniper,Set6_Socialite, Set6_Syndicate, Set6_Transformer, Set6_Twinshot, Set6_Yordle),)
        pred = model.predict(np.array(data))

        return render_template('index.html', pred=pred)

if __name__ == '__main__':
    model = joblib.load('./knn_model.pkl')
    app.run(host='0.0.0.0', port=8000, debug=True)