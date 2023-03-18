from os import listdir
from core.Models.product import Product
from core import app



@app.route("/")
def index():
    return "Hello World"

@app.route('/author')
def author():
    return "Author"

@app.route('/extractProduct')
def extractProduct():
    return "Product"

@app.route('/productsList')
def productsList():
    model = [product.split('.')[0] for product in listdir("app/products")]
    return "ProductsList(model)"


@app.route('/product/<id>')
def product(id):
    product = Product(id)
    product.read_json()
    return "Product"


