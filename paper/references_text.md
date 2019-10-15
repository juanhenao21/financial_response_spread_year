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
(Data availability)

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
(Statistical properties in financial time series)

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

**What really causes large prices changes?**
To understand our results it is essential that the reader understand the double
continuous auction, which is the standard mechanism for price formation in most
modern financial markets. Agents can place different types of orders, which can
be grouped into two categories: Impatient traders submit market orders, which
are requests to buy or sell a given number of shares immediately at the best
available price. More patient traders submit limit orders, or quotes which also
state a limit price $\pi$, corresponding to the worst allowable price for the
transaction. (Note that the word “quote” can be used either to refer to the
limit price or to the limit order itself.) Limit orders often fail to result in
an immediate transaction, and are stored in a queue called the limit order book.
Buy limit orders are called bids, and sell limit orders are called offers or
asks. At any given time there is a best (lowest) offer to sell with price $a(t)$,
and a best (highest) bid to buy with price $b(t)$. These are also called the
inside quotes or the best prices. The price gap between them is called the
spread $s(t) = a(t)−b(t)$. Prices are not continuous, but rather change in
discrete quanta called ticks, of size $\Delta p$. The number of shares in an
order is called either its size or its volume.
A high density of limit orders per price results in high liquidity for market
orders, i.e., it implies a small movement in the best price when a market order
is placed. There are a variety of different order types defined in real markets,
whose details differ from market to market. For our purposes here, any given
order can always be decomposed into two types: We will call any component of an
order that results in immediate execution an effective market order, and any
component that is not executed immediately, and is stored in the limit order
order book, an effective limit order.
(Orders explanation and liquidity)

Throughout the remainder of the paper we will simply call an effective limit
order a “limit order”, and an effective market market order a “market order”.
When a market order arrives it can cause changes in the best prices. This is
called market impact or price impact. Note that the price changes are always in
the same direction: A buy market order will either leave the best ask the same
or make it bigger, and a sell market order will either leave the best bid the
same or make it smaller. The result is that buy market orders can increase the
midprice $m(t) = (a(t) + b(t))/2$, and sell orders can decrease it.
There is no unique notion of price in a real market. We will let $\pi$ be the
limit price of a limit order, and $m(t) = (a(t) + b(t))/2$ be the midpoint
price or midprice defined by the best quotes. All the results of this paper
concern the midprice, rather than transaction prices, but at longer timescales
this makes very little difference, since the midpoint and transaction prices
rarely differ by more than half the spread. The midpoint price is more
convenient to study because it avoids problems associated with the tendency of
transaction prices to bounce back and forth between the best bid and ask. Price
changes are typically characterized as returns
$r_{\tau}(t) = \log m(t) − \log m(t − \tau)$.
(Orders explanation and midpoint price)

* Market orders. A market order bigger than the opposite best quote widens the
  spread by increasing the best ask if it is a buy order, or decreasing the
  best bid if it is a sell order.
* Limit orders. A limit order that falls inside the spread narrows it by
  increasing the best bid if it is a buy order, or decreasing the best ask if
  it is a sell order.
* Cancellations. A cancellation of the last limit order at the best price
  widens the spread by either increasing the best ask or decreasing the best
  bid.
(Midpoint price change)

It is natural to question whether events on this timescale reflect the
properties of longer timescales, e.g. on the daily timescale of many other
studies. Given that order arrival is highly clustered in time, it is also
natural to ask whether a description in event time also provides an explanation
in real time. [...] it seems clear that an explanation at the level of single
events is sufficient. This is particularly striking, given that on a longer
timescale other processes may become important, such as order splitting.
Figure 11 suggests that for understanding the statistical properties of prices
these can be neglected. The fact that we observe essentially identical
distributions when we aggregate over individual transactions or over fixed time
rules out any explanation of fat tails for price returns based on a subordinated
random process. While fluctuations in the number of events in a given length of
time might be quite important for other phenomena, such as clustered volatility,
they are clearly not important in determining the price return distribution.
(Timescale in price changes)

For the London Stock Exchange, we have shown that large fluctuations in prices
are unrelated to large transactions, or to the placement of large orders.
Instead, large price fluctuations occur when there are gaps in the occupied
price levels in the limit order book. Large changes occur when a market order
removes all the volume at the best price, creating a change in the best price
equal to the size of the gap.
At a higher level, these results demonstrate that large price changes are driven
by fluctuations in liquidity. There are times when the market absorbs changes
in supply and demand smoothly, and other times when a small change in supply or
demand can result in a very large change in the price. This is due to the fact
that supply and demand functions are not smooth, but rather have large,
irregular steps and jumps. The market is granular, due to the presence of only a
finite number of occupied price levels in the book. This is what in physics is
called a finite size effect.
(Price changes due fluctuations in liquidity)

**Introduction to econophysics: Correlations and Complexity in Finance**
_Chapter 5_
A truly gargantuan quantity of financial data is currently being recorded and
stored  in  computers.  Indeed,  nowadays  every  transaction  of  every
financial market in the entire world is recorded somewhere. The nature and
format of these  data  depend  upon  the  financial asset in question and on
the particular institution collecting the data. Data have been recorded

* on a daily basis since the 19th century
* with a sampling rate of 1 min or less since 1984
* transaction-by-transaction ('tick-by-tick') since 1993.
(Data recording)

**Fluctuations and response in financial markets**
There are two data files for each stock: one gives the list of all successive
quotes, i.e. the best buy (bid, b) and sell (ask, a) prices, together with the
available volume, and the time stamp accurate to the second. A quote can change
either as a result of a trade, or because new limit orders appear, or else
because some limit orders are cancelled. The other data file is the list of all
successive trades, with the traded price, traded volume and time stamp, again
accurate to the second. Sometimes, several trades are recorded at the very same
instant but at different prices: this corresponds to a market order of a size
which exceeds the available volume at the bid (or at the ask), and hits limit
orders deeper in the order book. In the following, we have grouped all these
trades together as a single trade. This allows one to create chronological
sequences of trades and quotes, such that between any two trades there is at
least one quote. The last quote before a given trade allows one to define the
sign of each trade: if the traded price is above the last midpoint
m = (a + b)/2, this means that the trade was triggered by a market order (or
marketable limit order) to buy, and we will assign to that trade a variable
$\varepsilon = +1$. If, on the other hand, the traded price is below the last
midpoint $m = (a + b)/2$, then $\varepsilon = −1$. With each trade is also
associated a volume $V$, corresponding to the total number of shares exchanged.
(Data description)

**The subtle nature of financial random walks**
A quantitative trace of human activity is recorded and stored, in some cases
every second. Some of these records span two centuries. These time series,
perhaps surprisingly, turn out to reveal a very rich and non- trivial
statistical structure, that is to some degree universal, across different
assets (stocks, commodities, currencies, rates, etc.), regions (U.S., European,
Asian) and epochs.
(Statistical structure of data)

In spite of its shortcomings, the model of Bachelier gets one important fact
right: price changes are to a first approximation uncorrelated, which makes
the prediction of stock markets difficult. However, the mechanism that
converts a rather predictable human behavior into a sequence of (nearly)
unpredictable price changes, has not been investigated in details until recently.
(Prices changes uncorrelated)

If one denotes $p(t)$ the price of an asset at time $t$, the return $r_{\tau}(t)$,
at time $t$ and scale $\tau$ is simply the relative variation of the price from
$t$ to $t + \tau$, $r_{\tau}(t) = [p(t + \tau) − p(t)] / p(t)$. If $\tau$ is
small enough, one has approximately $r_{\tau} (t) = \ln p(t + \tau) − ln p(t)$.
(Return definition)

The simplest universal feature of financial time series, uncovered by Bachelier
in 1900, is the linear growth of the variance of the return fluctuations with
time scale. More precisely, if $m  \tau$ is the mean return on scale $\tau$,
the following property holds, to a very good approximation:

$$\left\langle \left[r_{\tau}\left(t\right)-m\tau\right]^{2}\right\rangle_{e}
\simeq\sigma^{2}\tau$$

where $\left\langle \ldots\right\rangle _{e}$ denotes the sample average. This
behavior typically holds for ! between a few minutes to a few years, and is
equivalent to the statement that relative price changes are, in a first
approximation, uncorrelated. Very long time scales (beyond a few years) are
difficult to investigate, in particular because the average drift $m$ becomes
itself time dependent, but there are systematic studies suggesting some degree
of mean reversion on these long time scales. The absence of linear correlations
(Bachelier’s first law) in financial time series is often related to the
so-called market efficiency according to which one cannot make anomalous profits
by predicting future price values.
(Bachelier’s first law)

Volatility ($\sigma$) is the simplest quantity that measures the amplitude of
price fluctuations and therefore quantifies the risk associated with some given
asset. A linear growth of the variance of the fluctuations with time is typical
of the Brownian motion for the log-price x.
(Volatility)

The distribution of returns is in fact strongly non-Gaussian and its shape
continuously depends on the return period $\tau$. for $\tau$ large enough
(around few months), one observes quasi-Gaussian distributions while for small
$\tau$ values, the return distributions have fat tails.
(Non-Gaussian shape of returns)

Past price changes and future volatilities are negatively correlated —this is
the so-called leverage effect, which reflects the fact that markets become more
active after a price drop, and tend to calm down when the price rises. This
correlation is most visible on stock indices. This leverage effect leads to an
anomalous negative skew in the distribution of price changes.
(Leverage effect)

Price changes behave very differently from the simple geometric Brownian motion
description. Extreme events are much more probable, and interesting nonlinear
correlations (volatility–volatility and price–volatility) are observed.
These “statistical anomalies” are very important for a reliable estimation of
financial risk and for quantitative option pricing and hedging, for which one
often requires an accurate model that captures the statistics of returns on
different time horizons $\tau$.
(Price changes behavior)

The efficient market hypothesis (EMH) posits that all available information is
included in prices, which emerge at all times from the consensus between fully
rational agents, that would otherwise immediately arbitrage away any deviation
from the fair price. Price changes can then only be the result of unanticipated
news and are by definition totally unpredictable.
(Efficient market hypothesis)

There is a model at the other extreme of the spectrum where prices also follow
a pure random walk, but for a totally different reason. Assume that agents,
instead of being fully rational, have “zero intelligence” and randomly buy or
to sell. Suppose also that their action is interpreted by all the others agents
as potentially containing some information. Then, the mere fact of buying (or
selling) typically leads to a change of the ask $a(t)$ or bid $b(t)$ price and
hence of a change of the midpoint $m(t) = a(t) + b(t) / 2$. In the absence of
reliable information about the true price, the new midpoint is immediately
adopted by all other market participants as the new reference price around
which next orders are launched. In this case, the midpoint will also follow a
random walk (at least for sufficiently large times), even if trades are not
motivated by any rational decision and devoid of meaningful information.
(Zero intelligence model)

Based on a series of detailed empirical results obtained on trade by trade
data, that the random walk nature of prices is in fact highly nontrivial and
results from a fine-tuned competition between two populations of traders,
liquidity providers (or market makers), and liquidity takers. Liquidity
providers act such as to create antipersistence (or mean reversion) in price
changes that would lead to a subdiffusive behavior of the price, whereas
liquidity takers’ action leads to long range persistence and superdiffusive
behavior. Both effects very precisely compensate and lead to an overall
diffusive behavior, at least to a first approximation, such that (statistical)
arbitrage opportunities are absent, as expected. We argue that in a very
precise sense, the market is operating at a critical point;
(Liquidity providers and takers - Random walk)

In order to better understand the impact of trading on price changes, one can
study the following response function $\mathcal{R}(l)$, defined as

$$\mathcal{R}\left(l\right)=\left\langle \left(p_{n+l}-p_{n}\right)\cdot
\varepsilon_{n}\right\rangle$$

where $\varepsilon$ is the sign of the $n$th trade. The quantity $\mathcal{R}(l)
measures how much, on average, the price moves up conditioned to a buy order at
time $0$ (or a sell order moves the price down) a time $l$ later.
Note that $\mathcal{R}(l)} increases by a factor $~2$ between $l=1$ and
$l = l* \approx 1000$, before decreasing back. Including overnights allow one
to probe larger values of $l$ and confirm that $\mathcal{R}(l)$ decreases, and
even becomes negative beyond $l \simeq 5000$. Similar results have been obtained
for many different stocks as well. However, in some cases the maximum is not
observed and rather $\mathcal{R}(l)$ keeps increasing mildly.
(Response function and behavior)

This model of a totally random model of stock market is however qualitatively
incorrect for the following reason. Although, as mentioned above, the
statistics of price changes reveals very little temporal correlations, the
correlation function of the sign + n of the trades, surprisingly, reveals very
slowly decaying correlations as a function of trade time. More precisely, one
can consider the following correlation function:

$$\mathcal{C}_{0}\left(l\right)=\left\langle \varepsilon_{n+l}\varepsilon_{n}
\right\rangle -\left\langle \varepsilon_{n}\right\rangle ^{2}$$

If trades were random, one should observe that $\mathcal{C}_{0}(l)$ decays to
zero beyond a few trades. Surprisingly, this is not what happens, on the
contrary, $\mathcal{C}_{0}(l)$ is strong and decays very slowly toward zero, as
an inverse power-law of $l$.

$$\mathcal{C}_{0}\left(l\right)\simeq\frac{C_{0}}{l^{\gamma}}
,\,\left(l\ge1\right)$$

The value of $\gamma$ seems to be somewhat stock dependent, but is consistently
found to be smaller than unity, leading to a non-integrable correlation
function. This in general leads to superdiffusion, and is the main puzzle to
elucidate: how can one reconcile the strong, slowly decaying correlations in
the sign of the trades with the nearly diffusive nature of the price
fluctuations, and the nearly structureless response function?
(Explanation why zero intelligence model wrong)

One is that of liquidity takers, that trigger trades by putting in market
orders. The motivation for this category of traders might be to take advantage
of some information, and make a profit from correctly anticipating future price
changes. Information can in fact be of very different nature, fundamental
(firm based), macroeconomical, political, statistical (based on regularities
of price patterns), etc. Unfortunately, information is often hard to interpret
correctly—except of course for insiders—and it is probable that many of these
information driven trades are misguided. For example, systematic hedge funds
which take decisions based on statistical pattern recognition have a typical
success rate of only 52%. There is no compelling reason to believe that the
intuition of traders in markets room fares much better than that. Since market
orders are immediately executed, many impatient investors, who want to
liquidate their position, or hedge, etc., might be tempted to place market
orders, even at the expense of the bid-ask spread $s(t) = a(t) − b(t)$.
(liquidity takers)

The other category is that of liquidity providers (or market makers, although
on electronic markets all participants can act as liquidity providers by
putting in limit orders), who offer to buy or to sell but avoid taking any
bare position on the market. Their profit comes from the bid-ask spread $s$:
the sell price is always slightly larger than the buy price, so that each
round turn operation leads to a profit equal to the spread $s$, at least if
the midpoint has not changed in the mean time.
(liquidity providers)

This is where the game becomes interesting. Assume that a liquidity taker
wants to buy, so that an increased number of buy orders arrive on the market.
The liquidity providers are tempted to increase the offer (or ask) price a
because the buyer might be informed and really know that the current price is
too low and that it will most probably increase in the near future. Should
this happen, the liquidity provider, who has to close his position later,
might have to buy back at a much higher price and experience a loss. In order
not to trigger a sudden increase of a that would make their trade costly,
liquidity takers obviously need to put on not too large orders. This is the
rationale for dividing one’s order in small chunks and disperse these as much
as possible over time so as not to reveal their intentions. Doing so liquidity
takers necessarily create some temporal correlations in the sign of the trades.
Since these traders probably have a somewhat broad spectrum of volumes to
trade, and therefore of trading horizons (from a few minutes to several
weeks), this can easily explain the slow, power-law decay of the sign
correlation function $\mathcal{C}_{0}(l)$ reported above.
Now, if the market orders in fact do not contain useful information but are the
result of hedging, noise trading, misguided interpretations, errors, etc., then
the price should not move up on the long run, and should eventually mean revert
to its previous value.
Liquidity providers are obviously the active force behind this mean reversion,
again because closing their position will be costly if the price has moved up
too far from the initial price. However, this mean reversion cannot take place
too quickly, again because a really informed trader would then be able to buy a
large volume at a modest price. Hence, this mean reversion must be slow enough.
To summarize, liquidity takers must dilute their orders and create long range
correlations in the trade signs, whereas liquidity providers must correctly
handle the fact that liquidity takers might either possess useful information
(a rare situation, but that can be very costly since the price can jump as a
result of some significant news), or might not be informed at all and trade
randomly. By controlling the order flow such as to slowly mean reverting the
price, liquidity providers minimize the probability that they either sell too
low, or have to buy back too high. The delicate balance between these
conflicting tendencies conspire to put the market at the border between
persistence or antipersistence, and eliminate arbitrage opportunities.
Therefore, the mere fact of trading such as to minimize impact for liquidity
takers, and to optimize gains for liquidity providers, does lead to a random
walk dynamics of the price, even in the absence of any real information.
(Interaction between providers)

## Trades per minute


## Short long



## Shift
