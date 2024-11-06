#PETICOS - RPA Vakinha 🐶😺❤️
#--------------------------------------------------------------------------

#IMPORTS:
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
import psycopg2 as pg
import os
from dotenv import load_dotenv
import sys
#--------------------------------------------------------------------------

#Pegando a senha do banco no .env:
load_dotenv()
password = os.getenv('PASSWORD12')

#Conectando com o banco:
conn = pg.connect(
    dbname = "dbPeticos_2ano",
    user = "avnadmin",
    password = password,
    host = "db-peticos-cardosogih.k.aivencloud.com",
    port = 16207
)
cursor = conn.cursor()
#--------------------------------------------------------------------------

def inserindo_dados(link_vakinha, id_pet, id_user):
    #Iniciando RPA para pegar as informações da vakinha do link:

    #Entrando no link:
    #Definindo para abrir a página Web em segundo plano:
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    #"Abrindo" o Chrome:
    driver_vakinha = webdriver.Chrome(options=chrome_options)

    #Abrindo o site da vakinha:
    driver_vakinha.get(link_vakinha)

    #Dando um tempo para o carregamento da página:
    sleep(5)

    #--------------------------------------------------------------------------
    #Pegando as informações necessários com o XPATH:

    try:
        #Obtendo título da vakinha:
        title = str(driver_vakinha.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/h1').text)

        #Obtendo a imagem da vakinha:
        image_temp = driver_vakinha.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[1]/div/a/div/picture/div/img')

        #Obetando descrição da vakinha:
        description = str(driver_vakinha.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[3]/div[2]/div/div[4]').text)

        #Obtendo o valor arrecado na vakinha:
        total_donated_temp = driver_vakinha.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div/span').text

        #Obtendo a meta da vakinha:
        goal_amount_temp = driver_vakinha.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div/div[3]/span').text

        #Obtendo a quantidade de pessoas que já doaram:
        supporters_amount_temp = driver_vakinha.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div/div[4]/span').text
    except:
        return 'Não foi possível inserir essa vakinha'

    #--------------------------------------------------------------------------
    #Tratando os dados extraidos:

    #Tratando o campo imagem:
    image = str(image_temp.get_attribute('src'))

    #-------------------------------------------------------------
    #Tratando o campo total_donated:
    #Substituindo "R$" por vazio:
    total_donated_temp = total_donated_temp.replace("R$ ", "")

    #Substituindo o "." por vazio:
    total_donated_temp = total_donated_temp.replace(".", "")

    #Substituindo "," por ".", para poder transformar em número:
    total_donated = float(total_donated_temp.replace(",", "."))

    #-------------------------------------------------------------
    #Tratando o campo goal_amount:
    #Substituindo "R$" por vazio, para poder transformar em número:
    goal_amount_temp = goal_amount_temp.replace("R$ ", "")

    #Substituindo o "." por vazio:
    goal_amount_temp = goal_amount_temp.replace(".", "")

    #Substituindo "," por ".", para poder transformar em número:
    goal_amount = float(goal_amount_temp.replace(",", "."))

    #-------------------------------------------------------------
    #Tratando o campo supporters_amount:
    #Transformando o campo em int:
    supporters_amount = int(supporters_amount_temp)

    #-------------------------------------------------------------
    #Calculando porcentagem arrecadada do total:
    total_percentage = round(total_donated/goal_amount, 2) * 100

    #--------------------------------------------------------------------------
    #Inserindo os dados no banco:
    #Executando procedure para inserir os dados no banco:
    cursor.execute("CALL insert_vakinha(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_pet, title, link_vakinha, total_donated, goal_amount, supporters_amount, total_percentage, description, image, id_user))

    #Comitando:
    conn.commit()

    #Desconectando:
    cursor.close()
    conn.close()

#Verifica se os parametros da função foram passados corretamente:
if len(sys.argv) > 1:
    #Lista com os parametros:
    values = sys.argv
    #Chamando a função:
    inserindo_dados(values[1], values[2], values[3])
