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

    # require to insert records
    def __init__(self, name):
        self.name = name
        


#Define Route
@app.route("/")
def index():
    return render_template('index.html')

#Define Route for the category
@app.route("/categories")
def categories():
    #get the category from the database
    categories = Category.query.all()
    return render_template('category.html', categories=categories)

@app.route("/addCategory")
def addCategory():
    return render_template('add_category.html')

@app.route("/validCategory", methods=['POST'])
def validCategory():
    _name = request.form['inputName']
    # validate the received values
    if _name:
        # Insert Record Statement
        newCategory = Category(_name)
        db.session.add(newCategory)
        db.session.commit()
        return redirect('/categories')
    else:
        return redirect('/addCategory')

@app.route("/editCategory/<id>", methods=['GET'])
def editCategory(id):
    #query from the database
    category=Category.query.filter_by(id=id).first()
    return render_template('edit_category.html',category=category) 

@app.route("/updateCategory", methods=['POST'])
def updateCategory():
    _id = request.form['inputId']
    _name = request.form['inputName']
    # validate the received values
    if _name and _id:
        # Insert Record Statement
        updateCategory=Category.query.filter_by(id=_id).first()
        updateCategory.name=_name
        db.session.commit();
        return redirect('/categories')
    else:
        return redirect('/categories') 


@app.route("/deleteCategory/<id>", methods=['GET'])
def deleteCategory(id):
    #query from the database
    delCategory=Category.query.filter_by(id=id).first()
    db.session.delete(delCategory)
    db.session.commit();
    return redirect('/categories')
    
        
if __name__ == "__main__":
    app.run()