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
- Mining Pulse Tools
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

Simply speaking - focusing on hashrate would be like measuring profit / loss in raw dollar terms, whereas any well-informed investor knows that % returns are what really matter. For this reason the author will argue and aim to substantiate such argument with evidence (*based on the adjusted ability to produce blocks i.e. block times*) that miners "buy bottoms and sell tops" as often as the reverse. More on this to follow in the charts / analysis section (**Mining Pulse Tools**).

### Understanding Mild and Extreme Mining Conditions, Why the Difference Matters

Establishing that block times represent the adjusted ability to produce blocks is important for our discussion surrounding mild and extreme mining conditions. With this in mind, there are three general states of mining:

- Periods where it's relatively *difficult* to produce blocks (resulting in slow block times)
- Periods where it's *manageable* to produce blocks (resulting in block times near target)
- Periods where it's relatively *easy* to produce blocks (resulting in fast block times)

Now, these three mining states have differing underlying mechanics, and thus affect miners differently. These differences are shown in the table below:

[plug comparative table]