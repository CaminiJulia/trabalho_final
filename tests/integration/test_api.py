# tests/integration/test_api.py

import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    # Cria uma instância da nossa aplicação Flask
    flask_app = create_app()

    # ---- Configuração Específica para Testes ----
    # Força a aplicação a usar um banco de dados em memória (não usa o arquivo produtos.db)
    flask_app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
    })

    # Cria um cliente de teste que nos permite fazer requisições (GET, POST, etc.)
    with flask_app.test_client() as testing_client:
        # Estabelece o contexto da aplicação. Essencial para o SQLAlchemy funcionar.
        with flask_app.app_context():
            # Cria todas as tabelas do banco de dados em memória
            db.create_all()
            # 'yield' entrega o cliente de teste para as nossas funções de teste
            yield testing_client
            # Após todos os testes neste arquivo rodarem, limpa o banco de dados
            db.drop_all()


def test_criar_e_buscar_produto(test_client):
    """
    GIVEN um cliente de teste Flask
    WHEN uma requisição POST é enviada para '/api/produtos'
    THEN um novo produto deve ser criado no banco de dados
    AND o mesmo produto pode ser recuperado com uma requisição GET
    """
    # 1. Criar um produto via API
    response_post = test_client.post('/api/produtos', json={'nome': 'Teclado Gamer', 'preco': 299.99})
    
    # Verifica se a API retornou "201 Created"
    assert response_post.status_code == 201
    assert response_post.json['nome'] == 'Teclado Gamer'

    # 2. Buscar o produto que acabamos de criar
    produto_id = response_post.json['id']
    response_get = test_client.get(f'/api/produtos/{produto_id}')

    # Verifica se a API retornou "200 OK" e os dados corretos
    assert response_get.status_code == 200
    assert response_get.json['nome'] == 'Teclado Gamer'


def test_deletar_produto(test_client):
    """
    GIVEN um cliente de teste Flask com um produto existente
    WHEN uma requisição DELETE é enviada para o endpoint do produto
    THEN o produto deve ser removido do banco de dados
    """
    # 1. Primeiro, precisamos de um produto para deletar. Vamos criar um.
    produto_para_deletar = test_client.post('/api/produtos', json={'nome': 'Produto para Deletar', 'preco': 10.0})
    assert produto_para_deletar.status_code == 201
    produto_id = produto_para_deletar.json['id']

    # 2. Deletar o produto via API
    response_delete = test_client.delete(f'/api/produtos/{produto_id}')
    assert response_delete.status_code == 200
    assert 'deletado com sucesso' in response_delete.json['mensagem']

    # 3. Verificar se o produto realmente foi deletado
    response_get = test_client.get(f'/api/produtos/{produto_id}')
    assert response_get.status_code == 404 # Esperamos "Not Found"

    # tests/integration/test_api.py

# ... (outros testes existentes) ...

def test_atualizar_produto_api(test_client):
    """
    GIVEN um produto existente
    WHEN uma requisição PUT é enviada para a API
    THEN o produto deve ser atualizado no banco de dados
    """
    # 1. Criar um produto inicial
    response_post = test_client.post('/api/produtos', json={'nome': 'Produto Original', 'preco': 100.0})
    assert response_post.status_code == 201
    produto_id = response_post.json['id']

    # 2. Enviar a requisição de atualização (PUT)
    dados_atualizados = {'nome': 'Produto Atualizado', 'preco': 150.50}
    response_put = test_client.put(f'/api/produtos/{produto_id}', json=dados_atualizados)
    
    # 3. Verificar se a atualização foi bem-sucedida
    assert response_put.status_code == 200
    assert response_put.json['nome'] == 'Produto Atualizado'
    assert response_put.json['preco'] == 150.50