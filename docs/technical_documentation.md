# Technical Documentation

## 1. Project Overview

This project analyzes churn behavior in a European retail banking customer base. The objective is to identify churn-prone customer segments using demographic, transactional, and behavioral variables. The analysis supports retention strategy design and hypothesis testing for customer relationship management.

## 2. Business Context

Banks collect massive amounts of customer data but often struggle to convert it into actionable retention insight. A single overall churn rate is insufficient because churn risk varies by customer segment. The project therefore segments customers by geography, age, balance, tenure, and engagement.

## 3. Dataset Description

The dataset contains synthetic but realistic customer attributes for a European banking portfolio. Each row represents one customer, and the target variable is `Exited`, which is binary:

- 1 = churned
- 0 = retained

Core fields include:

- CustomerId
- Geography
- Gender
- Age
- Tenure
- Balance
- CreditScore
- NumOfProducts
- HasCrCard
- IsActiveMember
- EstimatedSalary
- Exited

## 4. Data Engineering Process

The workflow includes:

1. Loading the CSV file
2. Validating the binary churn target
3. Creating audience segments
4. Calculating churn for each segment
5. Comparing profile differences between churned and retained customers

## 5. Segment Logic

Derived features are created using business-friendly thresholds:

- Age groups: `<30`, `30-45`, `46-60`, `60+`
- Credit score: `Low`, `Medium`, `High`
- Tenure: `New`, `Mid-term`, `Long-term`
- Balance: `Zero-balance`, `Low-balance`, `High-balance`

These groupings allow decision-makers to understand which customer cohorts deserve retention intervention.

## 6. KPI Definitions

The dashboard calculates the following KPIs:

- Overall Churn Rate: Percentage of all customers who exited
- Segment Churn Rate: Weighted churn rate across relevant segments
- High-Value Churn Ratio: Churn rate among top-balance customers
- Geographic Risk Index: Average churn rate across countries
- Engagement Drop Indicator: Churn rate among inactive customers

## 7. Analytical Interpretation

The primary insight path is:

- identify segments with the highest churn risk
- compare retained vs exited customer profiles
- rank high-value groups by revenue sensitivity
- build retention campaigns based on evidence rather than intuition

## 8. Dashboard Design

The Streamlit application provides:

- KPI overview cards
- geography comparison
- age and tenure analysis
- segment-level churn tables
- high-value customer drill-down
- balance and salary visuals

This interface allows users to filter by geography and customer profile and update the dashboard in real time.

## 9. Deliverables

The project includes:

- synthetic churn dataset
- reusable Python analysis module
- interactive dashboard
- technical documentation
- executive summary for stakeholder communication

## 10. Recommended Next Steps

Possible extensions include:

- integrating a real banking dataset
- applying machine learning for predictive churn scoring
- linking dashboard metrics to campaign outcomes
- extending to product-level and branch-level analysis

## 11. Conclusion

The project demonstrates a practical, segment-based framework for understanding churn in European banking. It provides the structure needed for both operational retention planning and strategic customer risk management.
