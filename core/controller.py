from os import listdir
from flask import redirect, render_template, request, url_for
from core.Models.product import Product
from core import app



@app.route("/")
def index():
    return render_template('index.html.jinja')

@app.route('/author')
def author():
    return render_template('author.html.jinja')

@app.route('/extractProduct', methods = ['GET', 'POST'])
def extractProduct():
    if request.method == 'POST':
        id = request.form.get('id')
        product = Product(id)
        product.get_name()
        if product.name is not None:
            product.extract()
            product.write_json()
            return redirect(url_for('product', id = id))
        error = "&#9888; Kod produktu jest niepoprawny. Sprawdź poprawność wpisanego kodu (znaki specjalnie nie są dozwolone)." # #HACK Special characters forbidden for security purposes
        return render_template('extractProduct.html.jinja', error = error)
    return render_template('extractProduct.html.jinja')

@app.route('/productsList')
def productsList():
    model = [product.split('.')[0] for product in listdir("core/Mocks")]
    results = []
    for p_id in model:
        result = Product(p_id)
        result.read_json()
        result.stats_counter()
        stats_model = result.stats_model()
        results.append(stats_model)

    return render_template('productsList.html.jinja', products = str(results))


@app.route('/product/<id>')
def product(id):
    model = Product(id)
    model.read_json()
    return render_template('product.html.jinja', product = model, ceneo = "https://www.ceneo.pl/{}#tab=reviews".format(model.id))

@app.route('/charts/<id>')
def charts(id):
    model = Product(id)
    model.read_json()
    model.stats_counter()
    stats_model = model.stats_model()
    return render_template('charts.html.jinja', product = stats_model)