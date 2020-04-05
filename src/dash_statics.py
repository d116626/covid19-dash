
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc



def header(latestDate,confirmedCases):
    return html.Div(style={'marginRight': '1.5%',},
        id ='header',
        children=[
            html.H4(
                children="Coronavirus Monitor"),
            html.P(
                id="description",
                children=dcc.Markdown(
                    children=(
                    '''
                    On Dec 31, 2019, the World Health Organization (WHO) was informed 
                    an outbreak of “pneumonia of unknown cause” detected in Wuhan, Hubei Province, China. 
                    
                    The virus that caused the outbreak of COVID-19 was lately known as _severe acute respiratory syndrome coronavirus 2_ (SARS-CoV-2). 
                    
                    The WHO declared the outbreak to be a Public Health Emergency of International Concern on 
                    Jan 30, 2020 and recognized it as a pandemic on Mar 11, 2020. As of {}, there are {:,d} cases of COVID-19 confirmed globally.
                    
                    This dash board is developed to visualise and track the recent reported 
                    cases on a hourly timescale.'''.format(latestDate, confirmedCases),
                    )
                )
            ),
            html.Hr(style={'marginTop': '.5%'},),
                ]
            ),
    
def cards(daysOutbreak, today_data):
    
    
    card1 = dbc.Card(
        dbc.CardBody(
            [
                html.H1(
                    style={'textAlign': 'center', 'color': '#ffffff', 'padding': '.5rem', 'font-size': '2rem', 'font-weight': 'bold'},
                    children=' ',
                    ),
                html.H1(
                    style={'textAlign': 'center', 'color': '#2674f6', 'padding': '.5rem', 'font-size': '7rem', 'font-weight': 'bold'},
                    children=f"{daysOutbreak}",


                ),
                html.P(
                    style={'textAlign': 'center', 'color': '#2674f6', 'padding': '.5rem', 'font-size': '3rem', 'font-weight': 'normal'},
                    children='dias desde o primeiro caso',
                ),
            ],
            className="mb-3",

        ),
        # className="mb-3",
        className= "mb-3 h-100",
        

    )
    
    card2 = dbc.Card(
        dbc.CardBody(
            [
                # html.H4("Title", className="card-title"),
                html.H1(
                    style={'textAlign': 'center', 'color': '#d7191c', 'padding': '.5rem', 'font-size': '2rem', 'font-weight': 'bold'},
                    children='+ {:,d} nas ultimas 24h ({:.1%})'.format(today_data['new_cases'].values[0], today_data['new_cases'].values[0]/(today_data['confirmed'].values[0]- today_data['new_cases'].values[0])),
                ),
                html.H1(
                    style={'textAlign': 'center', 'color': '#d7191c', 'padding': '.5rem', 'font-size': '7rem', 'font-weight': 'bold'},
                    children='{:,d}'.format(today_data['confirmed'].values[0]),
                ),
                html.P(
                    style={'textAlign': 'center', 'color': '#d7191c', 'padding': '.5rem', 'font-size': '3rem', 'font-weight': 'normal'},
                    children='casos confirmados',
                ),
            ],
            className="mb-3",

        ),
        className="mb-3 h-100",

    
    ),
        
    card3 = dbc.Card(
        dbc.CardBody(
            [
                # html.H4("Title", className="card-title"),
                html.H1(
                    style={'textAlign': 'center', 'color': '#6C6C6C', 'padding': '.5rem', 'font-size': '2rem', 'font-weight': 'bold'},
                    children='+ {:,d} nas ultimas 24h ({:.1%})'.format(today_data['new_deaths'].values[0], today_data['new_deaths'].values[0]/(today_data['deaths'].values[0]- today_data['new_deaths'].values[0]))
                ),
                html.H1(
                    style={'textAlign': 'center', 'color': '#6C6C6C', 'padding': '.5rem', 'font-size': '7rem', 'font-weight': 'bold'},
                    children='{:,d}'.format(today_data['deaths'].values[0])
                ),
                html.P(
                    style={'textAlign': 'center', 'color': '#6C6C6C', 'padding': '.5rem', 'font-size': '3rem', 'font-weight': 'normal'},
                    children='mortes confirmadas',
                ),
            ],
            className="mb-3",

        ),

    className="mb-3 h-100",

    )
    
    
    return card1, card2, card3