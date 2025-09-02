# tests/system/test_e2e.py

import pytest
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from app import create_app, db

# --- Fixtures (Configuração do Ambiente de Teste) ---

@pytest.fixture(scope='class')
def test_app():
    """Cria e configura uma nova instância da aplicação para cada classe de teste."""
    app = create_app()
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
    })
    
    with app.app_context():
        db.create_all()
        yield app # Entrega a app para os testes
        db.drop_all()

@pytest.fixture(scope='class')
def live_server(test_app):
    """Inicia a aplicação Flask em uma thread separada."""
    server_url = "http://127.0.0.1:5002"
    
    def run_server():
        test_app.run(port=5002)

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1) # Aguarda o servidor iniciar
    yield server_url

@pytest.fixture(scope='class')
def browser():
    """Configura e fornece uma instância do navegador, e a fecha no final."""
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()

# --- Classe de Teste ---

@pytest.mark.usefixtures("live_server")
class TestLiveServer:
    def test_fluxo_crud_completo(self, live_server, browser):
        """
        GIVEN a aplicação Flask rodando
        WHEN um usuário acessa a página, cria um produto e depois o deleta
        THEN o produto deve aparecer e depois desaparecer da lista na tela
        """
        # 1. Acessar a página
        browser.get(live_server)
        wait = WebDriverWait(browser, 10)

        # 2. Criar um novo produto
        nome_produto = "Cadeira Gamer Teste"
        preco_produto = "1250.50"

        browser.find_element(By.ID, "nome").send_keys(nome_produto)
        browser.find_element(By.ID, "preco").send_keys(preco_produto)
        browser.find_element(By.XPATH, "//button[text()='Adicionar']").click()

        # 3. Verificar se o produto aparece na lista
        # Espera até que uma célula da tabela contenha o nome do novo produto
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//tbody"), nome_produto))

        # 4. Deletar o produto
        # Encontra o botão de deletar na mesma linha do produto que criamos e clica nele
        delete_button = browser.find_element(By.XPATH, f"//td[text()='{nome_produto}']/following-sibling::td/form/button")
        delete_button.click()

        # 5. Verificar se o produto foi removido da lista
        # Espera até que o elemento com o nome do produto não esteja mais visível
        wait.until(EC.invisibility_of_element_located((By.XPATH, f"//td[text()='{nome_produto}']")))

        # tests/system/test_e2e.py

# ... (código das fixtures sem alteração) ...

@pytest.mark.usefixtures("live_server")
class TestLiveServer:
    def test_fluxo_crud_completo(self, live_server, browser):
        # ... (passos 1 e 2 de acessar a página e criar o produto, sem alterações) ...
        browser.get(live_server)
        wait = WebDriverWait(browser, 10)
        nome_produto = "Cadeira Gamer Teste"
        preco_produto = "1250.50"
        browser.find_element(By.ID, "nome").send_keys(nome_produto)
        browser.find_element(By.ID, "preco").send_keys(preco_produto)
        browser.find_element(By.XPATH, "//button[text()='Adicionar']").click()
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//tbody"), nome_produto))

        # 3. NOVO PASSO: Editar o produto
        # Encontra o link de "Editar" na linha do produto que criamos e clica nele
        browser.find_element(By.XPATH, f"//td[text()='{nome_produto}']/following-sibling::td/a[text()='Editar']").click()

        # Espera a página de edição carregar e encontra os campos
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        nome_editado = "Cadeira de Escritório TOP"
        preco_editado = "1800.00"
        
        nome_input = browser.find_element(By.ID, "nome")
        preco_input = browser.find_element(By.ID, "preco")

        # Limpa os campos e insere os novos valores
        nome_input.clear()
        nome_input.send_keys(nome_editado)
        preco_input.clear()
        preco_input.send_keys(preco_editado)
        
        # Salva as alterações
        browser.find_element(By.XPATH, "//button[text()='Salvar Alterações']").click()

        # 4. Verificar se a edição aparece na lista
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//tbody"), nome_editado))
        # Verifica também se o nome antigo sumiu
        wait.until(EC.invisibility_of_element_located((By.XPATH, f"//td[text()='{nome_produto}']")))

        # 5. Deletar o produto (agora deletamos o produto editado)
        delete_button = browser.find_element(By.XPATH, f"//td[text()='{nome_editado}']/following-sibling::td/form/button")
        delete_button.click()

        # 6. Verificar se o produto foi removido da lista
        wait.until(EC.invisibility_of_element_located((By.XPATH, f"//td[text()='{nome_editado}']")))