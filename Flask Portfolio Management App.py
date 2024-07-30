
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_cors import CORS
import requests
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime
import os
import hashlib

app = Flask(__name__)
CORS(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

BASE_URL = 'https://query1.finance.yahoo.com/v7/finance/download/'

users = {
    'user1': {
        'username': 'user1',
        'password': 'password1',
        'portfolio': {
            'symbols': ['AAPL', 'GOOGL', 'MSFT'],
            'allocations': [0.4, 0.3, 0.3],
            'start_date': '2020-01-01',
            'end_date': datetime.now().strftime('%Y-%m-%d')
        }
    }
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('portfolio'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        session['username'] = username
        return redirect(url_for('portfolio'))
    else:
        return render_template('login.html', error='Invalid username or password.')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/portfolio')
def portfolio():
    if 'username' not in session:
        return redirect(url_for('index'))

    user = users[session['username']]
    portfolio_data = user['portfolio']
    symbols = portfolio_data['symbols']
    allocations = portfolio_data['allocations']
    start_date = portfolio_data['start_date']
    end_date = portfolio_data['end_date']

    portfolio_prices = {}
    portfolio_returns = {}
    cumulative_returns = {}
    volatility = {}

    for symbol in symbols:
        try:
            params = {
                'period1': int(datetime.strptime(start_date, '%Y-%m-%d').timestamp()),
                'period2': int(datetime.strptime(end_date, '%Y-%m-%d').timestamp()),
                'interval': '1d',
                'events': 'history'
            }
            url = f"{BASE_URL}{symbol}?{urllib.parse.urlencode(params)}"
            response = requests.get(url)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))
                df.set_index('Date', inplace=True)
                df.index = pd.to_datetime(df.index)
                df['Adj Close'] = df['Adj Close'].astype(float)
                portfolio_prices[symbol] = df['Adj Close']
            else:
                return jsonify({'error': f'Failed to fetch data for {symbol}'}), 404

        except Exception as e:
            return jsonify({'error': f'Error fetching data for {symbol}: {str(e)}'}), 500

    for symbol in symbols:
        portfolio_returns[symbol] = portfolio_prices[symbol].pct_change()
        cumulative_returns[symbol] = (portfolio_returns[symbol] + 1).cumprod() - 1
        volatility[symbol] = portfolio_returns[symbol].std() * np.sqrt(252)

    portfolio_returns_df = pd.concat(portfolio_returns.values(), axis=1)
    portfolio_returns_df.columns = symbols

    portfolio_returns_df['Portfolio'] = portfolio_returns_df.mul(allocations).sum(axis=1)

    portfolio_cumulative_returns = (portfolio_returns_df['Portfolio'] + 1).cumprod() - 1

    risk_free_rate = 0
    portfolio_excess_returns = portfolio_returns_df['Portfolio'] - risk_free_rate
    sharpe_ratio = portfolio_excess_returns.mean() / portfolio_excess_returns.std() * np.sqrt(252)

    traces = []
    for symbol in symbols:
        traces.append(go.Scatter(x=cumulative_returns[symbol].index, y=cumulative_returns[symbol], mode='lines', name=symbol))
    traces.append(go.Scatter(x=portfolio_cumulative_returns.index, y=portfolio_cumulative_returns, mode='lines', name='Portfolio', line=dict(dash='dash')))
    layout = go.Layout(title='Cumulative Returns',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title='Cumulative Returns'),
                       legend=dict(orientation='h'))
    fig = go.Figure(data=traces, layout=layout)
    plot_div = fig.to_html(full_html=False, default_height=500, default_width=700)

    return render_template('index.html',
                           symbols=symbols,
                           allocations=allocations,
                           start_date=start_date,
                           end_date=end_date,
                           portfolio_cumulative_returns=portfolio_cumulative_returns.tolist(),
                           portfolio_volatility=portfolio_volatility,
                           sharpe_ratio=sharpe_ratio,
                           plot_div=plot_div,
                           username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)

