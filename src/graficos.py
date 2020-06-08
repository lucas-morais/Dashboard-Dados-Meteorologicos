import plotly.graph_objects as go
from plotly.subplots import make_subplots
from bdconfig import carrega_tabela

def mapa():
    
    bd = "../dados/clima.db"
    info = carrega_tabela(nome = "Info", bd = bd, clima=False)
    


    latitude = info['Latitude']
    longitude = info['Longitude']
    texto = info['Cidade'].values
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


def graficos():

    bd = "../dados/clima.db"
    df = carrega_tabela(nome = "JoaoPessoa", bd = bd, clima=True)

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
            x=df['2008-01'].index, 
            y=df['TempBulboSeco']['2008-01']
        ),
        row = 1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['2008-01'].index, 
            y=df['TempBulboUmido']['2008-01']
        ),
        row = 1, col=2
    )

    fig.add_trace(
        go.Scatter(
            x=df['2008-01'].index, 
            y=df['UmidadeRelativa']['2008-01']
        ),
        row = 2, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['2008-01'].index, 
            y=df['PressaoAtmEstacao']['2008-01']
        ),
        row = 2, col=2
    )

    fig.add_trace(
        go.Scatter(
            x=df['2008-01'].index, 
            y=df['VelocidadeVento']['2008-01']
        ),
        row = 3, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['2008-01'].index, 
            y=df['Nebulosidade']['2008-01']
        ),
        row = 3, col=2
    )


    fig.update_layout(
        showlegend=False,
        template = "plotly_dark",
        margin = dict(l=20,r=20, t=40, b = 20), 
        
    )
    return fig