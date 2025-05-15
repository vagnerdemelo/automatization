from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Selenium
options = Options()
service = Service(executable_path="/usr/lib/chromium-browser/chromedriver")

# Logs Geral
logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)s - %(levelname)s - %(message)s',
  filename='app.log',
  filemode='a'
)

logger = logging.getLogger('main_logger')

#Logs de Erro
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)

error_handler = logging.FileHandler('errors.log')
error_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
error_handler.setFormatter(formatter)

if not error_logger.handlers:
  error_logger.addHandler(error_handler)


logger.info("Iniciando o scraper...")
time.sleep(2)

logger.info("Reading XLSX file...")

df = pd.read_excel(os.getenv("PLANILHA"))
codigos = df['codigo'].tolist()
logger.info(f"Total de códigos lidos: {codigos}")

logger.info(f"Initializing connection to the website...")
driver = webdriver.Chrome(service=service, options=options)
driver.get(os.getenv("SITE"))

logger.info("Login in progress...")
# Login
campo_usuario = driver.find_element(By.ID, "basic_email")
campo_senha = driver.find_element(By.ID, "basic_password")

campo_usuario.clear()
campo_usuario.send_keys(os.getenv("USUARIO"))
time.sleep(1)
campo_senha.clear()
campo_senha.send_keys(os.getenv("SENHA"))
time.sleep(1)

button_login = driver.find_element(By.XPATH, "//button[text()='Logar']")
button_login.click()
time.sleep(10)

logger.info("Login completed.")
cookie = driver.find_element(By.XPATH, "//span[text()='Aceitar']")
cookie.click()
time.sleep(3)

fechar = driver.find_element(By.XPATH, "//span[text()='Fechar']")
fechar.click()
time.sleep(3)

logger.info("Accessing the products page...")
try:

  produtos_menu = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'title-content') and text()='Produtos']"))
  )

  # Passa o mouse por cima usando ActionChains
  actions = ActionChains(driver)
  actions.move_to_element(produtos_menu).perform()
  time.sleep(10)

  logger.info("Menu Produtos encontrado e mouse posicionado.")
  WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-menu-submenu-popup')]"))
  )
  logger.info("Submenu encontrado.")

  submenu_opcao = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//li[contains(@data-menu-id, '/app/skus')]"))
  )
  logger.info("Submenu 'Produtos e Skus' encontrado e clicável.")

  submenu_opcao.click()
  time.sleep(2)
except Exception as e:
  # Se der erro, salva o HTML atual para análise
  error_logger.error(f"Erro: {e}")
  error_logger.error("Erro ao acessar a página de produtos.")
  driver.quit()
  raise e

logger.info("Search for products in progress...")

for codigo in codigos:
  busca = driver.find_element(By.NAME, "Search")
  busca.send_keys(codigo)
  time.sleep(1)
  busca.send_keys(Keys.ENTER)
  time.sleep(3)
  linhas = driver.find_elements(By.XPATH, "//table//tbody/tr[2]")

  for linha in linhas:
    qtde = linha.find_element(By.XPATH, ".//td[7]").text
    product_type = linha.find_element(By.XPATH, ".//td[5]").text
    logger.info(f"Produto: {codigo} - Quantidade: {qtde} - Tipo: {product_type}" )

    if qtde == "0" and product_type == "Sku":
      editar = linha.find_element(By.XPATH, ".//td[53]//span[contains(@name,'EditOutlined')]")
      editar.click()
      time.sleep(3)

      try:
        address = driver.find_element(By.XPATH, "//div[@class='ant-tabs-tab']//div[text()='Endereços']")
        address.click()
        time.sleep(5)

        delete = driver.find_elements(By.CSS_SELECTOR, 'span[name="DeleteOutlined"]')
        logger.info(f"Delete Elements:{delete}")
        logger.info(f"Delete Elements Count: {len(delete)}")
        for i in range(len(delete)):
          logging.info(f"Delete Element Text{i}: {delete[i].text}")
        time.sleep(1)
        delete[-1].click()
        time.sleep(1)

        confirm = driver.find_element(By.XPATH, "//span[text()='Sim']")
        confirm.click()
        time.sleep(3)
        logger.info(f"Endereço do produto {codigo} excluído com sucesso.")


        general = driver.find_elements(By.XPATH, "//div[@class='ant-tabs-tab']//div[text()='Geral']")
        logger.info(f"General Elements:{general}")
        logger.info(f"General Elements Count: {len(general)}")
        for i in range(len(general)):
          logger.info(f"General Element Text {i}: ---> {general[i].text}")
          logger.info(f"General Element Tag Name: ---> {general[i].tag_name}")
          logger.info(f"General Element Class Name: ---> {general[i].get_attribute('class')}")
          logger.info(f"General Element ID: ---> {general[i].get_attribute('id')}")
          logger.info(f"General Element HTML: ---> {general[i].get_attribute('outerHTML')}")

        general[0].click()
        time.sleep(5)

        dropdowns = driver.find_elements(By.CLASS_NAME, "ant-select-selector")
        dropdowns[0].click()
        time.sleep(1)
        opcao_kit_virtual = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and text()='Kit virtual - Kit']")
          )
        )
        opcao_kit_virtual.click()
        time.sleep(1)
        logger.info(f"Produto {codigo}: Tipo de produto alterado para 'kit'.")

        save = driver.find_element(By.NAME, "SaveOutlined")
        save.click()
        time.sleep(2)

        confirm_save = driver.find_element(By.XPATH, "//span[text()='Sim']")
        confirm_save.click()
        time.sleep(5)

        logger.info(f"Produto {codigo} editado com sucesso.")

        # sku = driver.find_element(By.XPATH, "//span[text()='Produtos e Skus']")
        # sku.click()
        # time.sleep(2)

        close_product = driver.find_elements(By.XPATH, "//i[@class='icon icon-close']")
        close_product[1].click()
        time.sleep(2)
        logger.info(f"Produto {codigo} fechado com sucesso.")

      except Exception as e:
        error_logger.error(f"Erro ao editar produto {codigo}: {e}")
        error_logger.error("Erro ao acessar a página de produtos.")
        # driver.quit()
        with open("erro.html", "w", encoding="utf-8") as f:
          f.write(driver.page_source)
        error_logger.info("Página salva em erro.html para análise.")
        raise e

  busca.send_keys(Keys.CONTROL + "a")
  busca.send_keys(Keys.BACKSPACE)
  time.sleep(1)

driver.quit()
logger.info("Processo finalizado com sucesso.")
