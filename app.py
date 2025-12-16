

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database')
os.makedirs(db_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path, 'events.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# MODEL
# ==========================
class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    idade_minima = db.Column(db.Integer)
    data = db.Column(db.Date)
    hora = db.Column(db.Time)
    cep = db.Column(db.String(20))
    uf = db.Column(db.String(2))
    cidade = db.Column(db.String(100))
    local = db.Column(db.String(200))


def create_tables():
    with app.app_context():
        db.create_all()


# ==========================
# ROTAS
# ==========================
@app.route("/")
def index():
    eventos = Evento.query.order_by(Evento.data).all()
    return render_template("index.html", eventos=eventos)


@app.route("/cadastrar-evento", methods=["GET", "POST"])
def cadastrar_evento():
    if request.method == "POST":
       
            nome=request.form.get("evento")
            idade = request.form.get("idade")
            data_str= request.form.get("data")
            hora_str= request.form.get("hora")
            cep=request.form.get("cep")
            uf=request.form.get("uf")
            cidade=request.form.get("cidade")
            local=request.form.get("local")
        
            idade_val = int(idade) if idade else None
            data_val = datetime.strptime(data_str, "%Y-%m-%d").date() if data_str else None
            hora_val = datetime.strptime(hora_str, "%H:%M").time() if hora_str else None

            evento = Evento(
                nome=nome, 
                idade_minima=idade_val, 
                data=data_val, 
                hora=hora_val, 
                cep=cep,
                uf=uf, 
                cidade=cidade, 
                local=local

            )
            db.session.add(evento)
            db.session.commit()
            flash("Evento cadastrado com sucesso!")
            return redirect(url_for("index"))

    return render_template("cadastrar-evento.html", evento=None)


@app.route("/editar-evento/<int:id>", methods=["GET", "POST"])
def editar_evento(id):
    evento = Evento.query.get_or_404(id)

    if request.method == "POST":
        evento.nome = request.form.get("evento")
        evento.idade_minima = int(request.form.get("idade")) if request.form.get("idade") else None
        evento.data = datetime.strptime(request.form.get("data"), "%Y-%m-%d").date()
        evento.hora = datetime.strptime(request.form.get("hora"), "%H:%M").time() if request.form.get("hora") else None
        evento.cep = request.form.get("cep")
        evento.uf = request.form.get("uf")
        evento.cidade = request.form.get("cidade")
        evento.local = request.form.get("local")

        db.session.commit()
        flash("Evento atualizado com sucesso!")
        return redirect(url_for("index"))

    return render_template("cadastrar-evento.html", evento=evento)


@app.route("/excluir-evento/<int:id>", methods=["POST"])
def excluir_evento(id):
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    flash("Evento excluído com sucesso!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
