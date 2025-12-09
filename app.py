from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Banco de dados em memória
pessoas = []

# -------------------------------------------------------------------
# LISTAR
# -------------------------------------------------------------------
@app.route("/")
def index():
    html = """
    <html>
    <head>
        <title>Cadastro de Clientes</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-light">
        <div class="container py-5">

            <h1 class="text-center mb-4">Cadastro de Clientes</h1>

            <!-- Formulário -->
            <div class="card mb-4">
                <div class="card-header">Cadastrar Novo Cliente</div>
                <div class="card-body">
                    <form method="POST" action="/add">
                        <div class="mb-3">
                            <label class="form-label">Nome Completo</label>
                            <input type="text" name="nome" class="form-control" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">CPF</label>
                            <input type="text" name="cpf" class="form-control" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">CEP Residencial</label>
                            <input type="text" name="cep" class="form-control" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">WhatsApp</label>
                            <input type="text" name="whatsapp" class="form-control" required>
                        </div>

                        <button class="btn btn-primary">Salvar</button>
                    </form>
                </div>
            </div>

            <!-- Lista -->
            <h2 class="mb-3">Clientes Cadastrados</h2>

            <table class="table table-striped table-bordered">
                <thead class="table-dark">
                    <tr>
                        <th>Nome</th>
                        <th>CPF</th>
                        <th>CEP</th>
                        <th>WhatsApp</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                {% for pessoa in pessoas %}
                    <tr>
                        <td>{{ pessoa.nome }}</td>
                        <td>{{ pessoa.cpf }}</td>
                        <td>{{ pessoa.cep }}</td>
                        <td>{{ pessoa.whatsapp }}</td>
                        <td>
                            <a href="/edit/{{ loop.index0 }}" class="btn btn-warning btn-sm">Editar</a>
                            <a href="/delete/{{ loop.index0 }}" class="btn btn-danger btn-sm">Excluir</a>
                        </td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>

        </div>
    </body>
    </html>
    """
    return render_template_string(html, pessoas=pessoas)

# -------------------------------------------------------------------
# CREATE
# -------------------------------------------------------------------
@app.route("/add", methods=["POST"])
def add():
    nova = {
        "nome": request.form["nome"],
        "cpf": request.form["cpf"],
        "cep": request.form["cep"],
        "whatsapp": request.form["whatsapp"]
    }
    pessoas.append(nova)
    return redirect("/")

# -------------------------------------------------------------------
# UPDATE
# -------------------------------------------------------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        pessoas[id]["nome"] = request.form["nome"]
        pessoas[id]["cpf"] = request.form["cpf"]
        pessoas[id]["cep"] = request.form["cep"]
        pessoas[id]["whatsapp"] = request.form["whatsapp"]
        return redirect("/")

    pessoa = pessoas[id]

    html = """
    <html>
    <head>
        <title>Editar Cliente</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">

            <h1 class="mb-4">Editar Cliente</h1>

            <form method="POST" class="card p-4">
                <div class="mb-3">
                    <label class="form-label">Nome Completo</label>
                    <input type="text" name="nome" value="{{ pessoa.nome }}" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">CPF</label>
                    <input type="text" name="cpf" value="{{ pessoa.cpf }}" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">CEP</label>
                    <input type="text" name="cep" value="{{ pessoa.cep }}" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">WhatsApp</label>
                    <input type="text" name="whatsapp" value="{{ pessoa.whatsapp }}" class="form-control" required>
                </div>

                <button class="btn btn-success">Salvar</button>
            </form>

        </div>
    </body>
    </html>
    """
    return render_template_string(html, pessoa=pessoa)

# -------------------------------------------------------------------
# DELETE
# -------------------------------------------------------------------
@app.route("/delete/<int:id>")
def delete(id):
    pessoas.pop(id)
    return redirect("/")

# -------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

