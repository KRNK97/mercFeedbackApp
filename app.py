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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:gopinath@localhost/mercedes' 

else:
    app.debug = False
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ftxvmnkkshojjs:b98df8eaa9edb698259f9711f080a2378166f260f4fdc36729659c422aaa9a87@ec2-3-210-23-22.compute-1.amazonaws.com:5432/d5cvra34a1lk01'

# suppress warnings {optional}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# class feedbackForm(FlaskForm):
#     customer_name = StringField('Customer Name',validators=[DataRequired()])

#     dealer = SelectField('Dealer',validators=[DataRequired()])

#     rating = RadioField('Please rate your dealer',validators=[DataRequired()])

#     comment = TextAreaField('Comment your experience') 

#     submit = SubmitField('Submit')    

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

            

            








if __name__ == '__main__':
    app.run()