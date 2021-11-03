from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask , redirect , url_for
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Register125@localhost/Assignment3'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    password = db.Column('password', db.Unicode)
    token = db.Column('token', db.Unicode)

    def __init__(self,id,name,password,token):
        self.id = id
        self.name = name
        self.password = password
        self.token = token


############    _FOR CHECK USERS IN DATABASE_    ################
# users = User.query.all()   
# @app.route('/')
# def d():
#     output = []
#     for user in users:
#         user_data = {}
#         user_data['id'] = user.id
#         user_data['name']=user.name
#         user_data['pass']=user.password
#         user_data['token']=user.token
#         output.append(user_data)

#     return jsonify({'users':output})
########################################################


@app.route('/login')
def login():

    auth = request.authorization

    if auth:
        user = User.query.filter_by(name = auth.username).first()

        if user:
            if user.password == auth.password:   
                token = jwt.encode({'user' : auth.username , 'exp':datetime.utcnow() + timedelta(minutes=30)}, str(app.config['SECRET_KEY']))
                
                if token :
                    update_token = User.query.filter_by(id = user.id).first()
                    update_token.token = str(token)
                    db.session.commit()
                return jsonify({'token': token })
           
            return '<h1>We found login {} but with incorrect password </h1>'.format(auth.username)
        
        return '<h1>Could not found a user with login:{} </h1>'.format(auth.username) 
        
        
    
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required'})
    
# @app.route('/protected/<string:token>')
# def protected(token):
#     return 'The string value is :' + token

@app.route('/protected')
def protected():

    token = request.args.get('token')

    protected_user= User.query.all()

    for user in protected_user:
        if token == user.token:
            return "<h1>Hello, token which is provided is correct </h1>, "

    return "<h1>Hello, Could not verify the token </h1>"

    

    # return '''<h1>The token value is: {}</h1>'''.format(token)
    # return redirect(url_for('protected',token = str(tok)))







if __name__ == '__main__':
        app.run(debug=True)