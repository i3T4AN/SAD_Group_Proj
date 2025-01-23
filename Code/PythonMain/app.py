from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)

def get_stock_recommendation(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    info = stock.info
    recommendation = "Hold"
    if info.get("recommendationKey") == "buy":
        recommendation = "Buy"
    elif info.get("recommendationKey") == "sell":
        recommendation = "Sell"
    return {
        "name": info.get("longName", stock_symbol),
        "symbol": stock_symbol,
        "price": info.get("regularMarketPrice"),
        "recommendation": recommendation,
    }

@app.route("/")
def index():
    stock_data = get_stock_recommendation("AAPL")  # Example stock symbol
    return render_template("index.html", stock=stock_data)

if __name__ == "__main__":
    app.run(debug=True)
