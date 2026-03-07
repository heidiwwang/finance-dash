# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash()

# assume you have a "long-form" data frame
df = pd.read_csv('finance.csv')

# Calculate Summary Statistics
summary = df.groupby('type')['amount'].sum().to_dict()

# Calculate Net Balance (Income - Expense)
income = summary.get('investment', 0) + summary.get('cash', 0)
expense = summary.get('debt', 0) - summary.get('expense', 0)
net_val = income + expense

fig = px.bar(df, x="type", y="amount", color="category", barmode="relative")

app.layout = html.Div(style={'fontFamily': 'Karla, Segoe UI, sans-serif', 'padding': '40px', 'backgroundColor': '#f9f9f9'}, children=[
    html.H1(children='Finance Summary', style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Div(children='''
        Dummy data generated using Gemini
    ''', style={'textAlign': 'center', 'color': '#2c3e50', 'padding': '10px'}),
    
    # Summary Cards Container
    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'marginBottom': '30px', 'padding': '10px'}, children=[
        # Dynamic cards for each type (Income/Expense)
        *[html.Div(children=[
            html.H3(t, style={'margin': '0', 'color': '#7f8c8d', 'fontSize': '16px'}),
            html.P(f"${val:,.2f}", style={'margin': '5px 0 0 0', 'fontSize': '24px', 'fontWeight': 'bold', 'color': '#2c3e50'})
        ], style={
            'padding': '20px', 
            'backgroundColor': 'white', 
            'borderRadius': '10px', 
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
            'minWidth': '200px',
            'textAlign': 'center'
        }) for t, val in summary.items()],

        # Additional Summary Box: Net Balance
        html.Div(children=[
            html.H3("Net Balance", style={'margin': '0', 'color': '#7f8c8d', 'fontSize': '16px'}),
            html.P(f"${net_val:,.2f}", style={'margin': '5px 0 0 0', 'fontSize': '24px', 'fontWeight': 'bold', 'color': '#27ae60' if net_val >= 0 else '#e74c3c'})
        ], style={
            'padding': '20px', 
            'backgroundColor': 'white', 
            'borderRadius': '10px', 
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
            'minWidth': '200px',
            'textAlign': 'center',
            'border': '1px solid #ddd'
        })
    ]),

    dcc.Graph(
        id='overview-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)