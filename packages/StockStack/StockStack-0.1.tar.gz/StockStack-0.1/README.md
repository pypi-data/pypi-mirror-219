# StockStack-CLI

Look up and plot current stock prices from your terminal.

This is a Python script for monitoring the current stock prices using the Yahoo Finance API to retrieve the latest
stock prices and display them in the terminal.

## INSTALLATION

1. Make sure to have [yfinance](https://pypi.org/project/yfinance/) and other needed dependecies installed

```
$ pip install -r stockstack/requirements.txt
```

2. Clone this repository to your local machine

```
$ git clone https://github.com/carlobortolan/StockStack.git ~/stockstack
```

3. Add <YOUR_ALIAS> as an alias to your _.bashrc_, _.zshrc_, etc.

```
$ echo 'alias <YOUR_ALIAS>="python3 ~/stockstack/caller.py"'>>~/.bashrc
```

> _**OPTIONAL**: If you want to have StockStack launch whenever you open a new terminal add:_
> ```
> $ echo '<YOUR_ALIAS>'>>~/.bashrc
> ```

4. Update your _.bashrc_, _.zshrc_, etc.

```
$ source ~/.bashrc
```

## USAGE

Retrieve current stock prices.

```
$ <YOUR_ALIAS>  [] [-s STOCK_SYMBOL [STOCK_SYMBOL ...]]
                [-d STOCK_SYMBOL [STOCK_SYMBOL ...]]
                [-u STOCK_SYMBOL [STOCK_SYMBOL ...]] 
                [-p] [--details] [-v] [-h]
```

```
options:
  -h, --help            show this help message and exit
  -s STOCK_SYMBOL [STOCK_SYMBOL ...], --stocks STOCK_SYMBOL [STOCK_SYMBOL ...]
                        List of stocks to monitor.
  -d STOCK_SYMBOL [STOCK_SYMBOL ...], --default_stocks STOCK_SYMBOL [STOCK_SYMBOL ...]
                        Set the default stocks to monitor.
  -u STOCK_SYMBOL [STOCK_SYMBOL ...], --update_default_stocks STOCK_SYMBOL [STOCK_SYMBOL ...]
                        Update the default stocks.
  -p [PLOT], --plot [PLOT]
                        Plot the current or default stocks.
  --details [DETAILS]   Display additional details about a stock.
  -v, --version         show program's version number and exit
```

## EXAMPLES

> _**NOTE**: Replace with your alias if necessary._

To retrieve the current stock prices for a list of stocks, run the script with the following command:

```
python caller.py -s AAPL MSFT TSLA
```

This will display the current prices for Apple, Microsoft and Tesla stocks.

To set the default stocks to monitor, use the `-d` or `--default_stocks` option:

```
python caller.py -d AAPL MSFT
```

This will set the default stocks to Apple and Microsoft.

To update the default stocks, use the `-u` or `--update_default_stocks` option:

```
python caller.py -u AAPL GOOG
```

This will add Apple and Google stocks to the default list (if not already added).

To view the current price of your default list run the script without any options:

```
python caller.py
```

To view details of your default list or other stocks use the `--details` option:

```
python caller.py --details
```

To plot the graph of your default list or other stocks use the `-p` or `--plot` option:

```
python caller.py -p
```

## CONTRIBUTING

Contributions are welcome! If you find a bug or have an idea for a new feature, please open an issue or submit a pull
request.

## LICENSE

This project is licensed under the GPL-3.0 license. See the [LICENSE](LICENSE) file for details.

---

© Carlo Bortolan

> Carlo Bortolan &nbsp;&middot;&nbsp;
> GitHub [carlobortolan](https://github.com/carlobortolan) &nbsp;&middot;&nbsp;
> contact via [carlobortolan@gmail.com](carlobortolan@gmail.com)
