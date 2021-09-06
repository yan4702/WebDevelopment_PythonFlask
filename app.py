from flask import Flask, render_template, session, request, redirect, url_for, jsonify
import os
from flask_pymongo import PyMongo
import pymongo, json
from pymongo import MongoClient
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key=os.urandom(24)

#Q2aii-define function and print out the data from login page.
@app.route('/', methods=['GET', 'POST'])
def loginFirst():
    if request.method == 'POST':
        session.pop('myEmailUser', None)
        reqData= request.form
        print('\nLogin User Detail\n', '-'*30)
        print('username:', reqData['myEmailUser'],'\n',\
             'password:', reqData['myPws'],'\n')
    return render_template('index.html')

#Q2aii-define function and print out the data from register page.
@app.route('/registerPage', methods=['GET', 'POST'])
def regisFirst():
    if request.method == 'POST':
        session.pop('myEmailUser', None)
        reqData= request.form
        print('\nRegister User Detail\n', '-'*30)
        print('username:', reqData['myEmailUser'],'\n',\
            'password:', reqData['myPws'],'\n',\
            'weight:', reqData['myWeight'],'\n',\
            'gender:',  reqData['myGender'],'\n')
    return render_template('register.html')

#function of create DB for logPage.
def storeCalorieFromLog():
    #Create localhost mongoDB. 
    createDB = MongoClient('mongodb://localhost:27017/')
    newdb = createDB['testDB']
    dbCol = newdb['DBcollection']
    return dbCol

#Q2bi-define function for log.html.
#get all log input from ajax via log.js to perform calculation.
#contiunue to set up mongoDB.
@app.route('/logPage', methods=["GET","POST"])
def logPage():
    if request.method == "POST":
        calorieJson = request.get_json()
        weightJs = calorieJson['weiVal']
        walkJs = calorieJson['walkAns'] 
        runJs = calorieJson['runAns']
        swimJs = calorieJson['swimAns']
        bicyJs = calorieJson['bicyAns']
 
        weightAns = int(weightJs)
        walkAns =(int(walkJs) * 0.084) * weightAns 
        runAns = (int(runJs)* 0.21) * weightAns 
        swimAns = (int(swimJs)* 0.13) * weightAns 
        bicyAns = (int(bicyJs)* 0.064) * weightAns

        #MongoDB to store the testing data into TestDB.
        dbCol = storeCalorieFromLog()
        dbCol.insert_one({'weight': weightJs,'Walking': walkJs, \
            'running': runJs, 'swimming': swimJs, 'bicycling': bicyJs})
        colDatas = list(dbCol.find())
        #outputCol = [{'Walking' : colData['Walking'], 'running' : colData['running'],\
            #'swimming' : colData['swimming'], 'bicycling' : colData['bicycling']} for colData in colDatas]

        #calculate total calorie consume. 
        calorieResult =  walkAns + runAns + swimAns + bicyAns
        print('Result of total calorie: ', round(calorieResult))

        #testing printing out data of calorie in mongoDB.
        for colData in colDatas:
            print('Calorie Detail from MongoDB: ','\n',\
                'Weight:', colData['weight'],'\n',\
                'Walking:', colData['Walking'],'\n',\
                'running:' , colData['running'],'\n',\
                'swimming:', colData['swimming'],'\n',\
                'bicycling:', colData['bicycling'],'\n')
        #pass the results of calculation to log.js for display.
        return jsonify({'calorieResult':calorieResult})
    return render_template('log.html')



#Set the path to store the .csv for uploadPage.
directoryF = os.path.dirname(os.path.abspath(__file__))
csvDir = app.config['UPLOAD_FOLDER'] = "{}".format(os.path.join(directoryF, "./"))

#function of create DB for uploadPage.
def storeUploadData():
    #Create localhost mongoDB. 
    createDB01 = MongoClient('mongodb://localhost:27017/')
    newdb01 = createDB01['uploadDummyDB']
    dbCol01 = newdb01['dummyCollection']
    return newdb01

#function of open csv with pandas for uploadPage.
def pdToReadFile(file):
    #open and read the .csv file using pandas.
    head = ["userEmail", "dataTime", "weight", "walking", "running", "swimming", "bicycling"]
    readD = pd.read_csv(os.path.join(os.path.dirname(__file__),file), encoding="ISO-8859–1", names = head) 
    return readD

#Q2.1.2-define function to save .csv, open .csv and store into mongoDB.
@app.route('/uploadPage', methods=['GET', 'POST'])
def uploadPage():
    if request.method == 'POST':
        fileListGet = request.files.getlist('myUpload')
        for multiFile in fileListGet:
            #print(multiFile.filename) #testing print filename.
            multiFile.save(os.path.join(csvDir, secure_filename(multiFile.filename)))
            print('file uploaded')
            
            #pass the uploaded file name to the function-pdToReadFile(multiFile.filename).
            pdData = pdToReadFile(multiFile.filename) #pandas to read csv
            dbCol = storeUploadData() #create mongoDB.

            #To drop collection if exists for testing purpose
            collist = dbCol.list_collection_names()
            if "dummyCollection" in collist:
                dbCol.dummyCollection.drop()
                print("The collection dropped.")


            #MongoDB to store the testing data into db.
            colDatas = ''
            for i in pdData.values.tolist():
                dbCol.dummyCollection.insert_one({'email': i[0], 'dateTime': i[1], \
                'weight':i[2],'Walking': i[3], \
                'running': i[4], 'swimming': i[5], 'bicycling': i[6]})
    return render_template('upload.html')


@app.route('/dashboardPage',methods=["POST", "GET"])
def dashboardPage():
    dbCol = storeUploadData() #connect to the mongoDB.
    emailfind = dbCol.dummyCollection.find({'email': 'admin@fitwell.com'}) 
    #print(adminEmail) 

    adminEmail = ''
    
    for x in emailfind[:1]:
        adminEmail = x['email']
    print(adminEmail)

    return render_template('dashboard.html', adminEmail = adminEmail)


@app.route('/dataForChart',methods=["GET"])
def dataForChart():
    dbCol = storeUploadData() #connect to the mongoDB.
    colDatas = list(dbCol.dummyCollection.find())

    dateLi = []
    timeLi = []
    calorieLi = []

    if colDatas:
        #testing printing out data of user in mongoDB.
        for colData in colDatas:
            print('User detail of upload csv from MongoDB: ','\n',\
                'user email:', colData['email'],'\n',\
                'date & time:', colData['dateTime'],'\n',\
                'Weight:', colData['weight'],'\n',\
                'Walking:', colData['Walking'],'\n',\
                'running:' , colData['running'],'\n',\
                'swimming:', colData['swimming'],'\n',\
                'bicycling:', colData['bicycling'],'\n')
            dateLi.append(colData['dateTime'][:10])
            timeLi.append(colData['dateTime'][11:])

            weightAns = int(colData['weight'])
            walkAns =(int(colData['Walking']) * 0.084) * weightAns 
            runAns = (int(colData['running'])* 0.21) * weightAns 
            swimAns = (int(colData['swimming'])* 0.13) * weightAns 
            bicyAns = (int(colData['bicycling'])* 0.064) * weightAns

            #calculate total calorie consume. 
            calorieResult =  walkAns + runAns + swimAns + bicyAns
            calorieLi.append(calorieResult)
    return jsonify({'date': dateLi,'value': calorieLi})




'''@app.route('/loginPage', methods=['GET', 'POST'])
def loginFirst01():
    if request.method == 'POST':
        session.pop('myEmailUser', None)
        if request.form['myPws'] == "password":
            #session['myEmailUser']= request.form['myEmailUser']
            return redirect(url_for('loggedPage'))
    return render_template('index.html')

@app.route('/logPage')
def loggedPage():
    return render_template('log.html')'''

if __name__ == '__main__':
    app.run(debug=True)