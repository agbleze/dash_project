#%%
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_trich_components as dtc
from style import cardbody_style, card_icon, cardimg_style, card_style
from helper_components import output_card, Dropdowns
import pandas as pd

#%%
#lsms_df = pd.read_csv('lsms_df.csv')

full_data = pd.read_csv(r'full_data.csv')

mk_dropdown = Dropdowns()

#%%
#full_data.columns
#%%
expend_page = dbc.Container([
    dbc.Row(
            children=[ 
                    #dbc.Col(lg=1),
                    dbc.Col(lg=2,
                            children=[
                                mk_dropdown.create_dropdown(label_name='Select State',
                                                            id='expense_state_dropdown',
                                                            colname='state_name',
                                                            ),
                                html.Br(), html.Br(), html.Br(),
                                mk_dropdown.create_dropdown(label_name='Select State',
                                                            id='expense_sector_dropdown',
                                                            colname='sector_name'
                                                            )
                            ]
                        
                    ),
                    dbc.Col(lg=9,
                            children=[
                                    dbc.Row(
                                            children=[
                                                        dbc.Row(
                                                                children=[
                                                                    output_card(id='avg_expense',
                                                                                card_label='Avergae Expenditure'
                                                                            ),
                                                                    output_card(id='max_expense',
                                                                                card_label='Maximum Expenditure'
                                                                            ),
                                                                    output_card(id='min_expense',
                                                                                card_label='Minimum Expenditure'
                                                                            )
                                                                    
                                                                ]
                                                            ),
                                            ]
                                        ),
                                    html.Br(), html.Br(),
                                    dbc.Row(
                                            children=[
                                                        dbc.Label(id="id_sector_type"),
                                                        output_card(id='avg_sector_expense',
                                                                    card_label='Average Expenditure'
                                                                ),
                                                        output_card(id='max_sector_expense',
                                                                    card_label='Maximum Expenditure'
                                                                ),
                                                        output_card(id='min_sector_expense',
                                                                    card_label='Minimum Expenditure'
                                                                )
                                                        
                                                    ]
                                    ),
                                    
                                #    html.Div([], id="container_to_render")
                                ]
                            )
            ]
    ),
    html.Br(), html.Br(),
    
    dbc.Row(
        [
            #dbc.Col(lg=2),
            dbc.Col(lg=6, children=dcc.Graph(id='expense_histgraph')),
            dbc.Col(lg=6, children=dcc.Graph(id='expense_bargraph'))
        ]
    ),
    
    html.Br(),
    dbc.Row(
        [
            #dbc.Col(lg=2),
            dbc.Col(lg=6, children=dcc.Graph(id='expense_sector_histgraph')),
            dbc.Col(lg=6, children=dcc.Graph(id='expense_sector_bargraph'))
        ]
    ),
])


income_page = html.Div(
                       children=[
                                dbc.Row(dbc.Row(
                                                [dbc.Col(lg=1),
                                                 
                                                 dbc.Col(lg=2,
                                                        children=[
                                                            mk_dropdown.create_dropdown(
                                                                label_name='Select State',
                                                                id='income_state_dropdown',
                                                                colname='state_name'
                                                            ),
                                                            html.Br(), html.Br(), html.Br(),
                                                            mk_dropdown.create_dropdown(
                                                                id="income_sector_dropdown"
                                                            )
                                                        ]
                                                    
                                                ),
                                                 dbc.Col(lg=9,
                                                         children=[
                                                             dbc.Row(
                                                                 children=[
                                                                     output_card(id='avg_income', 
                                                                                card_label='Average income'
                                                                            ),
                                                                    output_card(id='max_income',
                                                                                card_label='Maximum income'
                                                                                ),
                                                                    output_card(id='min_income',
                                                                                card_label='Minimum income'
                                                                                )
                                                                 ]
                                                             ),
                                                             html.Br(), html.Br(),
                                                             
                                                             dbc.Row(
                                                                    children=[
                                                                                dbc.Label(id="id_income_sector_type"),
                                                                                output_card(id='avg_sector_income',
                                                                                            card_label='Average Income'
                                                                                        ),
                                                                                output_card(id='max_sector_income',
                                                                                            card_label='Maximum Income'
                                                                                        ),
                                                                                output_card(id='min_sector_income',
                                                                                            card_label='Minimum Income'
                                                                                        )
                                                                                
                                                                            ]
                                                            )
                                                         ] 
                                                 ),
                                                
                                                ]
                                            )
                                        )
                    ]
)

credit_page = html.Div([
    dbc.Row(dbc.Row([dbc.Col(lg=1),
                     dbc.Col(lg=2,
                            children=[
                                mk_dropdown.create_dropdown(
                                    label_name='Select State',
                                    id='credict_state_dropdown',
                                    colname='state_name'
                                ), html.Br(), html.Br(), html.Br(),
                                mk_dropdown.create_dropdown(id='credict_sector_dropdown',
                                                            colname='sector_name'
                                                            )
                            ] 
                    ),
                    dbc.Col(lg=9,
                            children=[
                                        dbc.Row(
                                                children=[
                                                        output_card(id='avg_credict', 
                                                                    card_label='Average credit'
                                                                    ),
                                                        output_card(id='max_credict', 
                                                                    card_label='Maximum credit'
                                                                    ),
                                                        output_card(id='min_credict',
                                                                    card_label='Minimum credit'
                                                                    )
                                                        ]
                                            ),
                                        html.Br(), html.Br(),
                                        
                                        dbc.Row(
                                                children=[
                                                            dbc.Label(id="id_credict_sector_type"),
                                                            output_card(id='avg_sector_credict',
                                                                        card_label='Average credit'
                                                                    ),
                                                            output_card(id='max_sector_credict',
                                                                        card_label='Maximum credit'
                                                                    ),
                                                            output_card(id='min_sector_credict',
                                                                        card_label='Minimum credit'
                                                                    )
                                                            
                                                        ]
                                            )

                                ],
                            
                            )
                     
                    ]
                    )
            )
])

welcome_page = html.Div([
    dbc.Row(dbc.Row([dbc.Col(lg=1),
                        output_card(id='welcome', card_label='Welcome')
                    ]
                    )
            )
])

page_view = html.Div(
    [
        dtc.SideBar(children=[
                                dtc.SideBarItem(id='income_sidebar', label='Income', icon='far fa-money-bill-alt'),
                                dtc.SideBarItem(id='credit_sidebar', label='Credit', icon='bi bi-credit-card'),
                                dtc.SideBarItem(id='expend_sidebar', label='Expenditure', icon='bi bi-wallet-fill')
                            ]),
        html.Div([], id="content")
    ]
)
