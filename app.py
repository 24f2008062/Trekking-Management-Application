from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy  

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"



@app.route('/')
def home():
    return 'homepage'

@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html')





if __name__ == "__main__":
    app.run(debug=True)