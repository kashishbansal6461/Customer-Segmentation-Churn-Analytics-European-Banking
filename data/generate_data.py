import numpy as np
import pandas as pd
from pathlib import Path


rng = np.random.default_rng(42)


def build_dataset(n_rows: int = 2500) -> pd.DataFrame:
    geography_values = ["France", "Germany", "Spain"]
    geography_probs = [0.45, 0.27, 0.28]
    gender_values = ["Female", "Male"]
    gender_probs = [0.52, 0.48]

    data = {
        "CustomerId": np.arange(1, n_rows + 1),
        "Surname": [f"Customer{idx}" for idx in range(1, n_rows + 1)],
        "CreditScore": rng.integers(300, 850, size=n_rows),
        "Geography": rng.choice(geography_values, size=n_rows, p=geography_probs),
        "Gender": rng.choice(gender_values, size=n_rows, p=gender_probs),
        "Age": rng.integers(18, 72, size=n_rows),
        "Tenure": rng.integers(0, 11, size=n_rows),
        "Balance": np.round(rng.uniform(0, 250000, size=n_rows), 2),
        "NumOfProducts": rng.choice([1, 2, 3, 4], size=n_rows, p=[0.40, 0.38, 0.18, 0.04]),
        "HasCrCard": rng.integers(0, 2, size=n_rows),
        "IsActiveMember": rng.integers(0, 2, size=n_rows),
        "EstimatedSalary": np.round(rng.uniform(15000, 200000, size=n_rows), 2),
    }

    df = pd.DataFrame(data)

    def age_group(age: int) -> str:
        if age < 30:
            return "<30"
        elif age < 46:
            return "30-45"
        elif age < 61:
            return "46-60"
        return "60+"

    def credit_band(score: int) -> str:
        if score < 500:
            return "Low"
        elif score < 700:
            return "Medium"
        return "High"

    def tenure_group(tenure: int) -> str:
        if tenure < 3:
            return "New"
        elif tenure < 7:
            return "Mid-term"
        return "Long-term"

    def balance_segment(balance: float) -> str:
        if balance <= 0:
            return "Zero-balance"
        elif balance < 50000:
            return "Low-balance"
        return "High-balance"

    df["AgeGroup"] = df["Age"].map(age_group)
    df["CreditScoreBand"] = df["CreditScore"].map(credit_band)
    df["TenureGroup"] = df["Tenure"].map(tenure_group)
    df["BalanceSegment"] = df["Balance"].map(balance_segment)

    risk_components = []
    for _, row in df.iterrows():
        risk = -1.8

        if row["Geography"] == "Spain":
            risk += 0.50
        elif row["Geography"] == "Germany":
            risk += 0.18

        if row["Age"] >= 50:
            risk += 0.30
        if row["Age"] >= 60:
            risk += 0.30

        if row["CreditScore"] < 500:
            risk += 0.35
        elif row["CreditScore"] > 700:
            risk -= 0.15

        if row["Tenure"] <= 2:
            risk += 0.40
        elif row["Tenure"] >= 8:
            risk -= 0.20

        if row["Balance"] <= 20000:
            risk += 0.25
        elif row["Balance"] >= 120000:
            risk -= 0.10

        if row["NumOfProducts"] == 1:
            risk += 0.25
        elif row["NumOfProducts"] >= 3:
            risk -= 0.10

        if row["HasCrCard"] == 0:
            risk += 0.12
        if row["IsActiveMember"] == 0:
            risk += 0.75

        if row["Gender"] == "Male":
            risk += 0.05

        if row["EstimatedSalary"] > 150000:
            risk -= 0.08

        risk_components.append(risk)

    df["RiskScore"] = risk_components
    df["ExitedProbability"] = 1 / (1 + np.exp(-df["RiskScore"]))
    df["Exited"] = (rng.random(len(df)) < df["ExitedProbability"]).astype(int)

    df = df.drop(columns=["RiskScore", "ExitedProbability"])
    df = df[[
        "CustomerId",
        "Surname",
        "CreditScore",
        "Geography",
        "Gender",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary",
        "Exited",
        "AgeGroup",
        "CreditScoreBand",
        "TenureGroup",
        "BalanceSegment",
    ]]

    return df


if __name__ == "__main__":
    output_dir = Path(__file__).resolve().parent
    output_path = output_dir / "data" / "customer_churn_europe.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = build_dataset()
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
    print(f"Shape: {df.shape}")
    print(f"Churn rate: {df['Exited'].mean():.2%}")
