import plotly.graph_objects as go
from plotly.subplots import make_subplots
from bdconfig import carrega_tabela
import pandas as pd

class GraficoDash:

    bd = '../dados/clima.db'

    def __init__(self, nome, inicio, fim):
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self.df = carrega_tabela(self.nome, bd,clima=True)
        self.df = self.df[inicio:fim]
        self.info = carrega_tabela('Info', bd, clima=False)
    
    
    def graficos(self):
    
    
        fig = make_subplots(rows=3, cols=2, 
                subplot_titles=["Temperatura de Bulbo Seco",
                                "Temperatura de Bulbo Úmido",
                                "Umidade",
                                "Pressão Atmosférica",
                                "Velocidade do Vento",
                                "Nebulosidade"
                                ])

        fig.add_trace(
            go.Scatter(
                x=self.df.index, 
                y=self.df['TempBulboSeco']
            ),
            row = 1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=self.df.index, 
                y=self.df['TempBulboUmido']
            ),
            row = 1, col=2
        )

        fig.add_trace(
            go.Scatter(
                x=self.df.index, 
                y=self.df['UmidadeRelativa']
            ),
            row = 2, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=self.df.index, 
                y=self.df['PressaoAtmEstacao']
            ),
            row = 2, col=2
        )

        fig.add_trace(
            go.Scatter(
                x=self.df.index, 
                y=self.df['VelocidadeVento']
            ),
            row = 3, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=self.df.index, 
                y=self.df['Nebulosidade']
            ),
            row = 3, col=2
        )


        fig.update_layout(
            showlegend=False,
            template = "plotly_dark",
            margin = dict(l=20,r=20, t=40, b = 20), 
            plot_bgcolor = '#1a1a1a',
            paper_bgcolor=  '#1a1a1a',
            
        )
        return fig


    def mapa(self):
    

        latitude = self.info['Latitude']
        longitude = self.info['Longitude']
        texto = self.info['Cidade'].values
        lat = list(latitude.astype(str).values)
        lon = list(longitude.astype(str).values)
        centro = [latitude.mean(), longitude.mean()]


        fig = go.Figure(go.Scattermapbox(
            lat=lat,
            lon=lon,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14
            ),
            text=texto
        ))

        fig.update_layout(
            hovermode='closest',
            margin=dict(l=0,r=0, t=0, b=0),
            mapbox=dict(
                bearing=0,
                style='carto-darkmatter',
                center=go.layout.mapbox.Center(
                    lat=centro[0],
                    lon=centro[1]
                ),
                pitch=0,
                zoom=5
            )
        )
        return fig

    def tabela_resumo(self):

        tabela = self.df.describe().T.loc[:,['mean','std', '50%']]
        tabela.reset_index(inplace=True)
        tabela.columns = ['Medição','Média', 'Desvio Padrão','Mediana']
        tabela = tabela.round(2)
        tabela_resumo = tabela.to_dict('records')

        return tabela_resumo

    
    def tabela_vento(self):
    
        vento = self.df['DirecaoVento']
        vento_principal = vento.value_counts()[:3]
        tabela = pd.DataFrame([vento_principal.index, vento_principal.values]).T
        tabela.columns = ['Direção', 'Contagem']
        tabela_vento = tabela.to_dict('records')
        return tabela_vento