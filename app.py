import os

from flask import Flask
from flask import render_template,request,redirect,url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename

app = Flask(__name__)

#SQLAlchemy configuration
#dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost:3306/resturant?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock'
app.debug = True
db = SQLAlchemy(app)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

#Create Category Model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    #Defining One to Many relationships with the relationship function on the Parent Table
    recipes = db.relationship('Recipes', backref='recipes',lazy='dynamic')

    # require to insert records
    def __init__(self, name):
        self.name = name
        
#Create Recipes
class Recipes(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    image = db.Column(db.String(100))
    price = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime)
    #Defining the Foreign Key on the Child Table
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))

    #require to insert recods
    def __init__(self,name,description,image,price,recipes,pub_date=None):
        self.name=name,
        self.description=description,
        self.image=image,
        self.price=price,
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.recipes=recipes


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


#Define Route
@app.route("/")
def index():
    return render_template('index.html')

#Define Route for the category
"""
    -----------------Category Code ----------------------
"""
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
"""
    -----------------End Category Code ----------------------
"""

"""
    -----------------Recipe Code ----------------------
"""
@app.route("/recipes")
def recipes():
    #get the recipes
    allRecipes = Recipes.query.all()
    return render_template('recipes.html',recipes=allRecipes)

@app.route("/addRecipes")
def addRecipes():
    categories = Category.query.all()
    return render_template('add_recipes.html',categories=categories)

@app.route("/validateRecipes", methods=['POST'])
def validateRecipes():
    #get the form data
    _name = request.form['inputName']
    _description = request.form['inputDescription']

    # Get the name of the uploaded file
    file = request.files['inputImage']

    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        _image = str(_id)+"_"+secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], _image))
    else:
        _image =''


    _price = request.form['inputPrice']
    _categoryId= request.form['inputCategory']

    category= Category.query.filter_by(id=_categoryId).first()
    newRecipes= Recipes(_name,_description,_image,_price,category)
    db.session.add(newRecipes)
    db.session.commit()
    return redirect('/recipes')

@app.route("/editRecipes/<id>", methods=['GET'])
def editRecipes(id):
    #query from the database
    recipes=Recipes.query.filter_by(id=id).first()
    categories = Category.query.all()
    return render_template('edit_recipes.html',recipes=recipes,categories=categories)

@app.route("/updateRecipes", methods=['POST'])
def updateRecipes():

    #get the form data
    _id = request.form['inputId']

    # get the recipies data from the databse
    updateRecipes=Recipes.query.filter_by(id=_id).first()

    _name = request.form['inputName']
    _description = request.form['inputDescription']

    # Get the name of the uploaded file
    file = request.files['inputImage']

    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        _image = str(_id)+"_"+secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], _image))
    else:
        _image =updateRecipes.image

    _checkDelete = request.form.getlist('deleteCheck')
    if _checkDelete:
        #delete file from the folder
        os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], _checkDelete[0]))
        _image =''

    _price = request.form['inputPrice']
    _categoryId= request.form['inputCategory']

    category= Category.query.filter_by(id=_categoryId).first()

    # update record
    updateRecipes.name=_name
    updateRecipes.description=_description
    updateRecipes.image=_image
    updateRecipes.price=_price
    updateRecipes.recipes=category
    db.session.commit();
    return redirect('/recipes')
 
@app.route("/deleteRecipes/<id>", methods=['GET'])
def deleteRecipes(id):
    #query from the database
    delRecipes=Recipes.query.filter_by(id=id).first()
    os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], delRecipes.image))
    db.session.delete(delRecipes)
    db.session.commit();
    return redirect('/recipes')   
    
        
if __name__ == "__main__":
    app.run()