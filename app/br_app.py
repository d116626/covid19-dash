import numpy as np
import pandas as pd
from datetime import datetime, timedelta

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline

from paths import *
import yaml

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from src import dash_statics
from src import vis_dash
from src import io, transform


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
				assets_folder='./assets/',
				external_stylesheets =[dbc.themes.BOOTSTRAP],
				meta_tags=[
					{"name": "author", "content": "Jun Ye"},]
				
				)

app.title = 'MonitoraCovid'
app.config['suppress_callback_exceptions'] = True # This is to prevent app crash when loading since we have plot that only render when user clicks.

# app.index_string = """<!DOCTYPE html>
# <html>
#     <head>
#         <script data-name="BMC-Widget" src="https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js" data-id="qPsBJAV" data-description="Support the app server for running!" data-message="Please support the app server for running!" data-color="#FF813F" data-position="right" data-x_margin="18" data-y_margin="25"></script>
#         <!-- Global site tag (gtag.js) - Google Analytics -->
#         <script async src="https://www.googletagmanager.com/gtag/js?id=UA-154901818-2"></script>
#         <script>
#           window.dataLayer = window.dataLayer || [];
#           function gtag(){dataLayer.push(arguments);}
#           gtag('js', new Date());

#           gtag('config', 'UA-154901818-2');
#         </script>
#         {%metas%}
#         <title>{%title%}</title>
#         {%favicon%}
#         {%css%}
#         <script type='text/javascript' src='https://platform-api.sharethis.com/js/sharethis.js#property=5e5e32508d3a3d0019ee3ecb&product=sticky-share-buttons&cms=website' async='async'></script>
#     </head>
#     <body>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#     </body>
# </html>"""


final = io.load_map_data()

df_states = pd.read_csv('../data/tests/casos_estados.csv')
df_states = transform.transform_mytable(df_states)

firstDay   = min(df_states['date'])
lastDay    = max(df_states['date'])
firstDayDt = datetime.strptime(str(firstDay)[:10], "%Y-%m-%d")
lastDayDt  = datetime.strptime(str(lastDay)[:10], "%Y-%m-%d")
daysOutbreak = (lastDayDt - firstDayDt).days

today_data = df_states.query(f"state=='BRASIL' & date=='{lastDay}'")


avaliable_states = final['nome_uf'].unique().tolist()




header = dash_statics.header(latestDate=lastDay,confirmedCases=today_data['confirmed'].values[0])


card1, card2, card3= dash_statics.cards(daysOutbreak,today_data)


dropdown1 =  dcc.Dropdown(
	id='selected_state',
	options=[{'label':i, 'value':i} for i in avaliable_states],
	# value=['US','IT','ES','DE', 'CN','FR','UK','BR'],
	value=['São Paulo','Rio de Janeiro'],

	multi=True
)


app.layout = html.Div(style={'backgroundColor': '#fafbfd'},
	children = [
		
		dbc.Row(
			dbc.Col(header)
			),

		dbc.Row(
			children = [
				dbc.Col(card1),
				dbc.Col(card2),
				dbc.Col(card3),
			],
			className='cards',
			),
			
		dbc.Row(
			dbc.Col(dropdown1),
			className="dbox-1"
			),
	
		# dbc.Row([
		# 	dbc.Col(
		# 		dcc.Graph(id='country-graphic11'),
		# 		# width=5,
		# 		md=6,
		# 	),
		
		# 	dbc.Col(
		# 		dcc.Graph(id='country-graphic12'),
		# 		# width=5,
		# 		md=6,
		# 	),
		
		# ]),


		dbc.Row( 
		    dbc.Col(dcc.Graph(id='map-box')),
			className = "mapa"
		),


])

# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })



@app.callback(
    Output(component_id = 'map-box', component_property = 'figure'),
    [Input(component_id = 'selected_state', component_property= 'value')]
)
def update_graph2(state):
	
    # themes = yaml.load(open('../themes/custom_colorscales_dash.yaml', 'r'), Loader=yaml.FullLoader)

    fig = vis_dash.plot_city_map(final)
    
    return fig










# @app.callback(
# 	[Output(component_id = 'country-graphic11', component_property = 'figure'),
# 	 Output(component_id = 'country-graphic12', component_property = 'figure'),
# 	 Output(component_id = 'country-graphic21', component_property = 'figure'),
# 	 Output(component_id = 'country-graphic22', component_property = 'figure')],
	
# 	[Input(component_id = 'selected_country', component_property= 'value')]
# )
# def update_graph(geoids):
	
# 	themes = yaml.load(open('../themes/custom_colorscales_dash.yaml', 'r'), Loader=yaml.FullLoader)

# 	fig11 = vis_dash.total_casos(
# 		df            = df_all_countrys,
# 		mask_countrys = df_all_countrys['countrycode'].isin(geoids),
# 		themes        = themes['all_world_dash'],
# 		var           = 'cases',
# 		date          = today,
# 		save          = False
# 		)
	
# 	fig12 = vis_dash.total_casos(
# 		df            = df_all_countrys,
# 		mask_countrys = df_all_countrys['countrycode'].isin(geoids),
# 		themes        = themes['all_world_dash'],
# 		var           = 'deaths',
# 		date          = today,
# 		save          = False
# 		)
	
# 	fig21 = vis_dash.total_casos(
# 		df            = df_all_countrys,
# 		mask_countrys = df_all_countrys['countrycode'].isin(geoids),
# 		themes        = themes['all_world_dash'],
# 		var           = 'new_cases',
# 		date          = today,
# 		save          = False
# 		)
	
# 	fig22 = vis_dash.total_casos(
# 		df            = df_all_countrys,
# 		mask_countrys = df_all_countrys['countrycode'].isin(geoids),
# 		themes        = themes['all_world_dash'],
# 		var           = 'new_deaths',
# 		date          = today,
# 		save          = False
# 		)

# 	return fig11, fig12, fig21, fig22

# @app.callback(
#     Output(component_id = 'country-graphic2', component_property = 'figure'),
#     [Input(component_id = 'selected_country2', component_property= 'value')]
# )
# def update_graph2(geoid):
	
#     themes = yaml.load(open('../themes/custom_colorscales_dash.yaml', 'r'), Loader=yaml.FullLoader)

#     fig = vis_dash.total_by_country_dash(
#         df     = df_single_country,
#         geoid  = geoid,
#         themes = themes['by_country_dash'],
#         data   = today,
#         save   = False
#         )
	
#     return fig

if __name__ == '__main__':
	app.run_server(debug=True)








