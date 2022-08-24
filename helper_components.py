from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_trich_components as dtc
from style import cardbody_style, card_icon, cardimg_style, card_style
import pandas as pd

full_data = pd.read_csv(r'full_data.csv')

def output_card(id: str = None, card_label: str =None,
                style={"backgroundColor": 'yellow'}, 
                icon: str ='bi bi-cash-coin', card_size: int = 4):
    return dbc.Col(lg=card_size,
                    children=dbc.CardGroup(
                        children=[
                            dbc.Card(
                                    children=[
                                        html.H3(id=id),
                                        html.P(card_label)
                                    ]
                                ),
                            dbc.Card(
                                    children=[
                                        html.Div(
                                            className=icon,
                                            style=card_icon
                                        )
                                    ],
                                    style=style
                            )
                        ]
                    )
                )


class Dropdowns:
    def __init__(self, data: pd.DataFrame = full_data) -> None:
        self.data = data
        
    def create_dropdown(self, label_name: str = 'Select Sector',
                        id: str = 'id_income',
                        colname: str = 'sector_name'
                        ):
        return dbc.Col([dbc.Label(label_name),
                        dcc.Dropdown(id=id,
                                    options=[{'label': sector, 'value': sector}
                                            for sector in self.data[colname].unique()
                                            ],
                                    placeholder=label_name
                                ),
                        ]
                    )
           # )
        
        
        

