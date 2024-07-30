# Flask Portfolio Management App

This application is a web-based portfolio management tool built using Flask. It allows users to log in, manage their stock portfolio, and analyze their investments' performance. The app fetches stock data from Yahoo Finance, calculates cumulative returns, volatility, and the Sharpe ratio, and visualizes the data using Plotly.

## Features
- **User Authentication**: Login and logout functionality with session management.
- **Portfolio Management**: Users can view their stock symbols, allocations, and portfolio metrics.
- **Data Fetching**: Fetches historical stock data from Yahoo Finance.
- **Performance Analysis**: Calculates daily returns, cumulative returns, portfolio volatility, and Sharpe ratio.
- **Data Visualization**: Visualizes cumulative returns using Plotly.

## Endpoints and Routes
### Web Pages
- **Index** (`/`): The homepage with login functionality.
- **Login** (`/login`): Handles user authentication.
- **Logout** (`/logout`): Logs the user out and redirects to the homepage.
- **Portfolio** (`/portfolio`): Displays the user's portfolio with metrics and visualizations.

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/waqi786/portfolio-management-app.git
   cd portfolio-management-app

2. Create and activate a virtual environment:

   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required dependencies:

   pip install -r requirements.txt

4. Set up the secret key:
 Ensure that app.secret_key is securely set in the code.

5. Run the application:

   flask run

**Dependencies**

Flask
Flask-CORS
requests
pandas
numpy
plotly
Install the dependencies using the command:

   pip install flask flask-cors requests pandas numpy plotly

**Usage**

**Example User Portfolio**
A sample user portfolio is predefined for demonstration purposes. Users can view stock symbols, allocations, start and end dates, and the calculated metrics.

**Security Considerations**
Secret Key: Ensure the secret key is kept secure and not exposed publicly.
User Data: This demo uses hardcoded user data. For a production application, implement a secure user management system.

**Contribution**

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

**Developed by Waqar Ali.**


### Short Description

A Flask-based portfolio management app for tracking and analyzing stock investments, featuring user authentication, data fetching from Yahoo Finance, and performance visualization using Plotly.

Uploaded Date:

7/29/2024
