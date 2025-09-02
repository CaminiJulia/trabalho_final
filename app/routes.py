# app/routes.py

from flask import request, jsonify, Blueprint, render_template, redirect, url_for
from . import db
from .models import Produto

main_bp = Blueprint('main', __name__)

# --- ROTAS DA INTERFACE DE USUÁRIO (UI) ---

@main_bp.route('/', methods=['GET'])
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@main_bp.route('/adicionar', methods=['POST'])
def adicionar_produto_form():
    # ... (código existente, sem alterações)
    nome = request.form.get('nome')
    preco = request.form.get('preco')
    if nome and preco:
        novo_produto = Produto(nome=nome, preco=float(preco))
        db.session.add(novo_produto)
        db.session.commit()
    return redirect(url_for('main.index'))

# ROTA NOVA PARA MOSTRAR A PÁGINA DE EDIÇÃO
@main_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def pagina_editar(id):
    produto = db.session.get(Produto, id)
    if produto is None:
        return redirect(url_for('main.index')) # Se não achar, volta pra home

    if request.method == 'POST':
        # Lógica para salvar os dados do formulário
        produto.nome = request.form.get('nome')
        produto.preco = float(request.form.get('preco'))
        db.session.commit()
        return redirect(url_for('main.index'))

    # Se for GET, apenas mostra a página com os dados do produto
    return render_template('editar.html', produto=produto)


@main_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_produto_form(id):
    # ... (código existente, sem alterações)
    produto = db.session.get(Produto, id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
    return redirect(url_for('main.index'))

# --- ROTAS DA API ---

@main_bp.route('/api/produtos', methods=['POST'])
def criar_produto_api():
    # ... (código existente, sem alterações)
    dados = request.get_json()
    if not dados or 'nome' not in dados or 'preco' not in dados:
        return jsonify({'erro': 'Dados incompletos'}), 400
    novo_produto = Produto(nome=dados['nome'], preco=dados['preco'])
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify(novo_produto.to_json()), 201

# ROTA NOVA PARA ATUALIZAR UM PRODUTO VIA API
@main_bp.route('/api/produtos/<int:id>', methods=['PUT'])
def atualizar_produto_api(id):
    produto = db.session.get(Produto, id)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    dados = request.get_json()
    # Usamos .get() para permitir atualizações parciais
    produto.nome = dados.get('nome', produto.nome)
    produto.preco = dados.get('preco', produto.preco)
    db.session.commit()
    return jsonify(produto.to_json())


@main_bp.route('/api/produtos', methods=['GET'])
def get_produtos_api():
    # ... (código existente, sem alterações)
    produtos = Produto.query.all()
    return jsonify([produto.to_json() for produto in produtos])

@main_bp.route('/api/produtos/<int:id>', methods=['GET'])
def get_produto_api(id):
    # ... (código existente, sem alterações)
    produto = db.session.get(Produto, id)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify(produto.to_json())

@main_bp.route('/api/produtos/<int:id>', methods=['DELETE'])
def deletar_produto_api(id):
    # ... (código existente, sem alterações)
    produto = db.session.get(Produto, id)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto deletado com sucesso'})