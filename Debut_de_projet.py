from dash import html

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
import plotly.graph_objects as go
import dash
from dash import dcc, Output, Input

exc=pd.ExcelFile("chomage-zone-t1-2003-t2-2022.xlsx")
df=pd.read_excel(exc,"txcho_ze",skiprows=[0,1,2,3,4])

fig2=px.histogram(
    df,
    x=["LIBREG"]
)
df["ZE2020"]=df["ZE2020"].apply(lambda x: str(x).rjust(4,'0') if len(str(x))<4 else x)

da = df.iloc[:,3:].groupby("LIBREG").mean()
da = da.dropna(how = 'any')
dat= da.T
fig20=px.histogram(
    dat,
    x=dat.index,
    y=dat.columns,
    labels={
        "LIBREG":"Région",
        "index":"Date",
        "sum of value":"moyenne"
    },

).update_yaxes(
    title_text="Somme des moyennes"
).update_xaxes(
    title_text="Dates de relevés"
)

db = df.iloc[:,3:]
db = db.dropna(how = 'any')
dbt= db.T


#numpy.logical_or(db['LIBREG'] == "ILE DE FRANCE",db['LIBREG'] == "OCCITANIE")

fig21=px.histogram(
    db[np.logical_or(db['LIBREG'] == "ILE DE FRANCE",db['LIBREG'] == "OCCITANIE") ],
    x = "2003-T1",
    barmode="overlay",
    color = "LIBREG"
)





fichierJson = open("ze2020_2022.json")
geojson = json.load(fichierJson)


fig3 = px.choropleth_mapbox(df, geojson=geojson, featureidkey = "properties.ze2020", locations='ZE2020', color='2003-T1',
                           color_continuous_scale="Viridis",
                           range_color=(5, 12),
                           mapbox_style="carto-positron",
                           zoom=4, center = {"lat": 46.000, "lon": 2.00},
                           opacity=0.5,
                           labels={'2003-T1':'Année 2003 trimestre 1'}
                          )


fig5=px.line(
    x=pd.to_datetime(df.columns[5:]),
    markers=True,
    y=[df[df["LIBZE2020"]=="Avignon"].iloc[:,5:].iloc[0],
       df[df["LIBZE2020"]=="Paris"].iloc[:,5:].iloc[0]],

)

app=dash.Dash("TTTEEESSSSTT")
app.layout=html.Div(children=[
        html.H1(children="Nombre d'arbres",
                id="titre",
                style={
                    'textAlign': 'center',
                    'color': '#7fdbff'
                }),
        #dcc.Graph(
        #    id="graph1",
        #    figure=fig
        #),
    html.H1(
        children="Distrib"
    ),
dcc.Graph(
        id="graph20",
        figure=fig20
    ),

    dcc.Dropdown(

        id="dropdown_histo",
        options=[
            {"value": i, "label": i} for i in df["LIBREG"].dropna().unique()
        ],
        multi=True,
        value=["ILE DE FRANCE", "OCCITANIE"]

    ),
dcc.Graph(
        id="graph21",
        figure=fig21
    ),

    dcc.Slider(

        1, len(df.columns[5:]),
        step=1,
        id="slider_histo",
        value=1,
        marks={
            1: "2003",
            len(df.columns[5:]): "2022"
        },
        updatemode="drag",
    ),
dcc.Graph(
        id="graph3",
        figure=fig3
    ),
dcc.Graph(
        id="graph2",
        figure=fig2
    ),
    html.H1(
        id="sous-titre",
        children="Evolution temporelle"
    ),
    html.H1(
        id="date_inter",
        children="Entre l'année"
    ),
    dcc.Graph(
        id="timeline",
        figure=fig5
    ),
    dcc.Dropdown(
        id="emplacement_dropdown",
        options=[
            {"value": i, "label": i} for i in df["LIBZE2020"].dropna().unique()
        ],
        multi=True,
        value=["Alençon","Paris"]
    ),
    dcc.RangeSlider(
        0, len(df.columns[5:])-1,
            id="slider",
            step=1,
            marks=None,
            #marks=
            #{i: str(year) for i, year in enumerate(df['Arbre Exploitation - Planté le'].unique())},
            value=[5,7],
            tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.H1(
        id="selec_arrond",
        children=""
    ),
    ]
)

@app.callback(
    Output(component_id="graph21",component_property="figure"),
    [Input(component_id="dropdown_histo",component_property="value"),
     Input(component_id="slider_histo",component_property="value"),]
)
def update_histo(dropdown_value,slider_value):
    list_reg=[]
    for region in dropdown_value:
        list_reg.append(region)

    annee=db[db["LIBREG"].isin(list_reg)].columns[slider_value]
    if list_reg==[] or db[db["LIBREG"].isin(list_reg)]["2003-T1"].empty:
         return px.histogram(
             db[db["LIBREG"].isin(list_reg)],
             x=annee,
             barmode="relative",
             color="LIBREG"
         ).add_annotation(
        text="Pas de données disponibles pour ces valeurs demandées",
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            size=25
        )
         )

    return px.histogram(
            db[db["LIBREG"].isin(list_reg)],
            x=annee,
            barmode="relative",
            color="LIBREG"
        ).update_xaxes(
            range=[0,db[db["LIBREG"].isin(list_reg)][annee].max()+5]
    )



@app.callback(
    [Output(component_id="timeline", component_property="figure"),
     Output(component_id="date_inter", component_property="children"),
     Output(component_id="sous-titre", component_property="children")],
    [Input(component_id="slider",component_property="value"),
Input(component_id="emplacement_dropdown",component_property="value")
     ],

)
def update_figure_timeline(input_value,drop_input):

    ordonnee=[]
    for ville in drop_input:
        ordonnee.append(df[df["LIBZE2020"]==ville].iloc[:,5+input_value[0]:5+input_value[1]+1].iloc[0])
    #print(ordonnee)

    data_f=pd.DataFrame(ordonnee)
    data_f=data_f.T

    data_f.index.name="Date"
    data_f.columns=drop_input


    if drop_input==[] or data_f.empty:
        return [
            px.line(
                x=None,
                y=None
            ).add_annotation(
        text="Pas de données disponibles pour ces valeurs demandées",
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            size=25
        )
         ),
            f"Impossible d'afficher",
            f'Pas de villes renseingées'
        ]

    else:
        return [
            px.line(
            data_f,
            # x=pd.to_datetime(df.columns[5 + input_value[0]:5 + input_value[1]]),
            x=data_f.index,
            y=drop_input,
            # text=df.iloc[:, 5 + input_value[0]:5 + input_value[1]].iloc[0],
            markers=True,
            title="Evolution du taux d'emploi",
            labels={
                "x": "Années de relevé ",
                "value": "Taux d'emploi (en %) ",
                "variable":"Ville "
            }

        ).update_traces(textposition="top center")
        ,
    f'Evolution entre ({(df.columns[5+input_value[0]]).split(" ")[0]}) et ({(df.columns[5+input_value[1]]).split(" ")[0]})',
        #f'Dans la ville de ({" ".join([ville for ville in drop_input])})'
        f'Evolution du taux de chomage dans certaines villes'
    ]
app.run_server(debug=True)

