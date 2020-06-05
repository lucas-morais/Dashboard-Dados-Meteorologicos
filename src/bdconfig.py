import pandas as pd
import sqlite3

def carrega_csv(arquivo):
    
    # Função para carga de dados
    # 
    # arquivo:caminho do arquivo 


    if "_clima" in arquivo:
        df = pd.read_csv(arquivo,
                    delimiter = ";",
                    usecols=list(range(1,10)),
                    dtype={'Hora':'str', 'DirecaoVento':'str'},
                    parse_dates=[['Data', 'Hora']],
                    dayfirst=True
                   )
        df.rename(columns={'Data_Hora':'Horario'}, inplace=True)
        df.set_index('Horario', inplace=True)
    else :
        try:
            df = pd.read_csv(arquivo,
                            sep=";" 
                            )
        except:
            raise Exception("Arquivo não existe")
                
    return df

def cria_bd(db_file):
        
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def cria_conexao(db_file):
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def bd_clima():
    path = "../dados/"

    if "clima.db" in os.listdir(path):
        print("Banco de dados já criado")
    else:
        
        cria_bd(path+"clima.db")
        con = cria_conexao(path+"clima.db")

        arquivos = [arq for arq in os.listdir(path) if '.csv' in arq]

        for tabela in arquivos:

            if '_clima.csv' in tabela:
                nome= tabela.rsplit("_clima.csv")
                df = carrega_csv(path+tabela)
                df.to_sql(nome[0], con)
            else:
                nome = tabela.rsplit(".csv")
                df = carrega_csv(path+tabela)
                df.to_sql(nome[0], con)
        con.close()

def carrega_tabela(nome, bd, clima=False):

    con = cria_conexao(bd)
    query = "SELECT * FROM {}".format(nome)
    if clima:
        df = pd.read_sql_query(query, con=con, parse_dates='Horario', index_col='Horario')
    else:
        df = pd.read_sql_query(query, con=con)
        df.drop(columns='index', inplace=True)
    
    con.close()
    return df
