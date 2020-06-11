import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from bdconfig import carrega_tabela
from graficos import mapa, graficos, tabela_vento
from datetime import datetime as dt


bd = "../dados/clima.db"
info = carrega_tabela(nome = "Info", bd = bd, clima=False)
nome = info['Cidade']
label = [it.replace('-',' ') for it in nome]
value = [it.replace('-','') for it in nome]
listaCidades = []
for it1,it2 in zip(label, value):
    listaCidades.append(dict(label=it1, value=it2))

colunas = ['Média', 'Mediana', 'Desvio Padrão']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div(children=[

    html.Header(children=[
        html.H1("Dashboard de Dados Metereólogicos - Paraíba")
    ]),
    
    #html.Hr(),

    html.Div(className= "principal", children = [
        

        html.Div(className="grafico", children=[    
            dcc.Tabs([
                dcc.Tab(label = 'Mapa',children = [
                    html.Div(children=[
                        dcc.Graph(id='Mapa', figure=mapa())
                    ])
                ]),
                dcc.Tab(label = 'Gráficos',children = [
                    html.Div(children=[
                        dcc.Graph(id='Graficos')
                    ])
                ]),
            ],
            colors = dict(border="blue",primary="yellow",background="#1a1a1a")),
        ]),
        html.Div(className="resumo", children = [
            html.Label(children =[ 
                "Cidade:",
                dcc.Dropdown(
                    id = 'Cidades-Dropdown',
                    options = listaCidades,
                    value = 'JoaoPessoa',
                )
            ]),
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
            html.Label(children = [
                "Resumo",
                dash_table.DataTable(
                    id = 'Tabela',
                    columns=[{"name": i, "id": i} for i in ['Medição','Média', 'Desvio Padrão','Mediana']],
                    style_cell = dict(backgroundColor='#1a1a1a', color='whitesmoke')
                ),
                
            ]), 
            html.Label(children = [
                "Direção do Vento",
                dash_table.DataTable(
                    id = 'TabelaVento',
                    columns=[{"name": i, "id": i} for i in ['Direção','Cont' ]],
                    style_cell = dict(backgroundColor='#1a1a1a', color='whitesmoke')
                ),
                
            ]),   
        ])
    ])
])

@app.callback(
    [Output(component_id="Graficos", component_property="figure"),
    Output(component_id="Tabela", component_property="data"),
    Output(component_id="TabelaVento", component_property="data")],
    [Input(component_id="Cidades-Dropdown", component_property="value"),
    Input(component_id="Datas", component_property="start_date"),
    Input(component_id="Datas", component_property="end_date")]
)

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

    figura = graficos(cidade,inicio=inicio,fim=fim)
    
    df = carrega_tabela(cidade, bd = '../dados/clima.db', clima=True)
    tabela = df.describe().T.loc[:,['mean','std', '50%']]
    tabela.reset_index(inplace=True)
    tabela.columns = ['Medição','Média', 'Desvio Padrão','Mediana']
    tabela = tabela.round(2)

    tabelaVento = tabela_vento(cidade, inicio, fim)
    
    return figura, tabela.to_dict('records'), tabelaVento.to_dict('records')

if __name__ == "__main__":
    app.run_server(debug=True)