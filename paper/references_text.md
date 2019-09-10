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

## Trades per minute


## Short long



## Shift
