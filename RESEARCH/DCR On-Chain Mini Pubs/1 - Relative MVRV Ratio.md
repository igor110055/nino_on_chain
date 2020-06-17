# Decred On-Chain Mini Pub 1: Relative MVRV Ratio

## Relevant Reading

- [Decred On-chain: Realised Cap, MVRV Ratio and Gradient Oscillators](https://medium.com/decred/decred-on-chain-realised-cap-mvrv-ratio-and-gradient-oscillators-a36ed2cc8182)

---

## Rationale

For those unfamiliar with the Realized Cap, please read the linked piece above as [Checkmate](https://twitter.com/_Checkmatey_) did a rockstar job in formalizing the power behind the Realized Cap, how Bitcoin's differs from Decred's, and how this manifests itself in price action for each respective coin. For those more comfortable with the abbreviated version, a summary of relevant points surrounding the Realized Cap are included below:

- Realized Cap: Network value calculated by price at which UTXOs were last spent (as opposed to current exchange-traded price)
- Realized Cap: On-chain cost basis of network participants
- MVRV Ratio = Market Cap / Realized Cap
- Bitcoin's Realized Cap is slow-moving and rarely collides with Market Cap
- Whenever Bitcoin's Market Cap < Bitcoin's Realized Cap, it's historically a great buying opportunity
- Decred's Realized Cap is dynamic and moves closely with Market Cap 
- Decred's Realized Cap provides ultimate bull support / bear resistance depending on market conditions
- The difference in Realized Cap behaviors is a result of the fact that HODLers in Bitcoin rarely move their coins, whereas Decred HODLers' coins are constatnly on the move via tickets (i.e. staking)

With the above in mind, the tools presented within aim to establish the following:

- We have a relative market traded price for Decred vs Bitcoin (DCR/BTC), but lack a relative on-chain price - this can provide useful information
- Comparing Bitcoin / Decred MVRV Ratios can shed some light on the *premiums / discounts* these coins can trade against their on-chain price, and how they stack up against one another
- Tracking the trend of the MVRV Ratio can provide users with valuable data the *premium / discount* between market-traded and on-chain price

---

## On-Chain Toolkit

Relevant tools for analysis with their respective calculations are included below:

**On-Chain DCRBTC Price**: Compares the cost basis of each chain, and provides a network vs network "opportunity cost"

[place image here]

**Relative MVRV Ratio**: Compares the premium / discount of Market Price vs Realized Price across coins

[place image here]

**Relative MVRV Price**: The DCRBTC price at which the MVRV Ratios between Bitcoin and Decred are *equal* (DCR MVRV / BTC MVRV = 1)

[place image here]

**Relative Mid-Point**: The mid-point between (1) On-Chain DCRBTC Price and (2) Relative MVRV Price

[place image here]

**Relative MVRV Average**: The 142 day (numer of days it takes for an unvoted DCR ticket to expire) average of the Relative MVRV Ratio

[place image here]

---

## Charts + Analysis

[Decred Image]

- Decred has an elegant Relative Value Channel (the space between the On-Chain DCRBTC Price and the Relative MVRV Price)
- DCRBTC price action contained on the upside by the Relative MVRV Price, showing Bitcoin defending its relative on-chain premium vs Decred
- On-Chain DCRBTC price has provided historical support on many occasions
- Relative Mid-Point has provided DCRBTC support in bull trends and resistance in downtrends, as it represents an on-chain psychological line in the sand
- Relative MVRV Average has historically provided a response bull / bear line, depending which direction DCRBTC price crosses it

[Litecoin Image]

- LTCBTC doesn't respect its relative value channel the same way Decred does
- Every macro LTCBTC top has been nailed by collisions between the LTCBTC market price and the LTCBTC Relative MVRV Price, showing Bitcoin defending its on-chain premium once again

## Final Point

Bitcoin and Decred have high signal, yet different behaving Realized Caps as a function of their respective blockchain mechanics. The goal of this piece was to help highlight some of these differences, and how it plays out on the price charts. 

In particular, Decred's Realized Cap is one of a kind - the amount of valuable data it provides surrounding stakeholders is second to none. I likely have one more piece on this in the pipeline, and look forward to checking back on my findings

Until then - signing out.

[PBN](https://twitter.com/PermabullNino)

## Code

[Relative MVRV](https://github.com/permabullnino/nino_on_chain/blob/master/DCR/DCR_CM_2.11%20-%20RELATIVE%20MVRV.py)