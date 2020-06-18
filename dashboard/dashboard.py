import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime as dt
from bdconfig import carrega_tabela
from graficos import GraficoDash, mapa

#Criando listas para Dropdown
bd = "../dados/clima.db"
info = carrega_tabela(nome = "Info", bd = bd, clima=False)
nome = info['Cidade']
label = [it.replace('-',' ') for it in nome]
value = [it.replace('-','') for it in nome]
listaCidades = []
for it1,it2 in zip(label, value):
    listaCidades.append(dict(label=it1, value=it2))

#Colunas Para tabela de resumo
colunas = ['Média', 'Mediana', 'Desvio Padrão']

#Stylsheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Criando app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Layout do app
app.layout = html.Div(children=[

    #Cabeçalho
    html.Header(children=[
        html.H1("Dashboard de Dados Metereólogicos - Paraíba")
    ]),
    

    html.Div(className= "principal", children = [
        
        #Tela principal
        html.Div(className="grafico", children=[    
            #Tabs
            dcc.Tabs([
                #Mapa
                dcc.Tab(label = 'Mapa',children = [
                    html.Div(children=[
                        dcc.Graph(id='Mapa', figure=mapa())
                    ])
                ]),
                #Gráficos
                dcc.Tab(label = 'Gráficos',children = [
                    html.Div(children=[
                        dcc.Graph(id='Graficos')
                    ])
                ]),
            ],
            colors = dict(border="blue",primary="yellow",background="#1a1a1a")),
        ]),
        #Coluna de opções e tabelas
        html.Div(className="resumo", children = [
            
            #Dropdown: escolhe a cidade
            html.Label(children =[ 
                "Cidade:",
                dcc.Dropdown(
                    id = 'Cidades-Dropdown',
                    options = listaCidades,
                    value = 'JoaoPessoa',
                )
            ]),
            #Date-Picker: escolhe a data
            html.Label(children=[
                "Data:",
                html.Br(),
                dcc.DatePickerRange(
                    id = 'Datas',
                    min_date_allowed=dt(2008, 1, 1),
                    max_date_allowed=dt(2018,12,31),
                    display_format='DD/MM/YYYY',
                    start_date_placeholder_text='Data início',
                    end_date_placeholder_text='Data fim',
                )        
            ]), 
            #Tabela de resumo
            html.Label(children = [
                "Resumo",
                dash_table.DataTable(
                    id = 'Tabela',
                    columns=[{"name": i, "id": i} for i in ['Medição','Média', 'Desvio Padrão','Mediana']],
                    style_cell = dict(backgroundColor='#1a1a1a', color='whitesmoke')
                ),
                
            ]), 
            #Tabela de contagem de direção do vento
            html.Label(children = [
                "Direção do Vento",
                dash_table.DataTable(
                    id = 'TabelaVento',
                    columns=[{"name": i, "id": i} for i in ['Direção','Contagem' ]],
                    style_cell = dict(backgroundColor='#1a1a1a', color='whitesmoke')
                ),
                
            ]),   
        ])
    ])
])

#Callback para atualização de informações
@app.callback(
    [Output(component_id="Graficos", component_property="figure"),
    Output(component_id="Tabela", component_property="data"),
    Output(component_id="TabelaVento", component_property="data")],
    [Input(component_id="Cidades-Dropdown", component_property="value"),
    Input(component_id="Datas", component_property="start_date"),
    Input(component_id="Datas", component_property="end_date")]
)
#Função de callback
def update_dados(value, start_date, end_date):

    if value is not None:
        cidade = value
    else: 
        cidade = JoaoPessoa
    
    if start_date is not None:
        inicio = start_date
    else: 
        inicio = '2008-01'
    
    if end_date is not None:
        fim = end_date 
    else:
        fim = '2008-12'

    graf = GraficoDash(cidade, inicio, fim)
    
    figura = graf.graficos()
    tabela = graf.tabela_resumo()
    tabelaVento = graf.tabela_vento()
    
    return figura, tabela, tabelaVento

if __name__ == "__main__":
    app.run_server(debug=True)