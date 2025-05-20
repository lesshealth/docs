from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'wallpapers.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/products')
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM Product').fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/materials')
def materials():
    conn = get_db_connection()
    materials = conn.execute('SELECT * FROM Material').fetchall()
    conn.close()
    return render_template('materials.html', materials=materials)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            conn = get_db_connection()
            conn.execute('INSERT INTO Product (Name) VALUES (?)', (name,))
            conn.commit()
            conn.close()
            return redirect('/products')
    return render_template('add_product.html')


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM Product WHERE ID = ?', (product_id,)).fetchone()

    if not product:
        conn.close()
        return f"Продукт с ID {product_id} не найден", 404

    if request.method == 'POST':
        new_name = request.form['name']
        if new_name:
            conn.execute('UPDATE Product SET Name = ? WHERE ID = ?', (new_name, product_id))
            conn.commit()
            conn.close()
            return redirect('/products')

    conn.close()
    return render_template('edit_product.html', product=product)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()

    product = conn.execute('SELECT * FROM Product WHERE ID = ?', (product_id,)).fetchone()
    if not product:
        conn.close()
        return f"Продукт с ID {product_id} не найден", 404

    materials = conn.execute("""
        SELECT Material.Name, Material.Cost, ProductMaterial.Quantity
        FROM ProductMaterial
        JOIN Material ON Material.ID = ProductMaterial.MaterialID
        WHERE ProductMaterial.ProductID = ?
    """, (product_id,)).fetchall()

    conn.close()
    return render_template('product_detail.html', product=product, materials=materials)


if __name__ == '__main__':
    app.run(debug=True)
