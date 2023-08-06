import ipywidgets as widgets
from IPython.display import display, HTML
from datetime import datetime

# Predefined tickers
predefined_tickers = ["AAP", "TSLA", "SPX", "SPY"]

# Create widgets
ticker_box = widgets.VBox([widgets.Label("Tickers")])
date_box = widgets.VBox([widgets.Label("Dates")])
strike_box = widgets.VBox([widgets.Label("Strikes")])
ticker_rows = []
date_inputs = []
strike_inputs = []

# Function to add a new ticker row
def add_ticker_row(ticker):
    ticker_row = widgets.HBox([widgets.Label(ticker)], layout=widgets.Layout(border="1px solid black"))
    ticker_rows.append(ticker_row)
    ticker_box.children = [ticker_box.children[0]] + ticker_rows

    date_input = widgets.DatePicker(description="Date", value=datetime(2021, 7, 15))
    strike_input = widgets.Text(description="Strike")
    date_inputs.append(date_input)
    strike_inputs.append(strike_input)

    date_box.children = [date_box.children[0]] + [date_input]
    strike_box.children = [strike_box.children[0]] + [strike_input]

# Add predefined tickers
for ticker in predefined_tickers:
    add_ticker_row(ticker)

new_ticker_input = widgets.Text(placeholder="Enter new ticker")
ticker_column = widgets.VBox([ticker_box, new_ticker_input])

# Define function to handle new ticker input
def add_ticker(sender):
    ticker = new_ticker_input.value
    if ticker:
        add_ticker_row(ticker)
        new_ticker_input.value = ""

# Register add_ticker function as an event handler for new ticker input
new_ticker_input.on_submit(add_ticker)

# Create top date inputs
top_date_input1 = widgets.DatePicker(description="Top Date 1", value=datetime(2021, 7, 15))
top_date_input2 = widgets.DatePicker(description="Top Date 2", value=datetime(2021, 8, 15))

# Function to update individual ticker row dates
def update_row_dates(change):
    new_date = change['new']
    index = date_inputs.index(change.owner)
    date_inputs[index].value = new_date

# Register update_row_dates function as an event handler for individual date inputs
for date_input in date_inputs:
    date_input.observe(update_row_dates, 'value')

# Create layout for top date inputs
top_dates_box = widgets.HBox([top_date_input1, top_date_input2])

# Create layout for the columns
column_layout = widgets.HBox([ticker_column, date_box, strike_box])

# Display the GUI
display(top_dates_box, column_layout)
