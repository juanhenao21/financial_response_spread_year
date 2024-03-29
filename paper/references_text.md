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
spread $s(t) = a(t)-b(t)$. Prices are not continuous, but rather change in
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

**The price impact of order book events**
Traditionally, the above “one sell for one buy” paradox is resolved by arguing
that there are in fact two types of traders coexisting in the ecology of
financial markets:

* “informed” traders who place market orders for immediate execution, at the
  cost of paying half the bid-ask spread, and
* uninformed (or less informed) market makers who provide liquidity by placing
  limit orders on both sides of the order book, hoping to earn part of the
  bid-ask spread.
(Type of traders)

Quantitative studies of the price impact of market orders have by now firmly
established a number of stylized facts:

* Buy (sell) trades on average impact the price up (down). In other words, there
  is a strong correlation between price returns over a given time interval and
  the market order imbalance on the same interval.
* The impact curve as a function of the volume of the trade is strongly concave.
  In other words, large volumes impact the price only marginally more than small
  volumes.
* The sign of market orders is strongly autocorrelated in time. Despite this,
  the dynamics of the midpoint is very close to being purely diffusive.
(Impact of market orders)

**Econophysics: Empirical facts and agent-based models**
“Econophysics” was coined by H. E. Stanley by a merging of the words ‘Economics’
and ‘Physics’, at an international conference on Statistical Physics held in
Kolkata in 1995
(Origin word econophysics)

Economics deals with how societies efficiently use their resources to produce
valuable commodities and distribute them among different people or economic
agents. It is a discipline related to almost everything around us, starting from
the marketplace through the environment to the fate of nations.
(Definition economics)

On a general level, both economics and physics deal with “everything around us”,
despite with different perspectives. On a practical level, the goals of both
disciplines can be either purely theoretical in nature or strongly oriented
toward the improvement of the quality of life. On a more technical side,
analogies often become equivalences.
(Similarities physics and economics)

Branch of physics that combines the principles and procedures of statistics with
the laws of both classical and quantum mechanics, particularly with respect to
the field of thermodynamics. It aims to predict and explain the measurable
properties of macroscopic systems on the basis of the properties and behavior of
the microscopic constituents of those systems.
(Definition statistical mechanics)

The term “complex systems” was coined to cover the great variety of such systems
which include examples from physics, chemistry, biology and also social
sciences. The concepts and methods of statistical physics turned out to be
extremely useful in application to these diverse complex systems including
economic systems. Many complex systems in natural and social environments share
the characteristics of competition among interacting agents for resources and
their adaptation to dynamically changing environment.
(Definition complex systems)

Different kinds of financial time series have been recorded and studied for
decades, but the scale changed twenty years ago. The computerization of stock
exchanges that took place all over the world in the mid 1980’s and early 1990’s
has lead to the explosion of the amount of data recorded. Nowadays, all
transactions on a financial market are recorded tick-by-tick, i.e. every event
on a stock is recorded with a timestamp defined up to the millisecond, leading
to huge amounts of data.
(Data acquisition change)

The concept of “stylized facts” is adopted to describe empirical facts that
arose in statistical studies of financial time series and that seem to be
persistent across various time periods, places, markets, assets, etc.
(Stylized facts definition)

It has been largely observed and it is the first stylized fact, that the
empirical distributions of financial returns and log-returns are fat-tailed.
(Returns fat-tailed)

There is no evidence of correlation between successive returns, which is the
second “stylized-fact”. The autocorrelation function decays very rapidly to
zero, even for a few lags of 1 minute.
(No correlation between successive returns)

Absence of correlation between returns must no be mistaken for a property of
independence and identical distribution: price fluctuations are not identically
distributed and the properties of the distribution change with time. In
particular, absolute returns or squared returns exhibit a long-range slowly
decaying auto correlation function. This phenomena is widely known as
“volatility clustering”, and was formulated by Mandelbrot (1963) as “large
changes tend to be followed by large changes -of either sign - and small changes
tend to be followed by small changes”.
(Volatility clustering)

It has been observed that as one increases the time scale over which the returns
are calculated, the fat-tail property becomes less pronounced, and their
distribution approaches the Gaussian form.
(Returns in large scales)

Calendar time is the time usually used to compute statistical properties of
financial time series. This means that computing these statistics involves
sampling, which might be a delicate thing to do when dealing for example with
several stocks with different liquidity.
(Calendar time)

Let us first introduce event time. Using this count, time is increased by one
unit each time one order is submitted to the observed market. This framework is
natural when dealing with the simulation of financial markets, as it will be
showed in the companion paper. The main outcome of event time is its “smoothing”
of data.
(Event time)

Another count of time might be relevant, and we call it trade time or
transaction time. Using this count, time is increased by one unit each time a
transaction happens. The advantage of this count is that limit orders submitted
far away in the order book, and may thus be of lesser importance with respect to
the price series, do not increase the clock by one unit.
(Transaction time)

Going on with focusing on important events to increase the clock, we can use
tick time. Using this count, time is increased by one unit each time the price
changes. Thus consecutive market orders that progressively “eat” liquidity until
the first best limit is removed in an order book are counted as one unit time.
(Tick time)

We have seen above that when the sampling size increases, the distribution of
the log-returns tends to be more Gaussian. This property is much better seen
using trade time.
(Aggregational normality in trade time)

It is well-known that the series of the signs of the trades on a given stock
(usual convention: +1 for a transaction at the ask price, −1 for a transaction
at the bid price) exhibit large autocorrelation. A very plausible explanation of
this phenomenon relies on the execution strategies of some major brokers on a
given markets. These brokers have large transaction to execute on the account of
some clients. In order to avoid market making move because of an inconsiderably
large order, they tend to split large orders into small ones.
(Autocorrelation of trade signs in tick time)

Activity on financial markets is of course not constant throughout the day. the
observed market activity is larger at the beginning and the end of the day, and
more quiet around midday. Such a U-shaped curve is well-known.
(Intraday seasonality)

Correlation is defined as a relation existing between phenomena or things or
between mathematical or statistical variables which tend to vary, be associated,
or occur together in a way not expected on the basis of chance alone.
(Correlation)

When we talk about correlations in stock prices, what we are really interested
in are relations between variables such as stock prices, order signs,
transaction volumes, etc. and more importantly how these relations affect the
nature of the statistical distributions and laws which govern the price time
series.
(Correlation in stock prices)

If there are $N$ assets with price $P_{i}(t)$ for asset $i$ at time $t$, then
the logarithmic return of stock $i$ is
$r_{i}(t) = \ln P_{i}(t) - \ln P_{i}(t − 1)$, which for a certain consecutive
sequence of trading days forms the return vector $r_{i}$. In order to
characterize the synchronous time evolution of stocks, the equal time
correlation coefficients between stocks $i$ and $j$ is defined as

$$\rho_{ij}=\frac{\left\langle r_{i}r_{j}\right\rangle -\left\langle r_{i}\right
\rangle \left\langle r_{j}\right\rangle }{\sqrt{\left[\left\langle r_{i}^{2}
\right\rangle -\left\langle r_{i}\right\rangle ^{2}\right]\left[\left\langle
r_{j}^{2}\right\rangle -\left\langle r_{j}\right\rangle ^{2}\right]}}$$

where $\left\langle \ldots \right\rangle$ indicates a time average over the
trading days included in the return vectors. These correlation coefficients form
an $N \times N$ matrix with $−1 \le \rho_{ij} \le 1$. If $\rho_{ij} = 1$, the
stock price changes are completely correlated; if  $\rho_{ij} = 0$, the stock
price changes are uncorrelated, and if $\rho_{ij} = -1$, then the stock price
changes are completely anti-correlated.
(Correlation matrix)

Two types of mechanisms generated significant correlation between any two given
stocks. One was some kind of external effect (say, economic or political news)
that influenced both stock prices simultaneously, and the change for both
prices appeared at the same time, such that the maximum of the correlation was
at zero time shift.
The second effect was that, one of the companies had an influence on the other
company indicating that one company’s operation depended on the other, so that
the price change of the influenced stock appeared latter because it required
some time to react on the price change of the first stock displaying a “pulling
effect”. A weak but significant effect with the real data set was found, showing
that in many cases the maximum correlation was at non-zero time shift
indicating directions of influence between the companies, and the
characteristic time was of the order of a few minutes, which was compatible
with efficient market hypothesis. In the pulling effect, they found that in
general, more important companies (which were traded more) pulled the
relatively smaller companies.
(Correlations as the function of the time shift)

**Economics needs a scientific revolution**
Compared to physics, it seems fair to say that the quantitative success of the
economic sciences is disappointing. Rockets fly to the moon, energy is
extracted from minute changes of atomic mass without major havoc, global
positioning satellites help millions of people to find their way home. What is
the flagship achievement of economics, apart from its recurrent inability to
predict and avert crises, including the current worldwide credit crunch?
("Success" of economic sciences)

Classical economics is built on very strong assumptions that quickly become
axioms: the rationality of economic agents, the invisible hand and market
efficiency, etc. An economist once told me, to my bewilderment: These concepts
are so strong that they supersede any empirical observation. As Robert Nelson
argued in his book, Economics as Religion, the marketplace has been deified.
(Problem in classical economics)

In reality, markets are not efficient, humans tend to be over-focused in the
short-term and blind in the long-term, and errors get amplified through social
pressure and herding, ultimately leading to collective irrationality, panic and
crashes. Free markets are wild markets. It is foolish to believe that the
market can impose its own self-discipline.
(Market behavior)

**The economy needs agent-based modelling**
The best models they have are of two types, both with fatal flaws. Type one is
econometric: empirical statistical models that are fit to past data. These
successfully forecast a few quarters ahead as long as things stay more or less
the same, but fail in the face of great change. Type two goes by the name of
‘dynamic stochastic general equilibrium’. These models assume a perfect world,
and by their very nature rule out crises of the type we are experiencing now.
(Classical models to guide the economy)

**Economic crisis**
Economic theory failed to envisage even the possibility of a financial crisis
like the present one. A new foundation is needed that takes into account the
interplay between heterogeneous agents.
(Economic theory failure)

**The Market Impact Puzzle**
The square root model is strikingly simple. Let $G$ denote the percentage cost
of executing abet or meta-order of $Q$ shares of stock with price $P$,
expressed as a fraction of the value of the bet $|PQ|$. Let $\sigma^{2}$ denote
the asset’s returns variance per day, and let $V$ denote the asset’s trading
volume in shares per day. Then the square root model of market impact can be
written

$$G = g \left(\sigma, P, V; Q) \prop \sigma \left( frac{\left|Q\right|}{V}
\right)^{\frac{1}{2}}$$

where $g(\ldots)$ provides a functional form for the model and the notation
"\prop" means “is proportional to”. Trading volume and returns volatility are
easy to observe or estimate. Empirical estimates suggest that the
proportionality constant is close to one, and theory implies that it is exactly
one for each asset; thus, the same model can be applied to all assets
simultaneously. For example, if daily volatility is 2 percent and trading
volume is one million shares per day, then execution of 5 percent of daily
trading volume is expected to move prices or to cost a trader about 45 basis
points $\left(0.02\left(0.05\right)^{\frac{1}{2}\left)$, or about $0.45\%$ of
the dollar value traded.
(Square root model)

The square root model has two distinct disadvantages. First, even though the
square root model seems to be a reasonable approximation to empirical estimates
of transaction costs, there is still no consensus on whether market impact
functions can indeed be described exactly by the square root function.
Second, the square-root model is hard to reconcile with theoretical research.
Following the methodology proposed by Kyle and Obizhaeva (2017a), Pohl et al.
(2017) point out that volume and volatility are sufficient for deriving a
square root model using dimensional analysis and leverage neutrality. By
contrast, most theoretical models of market microstructure lead to a model of
linear market impact, not a square root model.
(Square root model disadvantages)

Models with non-linear market impactare usually analytically intractable and
seem to allow for simple arbitrage strategies. If market impact is sufficiently
concave in the size of bets, then one could hypothetically make profits simply
by making many purchases in small tranches and then selling the entire
accumulated position as one large order. For example, given market impact (1),
one could make profits by executing over time ten buy trades of 100 shares each
and then selling 1000 shares at once.
(Arbitrage in models with non-linear market impact)

**Econophysics**
_Thomas Guhr Book_
We set

$$\varepsilon\left(t\right)=\text{sign}\left(S\left(t\right)-m\left(t-\delta
  \right)\right)$$

where $\delta$ is a positive time increment smaller than all time differences
between consecutives trades. Hence we have

$$\varepsilon\left(t\right)=\left\{ \begin{array}{cc}
+1, & \text{If }S\left(t\right) \text{ is higher than the last } m\left( t \right)\\
-1, & \text{If }S\left(t\right) \text{ is lower than the last } m\left( t \right)
\end{array}\right.$$

What does the trade sign tell us? Suppose a trader urgently wishes to buy
shares, and he is satisfied with the best ask $a(t)$. He sends out a market
order and buys all shares offered at the best ask. Hence, the actual traded
price is equal to the best ask, $S(t) = a(t)$. As $a(t) > m(t)$, we have
$\varepsilon(t) = +1$. After this trade, the second best ask before the trade
becomes the new best bid. If he does not buy all shares, we still have
$S(t) = a(t)$ and thus $\varepsilon(t)=+1$, but the best bid after the trade is
the same as before the trade. Hence, $\varepsilon(t) = +1$ indicates that the
trade was triggered by a market order to buy. The corresponding considerations
apply, if this trader wants to sell shares. The traded price is then the best
bid, $S(t) = b(t)$, and due to $b(t) < m(t)$, we have $\varepsilon(t) = -1$.
Hence, a trade triggered by a market order to sell yields $\varepsilon(t) = -1$.

**The Effects of Beta, Bid-Ask Spread, Residual Risk, and Size on Stock Returns**
The bid-ask spread is related to the number of investors holding the asset,
which reflects the availability of information about it. A larger number of
shareholders brings about a narrower spread. Studies found the transaction
volume (which is more readily available than the number of shareholders) to be
highly correlated with the spread. The bid-ask spread also decreases when more
information is publicly available about the asset, since market makers set the
spread so as to compensate for their losses to better informed investors. Thus,
the incompleteness of public information about an asset, is reflected in its
bid-ask spread. In addition, the spread is negatively correlated with the firm
size. The bid-ask spread is also related to the residual risk, which may serve
as another measure of incomplete information. Risk-averse market makers charge
a higher spread on assets with higher variance to compensate for the risk of
their stock positions.
(Causes of the spread)

**Accounting Informotion and Bid-Ask Spreads**
the spread is comprised of three types of costs facing the dealer:
order-processing costs, inventory holding costs and adverse selection costs.
The order-processing costs are the dealer's costs of arranging trades and
clearing transactions. Tbe inventory holding costs are the dealer's costs of
arrying the necessary inventory of stock to be able to trade on demand, while
the adverse selection component of the spread is closely related to
information flows in capital markets
(Spread types of costs)

Firms with deeper (more liquid) markets tend to have lower spreads.
Specifically, quoted spreads are lower for larger, more actively-traded firms
with multiple dealers. Order processing and inventory costs are lower for more
actively-followed and actively-traded firms.
(Lower spreads)