# Used Car Regression Assignment

Rukmani Ghorasainee

Predict used-car resale prices and compare regression-based auction
purchases with a baseline that predicts the training-set average price.

## Data

- used_car_sales.csv — 240 cars sold in the previous year, supplied
  with the course assignment.
- auction_lots.csv — 40 auction cars, supplied with the course assignment.

The sales data is split into 168 training cars and 72 test cars using
random_state=42. Model fitting and feature selection use the training
data. The auction cars are used to evaluate buying decisions.

## Model

The selected model, v1, is a multiple linear regression using mileage,
age, horsepower, and accident history. Number of previous owners was
removed after comparing training results.

Buy when predicted resale price exceeds auction price plus $1,500.

## Run

From the repository folder on macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python explore.py
python fit.py
```

## Outputs

- test_predictions.csv — actual and predicted prices for the test cars.
- test_price_predictions.png — baseline and v1 predictions against actual prices.
- auction_decisions.csv — predictions, buying decisions, and profit if bought.
- auction_summary.csv — purchase counts, losing purchases, and total profits.

To save all printed results:

```bash
python fit.py > analysis_results.txt
```