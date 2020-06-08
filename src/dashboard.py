import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from bdconfig import carrega_tabela
from graficos import mapa, graficos


bd = "../dados/clima.db"

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
                        dcc.Graph(id='Graficos', figure=graficos())
                    ])
                ]),
            ],
            colors = dict(border="blue",primary="yellow",background="#1a1a1a")),
        ]),
        html.Div(className="resumo")
    ])


])



if __name__ == "__main__":
    app.run_server(debug=True)