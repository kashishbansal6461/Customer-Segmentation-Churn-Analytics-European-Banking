# Customer Segmentation & Churn Pattern Analytics in European Banking

This project analyzes churn behavior in a European retail banking customer base using segmentation-driven analytics and an interactive Streamlit dashboard. The solution is designed to help banks identify the most churn-prone customer segments and prioritize retention actions based on geography, demographics, engagement, and financial profile.

## Project Vision

Customer churn is one of the main hidden costs in retail banking. Losing customers affects:

- lifetime value
- cross-selling potential
- acquisition efficiency
- long-term revenue stability

This project addresses the need for a data-driven retention strategy by combining descriptive analytics, customer segmentation, and live dashboard reporting.

## Business Questions

The analysis answers the following questions:

- What is the overall churn rate?
- Which customer groups are most likely to churn?
- How does churn vary by country, age, tenure, and balance profile?
- Are inactive or high-balance customers more exposed to churn risk?
- Which customer segments should be prioritized for retention campaigns?

## Dataset

The project uses a synthetic banking dataset inspired by a European financial institution. It includes the following fields:

- CustomerId
- Surname
- CreditScore
- Geography
- Gender
- Age
- Tenure
- Balance
- NumOfProducts
- HasCrCard
- IsActiveMember
- EstimatedSalary
- Exited

## Key Segmentation Dimensions

The analysis creates derived customer segments using:

- Geography: France, Spain, Germany
- Age group: <30, 30-45, 46-60, 60+
- Credit score band: Low, Medium, High
- Tenure group: New, Mid-term, Long-term
- Balance segment: Zero-balance, Low-balance, High-balance

## Analytical Framework

The project follows these steps:

1. Data ingestion and validation
2. Cleaning and feature preparation
3. Segment construction
4. Churn distribution analysis
5. Demographic and behavior comparison
6. High-value customer analysis
7. Dashboard-based stakeholder reporting

## Repository Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── run_guide.md
├── data/
│   ├── generate_data.py
│   └── customer_churn_europe.csv
├── src/
│   ├── __init__.py
│   └── churn_analysis.py
├── docs/
│   ├── technical_documentation.md
│   └── executive_summary.md
└── notebooks/
    └── churn_eda.ipynb
```

## How to Run the Project

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate the dataset

```bash
python data/generate_data.py
```

### 4. Launch the dashboard

```bash
streamlit run app.py
```

## Dashboard Features

The Streamlit dashboard includes:

- overall churn KPI cards
- geography-wise churn comparison
- age-group churn trends
- balance segment analysis
- high-value customer churn explorer
- segment filters for dynamic reporting

## Expected Insights

The analysis is designed to highlight patterns such as:

- higher churn risk in low-engagement or newly acquired customers
- country-specific churn differences
- elevated risk among certain age cohorts
- significant financial exposure in high-balance customer segments

## Deliverables

This project produces the following outputs:

- exploratory analysis and segmentation report
- interactive dashboard
- executive summary for non-technical stakeholders
- codebase ready for extension and presentation

## License

This project is distributed under the MIT License.

## Conclusion

This project provides a structured and actionable framework for customer retention analysis in European banking. By uncovering churn patterns across geography, demographics, and financial profiles, it helps banks build targeted strategies that reduce customer loss and protect revenue.
