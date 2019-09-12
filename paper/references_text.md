# References text

## Introduction

**Inferring Trade Direction from Intraday Data**
The increasing availability of intraday trade and quote data is opening new
frontiers for financial market research. The improved ability to discern
whether a trade was a buy order or a sell order is of particular importance.
(Trades classification)

The intraday trade and quote data do not identify whether a trade was
triggered by a market buy or sell order, so this information must be inferred
from the data.
(Trades classification)

**Empirical properties of asset returns: stylized facts and statistical issues**
Although statistical properties of prices of stocks and commodities and market
indexes have been studied using data from various markets and instruments for
more than half a century, the availability of large data sets of high-frequency
price series and the application of computer-intensive methods for analysing
their properties have opened new horizons to researchers in empirical finance
in the last decade and have contributed to the consolidation of a data-based
approach in financial modelling.
(Introduction)

$S\left(t\right)$ will denote the price of a financial asset —a stock, an
exchange rate or a market index— and $X\left(t\right) = \ln S\left(t\right)$
its logarithm. Given a time scale $\Delta t$, which can range from a few
seconds to a month, the log return at scale $\Delta t$ is defined as:
$$r\left(t,\Delta t\right)=X\left(t+\Delta t\right)-X\left(t\right)$$
(Returns definition)

As revealed by a casual examination of most financial newspapers and journals,
the view point of many market analysts has been and remains an event-based
approach in which one attempts to ‘explain’ or rationalize a given market
movement by relating it to an economic or political event or announcement.
From this point of view, one could easily imagine that, since different assets
are not necessarily influenced by the same events or information sets, price
series obtained from different assets and—a fortiori—from different markets
will exhibit different properties. After all, why should properties of corn
futures be similar to those of IBM shares or the Dollar/Yen exchange rate?
Nevertheless, the result of more than half a century of empirical studies on
financial time series indicates that this is the case if one examines their
properties from a statistical point of view: the seemingly random variations
of asset prices do share some quite non-trivial statistical properties. Such
properties, common across a wide range of instruments, markets and time
periods are called stylized empirical facts.
(statistical properties in financial time series)

Mandelbrot pointed out the insufficiency of the normal distribution for
modelling the marginal distribution of asset returns and their heavy-tailed
character. Since then, the non-Gaussian character of the distribution of price
changes has been repeatedly observed in various market data. One way to
quantify the deviation from the normal distribution is by using the kurtosis of
the distribution $F_T$ defined as
$$\kappa=\frac{\left\langle \left(r\left(t,T\right)-\left\langle
  r\left(t,T\right)\right\rangle \right)^{4}\right\rangle }
  {\sigma\left(T\right)^{4}}-3$$
The kurtosis is defined such that $\kappa = 0$ for a Gaussian distribution, a
positive value of $\kappa$ indicating a ‘fat tail’, that is, a slow asymptotic
decay of the PDF.
(Kurtosis and fat tails)

**What really causes large price changes?**
To understand our results it is essential that the reader understand the
double continuous auction, which is the standard mechanism for price formation
in most modern financial markets. Agents can place different types of orders,
which can be grouped into two categories: Impatient traders submit market
orders, which are requests to buy or sell a given number of shares immediately
at the best available price. More patient traders submit limit orders, or
quotes which also state a limit price $\pi$, corresponding to the worst
allowable price for the transaction. (Note that the word “quote” can be used
either to refer to the limit price or to the limit order itself). Limit orders
often fail to result in an immediate transaction, and are stored in a queue
called the limit order book. Buy limit orders are called bids, and sell limit
orders are called offers or asks. At any given time there is a best (lowest)
offer to sell with price $a\left(t\right)$, and a best (highest) bid to buy
with price $b\left(t\right)$. These are also called the inside quotes or the
best prices. The price gap between them is called the spread
$s\left(t\right) = a\left(t\right)−b\left(t\right)$. Prices are not continuous,
but rather change in discrete quanta called ticks, of size $\Delta p$. The
number of shares in an order is called either its size or its volume.
(Double continuous auction explanation)

A high density of limit orders per price results in high liquidity for market
orders, i.e., it implies a small movement in the best price when a market
order is placed.
(Liquidity)

There are a variety of different order types defined in real markets, whose
details differ from market to market. For our purposes here, any given order
can always be decomposed into two types: We will call any component of an
order that results in immediate execution an effective market order, and any
component that is not executed immediately, and is stored in the limit order
order book, an effective limit order.
Throughout the remainder of the paper we will simply call an effective limit
order a “limit order”, and an effective market market order a “market order”.
(effective market and limit order)

When a market order arrives it can cause changes in the best prices. This is
called market impact or price impact. Note that the price changes are always
in the same direction: A buy market order will either leave the best ask the
same or make it bigger, and a sell market order will either leave the best bid
the same or make it smaller. The result is that buy market orders can increase
the midprice $m\left(t\right) = \nicefrac{a\left(t\right) + b\left(t\right)}{2}$,
and sell orders can decrease it.
(Market impact or price impact)

There is no unique notion of price in a real market. We will let $\pi$ be the
limit price of a limit order, and
$m\left(t\right) = \nicefrac{a\left(t\right) + b\left(t\right)}{2}$ be the
midpoint price or midprice defined by the best quotes. All the results of this
paper concern the midprice, rather than transaction prices, but at longer
timescales this makes very little difference, since the midpoint and
transaction prices rarely differ by more than half the spread. The midpoint
price is more convenient to study because it avoids problems associated with
the tendency of transaction prices to bounce back and forth between the best
bid and ask. Price changes are typically characterized as returns
$r_{\tau} }left(t\right) = \ln m\left(t\right) − ln m\left(t − \tau \left)$.
(Explanation use midpoint price)

The arrival of three kinds of events can cause the midprice to change:

* Market orders. A market order bigger than the opposite best quote widens the
  spread by increasing the best ask if it is a buy order, or decreasing the
  best bid if it is a sell order.
* Limit orders. A limit order that falls inside the spread narrows it by
  increasing the best bid if it is a buy order, or decreasing the best ask if
  it is a sell order.
* Cancellations. A cancellation of the last limit order at the best price
  widens the spread by either increasing the best ask or decreasing the best
  bid.
(Changes in the midpoint price)

## Trades per minute


## Short long



## Shift
