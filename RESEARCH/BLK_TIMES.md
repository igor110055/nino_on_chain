# Decred On-Chain: Analyzing the Pulse of Miners

## Introduction

Decred has three groups of network stakeholders who leave consistent, on-chain footprints:

- Contractors
- Stakers
- Miners

Each group's on-chain footprint fluctuates / oscillates over time as a function of their share of block rewards earned (10/30/60 respectively) and financial needs (for example - selling DCR to pay bills). Crypto networks early in their lifecycles tend to have strong ties between (1) network value and (2) on-chain activity, as stakeholders are early adopters who are more comfortable transacting on-chain. Thus, their footprints tend to have higher signal when compared to larger crypto networks which have larger off-chain signatures. 

The author's previous explorations into Decred's on-chain data have had a stronger focus on staking data, covering a healthy portion of the consistent, on-chain transactors. However - this has admittedly left a gap in the author's understanding of the mining and contracting groups. This piece is a first attempt at scratching the mining itch, and will be explored with the following plan of attack:

- Why Look at Block Times?
- Mining Musings
- Decred Mining
- Mining Pulse
- Bitcoin Capitulations
- Conclusion

---

## Why Look at Block Times?

The two primary reasons block times are a worthwhile point of focus surrounding mining are:

- Block times are natural oscillators
- Block times are the "final product" in mining data

Let's briefly expand on these two points below...

### Block Times are Natural Oscillators

When performing on-chain analysis, it can be *incredibly* helpful to focus on patterns that repeat themselves time and time again. This logic is leveraged in most popularly known on-chain indicators, such as the NVT Ratio, the MVRV Ratio, and on a more mining specific note - the Puell Multiple. Top and bottom patterns in the same range provide high signal, simple ways for analysis and decision-making when combined with the proper historical context:

[plug chart]

Block times fall right into this camp of repeating patterns, as they're designed to oscillate within a certain range of the *target block time*. A look at the block times chart on Decred's block explorer shows this quite clearly:

[plug chart]

Another item worth point out about fractals (repeating patterns over time) is that when something in large part moves predictably within a range, *moves outside of that range* are likely significant. Another look at the block times chart above will show that there are spikes upwards and downwards outside the predictable range - revealing points of possible volatility within the Decred mining ecosystem.

### Block Times are the "Final Product" in Mining Data

There are four on-chain footprints that can be used to study mining behavior:

- Block rewards
- Difficulty
- Hashrate
- Block time

Each of the four footprints represent the following, respectively:

- Incentive
- Established standard / goal to receive reward
- Work put forward to accomplish goal
- Result, which is a function of previous three points

Miners are in many cases ideological, but above all else they're profit motivated actors. Their number one goal is to maximize their bottom line i.e. *earn the maximum amount of block rewards while minimizing their costs to do so.* The way they earn these rewards is by discovering a hash below the network's established difficulty target, which gives them the right to create a block. This newly created block includes a *coinbase transaction* which mints new coins to be sent to the address of the discovering miner's choice.

Block times are a high signal tool because it gives on-chain onlookers a glance at the current state of the balancing act playing out between profit motivated actors who are inputting work against a standard demanding certain costs to earn a favorable result. Instead of looking at each piece of the puzzle individually, we're honing in on the result to truly understand what the big picture is in whole. The next section will flesh out this thought process more thoroughly.

[plug chart that shows block times being a function of the three other parts]

---

## Mining Musings

There are a few topics addressed in this section:

- The idea that price leads, miners follow
- Understanding mild and extreme mining conditions, why the difference matters

### Price Leads, Miners Follow

"Price leads, Miners Follow" in normal-speak translates to "Miners are top buyers and bottom sellers". If we were to take the hashrate chart versus price, that would seem to be the easy conclusion - with run ups in hashrate until price corrects downwards, where hashrate corrects downwards in response. However, an argument can be made that this conclusion is misleading. Why? For the following reasons:

- Hashrate shows the *unadjusted* ability to produce blocks
- Block time shows the *adjusted* ability to produce blocks

Simply speaking - focusing on hashrate would be like measuring profit / loss in raw dollar terms, whereas any well-informed investor knows that % returns are what really matter. For this reason the author will argue and aim to substantiate such argument with evidence (*based on the adjusted ability to produce blocks i.e. block times*) that miners "buy bottoms and sell tops" as often as the reverse. More on this to follow in the charts / analysis section.

### Understanding Mild and Extreme Mining Conditions, Why the Difference Matters

Establishing that block times represent the adjusted ability to produce blocks is important for our discussion surrounding mild and extreme mining conditions. With this in mind, there are three general states of mining:

- Periods where it's relatively *difficult* to produce blocks (resulting in slow block times)
- Periods where it's *manageable* to produce blocks (resulting in block times near target)
- Periods where it's relatively *easy* to produce blocks (resulting in fast block times)

Now, these three mining states have differing underlying mechanics, and thus affect miners / the market at large differently. These differences are shown in the table below:

[plug comparative table]

A few items are worth fleshing out a bit more here:

- At the extremes (slow and fast block times), the end result is the same: miners get squeezed, which results in more coins being sold to maintain operations
- In the crypto space, people tend to obssess a bit over the slower block time squeezes, but *generally* overlook the other side of the coin. The author admittedly hadn't thought much about the idea of miners weighing on price on the upside until Leo Zhang had written about it here(include link)
- Ideal mining conditions are the sweet spot in between, where mining cost and mining reward are at a healthy equilibrium
- Ideal mining conditions = Ideal price conditions

The discussion points in this section will be key in analyzing the Mining Pulse chart later on.

---

## Decred Mining

The highlights of Decred mining, and that are relevant to block time analysis are as follows:

- Miners earn 60% of block rewards issued
- Difficulty adjusts every 144 blocks (~12 hours on average)
- Block rewards adjust downwards by a factor of 100/101 every 6,144 blocks (~21 days on average)
- ASICs were introduced mid-2018
- Target block times are 300 seconds (5 minutes)

For analytical purposes, the importance of these points respectively, are:

- Miners are the largest natural sellers within the network
- Difficulty adjusts very often, thus making block time data very responsive and reliable for tracking trends
- Block reward adjustment period impacts miners' bottom line, and this period will be used for analysis
- Expect temporary impact on block time data around mid-2018
- Target block time = baseline for analysis

---

## Mining Pulse

The calculation for Mining Pulse is included below:

[plug image that shows calc]

Mining Pulse calculates the *three mining cycle average block time versus the target block time*. Differences show a block time surplus / deficit, which means the following:

- Surplus: Three week average > target block time = slow block times
- Deficit: Three week average < target block time = fast block times

Furthermore - it's important to note that block time will be herein measured in seconds, not minutes. Thus, any surplus / deficit tells users how many seconds the average is above / below the target block time for the Decred network. Without further delay, here is the first look at the Mining Pulse chart:

[plug chart using lines]