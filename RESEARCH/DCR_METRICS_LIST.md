# On-Chain Definitions

## Basic Definitions
- **Ticket Purchasers**: Long term holders
- **Standard Transactors**: Marginal Buyers / Sellers
- **Miners**: Largest natural sellers

- **Mining Block Subsidies**: 60% of total subsidy
- **Staking Block Subsidies**: 30% of total subsidy
- **Treasury Block Subsidies**: 10% of total subsidy

- **21 Days (6,144 blocks)**: Average amount of time it takes for Decred block subsidies to decrease (by a factor of 100/101)
- **28 Days**: Average ticket voting time, also average amount of time it takes to fill up the ticket pool 
- **142 Days**: Tickets that have *not* voted expire

- **Target Block Time**: 5 minutes
- **Difficulty Adjustment Period (Staking + Mining)**: 12 hours (144 blocks)
- **Target Ticket Pool Size**: 40,960 tickets
- **Target Ticket Volume**: 720 tickets purchased per adjustment period

## Trading / Price-Focsued Analytical Tools
- **Block Subsidy Lines**: Shows the lifetime USD & BTC value of DCR block subsidies issued, with rewards valued by the USD or BTC price on the day they were issued
- **Ticket Pool Volume Weighted Average Price**: Shows the average price on a USD/BTC basis of DCR that went into tickets, and weighted for the sum of DCR that went into tickets over different periods
- **Ticket Funding Rates**: Shows a responsive means to gauage on-chain HODLer sentiment by tracking the change in ROI offered in tickets over time
- **HODLer Conversion Rates**: Shows how DCR flows dominated by HODLers, marginal buyers, and marginal sellers reflects itself in short / long term price action
- **Strongest Hand Market Cap / Ratio**: Shows how the strong the largest instances of Decred ticket purchases establish the maximum willingness to hold for network participants, and this threshold can provide users with an on-chain implied valuation for the network
- **Mining Pulse**: Shows how trends in block times provide a quality lens for evaluating mild and extreme mining conditions

---

# Unadjusted Metrics

## Unadjusted Staking Metrics
- **Ticket Price**: Minimum threshold to stake
- **Ticket Volume (Denominated in DCR)**: Raw *aggregate* cost to purchase tickets

## Unadjusted Mining Metrics
- **Difficulty**: Minimum threshold to produce a block
- **Hashrate**: Raw *aggregate* cost to produce blocks

## Unadjusted Transactional Metrics
- **DCR Moved On-chain**: Raw sum of DCR moved on-chain

## Block Subsidies
- **DCR Earned**: Raw reward for Mining / Staking

# Adjusted Metrics

## Adjusted Staking Metrics
- **Ticket Volume (Denominated in Tickets Purchased)**: Adjusted ability to purchase tickets

## Adjusted Mining Metrics
- **Block Time**: Adjusted ability to produce blocks

## Adjusted Transactional Metrics
- **DCR Moved On-chain / Supply**: DCR moved on a pound for pound basis 

## Block Subsidies
- **Subsidy / Cost**: Adjusted rate of return for committing stake / work to the network

---

# Research Takeaways

## Differences Between Decred & Bitcoin's On-chain Mechanics
- Decred's block rewards adjust every 21 days, whereas Bitcoin's block rewards adjust every 4 years
- Decred's mining difficulty adjusts every 12 hours, whereas Bitcoin's mining difficulty adjusts every 2 weeks
- Decred's target block times are 5 minutes, and Bitcoin's are 10 minutes
- Decred's miners only receive 60% of block subsidy, whereas Bitcoin's receive 100% of block subsidy
- Decred's initial supply was 1.68 million DCR, Bitcoin's supply started at zero BTC
- Decred's realized cap is dynamic and moves closely with market cap, whereas Bitcoin's lags the market cap

## Trading / Price-Focused
- Very fast / slow block times: miners sweating from either (1) difficulty in earning subisidies due to mining competitiveness or (2) price is too low to justify the mining cost, which *likely* results in more selling pressure
- Large outflows from the ticket pool are indicative of extremes in price action, and likely showing latent DCR selling power coming onto the market
- The realized price for Decred is very dynamic due to the fact that HODLers coins are constantly in motion via tickets. This dynamic nature makes the realized price a quality measure for identifying the stakeholder-wide on-chain cost-basis, and serves as the ultimate price support during bull markets (viceversa for bear markets)
- PoW lifetime subsidies issued line has historically been very strong bear-market-bottoming support
- Decred has shown to have elegant difficulty ribbon contractions / expansions, and these can be used to estimate the cost of mining (*will be published in a future piece*)
- Large ticket buying is in fact significant, but factors such as timing, USD/BTC prices, ticket prices are all relevant in determing the threshold for considering something large / small ticket buying
- Periods where on-chain flows are dominated by ticket-based transacting have been historically bearish, as it indicates an absence of marginal buyers / sellers within the Decred ecosystem
- Capitulation for Decred requires not only (1) mining capitulation, but also (2) staking capitulation, and there's evidence pointing towards there being some overlap between the two groups

## Foundational
- Decred can reasonably be considered one of the top three most secure and censorship-resistant public ledgers in the cryptocurrency market
- Decred has *to date* followed a similar S2F path as Bitcoin
- Decred's ticket pool supply has followed closely to the sum of DCR issued to PoW miners to date
- More DCR are being HODL'd / staked since the release of ASICs

## Governance


## Additional Notes
- Stake Difficulty Adjustment Algorithm altered at **Block 149,248** in order to fix erratic ticket buying that was taking place on the network
- Coinshuffle ++ went live October 2019, which can impact transactional flow analysis
- Decred ASIC mining began early 2018, which pushed up hashrate / difficulty very quickly