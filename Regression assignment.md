# Used car prices: should the dealer buy this car?

## The question

A used car dealer buys cars at wholesale auction and resells them on its lot. Its buyer has a few minutes per car and bids on gut feel. **Can the dealer predict what a car will sell for on the lot well enough to decide which cars to buy at auction, and how much is that worth compared to how it buys today?**

## The model

**Linear regression.** The outcome is a continuous dollar amount: a car's sale price. Use any software that fits a multiple linear regression and reports coefficients, p-values, and R².

## Context

The dealer's decision rule: **buy a car at auction if the auction price plus the cost to get it on the lot is below the price it is predicted to sell for; otherwise pass.** Getting a car ready to sell (inspection, reconditioning, detailing, and lot time) costs about **$1,500 per car**.

Without a model, the dealer's best single guess for any car is the average sale price. That is the **baseline**: it predicts the same price for every car, so its rule is to buy any car whose auction price plus $1,500 is below that average.

## The data

**`used_car_sales.csv`**: 240 cars the dealer sold in the last year, one row per car. Use this to fit the model.

| Column | Meaning |
|---|---|
| `Sale_Price` | what the car sold for on the lot, in dollars. |
| `Mileage_K` | odometer reading in thousands of miles (70 = 70,000 miles) |
| `Age_Years` | age of the car at sale, in years |
| `Horsepower` | engine horsepower |
| `Accident` | "yes" if the vehicle history report shows an accident, "no" if not |
| `Num_Owners` | number of previous owners |

**`auction_lots.csv`**: 40 cars the buyer looked at in one recent auction. It has the same five feature columns, plus `Lot` (lot number), `Auction_Price` (the winning bid), and `Later_Sale_Price` (what each car later sold for at retail, from a market data service). Do not use these 40 cars to fit the model. Use them to test the decision rule: for every car a rule says to buy, the dealer's profit is `Later_Sale_Price − Auction_Price − 1,500`.


## The task

1. **Split the data.** Randomly set aside 30% of the 240 cars as a test set. Fit everything on the remaining 70% (the training set). The test cars are only for evaluating fit.
2. **Fit the model.** Fit a linear regression of sale price on the features using the training cars (v1). Read the output: what each coefficient means for the dealer, which features matter (p-values), and the adjusted R². If a feature does not earn its place, you may fit a second version without it and compare adjusted R². Say which version you would hand over and why; call that one v1 on your slides.
3. **Evaluate fit on the test cars.** Predict the sale price of each test car with the baseline (the training-set average) and with v1. For each, compute R² and the typical error in dollars (root mean squared error) on the test cars. The comparison is **baseline vs v1 on cars the model never saw**.
4. **Make the decision.** Write the dealer's rule as a function that takes one car's features and its auction price and returns buy or pass. Apply it, and the baseline rule, to the 40 auction lots. For each rule, report how many cars it buys, how many of those lose money, and the total profit.
5. **Present it.** Make two slides for the dealer's owner, not for a statistics audience.

## Deliverables
Note: you may use AI throughout and it is expected that you do so for coding, however, do not use AI to generate your slides. The value of this assignment is interpreting the technical output and synthesizing for business decision-makers. It is better to have succinct black text on white background that you wrote yourself rather than volumes of AI-generated nonsense for your "boss" to have to parse. (Asking AI to write python code to create graphs/charts for your slides is expected, copying-pasting an a graph made by ChatGPT/Claude/Gemini is not.)

One submission: **one PDF.**

1. **Title slide:** your name and the link to your GitHub repo containing the code and analysis for the project. The code reproduces every number on your slides.
2. **Two slides covering:**
   - Data: source, rows, period, the 70/30 split. 
   - Model specification: outcome, features, model family, any feature you dropped, and the adjusted R² of the training fit. Evaluate fit on the test cars
   - Fit baseline vs v1 comparisons: R² and typical error in dollars, with a chart (predicted vs actual sale price for the test cars works well).
   - Business decision and value quantification:
   -- Headline in one sentence- what the model changes for the dealer and what it is worth
   -- Compare value quantification of baseline vs v1: on the 40 auction compare cars bought, money-losing cars bought, and total profit
