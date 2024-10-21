from flask import Flask, render_template, request

app = Flask(__name__)
DISCOUNT = 5

def intra_day_trade(investment_amount, stock_price, short_selling=False):
    intra_day_stock_price = stock_price / DISCOUNT
    current_portfolio_amount = (investment_amount *  DISCOUNT)
    number_of_shares = investment_amount / intra_day_stock_price

    results = []
    stop_loss = stock_price * 0.007

    stoploss_for_intraday = stock_price - stop_loss

    stoploss_for_shortselling = stock_price + stop_loss     
    stop_loss = stoploss_for_shortselling if short_selling else stoploss_for_intraday
    for profit in range(1000, 10001, 500):
        intra_day_share_price = stock_price + profit / number_of_shares
        short_selling_share_price = stock_price - profit / number_of_shares
        
        if short_selling:
            results.append({'profit_goal': profit, 'price': short_selling_share_price})
        else:
            results.append({'profit_goal': profit, 'price': intra_day_share_price})

    return current_portfolio_amount, number_of_shares, stop_loss, results

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        investment_amount = float(request.form.get("investment_amount"))
        stock_price = float(request.form.get("stock_price"))
        short_selling = request.form.get("short_selling") == "on"

        current_portfolio_amount, number_of_shares, stop_loss, trade_results = intra_day_trade(investment_amount, stock_price, short_selling)

        return render_template("index.html", 
                               current_portfolio_amount=current_portfolio_amount,
                               number_of_shares=number_of_shares,
                               stop_loss = stop_loss,
                               trade_results=trade_results,
                               short_selling=short_selling)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
