# Decred On-Chain Mini Pub 1: Relative MVRV Ratio

## Relevant Reading

- [Introducing the Difficulty Ribbon, signaling the best times to buy Bitcoin](https://woobull.com/introducing-the-difficulty-ribbon-the-best-times-to-buy-bitcoin/)

---
## Rationale

[include image from Willy's article]

- The Difficulty Ribbon was an on-chain tool created by [Willy Woo](https://twitter.com/woonomic) in order to track distress among Bitcoin miners
- The Difficulty Ribbon consists of the (1) the network difficulty and (2) an assortment of moving averages of difficulty, with the 200 day moving average being the slowest-moving
- Contractions in the Difficulty Ribbon have been historical signals for mining capitulation i.e. **actual price is very close to the cost of mining**

This tool is a simple, high-signal way for the average person to gauge the current state of mining within a cryptocurrency network. Furthermore, it doesn't rely on electricity cost assumptions or other complex means to track mining costs. If we can glean more information from this strong base, we can gain a better understanding of the economics behind a large stakeholder group within the Decred ecosystem.

With the above in mind, we're going to expand on the Difficulty Ribbons in the following ways:

- Show that Difficulty Ribbons can provide a reliable estimate for the current cost to mine 
- The cost to mine can also be estimated on a DCRBTC basis
- Illustrate the impact of ASIC introduction on the cost to mine, and how this impacts price action
- Why "mining capitulation" is a quality marker for bear market bottoms

---

## On-Chain Toolkit

Before showing the tools with their respective calculations, please note that "mining capitulation" will be considered to be taking place when actual mining difficulty collides with the 200 day average of mining difficulty. When this occurs, there's sufficient evidence to suggest that growth in mining is reaching a stand-still due to a lack of profitability.

Relevant tools for analysis with their respective calculations are included below:

**Difficulty Multiple**: The ratio between current mining difficulty and the 200 day mining difficulty average. This ratio represents the current market traded price in ratio form.

[plug image here]

**USD Difficulty Price**: Multiply the inverse Difficulty Multiple by actual price to determine the cost to mine (when ratio = 1)

[plug image here]

**BTC Difficulty Price**: Divide the USD Difficulty Price by the actual Bitcoin price to determine how many BTC miners could receive if they sold their rewards into BTC on the day they were mined

[plug image here]

---
## Why Do These Tools Matter?

Miners are the largest natural sellers of any PoW cryptocurrency. Conversely (and generally speaking), they're also the cheapest accumulators of coins - by acquiring coins below the current market traded price.

An increase in mining profitability (the ability to acquire coins below market traded price) is sharp on both sides: 

(1) Allows a larger cross section of miners to hold DCR without selling, however
(2) It keeps weaker miners in the game, who begin to weigh on price as price starts moving downwards

Actual price increasing can improve profitability, however this piece is focused on the cost side of the equation. Now, there are two ways the cost to mine can decrease:

(1) Difficulty adjusting downwards, lowering the minimum threshold to generate a hash below target or
(2) Hash becomes cheaper to acquire, due to improvements in hardware which allow more hash to be generated per unit of electricity committed

The introduction of ASICs for Decred took place in early 2018, and with this came a large decrease in the cost to acquire hash. Depending on timing, this can weigh very heavily on price for a cryptocurrency. In the case of Decred, it got the worst of both worlds: the evaporation of the marginal buyer (which happens for any coin in a bear market) and a decrease in the cost to mine, allowing miners to keep selling their DCR *profitably* at much lower prices. 

This inevitably kept pushing prices until selling no longer becomes profitable for marginal sellers and most importantly natural sellers (miners), which occurs at the cost to mine DCR. The charts and analysis below will hopefully help everyone better understand the mechanics that have been at play since ASIC introduction, and arms everyone better for future market cycles.

---
## Charts + Analysis


---
## Final Point



---
## Code