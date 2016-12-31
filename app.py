from flask import Flask
from flask import render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#SQLAlchemy configuration
#dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost:3306/resturant?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock'
db = SQLAlchemy(app)

#Create Category Model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


#Define Route
@app.route("/")
def index():
	return render_template('index.html')

@app.route("/categories")
def categories():
	#get the category from the database
	categories = Category.query.all()
	return render_template('category.html', categories=categories)

if __name__ == "__main__":
    app.run()