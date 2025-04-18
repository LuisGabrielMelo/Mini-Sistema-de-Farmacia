
from flask import Flask, render_template, request, redirect, url_for
from models import db, Medicamento

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmacia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    medicamentos = Medicamento.query.all()
    return render_template('medicamentos.html', medicamentos=medicamentos)

@app.route('/add', methods=['POST'])
def add_medicamento():
    nombre = request.form['nombre']
    stock = int(request.form['stock'])
    precio = float(request.form['precio'])
    nuevo = Medicamento(nombre=nombre, stock=stock, precio=precio)
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit_medicamento(id):
    medicamento = Medicamento.query.get_or_404(id)
    return render_template('editar.html', medicamento=medicamento)

@app.route('/update/<int:id>', methods=['POST'])
def update_medicamento(id):
    medicamento = Medicamento.query.get_or_404(id)
    medicamento.nombre = request.form['nombre']
    medicamento.stock = int(request.form['stock'])
    medicamento.precio = float(request.form['precio'])
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_medicamento(id):
    medicamento = Medicamento.query.get_or_404(id)
    db.session.delete(medicamento)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
