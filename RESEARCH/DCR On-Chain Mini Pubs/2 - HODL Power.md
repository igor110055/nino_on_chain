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

![Supply in Ticket Pool](https://github.com/permabullnino/nino_on_chain/blob/master/RESEARCH/DCR%20On-Chain%20Mini%20Pub%20Images/2%20-%20HODL%20Power%20Images/Supply%20in%20Ticket%20Pool.PNG)

**Full HODL Factor**: Adjustment multiple to calculate for *full* adoption (i.e. 100% of DCR supply in the ticket pool)

![Full HODL Factor](https://github.com/permabullnino/nino_on_chain/blob/master/RESEARCH/DCR%20On-Chain%20Mini%20Pub%20Images/2%20-%20HODL%20Power%20Images/Full%20HODL%20Factor.PNG)

**Full HODL Power**: Illustrates the fair value of the network *if* Decred was at full adoption - with 100% of outstanding supply within the ticket pool

![Full HODL Power](https://github.com/permabullnino/nino_on_chain/blob/master/RESEARCH/DCR%20On-Chain%20Mini%20Pub%20Images/2%20-%20HODL%20Power%20Images/Full%20HODL%20Power.PNG)

**Realized Float Factor**: Adjustment multiple to calculate for supply held by non-adopters

![Realized Float Factor](https://github.com/permabullnino/nino_on_chain/blob/master/RESEARCH/DCR%20On-Chain%20Mini%20Pub%20Images/2%20-%20HODL%20Power%20Images/Realized%20Float%20Factor.PNG)

**Realized Float Cap**: Adjusts Realized Cap for the % of DCR supply that is NOT in tickets - showing the fair value of the network from the non-adopters point of view, and where they become heavily interested in accumulating DCR

![Realized Float Cap](https://github.com/permabullnino/nino_on_chain/blob/master/RESEARCH/DCR%20On-Chain%20Mini%20Pub%20Images/2%20-%20HODL%20Power%20Images/Realized%20Float%20Cap.PNG)

---

## Charts + Analysis

![Price Chart](https://github.com/permabullnino/nino_on_chain/blob/master/RESEARCH/DCR%20On-Chain%20Mini%20Pub%20Images/2%20-%20HODL%20Power%20Images/Price%20Chart.PNG)

- Bull trend support is the Realized Cap, with resistance at Full HODL Power
- Bear trend resistance is the Realized Cap, with support at the Realized Float Cap

- MVRV Ratio consistently tops at the Full HODL Factor line
- MVRV Ratio consistently bottoms at the Realized Float Factor line - even catching the early 2017 shallow MVRV Ratio bottom
- As adoption ramps up, the gap between the Realized Cap and the Full HODL Power line narrows - showing a decreasing R/R as adoption accelerates
- As adoption ramps up, the gap between the Realized Cap and the Realized Float Cap line widens - also showing a decreasing R/R as adoption accelerates
- Over time, the Realized Cap and the Full HODL Power lines should converge if more and more DCR supply ends up in tickets

- When there's lower amounts of DCR supply in the ticket pool, the Realized Cap behaves more like Bitcoin's Realized Cap - rare visits below it, and Realized Cap provides little resistance on the attempted moves above it (see early 2017)
- When larger amounts of supply sit in tickets, the Realized Cap more accurately reflects current fair value, and as such transforms into a support / resistance line in bull / bear markets
- This change in behavior shows that Decred's Realized Cap is incredibly adaptable and dynamic
- At full adoption (100% of DCR supply in tickets), DCR are constantly on the move, which is very deliberate HODLing. As such, this should very accurately reflect fair value of the network because the deliberate nature of DCR HODLing implies users understand the opportunity costs of keeping DCR versus moving funds elsewhere

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