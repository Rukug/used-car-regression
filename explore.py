import pandas as pd

sales = pd.read_csv("used_car_sales.csv")
auctions = pd.read_csv("auction_lots.csv")

print("SALES DATA — rows and columns")
print(sales.shape)

print("\nFirst five sales")
print(sales.head().to_string(index=False))

print("\nMissing values in sales data")
print(sales.isna().sum())

print("\nAccident categories")
print(sales["Accident"].value_counts(dropna=False))

print("\nAUCTION DATA — rows and columns")
print(auctions.shape)

print("\nAuction column names")
print(auctions.columns.tolist())

print("\nMissing values in auction data")
print(auctions.isna().sum())