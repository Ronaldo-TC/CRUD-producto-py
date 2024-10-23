from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super secret key"

def generar_id_producto():
    if 'productos' in session and len(session['productos']) > 0:
        return max(producto['id'] for producto in session['productos']) + 1
    else:
        return 1

@app.route("/")
def index():
    productos = session.get('productos', [])
    return render_template("index.html", productos=productos)

@app.route("/nuevo_producto", methods=["GET", "POST"])
def nuevo_producto():
    if request.method == "POST":
        id = generar_id_producto()
        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])
        fecha_vencimiento = datetime.strptime(request.form["fecha_vencimiento"], "%Y-%m-%d")
        categoria = request.form["categoria"]

        nuevo_producto = {
            "id": id,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "fecha_vencimiento": fecha_vencimiento,
            "categoria": categoria
        }

        if 'productos' not in session:
            session['productos'] = []

        session['productos'].append(nuevo_producto)
        session.modified = True
        return redirect(url_for("index"))

    return render_template("nuevo_producto.html")

@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id), None)

    if producto is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        producto["nombre"] = request.form["nombre"]
        producto["cantidad"] = int(request.form["cantidad"])
        producto["precio"] = float(request.form["precio"])
        producto["fecha_vencimiento"] = datetime.strptime(request.form["fecha_vencimiento"], "%Y-%m-%d")
        producto["categoria"] = request.form["categoria"]
        session.modified = True
        return redirect(url_for("index"))

    return render_template("editar_producto.html", producto=producto)

@app.route("/eliminar_producto/<int:id>", methods=["POST"])
def eliminar_producto(id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id), None)

    if producto:
        session['productos'].remove(producto)
        session.modified = True

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)