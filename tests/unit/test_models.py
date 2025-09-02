from app.models import Produto

def test_criação_produto():
    """
    Testa se um objeto Produto pode ser criado corretamente,
    sem interagir com o banco de dados.
    """
    p = Produto(nome="Notebook", preco=3500.00)
    assert p.nome == "Notebook"
    assert p.preco == 3500.00

def test_produto_to_json():
    """
    Testa se a conversão para JSON funciona como esperado.
    """
    p = Produto(id=1, nome="Mouse", preco=99.90)
    p_json = p.to_json()
    assert p_json['id'] == 1
    assert p_json['nome'] == "Mouse"
    assert p_json['preco'] == 99.90