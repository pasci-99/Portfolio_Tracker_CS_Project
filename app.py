import streamlit as st
import yfinance as yf

# Function to get stock suggestions based on user input
def get_stock_suggestions(query):
    suggestions = yf.Ticker(query).suggestions
    return [s['symbol'] for s in suggestions]

# Streamlit app
def main():
    st.title("Stock Comparison App")

    # User input for the first stock
    stock1 = st.text_input("Enter the first stock symbol:", "").upper()
    stock1_suggestions = get_stock_suggestions(stock1)

    # Display suggestions for the first stock
    if stock1_suggestions:
        st.write("Suggestions for the first stock:", stock1_suggestions)

    # User input for the second stock
    stock2 = st.text_input("Enter the second stock symbol:", "").upper()
    stock2_suggestions = get_stock_suggestions(stock2)

    # Display suggestions for the second stock
    if stock2_suggestions:
        st.write("Suggestions for the second stock:", stock2_suggestions)

    # Compare stocks when the user submits
    if st.button("Compare Stocks"):
        if stock1 and stock2:
            # Fetch stock data
            data1 = yf.download(stock1, start="2022-01-01", end="2023-01-01")
            data2 = yf.download(stock2, start="2022-01-01", end="2023-01-01")

            # Display stock data or any other desired comparison
            st.write("Stock 1 data:")
            st.write(data1)

            st.write("Stock 2 data:")
            st.write(data2)

if __name__ == "__main__":
    main()
