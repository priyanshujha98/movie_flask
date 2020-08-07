from flask import Flask, render_template, make_response, request, url_for, session, redirect
from flask_mail import Mail, Message
from uuid import uuid4



app = Flask(__name__)
app.secret_key = 'super secret key'
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = # Your email address
app.config['MAIL_PASSWORD'] = # Your password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

@app.route('/reset')
def reset():
    return render_template('reset.html')


@app.route('/send_pass/', methods = ['POST','GET'])
def send_pass():
    if request.method =='POST':
        var={}
        for i,j in zip(request.form.keys(),request.form.values()):
            var[i]=j
        print(var)
        msg = Message('Password Reset', sender = 'priyanshjha98@gmail.com', recipients = [var['email']])
        
        rand_token = str(uuid4())
        session['token'] = rand_token
        
        print(session['token'])
        msg.html = render_template('reset_password.html', username=var['email'], link=url_for('reset_password',email=var['email'],token=rand_token))

        
        mail.send(msg)
        return "Password was sent to your email"

@app.route('/reset_password/', methods=['GET',"POST"])
def reset_password():
    email = request.args.get('email')
    token = request.args.get('token')
    
    if session['token'] == token:
        if request.method == 'POST':
            
            # To reset the pass db
            
            return redirect(url_for('clear'))
        return render_template('new_password.html')
@app.route('/clear/')
def clear():
    session.clear()
    try:
        print('session',session['token'])
    except:
        pass
    return 'Done'

if __name__=='__main__':
    app.run(debug=False)
