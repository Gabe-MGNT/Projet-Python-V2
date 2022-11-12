from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
import dash
from dash import dcc, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

"""
Fichier principal contenant la déclaration et création du DashBoard, en plus de récupérer les données et les traiter si nécesssaire.
Contient aussi la création ainsi que la mise à jour de tous les graphiques visibles.
"""



"""
Récupération des données depuis le fichier .xlsx en un DataFrame pandas
Comme le fichier excel contient plusieurs pages, on utilise celle nommée 'txcho_ze', et on retire les 5 premières lignes ne contenant pas d'informations
"""
exc = pd.ExcelFile("data/chomage-zone-t1-2003-t2-2022.xlsx")
df = pd.read_excel(exc, "txcho_ze", skiprows=[0, 1, 2, 3, 4])

"""
Thème graphique appliqué aux futures figures créées
"""
load_figure_template("simplex")

"""
Création d'une pie-chart comptant le nombre de relevés par régions
Et formattage des données pour les afficher à l'intérieur
"""
pie_df = df["LIBREG"].value_counts()
fig_pie_hole = px.pie(
    pie_df,
    values=pie_df,
    names=pie_df.index,
    hole=.4,
    labels={
        "index": "Régions",
        "values": "Nombre de villes"
    },
    title="Nombre de relevés par régions par trimestre",
).update_traces(
    textposition='inside',
    insidetextorientation='radial',
    textinfo='label+value',
    textfont_size=14,
    marker=dict(
        line=dict(color='#000000', width=1)
    )
).update_layout(
    showlegend=False
)

"""
Création du bar chart de l'évolution général du chomage, avec :
    - Groupement des données par les régions
    - Prise de la moyenne du chomage pour chaque région sur tous les relevés
    - Transposition pour meilleur accès des données
"""
da = df.iloc[:, 3:].groupby("LIBREG").mean()
da = da.dropna(how='any')
dat = da.T
figChomageParRegion = px.bar(
    dat,
    title="Evolution du chômage moyen par région",
    x=dat.index,
    y=dat.columns,
    labels={
        "LIBREG": "Région",
        "index": "Date",
        "value": "Moyenne (en %)"
    },

).update_yaxes(
    title_text="Somme des moyennes"
).update_xaxes(
    title_text="Dates de relevés"
)

"""
Création d'un histogramme représentant la distribution du chomage dans certaine régions
    - Récupération des colonnes contenant les régions et le relevés de chaques années
"""
db = df.iloc[:, 3:]
db = db.dropna(how='any')
dbt = db.T
fig21 = px.bar(
    # db[np.logical_or(db['LIBREG'] == "ILE DE FRANCE",db['LIBREG'] == "OCCITANIE") ],
    # title="Répartitions des zones d'emplois de régions en fonction du chomage",
    # x = "2003-T1",
    # barmode="overlay",
    # color = "LIBREG"
)

"""
Création de la carte choroplèthe du taux de chomage par région, avec :
    - Padding de 0 pour les codes de régions mal importés
    - Chargement du fichier json contenant les données pour tracer
    - Création de la carte en faisant le lien entre le code de région du DataFrame et le code de région du fichier JSON
"""
df["ZE2020"] = df["ZE2020"].apply(lambda x: str(x).rjust(4, '0') if len(str(x)) < 4 else x)
fichierJson = open("data/ze2020_2022.json")
geojson = json.load(fichierJson)
figCarte = px.choropleth_mapbox(
    df,
    geojson=geojson,
    featureidkey="properties.ze2020",
    locations='ZE2020',
    color='2003-T1',
    title="Carte du chômage en France par zone d'emplois",
    hover_name='LIBZE2020',
    color_continuous_scale="orrd",
    range_color=(5, 12),
    mapbox_style="carto-positron",
    zoom=4, center={"lat": 46.000, "lon": 2.00},
    opacity=0.5,
    labels={'ZE2020': 'Code zone d\'emploi:'}
)

"""
Création d'un diagramme ligne, représentant l'évolution temporelle du taux de chomage dans certaines régions
"""
figTimeline = px.line(
    x=pd.to_datetime(df.columns[4:]),
    markers=True,
    y=[df[df["LIBZE2020"] == "Avignon"].iloc[:, 4:].iloc[0],
       df[df["LIBZE2020"] == "Paris"].iloc[:, 4:].iloc[0]],

)

"""
Mise en place visuelle du dashboard
"""
app = dash.Dash("Lancement du dashboard")
app.layout = html.Div(children=[
    html.H1(children="Le chomage en France entre 2003 et 2022",
            id="titre",
            style={
                'textAlign': 'center',
                'color': 'black'
            }),
    html.Br(),
    html.H2(children="Présentation du jeu de données"),
    html.Div(
        children=[
            html.Div(
                children=dcc.Graph(
                    id="pie_count",
                    figure=fig_pie_hole
                ),
                style={'width': '30%',
                       "display": "inline-block",
                       "padding": "10px",
                       # "box-shadow": "0 3px 10px rgb(0 0 0 / 0.2)",
                       }
            ),
            html.Div(
                children=[
                    html.H3(children="Provenance : jeu de données de l'INSEE"),
                    html.Hr(),
                    html.H4(
                        "Sujet : Le taux de chômage entre 2003 et 2022 dans les régions françaises"
                    ),
                    html.Br(),
                    html.P(
                        "Description : Ce Dashboard a pour but de montrer le chomage en France par zone d'emplois (ZE), et son évolution entre 2003 et 2022, par trimestre. Les chiffres pour les Drom-Com n'apparaissent qu'après 2014."
                    )

                ],
                style={
                    "padding": "20px",
                    "margin-left": "20px",
                    "margin-top": "120px",
                    "display": "inline-block",
                    "position": "absolute",
                    "width": "50%",
                    "height": "30%",
                    "background": "#eee",
                    "border-radius": "20px",
                    "box-shadow ": "0 3px 10px rgb(0 0 0 / 0.2)",
                }

            )

        ],
        style={
            "padding": "10",
            "flex": "1",

        }

    ),
    html.Hr(),
    html.H2(
        children="Localisation du chômage en France"
    ),
    html.Div(
        children="Afin de mieux comprendre le phénomène du chômage, on peut d'abord voir sa répartition dans les régions françaises à l'aide d'une carte. (L'actualisation de la carte prend du temps au vue de sa complexité, il faut donc attendre un peu avant de voir les modifications visuellement)"
    ),
    dcc.Graph(
        id="graphCarte",
        figure=figCarte,
        config=dict(
            {
                'scrollZoom': False
            }
        )
    ),
    dcc.Slider(
        0, len(df.columns[4:]) - 1,
        id="slider_carte",
        step=1,
        marks={
            i: str(2003 + i // 4) for i in range(0, len(df.columns[4:]) - 1, 4)
        },
        value=76,
    ),
    html.Br(),
    html.Div(children=f'''
                            Les zones les plus touchées par le chomage sont le nord est, région anciennement industrialisées qui peinent a réussir leurs transition dans l'économie tertiaire, et le sud ouest, très attractif, n'arrive pas a suivre l'arrivée massive de population active attiré par le tourisme.
                            \n Il est possible de faire évoluer dans le temps la carte avec le slider ci-dessus.
                            ''', style={
        "padding": "20px"
    }),

    html.Br(),
    html.Hr(),
    html.H2(
        children="Évolution générale du taux de chômage en France"
    ),

    html.Div(
        children=dcc.Graph(
            id="graphChomageParRegion",
            figure=figChomageParRegion
        ),
        style={
            "padding": '50px',
        }
    ),
    html.Div(children=f'''
                            Ce diagramme permet de visualiser l'évolution du chommage dans chaque région, mais aussi de manière générale.
                            Ici l'impact de la crise de 2008 est notable avec une forte hausse dans les années suivantes ; la décroissance qui suit montre une stabilité du marché du travail en France. Puis vient la crise du COVID en 2020, soit le moment où un énorme pic apparaît.
                            \n De plus amples informations peuvent être obtenues en glissant votre souris sur les barres pour afficher les informations.
                            ''',
             style={
                 "padding": "20px"
             }),

    html.Br(),
    html.Hr(),
    html.H2(
        children="Distribution du taux de chômage"
    ),

    html.Div(
        children=dcc.Graph(
            id="graph21",
            figure=fig21
        ),
        style={
            "padding": "50px"
        }
    ),
    dcc.Dropdown(

        id="dropdown_histo",
        options=[
            {"value": i, "label": i} for i in df["LIBREG"].dropna().unique()
        ],
        multi=True,

        value=["ILE DE FRANCE", "OCCITANIE"]
    ),

    dcc.Slider(
        0, len(df.columns[4:]) - 1,
        step=1,
        id="slider_histo",
        value=1,
        marks={
            # 0: "2003 - T1",
            # len(df.columns[4:])-1: "2022 - T2"
            i: str(2003 + i // 4) for i in range(0, len(df.columns[4:]) - 1, 4)
        },
        updatemode="drag",
    ),

    html.Br(),
    html.Div(children=f'''
                            Ce diagramme permet de comparer les zones d'emplois dans plusieurs régions en simultanés. L'axe des ordonées représente le nombre de zones d'emplois d'un région dans l'intervalle de chomage désigné.
                            On peut y séléctionner les régions voulues ainsi que l'année voulue.
                            Ce graphique permet d'observer la tendance que la région Ile-De-France semble moins affectée par le chômage avec es taux plus faibles que les autres régions.
                            Les régions situées dans le Sud semble avoir des répartitions plus hautes en terme de taux de chômage.
                            ''', style={
        "padding": "20px"
    }),
    html.Br(),
    html.Hr(),
    html.H2(
        children="Evolution temporelle du taux de chomage"
    ),

    html.Div
        (children=dcc.Graph(
        id="timeline",
        figure=figTimeline
    ),
        style={
            "padding": "50px"
        }
    ),
    dcc.Dropdown(
        id="emplacement_dropdown",
        options=[
            {"value": i, "label": i} for i in df["LIBZE2020"].dropna().unique()
        ],
        multi=True,
        value=["Alençon", "Paris"]
    ),
    dcc.RangeSlider(
        0, len(df.columns[4:]) - 1,
        id="slider",
        step=1,
        marks={
            i: str(2003 + i // 4) for i in range(0, len(df.columns[4:]) - 1, 4)
        },
        # marks=
        # {i: str(year) for i, year in enumerate(df['Arbre Exploitation - Planté le'].unique())},
        value=[5, 55],
    ),
    html.Br(),
    html.Div(children=f'''
                                Ce diagramme permet de comparer le taux de chômage dans certaines villes. L'axe des abscisses représente l'intervalle de temps sur lequel on souhaite observer les données, réglable à l'aide du slider ci-dessous.
                                L'axe des ordonnées représente le taux de chômage dans les villes (en %)
                                Il est possible de choisir quelles villes voir à l'aide du menu en dessous.
                                Ce graphique permet de voir les différents impacts qu'ont eu la crise de 2008 et la crise Covid sur le chômage sur certaines villes françaises et la France en général.
                                Pour certaines villes, 2015 mest marquée par un fort taux de chômage (+10%), mais aussi l'adoptinon de la loi El-Khomri qui montre avoir des gros effets en général après 2015.
                                Ensuite, en choisissant correctement les villes, on peut voir que finalement les villes autour de Paris semble avoir un taux de chômage plus faibles que les autres.
                                Alors que les villes du Sud, région Centre, et au Nord semble avoir des taux de chômages plus élevés en général.
                                ''', style={
        "padding": "20px"
    }),
],
    style={
        "padding-left": "30px",
        "padding-right": "30px"
    }
)

"""
Création des callback permettant la mise à jour des graphiques en fonction d'entrées
"""

"""
Mise à jour de la carte chroplethe par la valeur d'un slider
    - Selon la valeur du slider, se place dans la colonne des annes voulues
    - Actualise la carte avec les nuvelles données
"""


@app.callback(
    Output(component_id="graphCarte", component_property="figure"),
    [Input(component_id="slider_carte", component_property="value")]
)
def update_carte(slider_value):
    # Récupère la date selon la valeur du slider
    list_temps = df.columns
    x = list_temps[slider_value + 4]

    # Créer la carte choropleth en conséquence
    return px.choropleth_mapbox(df, geojson=geojson, featureidkey="properties.ze2020", locations='ZE2020', color=str(x),
                                title="Carte du chômage en France par zone d'emplois",
                                hover_name='LIBZE2020',
                                color_continuous_scale="orrd",
                                range_color=(5, 12),
                                mapbox_style="carto-positron",
                                zoom=4, center={"lat": 46.000, "lon": 2.00},
                                opacity=0.5,
                                labels={
                                    'ZE2020': 'Code zone d\'emploi',
                                    str(x):"Taux de chômage (en %) "
                                }
                                )


"""
Mise a jour de l'histogramme de la distribution du chomage dans certaines régions
A l'aide des valeurs du 'DropDown Menu', ajout des régions séléctionnées dans le DataFrame séléctionné
"""


@app.callback(
    Output(component_id="graph21", component_property="figure"),
    [Input(component_id="dropdown_histo", component_property="value"),
     Input(component_id="slider_histo", component_property="value"), ]
)
def update_histo(dropdown_value, slider_value):
    # Récupération de toutes les régions contenues dans le menu dropdown
    list_reg = []
    for region in dropdown_value:
        list_reg.append(region)

    # Création du dataframe contenant les villes, et la date voulue grâce à la valeur du slider
    annee = db[db["LIBREG"].isin(list_reg)].columns[1 + slider_value]

    # Gère le cas où rien n'est demandé
    # Affiche donc un graph avec un message d'erreur
    if list_reg == [] or db[db["LIBREG"].isin(list_reg)]["2003-T1"].empty:
        return px.histogram(
            db[db["LIBREG"].isin(list_reg)],
            x=annee,
            barmode="group",
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

    # Sinon retourne le graph avec les données
    return px.histogram(
        db[db["LIBREG"].isin(list_reg)],
        x=annee,
        title="Distribution du chômage des régions",
        barmode="group",
        color="LIBREG",
        labels={
            "LIBREG":"Région ",
            str(annee):"Intervalle du taux de chômage "
        },
    ).update_xaxes(
        range=[0, db[db["LIBREG"].isin(list_reg)][annee].max() + 5]
    ).update_layout(
        bargap=0.35
    ).update_yaxes(
        title_text="Nombre de villes"
    )


"""
Mise à jour du graphique de l'évolution temporelle du chomage dans certaines régions
A l'aide de la valeur d'un slider et de celles d'un 'DropDown Menu', actualisation du DataFrrame
utilisé pour contenir l'intervalle de dates voulues et les régions souhaitées
"""


@app.callback(
    [Output(component_id="timeline", component_property="figure")],
    [Input(component_id="slider", component_property="value"),
     Input(component_id="emplacement_dropdown", component_property="value")
     ],

)
def update_figure_timeline(input_value, drop_input):
    # Récupère les lignes du dataframe original contenant villes contenues dans le menu dropdown en tenant compte des années fournies par le slider
    ordonnee = []
    for ville in drop_input:
        ordonnee.append(df[df["LIBZE2020"] == ville].iloc[:, 4 + input_value[0]:4 + input_value[1] + 1].iloc[0])

    # Création d'un dataframe contenant les différentes lignes de données
    # Formattage du nom des index et des colonnes
    data_f = pd.DataFrame(ordonnee)
    data_f = data_f.T
    data_f.index.name = "Date"
    data_f.columns = drop_input

    # Gère le cas où les données entrées sont vides
    # Renvoie alors un graph avec un message d'erreur
    if drop_input == [] or data_f.empty:
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

    # Sinon renvoie un graph avec les données voulues
    else:
        return [
            px.line(
                data_f,
                x=data_f.index,
                y=drop_input,
                markers=True,
                title=f'Evolution du taux de chômage entre {(df.columns[4 + input_value[0]]).split(" ")[0]} et {(df.columns[4 + input_value[1]]).split(" ")[0]}',
                labels={
                    "x": "Années de relevé ",
                    "value": "Taux de chômage (en %) ",
                    "variable": "Ville "
                }

            ).update_traces(textposition="top center")
        ]


def get_dashboard():
    """
    Retourne le dashboard créé pour pouvoir être éxécuté de facon externe à ce fichier

        :returns
            app (Dash) : Un objet Dash prêt à être éxécuté
    """
    return app
