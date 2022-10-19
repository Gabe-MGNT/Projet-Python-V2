import json

from dash import html

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, Output, Input

#print(px.data.election().head())
geojson = open("ze2020_2022.json")
test = json.load(geojson)
print(test["features"][0]['properties'].keys())
