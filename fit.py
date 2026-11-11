import pandas as pd
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split

sales = pd.read_csv("used_car_sales.csv")

# Keep the same random split each time we run the script.
train, test = train_test_split(
    sales,
    test_size=0.30,
    random_state=42,
)

print(f"Training cars: {len(train)}")
print(f"Test cars: {len(test)}")

# The baseline predicts the training average for every car.
baseline_price = train["Sale_Price"].mean()
print(f"\nBaseline predicted sale price: ${baseline_price:,.2f}")

# Use all five features to fit the initial model.
full_model = smf.ols(
    'Sale_Price ~ Mileage_K + Age_Years + Horsepower '
    '+ C(Accident, Treatment(reference="no")) + Num_Owners',
    data=train,
).fit()

print("\nINITIAL MODEL — TRAINING RESULTS")
print(full_model.summary())

reduced_model = smf.ols(
    'Sale_Price ~ Mileage_K + Age_Years + Horsepower '
    '+ C(Accident, Treatment(reference="no"))',
    data=train,
).fit()

print("\nMODEL WITHOUT NUMBER OF OWNERS — TRAINING RESULTS")
print(reduced_model.summary())

comparison = pd.DataFrame({
    "Model": ["All five features", "Without Num_Owners"],
    "Training R-squared": [
        full_model.rsquared,
        reduced_model.rsquared,
    ],
    "Training adjusted R-squared": [
        full_model.rsquared_adj,
        reduced_model.rsquared_adj,
    ],
})

print("\nTRAINING MODEL COMPARISON")
print(comparison.to_string(index=False, float_format="%.4f"))

from sklearn.metrics import r2_score, mean_squared_error

# Choose the model using the training results.
v1 = reduced_model

actual_prices = test["Sale_Price"]

baseline_predictions = pd.Series(
    baseline_price,
    index=test.index,
)
v1_predictions = v1.predict(test)

test_comparison = pd.DataFrame({
    "Model": ["Baseline", "v1"],
    "Test R-squared": [
        r2_score(actual_prices, baseline_predictions),
        r2_score(actual_prices, v1_predictions),
    ],
    "Test RMSE ($)": [
        mean_squared_error(
            actual_prices, baseline_predictions
        ) ** 0.5,
        mean_squared_error(
            actual_prices, v1_predictions
        ) ** 0.5,
    ],
})

print("\nTEST RESULTS — 72 CARS")
print(test_comparison.to_string(
    index=False,
    float_format="%.4f",
))

# Save the actual and predicted prices for checking and charting.
test_results = test[[
    "Sale_Price", "Mileage_K", "Age_Years",
    "Horsepower", "Accident", "Num_Owners",
]].copy()

test_results["Baseline_Prediction"] = baseline_predictions
test_results["V1_Prediction"] = v1_predictions
test_results.to_csv("test_predictions.csv", index=False)

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

fig, ax = plt.subplots(figsize=(7, 6))

ax.scatter(
    actual_prices,
    baseline_predictions,
    label="Baseline",
    color="#999999",
    marker="x",
    alpha=0.7,
)
ax.scatter(
    actual_prices,
    v1_predictions,
    label="v1 regression",
    color="#2563EB",
    alpha=0.8,
    edgecolors="white",
    linewidths=0.5,
)

# Use the same range on both axes.
all_prices = pd.concat([
    actual_prices,
    baseline_predictions,
    v1_predictions,
])
lower = all_prices.min() - 1500
upper = all_prices.max() + 1500

ax.plot(
    [lower, upper],
    [lower, upper],
    color="black",
    linewidth=1,
    label="Perfect prediction",
)

ax.set_xlim(lower, upper)
ax.set_ylim(lower, upper)
ax.set_aspect("equal", adjustable="box")

ax.set_title(
    "Resale price predictions for 72 test cars",
    fontweight="bold",
    pad=12,
)
ax.set_xlabel("Actual sale price")
ax.set_ylabel("Predicted sale price")
ax.xaxis.set_major_formatter(StrMethodFormatter("${x:,.0f}"))
ax.yaxis.set_major_formatter(StrMethodFormatter("${x:,.0f}"))

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="x", labelrotation=45)
ax.legend(frameon=False)

fig.tight_layout()
fig.savefig("test_price_predictions.png", dpi=300)
plt.close(fig)

print("\nSaved chart: test_price_predictions.png")

PREPARATION_COST = 1500

def dealer_decision(car, auction_price):
    """Return buy or pass using the fitted v1 model."""
    features = pd.DataFrame([{
        "Mileage_K": car["Mileage_K"],
        "Age_Years": car["Age_Years"],
        "Horsepower": car["Horsepower"],
        "Accident": car["Accident"],
    }])

    predicted_price = float(v1.predict(features).iloc[0])

    if auction_price + PREPARATION_COST < predicted_price:
        return "buy"
    return "pass"


def baseline_decision(auction_price):
    """Return buy or pass using the training average."""
    if auction_price + PREPARATION_COST < baseline_price:
        return "buy"
    return "pass"


auctions = pd.read_csv("auction_lots.csv")

auctions["Baseline_Prediction"] = baseline_price
auctions["V1_Prediction"] = v1.predict(auctions)

auctions["Baseline_Decision"] = [
    baseline_decision(price)
    for price in auctions["Auction_Price"]
]

auctions["V1_Decision"] = [
    dealer_decision(car, car["Auction_Price"])
    for _, car in auctions.iterrows()
]

# Actual profit if the dealer bought this car.
auctions["Profit_If_Bought"] = (
    auctions["Later_Sale_Price"]
    - auctions["Auction_Price"]
    - PREPARATION_COST
)

summary_rows = []

for name, decision_column in [
    ("Baseline", "Baseline_Decision"),
    ("v1", "V1_Decision"),
]:
    bought = auctions[decision_column] == "buy"
    bought_profits = auctions.loc[bought, "Profit_If_Bought"]

    summary_rows.append({
        "Rule": name,
        "Cars bought": int(bought.sum()),
        "Money-losing cars bought": int((bought_profits < 0).sum()),
        "Total profit ($)": bought_profits.sum(),
    })

auction_summary = pd.DataFrame(summary_rows)

print("\nAUCTION RESULTS — 40 LOTS")
print(auction_summary.to_string(
    index=False,
    float_format="%.2f",
))

extra_profit = (
    auction_summary.loc[1, "Total profit ($)"]
    - auction_summary.loc[0, "Total profit ($)"]
)
print(f"\nv1 profit minus baseline profit: ${extra_profit:,.2f}")

auctions.to_csv("auction_decisions.csv", index=False)
auction_summary.to_csv("auction_summary.csv", index=False)

print("\nSaved auction_decisions.csv and auction_summary.csv")