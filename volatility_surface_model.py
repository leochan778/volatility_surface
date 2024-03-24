# volatility surface model
import yfinance as yf
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

def fetch_expiry_dates(symbol):
    expiry_dates = yf.Ticker(symbol).options
    return expiry_dates

def fetch_option_chain(symbol, expiry_date):
    option_chain = yf.Ticker(symbol).option_chain(expiry_date)
    return option_chain

def calculate_implied_volatility(option_chain, option_type, use_log):
    implied_volatilities = option_chain[0 if option_type == 'calls' else 1]['impliedVolatility'].to_numpy()
    if use_log:
        return np.log(implied_volatilities)  # Log-transform the implied volatilities
    else:
        return implied_volatilities

def build_volatility_surface(symbol, expiry_dates, option_type, use_log):
    all_strikes = []
    all_implied_volatilities = []
    expiry_indices = []

    for i, expiry_date in enumerate(expiry_dates):
        option_chain = fetch_option_chain(symbol, expiry_date)
        implied_volatilities = calculate_implied_volatility(option_chain, option_type, use_log)

        if len(implied_volatilities) == 0:
            print(f"No {option_type} data found in option chain")
            continue

        strikes = option_chain[0 if option_type == 'calls' else 1]['strike'].to_numpy()

        all_strikes.extend(strikes)
        all_implied_volatilities.extend(implied_volatilities)
        expiry_indices.extend([i] * len(strikes))

    X = np.array(expiry_indices)
    Y = np.array(all_strikes)
    Z = np.array(all_implied_volatilities)

    return X, Y, Z, expiry_dates

def plot_volatility_surface(X, Y, Z, expiry_dates):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(X, Y, Z, cmap='viridis')
    ax.set_xlabel('Expiry Dates')
    ax.set_ylabel('Strike Prices')
    ax.set_zlabel('Log Implied Volatility')  # Default to log scale

    # Show only every 3rd expiry date on x-axis
    ax.set_xticks(np.arange(0, len(expiry_dates), 3))
    ax.set_xticklabels(expiry_dates[::3])

    if save_path:
        plt.savefig(save_path)  # Save the plot to the specified file path

    plt.show()

if __name__ == "__main__":
    symbol = 'WBD'
    expiry_dates = fetch_expiry_dates(symbol)
    option_type = 'calls'  # Change this to 'puts' if needed
    use_log = True  # Change this to False if you don't want log scale

    X, Y, Z, expiry_dates = build_volatility_surface(symbol, expiry_dates, option_type, use_log)
    save_path = "volatility_surface.png"
    plot_volatility_surface(X, Y, Z, expiry_dates)
