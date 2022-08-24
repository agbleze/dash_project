# %% import modules
import pandas as pd
import numpy as np
import plotly.express as px
from datar.all import case_when, f, mutate, pivot_wider
from urllib.parse import unquote

#%%
full_data = pd.read_csv(r'full_data.csv')


#%%
#Dash imports
import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import dash_trich_components as dtc
from dash.exceptions import PreventUpdate

#%%
from style import cardbody_style, card_icon, cardimg_style, card_style
import analytic_page
from helper_components import output_card
#%%
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.CYBORG, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME])


start_page = html.Div(
    children=[     
        dcc.Location(id='location_url'),
        dbc.Row(html.Div(id="page_location"))
        ],
)

homepage = html.Div(children=[
    
    dbc.Container(children=[       
        dbc.Row([
                    html.H3('Analysis on Living Standard Measurement Survey')                    
                ]
            ),
        html.Br(),
        dbc.Row(
                children=[
                    dbc.Tabs(
                        children=[
                                    dbc.Tab(
                                            children=[
                                                        html.Ul(
                                                            [
                                                                html.Br(),
                                                                html.Li('Number of states in Nigeria:37'),
                                                                html.Li('Number of lga:774'),
                                                                html.Li('Currency:Naira'),
                                                                html.Li('Population:175 million:2014 estimate'),
                                                                html.Li([
                                                                        'Source:',
                                                                        html.A('https://nigerianfinder.com/facts-about-nigeria/',
                                                                                href='https://nigerianfinder.com/facts-about-nigeria/'
                                                                                )
                                                                        ]
                                                                    )
                                                            ]
                                                        )
                                                    ], 
                                            label='Key Facts'
                                        ),
                                    dbc.Tab([
                                        html.Ul([
                                            html.Br(),
                                            html.Li('General Household Survey, Panel 2015-2016,'),
                                            html.Li('Analyzing and visualizing average expenditure of selected items by States'),
                                            html.Li('Dash presentation pracice'),
                                            html.Li([
                                                'Source:',
                                                    html.A('https://microdata.worldbank.org/index.php/catalog/2734/data-dictionary',
                                                        href='https://microdata.worldbank.org/index.php/catalog/2734/data-dictionary'),
                                                        
                                                    ])
                                        ])
                                    ], label='Project Info')
                                ]
                            ),
    
                        ]
                    ),
                html.Br(),
        dbc.Row([
                 dbc.Col([
                         dbc.Card(
                            [
                                dbc.CardImg(
                                    src='./Img/firmbee-com-jrh5lAq-mIs-unsplash.jpeg',
                                
                                    style=cardimg_style,
                                ),
                                dbc.CardLink(id="analytics_link",
                                    children=[
                                        dbc.CardImgOverlay(
                                            [
                                                dbc.CardBody(
                                                    html.H3(
                                                        "Analytics",
                                                        style=cardbody_style,
                                                    )
                                                )
                                            ]
                                        )
                                    ],
                                    href="analytics",
                                ),
                            ],
                            style=card_style,
                        )
                     #])
                     ]),
                 html.Br(),
                 dbc.Col([
                        dbc.Card(
                            dbc.Card(
                                [
                                    dbc.CardImg(
                                        src=img2,
                                        style=cardimg_style,
                                    ),
                                    dbc.CardLink(id="ml_link",
                                        children=[
                                            dbc.CardImgOverlay(
                                                [
                                                    dbc.CardBody(
                                                        html.H3(
                                                            "Machine leARNING",
                                                            style=cardbody_style,
                                                        )
                                                    )
                                                ]
                                            )
                                        ],
                                        href="ml",
                                    ),
                                ],
                                style=card_style,
                            )
                        )
                    ])   
        ])
                ],
                  
            ),
    
        
        
    ])
#])


ml_page = html.Div([])

app.layout = start_page
app.validation_layout = html.Div([homepage, analytic_page.page_view, ml_page])

######## callback  ######
@app.callback(Output(component_id="page_location", component_property="children"),
              Input(component_id="location_url", component_property="href")
              )
def render_page_selected(page_link):
    page_selected = page_link.split('/')[-1]
    
    if page_selected == 'ml':
        return ml_page
    elif page_selected == 'analytics':
        return analytic_page.page_view
    else:
        return homepage
 
## Expenditure callbacks    
@app.callback(Output(component_id='avg_expense', component_property='children'),
              Output(component_id='max_expense', component_property='children'),
              Output(component_id='min_expense', component_property='children'),
              Output(component_id='expense_bargraph', component_property='figure'),
              Output(component_id='expense_histgraph', component_property='figure'),
              Input(component_id='expense_state_dropdown', component_property='value'))
def render_state_avg_income(state_selected):
    state_df = full_data[full_data['state_name'] == state_selected] 
    state_avg_expd = state_df['expenditure'].mean()  
    state_max_expd = state_df['expenditure'].max()
    state_min_expd = state_df['expenditure'].min()
    df=state_df.groupby(['item_desc'])['expenditure'].mean().reset_index()
    
    fig = px.bar(
                data_frame=df,
                x="item_desc",
                y="expenditure",
                #barmode="group",
                color="item_desc",
                labels={"item_desc": "Fuel type"},
                title=f"Average fuel expenditure by fuel type in {state_selected}",
                template="plotly_dark",
    )
    fig.layout.bargroupgap = 0.2
    
    fig2 = px.histogram(data_frame=state_df, x="expenditure",
                        title=f"Distribution of expenditure in {state_selected}",
                        template="plotly_dark"
                        )

    return (f'{round(state_avg_expd)}', 
            f'{round(state_max_expd)}',
            f'{round(state_min_expd)}',
            fig, fig2
            )

## expenditure for sector
@app.callback(Output(component_id="id_sector_type", component_property="children"),
              Output(component_id="avg_sector_expense", component_property="children"),
              Output(component_id="max_sector_expense", component_property="children"),
              Output(component_id="min_sector_expense", component_property="children"),
              Output(component_id="expense_sector_histgraph", component_property="figure"),
              Output(component_id="expense_sector_bargraph", component_property="figure"),
              Input(component_id="expense_sector_dropdown", component_property="value")
              )
def render_sector_expense(sector_selected):
    sector_df = full_data[full_data['sector_name'] == sector_selected]
    sector_expense_avg = sector_df['expenditure'].mean()
    sector_expense_max = sector_df['expenditure'].max()
    sector_expense_min = sector_df['expenditure'].min()
    
    fig_sec_hist = px.histogram(data_frame=sector_df, x='expenditure',
                                title=f"Distribution of expenditure in {sector_selected}",
                                template="plotly_dark"
                            )
    
    avg_sector_df = sector_df.groupby(['item_desc'])['expenditure'].mean().reset_index()
    fig_sec_bar = px.bar(data_frame=avg_sector_df, x='item_desc', y='expenditure',
                        template = "plotly_dark",
                        labels={'item_desc': 'fuel_type'},
                        title=f'Average expenditure per fuel type in {sector_selected}', 
                        color='item_desc'
                        )
    fig_sec_bar.layout.bargroupgap = 0.2
    
    return(sector_selected,
           f'{round(sector_expense_avg)}',
           f'{round(sector_expense_max)}',
           f'{round(sector_expense_min)}',
           fig_sec_hist,
           fig_sec_bar
           )


@app.callback(
    Output("content", "children"),
    Input("income_sidebar", "n_clicks_timestamp"),
    Input("credit_sidebar", "n_clicks_timestamp"),
    Input("expend_sidebar", "n_clicks_timestamp")
)
def show_sidebar_content(income_sidebar: str, credit_sidebar: str, expend_sidebar: str):
    ctx = dash.callback_context
    button_clicked = ctx.triggered[0]["prop_id"].split(".")[0]

    if not ctx.triggered:
        button_clicked = "None"
    elif button_clicked == "income_sidebar":
        return analytic_page.income_page
    elif button_clicked == "credit_sidebar":
        return analytic_page.credit_page
    elif button_clicked == "expend_sidebar":
        return analytic_page.expend_page
    else:
        return analytic_page.welcome_page
   

##  render state income    
@app.callback(Output(component_id="avg_income", component_property="children"),
              Output(component_id="max_income", component_property="children"),
              Output(component_id="min_income", component_property="children"),
              Input(component_id="income_state_dropdown", component_property="value")
              )
def render_income_values(state_selected: str) -> int:
    if not state_selected:
        PreventUpdate
    state_df = full_data[full_data['state_name'] == state_selected]
    state_income_avg = state_df['income'].mean()
    state_income_max = state_df['income'].max()
    state_income_min = state_df['income'].min()
    
    return(#sector_selected,
           round(state_income_avg),
           round(state_income_max),
           round(state_income_min),
           #fig_sec_hist,
           #fig_sec_bar
           )
    

## render sector income
@app.callback(Output(component_id="avg_sector_income", component_property="children"),
              Output(component_id="max_sector_income", component_property="children"),
              Output(component_id="min_sector_income", component_property="children"),
              Output(component_id='id_income_sector_type', component_property='children'),
              Input(component_id="income_sector_dropdown", component_property="value")
              )
def render_sector_income_values(sector_selected: str) -> int:
    if not sector_selected:
        PreventUpdate
    state_df = full_data[full_data['sector_name'] == sector_selected]#.dropna()
    sector_income_avg = state_df['income'].mean()
    sector_income_max = state_df['income'].max()
    sector_income_min = state_df['income'].min()
    
    return(
        round(sector_income_avg),
        round(sector_income_max),
        round(sector_income_min),
        sector_selected
    )


## render credict amount
@app.callback(Output(component_id="avg_credict", component_property="children"),
              Output(component_id="max_credict", component_property="children"),
              Output(component_id="min_credict", component_property="children"),
              Input(component_id="credict_state_dropdown", component_property="value")
              )
def render_credit_values(state_selected: str) -> int:
    state_df = full_data[full_data['state_name'] == state_selected]#.dropna()
    state_credit_avg = state_df['credit'].mean()
    state_credit_max = state_df['credit'].max()
    state_credit_min = state_df['credit'].min()
    
    return (
        f'{round(state_credit_avg)}',
        f'{round(state_credit_max)}',
        f'{round(state_credit_min)}'
    )
    
    
## render sector credict
@app.callback(Output(component_id="avg_sector_credict", component_property="children"),
              Output(component_id="max_sector_credict", component_property="children"),
              Output(component_id="min_sector_credict", component_property="children"),
              Output(component_id='id_credict_sector_type', component_property='children'),
              Input(component_id="credict_sector_dropdown", component_property="value")
              )
def render_credit_values(sector_selected: str) -> int:
    sector_df = full_data[full_data['sector_name'] == sector_selected]
    sector_credit_avg = sector_df['credit'].mean()
    sector_credit_max = sector_df['credit'].max()
    sector_credit_min = sector_df['credit'].min()
    
    return (
        f'{round(sector_credit_avg)}',
        f'{round(sector_credit_max)}',
        f'{round(sector_credit_min)}',
        sector_selected
    )


if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False, port='8013')
   
