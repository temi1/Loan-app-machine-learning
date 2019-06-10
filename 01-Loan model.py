import pandas as pd
from sklearn.externals import joblib
import pickle
from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField,IntegerField,DateTimeField,RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired


app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'

# Now create a WTForm Class
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html
class InfoForm(FlaskForm):
    '''
    This general class gets a lot of form about puppies.
    Mainly a way to go through many of the WTForms Fields.
    '''
    xName=StringField ('Welcome, What is your name?', validators=[DataRequired()])
    xGender=RadioField ('What Gender are you ?',choices=[('Male','Male'),('Female','Female')])
    xMarried=SelectField(u'Are you married',choices=[('Yes','Yes'),('No','No')])
    xDepend=SelectField(u'How many dependants do yo have?',choices=[('0','1'),('1','1'),('2','2'),('3+','Over 3')])
    xEducation=SelectField(u'Education Level',choices=[('Graduate','Graduate'),('Not Graduate','Not A Graduate')])
    xSelf_Employ=RadioField ('Are you Self Employed?',choices=[('Yes','Yes'),('No','No')])
    xApplicantIncome= IntegerField ('kindly disclose you Monthly income',validators=[DataRequired()])
    xCoapplicantIncome= IntegerField('kindly disclose the coapplicant Monthly income',validators=[DataRequired()])
    xLoanAmount= IntegerField('kindly disclose the amount you need',validators=[DataRequired()])
    xLoan_Amount_Term= SelectField(u'How long do you need the loan for',choices=[('12','12'),('36','36'),('60','60'),('84','84'),('120','120'),('180','180'),('240','240'),('300','300'),('360','360'),('480','480')])
    xCredit=SelectField(u'Have you taken Loan before',choices=[('1','Yes'),('0','No')])
    xPropty= SelectField(u'Which of these propery area do you stay?',choices=[('Urban','Urban'),('Semiurban','Semiurban'),('Rural','Rural')])

    submit = SubmitField('Submit')



@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = InfoForm()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        # Grab the data from the breed on the form.

        session['xName']=form.xName.data
        session['xGender']=form.xGender.data
        session['xMarried']=form.xMarried.data
        session['xDepend']=form.xDepend.data
        session['xEducation']=form.xEducation.data
        session['xSelf_Employ']=form.xSelf_Employ.data
        session['xApplicantIncome']=form.xApplicantIncome.data
        session['xCoapplicantIncome']=form.xCoapplicantIncome.data
        session['xLoanAmount']=form.xLoanAmount.data
        session['xLoan_Amount_Term']=form.xLoan_Amount_Term.data
        session['xCredit']=form.xCredit.data
        session['xPropty']=form.xPropty.data


        return redirect(url_for("thankyou"))


    return render_template('loan-home.html', form=form)


@app.route('/thankyou')
def thankyou():
    d= {'Gender':session['xGender'],'Education':session['xEducation'],'Married':session['xMarried'] ,'Dependents': session['xDepend'],'Self_Employed':session['xSelf_Employ'], 'Credit_History':session['xCredit'] ,'Loan_Amount_Term':session['xLoan_Amount_Term'] ,'LoanAmount':session['xLoanAmount'],'ApplicantIncome':session['xApplicantIncome'],'CoapplicantIncome':session['xCoapplicantIncome'],'Property_Area':session['xPropty']}
    d= pd.DataFrame(d,index=[0])
    X=d.copy()
    X['Credit_History'] = X['Credit_History'].astype(int)
    X['Loan_Amount_Term'] = X['Loan_Amount_Term'].astype(int)
    X=pd.get_dummies(X)
    
    with open("C:\\Users\\TEMILOLUWA\\Documents\\TemiloluwaTechnidus\\model_columns2.pkl", 'rb') as file:  
        model_col = pickle.load(file)

        
    #with open("C:\\Users\\aoluleye001\\Desktop\\Learning\\COUSERA\\Data_and_Analytics\\Python\\Forms, HTML\\Flask-Bootcamp-master\\04-Forms\\mymodel.pkl", 'rb') as file1:  
        #mymodel = pickle.load(file1)
    
    mymodel = joblib.load("C:\\Users\\TEMILOLUWA\\Documents\\TemiloluwaTechnidus\\modely.pkl")

    cols = X.columns
    def diff(li1, li2): 
        new_cols = (list(set(li1) - set(li2)))
        return new_cols
    
    new_cols = diff(model_col,cols)
    for col in new_cols:
        X[col]= 0


    print(X)
    print(mymodel)
    
    prediction = mymodel.predict(X)
    #prediction = X.iloc[0,0]
    #prediction=prediction.astype('str')

    print(prediction)

    if prediction=='Y':
        prediction="Loan Approved"
    elif prediction=='N':
        prediction="Loan Rejected"
    else:
        prediction="No Loan Status"

    #return prediction.astype('str')



    return render_template('loan-thankyou.html',prediction= prediction)


if __name__ == '__main__':
    app.run(debug=True)
