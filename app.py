from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def load_data(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "Exited" not in df.columns:
        raise ValueError("The dataset must contain an 'Exited' column for the churn target.")
    return df


def prepare_segments(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

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

    out["AgeGroup"] = out["Age"].map(age_group)
    out["CreditScoreBand"] = out["CreditScore"].map(credit_band)
    out["TenureGroup"] = out["Tenure"].map(tenure_group)
    out["BalanceSegment"] = out["Balance"].map(balance_segment)
    return out


def overall_kpis(df: pd.DataFrame) -> dict:
    total_customers = len(df)
    churn_rate = df["Exited"].mean()

    segment_summary = (
        df.groupby(["Geography", "AgeGroup", "CreditScoreBand", "TenureGroup", "BalanceSegment"], dropna=False)
        .agg(customers=("CustomerId", "count"), churn_rate=("Exited", "mean"))
        .reset_index()
    )
    segment_churn_rate = (
        np.average(segment_summary["churn_rate"], weights=segment_summary["customers"])
        if not segment_summary.empty
        else 0.0
    )

    high_value_threshold = df["Balance"].quantile(0.75)
    high_value = df[df["Balance"] >= high_value_threshold]
    high_value_churn_ratio = high_value["Exited"].mean() if not high_value.empty else 0.0

    geographic_risk = df.groupby("Geography")["Exited"].mean()
    geographic_risk_index = geographic_risk.mean() if not geographic_risk.empty else 0.0

    inactive = df[df["IsActiveMember"] == 0]
    engagement_drop_indicator = inactive["Exited"].mean() if not inactive.empty else 0.0

    churned_customers = len(df[df["Exited"] == 1])
    retained_customers = total_customers - churned_customers

    active_members = len(df[df["IsActiveMember"] == 1])
    inactive_members = total_customers - active_members

    avg_balance = df["Balance"].mean()
    avg_salary = df["EstimatedSalary"].mean()
    avg_age = df["Age"].mean()
    avg_tenure = df["Tenure"].mean()

    return {
        "total_customers": total_customers,
        "churned_customers": churned_customers,
        "retained_customers": retained_customers,
        "overall_churn_rate": churn_rate,
        "segment_churn_rate": segment_churn_rate,
        "high_value_churn_ratio": high_value_churn_ratio,
        "high_value_threshold": high_value_threshold,
        "geographic_risk_index": geographic_risk_index,
        "engagement_drop_indicator": engagement_drop_indicator,
        "active_members": active_members,
        "inactive_members": inactive_members,
        "avg_balance": avg_balance,
        "avg_salary": avg_salary,
        "avg_age": avg_age,
        "avg_tenure": avg_tenure,
    }


def segment_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["Geography", "AgeGroup", "CreditScoreBand", "TenureGroup", "BalanceSegment"], as_index=False, dropna=False)
        .agg(customers=("CustomerId", "count"), churn_rate=("Exited", "mean"))
        .sort_values("churn_rate", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def high_value_metrics(df: pd.DataFrame) -> pd.DataFrame:
    threshold = df["Balance"].quantile(0.75)
    high_value = df[df["Balance"] >= threshold].copy()
    if high_value.empty:
        return pd.DataFrame(columns=["BalanceThreshold", "Geography", "Customers", "ExitedRate", "AvgBalance", "AvgSalary"])

    high_value_summary = (
        high_value.groupby("Geography", as_index=False)
        .agg(
            Customers=("CustomerId", "count"),
            ExitedRate=("Exited", "mean"),
            AvgBalance=("Balance", "mean"),
            AvgSalary=("EstimatedSalary", "mean"),
        )
        .sort_values("ExitedRate", ascending=False)
        .reset_index(drop=True)
    )
    high_value_summary["BalanceThreshold"] = threshold
    return high_value_summary


def churn_profile_summary(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy["ChurnStatus"] = np.where(df_copy["Exited"] == 1, "Exited", "Retained")
    profile = (
        df_copy.groupby("ChurnStatus", as_index=False)
        .agg(
            AvgAge=("Age", "mean"),
            AvgBalance=("Balance", "mean"),
            AvgSalary=("EstimatedSalary", "mean"),
            AvgTenure=("Tenure", "mean"),
            Customers=("CustomerId", "count"),
        )
    )
    return profile


def main():
    st.set_page_config(page_title="Bank Churn Analytics Dashboard", layout="wide")
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .kpi-header {
            font-size: 24px;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🏦 European Banking Customer Segmentation & Churn Pattern Analytics")
    st.markdown("---")

    data_path = Path(__file__).resolve().parent / "data" / "customer_churn_europe.csv"

    if not data_path.exists():
        st.warning("⚠️ Dataset not found. Run: python data/generate_data.py")
        return

    df = load_data(data_path)
    df = prepare_segments(df)

    # Sidebar Filters
    with st.sidebar:
        st.header("📊 Dashboard Filters")
        st.markdown("---")
        
        geography = st.multiselect(
            "📍 Select Geography",
            sorted(df["Geography"].unique()),
            default=sorted(df["Geography"].unique()),
        )
        
        genders = st.multiselect(
            "👥 Select Gender",
            sorted(df["Gender"].unique()),
            default=sorted(df["Gender"].unique()),
        )
        
        age_min, age_max = st.slider(
            "🎂 Age Range",
            int(df["Age"].min()),
            int(df["Age"].max()),
            (int(df["Age"].min()), int(df["Age"].max())),
        )
        
        credit_bands = st.multiselect(
            "💳 Credit Score Band",
            sorted(df["CreditScoreBand"].unique()),
            default=sorted(df["CreditScoreBand"].unique()),
        )
        
        tenure_groups = st.multiselect(
            "⏱️ Tenure Group",
            sorted(df["TenureGroup"].unique()),
            default=sorted(df["TenureGroup"].unique()),
        )

    filtered = df[
        (df["Geography"].isin(geography))
        & (df["Gender"].isin(genders))
        & (df["Age"].between(age_min, age_max))
        & (df["CreditScoreBand"].isin(credit_bands))
        & (df["TenureGroup"].isin(tenure_groups))
    ].copy()

    if filtered.empty:
        st.warning("⚠️ No records match the current filter selection. Please adjust your filters.")
        return

    kpis = overall_kpis(filtered)

    # 1. EXECUTIVE KPI OVERVIEW
    st.subheader("📈 Executive KPI Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("👥 Total Customers", f"{kpis['total_customers']:,}")
    with col2:
        st.metric("📉 Churned", f"{kpis['churned_customers']:,}", delta=f"{kpis['overall_churn_rate']:.1%}")
    with col3:
        st.metric("✅ Retained", f"{kpis['retained_customers']:,}", delta=f"{1-kpis['overall_churn_rate']:.1%}")
    with col4:
        st.metric("💰 Avg Balance", f"€{kpis['avg_balance']:,.0f}")
    with col5:
        st.metric("💵 Avg Salary", f"€{kpis['avg_salary']:,.0f}")

    st.markdown("---")

    # 2. KEY METRICS ROW
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 Overall Churn Rate", f"{kpis['overall_churn_rate']:.2%}")
    with col2:
        st.metric("🎯 Segment Churn Rate", f"{kpis['segment_churn_rate']:.2%}")
    with col3:
        st.metric("💎 High-Value Churn", f"{kpis['high_value_churn_ratio']:.2%}")
    with col4:
        st.metric("🌍 Geographic Risk", f"{kpis['geographic_risk_index']:.2%}")
    with col5:
        st.metric("😴 Inactive Risk", f"{kpis['engagement_drop_indicator']:.2%}")

    st.markdown("---")

    # 3. ENGAGEMENT METRICS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🟢 Active Members", f"{kpis['active_members']:,}")
    with col2:
        st.metric("🔴 Inactive Members", f"{kpis['inactive_members']:,}")
    with col3:
        st.metric("📅 Avg Tenure (Years)", f"{kpis['avg_tenure']:.1f}")

    st.markdown("---")

    # 4. VISUALIZATIONS
    st.subheader("📊 Churn Analysis by Dimensions")

    # Geography, Age, Tenure Charts
    col_left, col_center, col_right = st.columns(3)

    with col_left:
        region_summary = (
            filtered.groupby("Geography", as_index=False)["Exited"]
            .agg(churn_rate="mean", customers="size")
            .sort_values("churn_rate", ascending=False)
        )
        fig_geography = px.bar(
            region_summary,
            x="Geography",
            y="churn_rate",
            color="Geography",
            title="Churn Rate by Geography",
            text_auto=".2%",
            labels={"churn_rate": "Churn Rate"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_geography.update_layout(height=400)
        st.plotly_chart(fig_geography, use_container_width=True)

    with col_center:
        age_summary = (
            filtered.groupby("AgeGroup", as_index=False)["Exited"]
            .agg(churn_rate="mean", customers="size")
        )
        age_order = ["<30", "30-45", "46-60", "60+"]
        age_summary["AgeGroup"] = pd.Categorical(age_summary["AgeGroup"], categories=age_order, ordered=True)
        age_summary = age_summary.sort_values("AgeGroup")
        
        fig_age = px.bar(
            age_summary,
            x="AgeGroup",
            y="churn_rate",
            color="AgeGroup",
            title="Churn Rate by Age Group",
            text_auto=".2%",
            labels={"churn_rate": "Churn Rate"},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_age.update_layout(height=400)
        st.plotly_chart(fig_age, use_container_width=True)

    with col_right:
        tenure_summary = (
            filtered.groupby("TenureGroup", as_index=False)["Exited"]
            .agg(churn_rate="mean", customers="size")
        )
        tenure_order = ["New", "Mid-term", "Long-term"]
        tenure_summary["TenureGroup"] = pd.Categorical(tenure_summary["TenureGroup"], categories=tenure_order, ordered=True)
        tenure_summary = tenure_summary.sort_values("TenureGroup")
        
        fig_tenure = px.bar(
            tenure_summary,
            x="TenureGroup",
            y="churn_rate",
            color="TenureGroup",
            title="Churn Rate by Tenure Group",
            text_auto=".2%",
            labels={"churn_rate": "Churn Rate"},
            color_discrete_sequence=px.colors.qualitative.Light
        )
        fig_tenure.update_layout(height=400)
        st.plotly_chart(fig_tenure, use_container_width=True)

    st.markdown("---")

    # 5. CREDIT SCORE & BALANCE ANALYSIS
    col_left, col_right = st.columns(2)

    with col_left:
        credit_summary = (
            filtered.groupby("CreditScoreBand", as_index=False)["Exited"]
            .agg(churn_rate="mean", customers="size")
        )
        credit_order = ["Low", "Medium", "High"]
        credit_summary["CreditScoreBand"] = pd.Categorical(credit_summary["CreditScoreBand"], categories=credit_order, ordered=True)
        credit_summary = credit_summary.sort_values("CreditScoreBand")
        
        fig_credit = px.bar(
            credit_summary,
            x="CreditScoreBand",
            y="churn_rate",
            color="CreditScoreBand",
            title="Churn Rate by Credit Score Band",
            text_auto=".2%",
            labels={"churn_rate": "Churn Rate"},
            color_discrete_sequence=["#ff6b6b", "#ffd93d", "#6bcf7f"]
        )
        fig_credit.update_layout(height=400)
        st.plotly_chart(fig_credit, use_container_width=True)

    with col_right:
        balance_summary = (
            filtered.groupby("BalanceSegment", as_index=False)["Exited"]
            .agg(churn_rate="mean", customers="size")
        )
        balance_order = ["Zero-balance", "Low-balance", "High-balance"]
        balance_summary["BalanceSegment"] = pd.Categorical(balance_summary["BalanceSegment"], categories=balance_order, ordered=True)
        balance_summary = balance_summary.sort_values("BalanceSegment")
        
        fig_balance = px.bar(
            balance_summary,
            x="BalanceSegment",
            y="churn_rate",
            color="BalanceSegment",
            title="Churn Rate by Balance Segment",
            text_auto=".2%",
            labels={"churn_rate": "Churn Rate"},
            color_discrete_sequence=["#ff6b6b", "#ffa500", "#4ecdc4"]
        )
        fig_balance.update_layout(height=400)
        st.plotly_chart(fig_balance, use_container_width=True)

    st.markdown("---")

    # 6. SEGMENT-LEVEL CHURN ANALYSIS
    st.subheader("🔍 Segment-Level Churn Analysis (Top 25)")
    seg_summary = segment_churn_summary(filtered)
    seg_summary_display = seg_summary.head(25).copy()
    seg_summary_display["churn_rate"] = seg_summary_display["churn_rate"].apply(lambda x: f"{x:.2%}")
    st.dataframe(seg_summary_display, use_container_width=True)

    st.markdown("---")

    # 7. HIGH-VALUE CUSTOMER EXPLORER
    st.subheader("💎 High-Value Customer Churn Explorer (Top 25% by Balance)")
    hv = high_value_metrics(filtered)
    if not hv.empty:
        hv_display = hv.copy()
        hv_display["ExitedRate"] = hv_display["ExitedRate"].apply(lambda x: f"{x:.2%}")
        hv_display["AvgBalance"] = hv_display["AvgBalance"].apply(lambda x: f"€{x:,.0f}")
        hv_display["AvgSalary"] = hv_display["AvgSalary"].apply(lambda x: f"€{x:,.0f}")
        hv_display["BalanceThreshold"] = hv_display["BalanceThreshold"].apply(lambda x: f"€{x:,.0f}")
        st.dataframe(hv_display, use_container_width=True)

    st.markdown("---")

    # 8. CUSTOMER PROFILE COMPARISON
    st.subheader("👥 Customer Profile Comparison")
    
    col_left, col_right = st.columns(2)

    with col_left:
        comp = filtered.assign(ChurnStatus=np.where(filtered["Exited"] == 1, "Exited", "Retained"))
        profile_fig = px.histogram(
            comp,
            x="Balance",
            color="ChurnStatus",
            barmode="overlay",
            title="Balance Distribution by Churn Status",
            nbins=35,
            color_discrete_map={"Exited": "#ff6b6b", "Retained": "#51cf66"}
        )
        profile_fig.update_layout(height=400)
        st.plotly_chart(profile_fig, use_container_width=True)

    with col_right:
        scatter_fig = px.scatter(
            comp,
            x="EstimatedSalary",
            y="Balance",
            color="ChurnStatus",
            title="Estimated Salary vs Balance by Churn Status",
            opacity=0.7,
            color_discrete_map={"Exited": "#ff6b6b", "Retained": "#51cf66"}
        )
        scatter_fig.update_layout(height=400)
        st.plotly_chart(scatter_fig, use_container_width=True)

    st.markdown("---")

    # 9. CHURN STATUS PROFILE SUMMARY
    st.subheader("📋 Churn Status Profile Summary")
    profile_summary = churn_profile_summary(comp)
    
    profile_display = profile_summary.copy()
    profile_display["AvgAge"] = profile_display["AvgAge"].apply(lambda x: f"{x:.1f}")
    profile_display["AvgBalance"] = profile_display["AvgBalance"].apply(lambda x: f"€{x:,.0f}")
    profile_display["AvgSalary"] = profile_display["AvgSalary"].apply(lambda x: f"€{x:,.0f}")
    profile_display["AvgTenure"] = profile_display["AvgTenure"].apply(lambda x: f"{x:.1f}")
    
    st.dataframe(profile_display, use_container_width=True)

    st.markdown("---")

    # 10. AGE VS CHURN SCATTER
    st.subheader("📊 Additional Insights")
    
    col_left, col_right = st.columns(2)

    with col_left:
        age_churn_fig = px.scatter(
            comp,
            x="Age",
            y="CreditScore",
            color="ChurnStatus",
            title="Age vs Credit Score by Churn Status",
            size="Balance",
            opacity=0.6,
            color_discrete_map={"Exited": "#ff6b6b", "Retained": "#51cf66"}
        )
        age_churn_fig.update_layout(height=400)
        st.plotly_chart(age_churn_fig, use_container_width=True)

    with col_right:
        tenure_age_fig = px.scatter(
            comp,
            x="Tenure",
            y="Age",
            color="ChurnStatus",
            title="Tenure vs Age by Churn Status",
            size="Balance",
            opacity=0.6,
            color_discrete_map={"Exited": "#ff6b6b", "Retained": "#51cf66"}
        )
        tenure_age_fig.update_layout(height=400)
        st.plotly_chart(tenure_age_fig, use_container_width=True)

    st.markdown("---")
    st.success("✅ Dashboard updated with all customer data and filters applied successfully!")


if __name__ == "__main__":
    main()
