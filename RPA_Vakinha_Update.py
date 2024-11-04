#PETICOS - RPA Vakinha 🐶😺❤️
#--------------------------------------------------------------------------

#IMPORTS:
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import psycopg2 as pg
import os
from dotenv import load_dotenv
from time import sleep

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

#Função que atualiza as informações de cada vakinha:
def atualizando_dados(link_vakinha):
    #Explicação do que é cada parametro:
    '''
    - link_vakinha = link da vakinha que deverá ser atualizada.
    - id_pet = id do pet que a vakinha é relacionada.
    - id_user = id do user que é dono do pet.
    '''

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

    #Obtendo o valor arrecado na vakinha:
    total_donated_temp = driver_vakinha.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div/span').text

    #Obtendo a meta da vakinha:
    goal_amount_temp = driver_vakinha.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div/div[3]/span').text

    #Obtendo a quantidade de pessoas que já doaram:
    supporters_amount_temp = driver_vakinha.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div/div[3]/div/div[4]/span').text

    #--------------------------------------------------------------------------
    #Tratando os dados extraidos:

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
    #Executando procedure para atualizar o banco passando os valores atualizados:
    cursor.execute("CALL update_vakinha(%s, %s, %s, %s, %s)", (link_vakinha, total_donated, goal_amount, supporters_amount, total_percentage))

    #Comitando:
    conn.commit()

    #Desconectando:
    cursor.close()
    conn.close()


#Lendo o link de todas as vakinhas que estão no banco:
cursor.execute("SELECT link FROM vakinha")
tabela = cursor.fetchall()[0]

#Percorrendo cada link para atualizar os valores:
for i in tabela:
    #Passando o link da vakinha que deve ser atualizado para a função de atualização:
    atualizando_dados(i)

    #Dando um tempo entre as atualizações:
    sleep(3)