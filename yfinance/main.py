import yfinance.stock_utils as stock_utils

import typer
from typing_extensions import Annotated
from typing import List, Optional


# Main method variables
app = typer.Typer(pretty_exceptions_show_locals=False)
state = {}


@app.command()
def stock(tickers: Annotated[
    List[str], typer.Argument(help="Stock tickers symbols")] = None ):

    stocks = [] # Collection of data fields for given stock tickers.

    # If no stock tickers, return early.
    if tickers == None:
        return stocks

    # Populating stocks with ticker data
    for ticker in tickers:
        stock_data = stock_utils.fetchStock(ticker.upper()) # Forcing ticker to upper case
        for data in stock_data:
            stocks.append(data)

    # Writing output
    stock_utils.out(stocks, state["csv"], state["json"], state["console"])

    return stocks


@app.callback()
def main(
        console:
        Annotated[
            Optional[bool],
            typer.Option(
                help="Prints stock information to terminal window."
            )] = False,
        csv: Annotated[
            Optional[typer.FileText],
            typer.Option(mode="w+")] = None,
        json: Annotated[
            Optional[typer.FileText],
            typer.Option(mode="w+")] = None,):

    state['console'] = console
    state['csv'] = csv
    state['json'] = json


if __name__ == "__main__":
    app()