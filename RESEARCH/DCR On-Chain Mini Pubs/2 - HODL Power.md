# Decred On-Chain Mini Pub 2: HODL Power 

## Relevant Reading

- [Decred On-chain: Realised Cap, MVRV Ratio and Gradient Oscillators](https://medium.com/decred/decred-on-chain-realised-cap-mvrv-ratio-and-gradient-oscillators-a36ed2cc8182)
- [Decred On-Chain Mini Pub 1: Relative MVRV Ratio](https://github.com/permabullnino/nino_on_chain/blob/master/RESEARCH/DCR%20On-Chain%20Mini%20Pubs/1%20-%20Relative%20MVRV%20Ratio.md)

---

## Rationale

The two linked pieces above are components of the expanding documentation on Decred's Realized Cap, one of the most powerful on-chain tools within the cryptocurrency space. Relevant information provided within these pieces are summarized below:

- Realized Cap: Network value calculated by price at which UTXOs were last spent (as opposed to current exchange-traded price)
- Realized Cap: On-chain cost basis of network participants
- MVRV Ratio = Market Cap / Realized Cap
- Decred's Realized Cap is dynamic and moves closely with Market Cap 
- Decred's Realized Cap is a function of consistent UTXO flows from (1) ticket holders and (2) standard transactors
- Ticket Holders = HODLers
- Standard Transactors = Marginal buyers and sellers

Within this piece we will build on these principles in the following ways:

- The oscillations in % of DCR supply in the ticket pool can be viewed as a proxy for adoption over long timeframes
- Higher % = More Adoption
- Lower % = Less Adoption
- The higher the adoption, the more implied information about Decred is available, which = less potential upside in speculating on DCR
- The lower the adoption, the less implied information about Decred is available, which = more potential upside in speculating on DCR

- HODLers and standard transactors can be separted within the Realized Cap
- We can use % of DCR supply in tickets to gauge where the MVRV Ratio should top and bottom
- Realized Cap = Current fair value based on *current* adoption levels

---

## On-Chain Toolkit

Relevant tools for analysis with their respective calculations are included below:

**% of Supply in Ticket Pool**: Shows the current conversion rate (i.e. ability to turn standard transactors into HODLers) of outstanding DCR supply

[place image here]

**Full HODL Factor**: Adjustment multiple to calculate for *full* adoption (i.e. 100% of DCR supply in the ticket pool)

[place image here]

**Full HODL Power**: Illustrates the fair value of the network *if* Decred was at full adoption - with 100% of outstanding supply within the ticket pool

[place image here]

**Realized Float Factor**: Adjustment multiple to calculate for supply held by non-adopters

[place image here]

**Realized Float Cap**: Adjusts Realized Cap for the % of DCR supply that is NOT in tickets - showing the fair value of the network from the non-adopters point of view, and where they become heavily interested in accumulating DCR

[place image here]

---

## Charts + Analysis

[Decred Image]

- MVRV Ratio consistently tops at the Full HODL Factor line
- MVRV Ratio consistently bottoms at the Realized Float Factor line - even catching the early 2017 shallow MVRV Ratio bottom
- As adoption ramps up, the gap between the Realized Cap and the Full HODL Power line narrows - showing a decreasing R/R as adoption accelerates
- As adoption ramps up, the gap between the Realized Cap and the Realized Float Cap line widens - also showing a decreasing R/R as adoption accelerates
- These charts illustrate the true dynamic nature of Decred's Realized Cap and MVRV Ratio

- When there's lower amounts of DCR supply in the ticket pool, the Realized Cap behaves more like Bitcoin's Realized Cap - rare visits below it, and Realized Cap provides little resistance on the attempted moves above it (see early 2017)
- When larger amounts of supply sit in tickets, the Realized Cap more accurately reflects current fair value, and as such transforms into a support / resistance line in bull / bear markets
- This change in behavior shows that Decred's Realized Cap is incredibly adaptable and dynamic

## Final Point

After this piece, we now have the following for Decred's Realized Cap:

- Momentum indicator in the Realized Gradient
- A toolset for DCRBTC in the Relative MVRV Ratio 
- An adjusted Realized Cap in the HODL Power toolset

With time I expect our understanding of the Realized Cap to further expand, and with that new tools released into the on-chain wild. 

Until then - signing out.

[PBN](https://twitter.com/PermabullNino)

## Code

[HODL Power](https://github.com/permabullnino/nino_on_chain/blob/master/DCR/DCR_CM_2.4%20-%20HODL%20POWER.py)