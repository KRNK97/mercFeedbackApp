import smtplib
from email.mime.text import MIMEText

def send_mail(customer,email,dealer,rating,comment):

    port = 2525
    server = "smtp.mailtrap.io"
    user = "63321ae3f64dc3"
    password = "80c1fd84eb8aec"
    message = f'<h3>Mercedes-Benz Feedback Submission -</h3><ul><li>Customer Name: {customer}</li><li>Customer Email: {email}</li><li>Dealer Name: {dealer}</li><li>Rating : {rating}</li><li>Comment : {comment}</li></ul>'

    sender_email = 'examplesender@gmail.com'
    receiver_email = 'examplereceiver@gmail.com'

    msg = MIMEText(message,'html')
    msg['Subject'] = 'Mercedes Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(server,port) as server:
        server.login(user,password)
        server.sendmail(sender_email,receiver_email,msg.as_string())

