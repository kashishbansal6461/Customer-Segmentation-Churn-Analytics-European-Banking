# Easy Run Guide for the Banking Churn Analytics Project

This guide explains how to open the project, install dependencies, and run the dashboard on your computer.

## 1. Download the project

Open the repository in GitHub:

https://github.com/KashishB6812/Customer-Segmentation-Churn-Analytics-European-Banking

Then click the green Code button and choose Download ZIP.

Once downloaded, extract the ZIP file to a folder such as:

- C:\Users\YourName\Desktop\banking-churn-project
- /Users/YourName/Desktop/banking-churn-project

## 2. Open the project in VS Code

1. Open Visual Studio Code
2. Click File > Open Folder
3. Select the extracted project folder

## 3. Open the terminal in VS Code

Go to:

- Terminal > New Terminal

This opens the command prompt inside the project folder.

## 4. Install Python dependencies

Run the following command:

```bash
pip install -r requirements.txt
```

If this does not work, use:

```bash
python -m pip install -r requirements.txt
```

If Python is not found, try:

```bash
py -m pip install -r requirements.txt
```

## 5. Generate the dataset

In the terminal, run:

```bash
python data/generate_data.py
```

If required, use:

```bash
py data/generate_data.py
```

This creates the dataset file inside the data folder.

## 6. Run the dashboard

Now start the Streamlit app:

```bash
streamlit run app.py
```

If that does not work, use:

```bash
python -m streamlit run app.py
```

Or:

```bash
py -m streamlit run app.py
```

## 7. Open the dashboard in browser

After running the command, Streamlit will show a local URL such as:

```text
http://localhost:8501
```

Open that URL in your browser.

## 8. If you get errors

### Case 1: 'python' is not recognized
Use:

```bash
py
```

Example:

```bash
py data/generate_data.py
py -m streamlit run app.py
```

### Case 2: Streamlit not installed
Run:

```bash
pip install streamlit
```

### Case 3: Module error
Try installing all project requirements again:

```bash
pip install -r requirements.txt
```

### Case 4: Data file missing
Run:

```bash
generate_data.py
```

or:

```bash
python data/generate_data.py
```

## 9. What this project does

The app shows:

- overall churn rate
- churn by geography
- churn by age group
- churn by tenure group
- customer profile comparison
- high-value customer analysis

## 10. Project folder structure

```text
banking-churn-project/
├── app.py
├── requirements.txt
├── README.md
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

## 11. Summary

To run the project, the basic flow is:

```bash
pip install -r requirements.txt
python data/generate_data.py
streamlit run app.py
```

If you want, I can also make a one-page beginner version of this guide or help you fix any error you get while running it.
