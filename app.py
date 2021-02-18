from flask import Flask,get_flashed_messages,redirect,render_template,request,url_for,flash
# from wtforms import StringField,TextAreaField,SubmitField,SelectField,RadioField
# from flask_wtf import FlaskForm
# from wtforms.validators import DataRequired,Email,ValidationError
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail


app = Flask(__name__)


ENV = 'prod'

if ENV =='dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = '' 

else:
    app.debug = False
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

    
# suppress warnings {optional}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


########### Not Used ##############
# class feedbackForm(FlaskForm):
#     customer_name = StringField('Customer Name',validators=[DataRequired()])
#     dealer = SelectField('Dealer',validators=[DataRequired()])
#     rating = RadioField('Please rate your dealer',validators=[DataRequired()])
#     comment = TextAreaField('Comment your experience') 
#     submit = SubmitField('Submit')    



######### Model ##############
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    customer = db.Column(db.String(25),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    dealer = db.Column(db.String(25),nullable=False)
    rating = db.Column(db.Integer,nullable=False)
    comment = db.Column(db.Text(),nullable=True)

    def __init__(self,customer,email,dealer,rating,comment):
        self.customer = customer
        self.email = email
        self.dealer = dealer
        self.rating = rating
        self.comment = comment


########### Routes #############3
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/success',methods=['GET'])
def success():
    return render_template('success.html')

@app.route('/submit',methods=['POST'])
def submit():

    customer_name = request.form['customer_name']
    email = request.form['email']
    dealer = request.form['dealer']
    rating = request.form['rating']
    comment = request.form['comment']

    print(customer_name,email,dealer,rating,comment)

    if customer_name !='':
        if email !='':
            customer = Feedback.query.filter_by(email = email).first()
            if customer:
                flash('Feedback with this email was already sent! |  check the email entered')
                return redirect('/')
            else:
                if dealer !='':
                    feedback = Feedback(customer_name,email,dealer,rating,comment)

                    db.session.add(feedback)
                    db.session.commit()

                    send_mail(customer_name,email,dealer,rating,comment)

                    return render_template('success.html')
                else:
                    flash('Please select a Dealer !')
                    return redirect('/')
        else:
            flash('Email is required !')
            return redirect('/')

    else:
        flash('Customer name is required !')
        return redirect('/')

############# Run App #############
if __name__ == '__main__':
    app.run()
