


######



from flask import Flask, render_template,request,json
from flaskext.mysql import MySQL
import MySQLdb
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

mysql=MySQL()

app=Flask(__name__)
app.config['MYSQL_DATABASE_USER']='antonioACR1'
app.config['MYSQL_DATABASE_PASSWORD']='password123'
app.config['MYSQL_DATABASE_DB']='antonioACR1$suggestions'
app.config['MYSQL_DATABASE_HOST']='antonioACR1.mysql.pythonanywhere-services.com'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('website.html')


@app.route('/showShareSong')
def showShareSong():
    return render_template('nombre_edad_share.html')
    
@app.route('/shareSong',methods=['POST','GET'])
def shareSong():
        _age = request.form['inputAge']
        _region=request.form['inputRegion']
        _sex=request.form['inputSex']
        _answer1=request.form['inputAnswer1']
        _answer2=request.form['inputAnswer2']
        _answer3=request.form['inputAnswer3']
        _answer4=request.form['inputAnswer4']
        _answer5=request.form['inputAnswer5']
        _answer6=request.form['inputAnswer6']
        _song=request.form['inputSong']
        _artist=request.form['inputArtist']
        _link=request.form['inputLink']

        if _age and _region and _sex and _answer1 and _answer2 and _answer3 and _answer4 and _answer5 and _answer6 and _song and _artist and _link:
            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.callproc('sp_createUser',(_age,_region,_sex,_answer1,_answer2,_answer3,_answer4,_answer5,_answer6,_song,_artist,_link))
            data=cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'html':'<span>All fields good !!</span>'})
            else:
                return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/thankYou')
def thankYou():
    return render_template('thanks.html')
#construct predictive model

@app.route('/showSuggestSong')
def showSuggestSong():
    return render_template('nombre_edad.html')


@app.route('/suggestSong',methods=['GET','POST'])
def suggestSong():    
        _age = request.form.get('inputAge',type=int)
        _region=request.form.get('inputRegion',type=int)
        _sex=request.form.get('inputSex',type=int)
        _answer1=request.form.get('inputAnswer1',type=int)
        _answer2=request.form.get('inputAnswer2',type=int)
        _answer3=request.form.get('inputAnswer3',type=int)
        _answer4=request.form.get('inputAnswer4',type=int)
        _answer5=request.form.get('inputAnswer5',type=int) 
        _answer6=request.form.get('inputAnswer6',type=int)
        db = MySQLdb.connect(host="antonioACR1.mysql.pythonanywhere-services.com", user="antonioACR1", passwd="password123", db="antonioACR1$suggestions")
        df_train = pd.read_sql('SELECT age,region,sex,answer1,answer2,answer3,answer4,answer5,answer6 FROM answers WHERE accepted = 1',con=db)    
#ASEGURARSE QUE HAY UNA OBSERVACION POR CADA REGION EN EL TRAINING 
        y_train=pd.read_sql('SELECT suggestion FROM answers WHERE accepted=1',con=db)
        modelo=DecisionTreeClassifier()
        modelo.fit(df_train,y_train)
#Prediction
        new_observation= pd.DataFrame({'age':[_age],'region':[_region],'sex':[_sex],'answer1':[_answer1],'answer2':[_answer2],'answer3':[_answer3],'answer4':[_answer4],'answer5':[_answer5],'answer6':[_answer6]}) 
        suggestion=modelo.predict(new_observation)[0]
#getting artist/song names and link of the suggestion
        name_song=pd.read_sql('SELECT nameSong FROM answers WHERE suggestion = ' + str(suggestion) + ' LIMIT 1',con=db)   
        name_artist=pd.read_sql('SELECT nameArtist FROM answers WHERE suggestion = ' + str(suggestion) + ' LIMIT 1',con=db)
        link=pd.read_sql('SELECT link FROM answers WHERE suggestion = ' + str(suggestion) + ' LIMIT 1',con=db)         
        return render_template('suggested_song.html',name_song=name_song.iloc[0,0],name_artist=name_artist.iloc[0,0],link=link.iloc[0,0])
        




if __name__ == "__main__":
    app.run(debug=True)







