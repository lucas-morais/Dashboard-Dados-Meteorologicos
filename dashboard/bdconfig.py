import os
import pandas as pd
import sqlite3


def carrega_csv(arquivo):
    
    #arquivo: Arquivo do tipo csv
    #retorno: Dataframe pandas
    
    if "_clima" in arquivo:
        df = pd.read_csv(arquivo,
            delimiter = ";",
            usecols=list(range(1,10)),               
            dtype={'Hora':'str','DirecaoVento':'str'},
            parse_dates=[['Data', 'Hora']],      
            dayfirst = True,
            index_col = 0
        )   
        vento = pd.read_csv('../dados/DirecaoVento.csv', delimiter=';', dtype={'Codigo':'str' })
        mapper = dict(zip(vento['Codigo'], vento['Descricao']))
        df['DirecaoVento']=df['DirecaoVento'].map(mapper)
        df.index.rename('Horario', inplace=True)

    else :
        try:
            df = pd.read_csv(arquivo,
                            sep=";" 
                            )
        except:
            raise Exception("Arquivo não existe")
            
    return df

def cria_bd(bd_file):

    #Função para criar naco de dados com sqlite3

    #bd_file: nome do arquivo

    #testa se o arquvio existe    
    if not os.path.exists(bd_file):
        con = None
        try:
            con = sqlite3.connect(bd_file)
        except sqlite3.Error as e:
            print(e)
        finally:
            if con:
                con.close()
    else:
        print("Arquivo existe")

def bd_clima():
    
    #Função para criar banco de dados com dados metereológicos
    path = "../dados/"

    if "clima.db" in os.listdir(path):
        print("Banco de dados já criado")
    else:
        con = None
        try:
            
            con = sqlite3.connect(path+"clima.db")
            
            #Loop dos arquivos csv
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

            print("Banco de dados criado")
       
        except sqlite3.Error as e:
            print(e)
        
        finally:
            if con:
                con.close()


def carrega_tabela(nome, bd, clima=False):

    #Função para carregar tabela

    #nome: Nome da tabela
    #bd: Arquivo do banco de dados 
    #Clima: Define se a tabela é de informações ou medições metereológicas 
    
    con = None
    df = None
    try:

        con = sqlite3.connect(bd)
        query = "SELECT * FROM {}".format(nome)
        if clima:
            df = pd.read_sql_query(query, con=con, parse_dates='Horario', index_col='Horario')
        else:
            df = pd.read_sql_query(query, con=con)
            df.drop(columns='index', inplace=True)
    
    except sqlite3.Error as e:
            print(e)
        
    finally:
        if con:
            con.close()
    
    return df
