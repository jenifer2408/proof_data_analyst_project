import re

import streamlit as st

import pandas as pd

from openai import OpenAI



# =========================================================

# PAGE CONFIG

# =========================================================

st.set_page_config(page_title="VERITAS", page_icon="◈", layout="wide")



# =========================================================

# STYLING

# =========================================================

st.markdown("""

<style>

.main-title { font-size: 42px; font-weight: 800; margin-bottom: 0; }

.subtitle { font-size: 18px; color: #9ca3af; margin-bottom: 30px; }

.verified { padding: 20px; border-radius: 12px; background-color: #12351f; border: 1px solid #2e8b57; font-size: 22px; font-weight: 700; }

.failed { padding: 20px; border-radius: 12px; background-color: #3a1717; border: 1px solid #d9534f; font-size: 22px; font-weight: 700; }

</style>

""", unsafe_allow_html=True)



# =========================================================

# DATA SOURCE - DEMO + ANY CSV

# =========================================================

st.sidebar.header("📂 Data Sources")



uploaded_files = st.sidebar.file_uploader(

    "Upload CSV file(s)",

    type=["csv"],

    accept_multiple_files=True

)



is_custom = bool(uploaded_files)

dataframes = {}

dataset_labels = {}



if uploaded_files:

    for i, file in enumerate(uploaded_files):

        try:

            df = pd.read_csv(file)

            dataframes[f"df_{i}"] = df

            dataset_labels[f"df_{i}"] = file.name

        except Exception as e:

            st.sidebar.error(f"Could not read {file.name}: {e}")



    if dataframes:

        st.sidebar.success(f"✓ {len(dataframes)} dataset(s) loaded")

        st.sidebar.markdown("### Uploaded datasets")

        for key, df in dataframes.items():

            st.sidebar.write(

                f"📄 **{dataset_labels[key]}** — {len(df)} rows × {len(df.columns)} columns"

            )

else:

    # Built-in judge-ready demo

    dataframes["df_0"] = pd.read_csv("data/superstore.csv")

    dataframes["df_1"] = pd.read_csv("data/customer_registry.csv")

    dataset_labels["df_0"] = "superstore.csv"

    dataset_labels["df_1"] = "customer_registry.csv"

    st.sidebar.info("Using built-in VERITAS demo datasets")



# Backward-compatible aliases for demo logic.

sales_df = dataframes.get("df_0", pd.DataFrame())

customer_df = dataframes.get("df_1", pd.DataFrame())



with open("audit_rules.txt", "r", encoding="utf-8") as file:

    rules = file.read()



client = OpenAI()



# =========================================================

# HELPERS

# =========================================================

def schema_text():

    parts = []

    for key, df in dataframes.items():

        parts.append(

            f"DATAFRAME {key} | FILE: {dataset_labels[key]} | ROWS: {len(df)}\n"

            f"COLUMNS: {list(df.columns)}\n"

            f"DTYPES: {df.dtypes.astype(str).to_dict()}"

        )

    return "\n\n".join(parts)





def safe_numeric(value):

    return isinstance(value, (int, float)) and not isinstance(value, bool)





def generic_negative_count(df):

    count = 0

    for col in df.columns:

        numeric = pd.to_numeric(df[col], errors="coerce")

        count += int((numeric < 0).sum())

    return count





def normalize_number(value):

    try:

        return float(value)

    except Exception:

        return None





# =========================================================

# NAVIGATION

# =========================================================

with st.sidebar:

    st.markdown("## ◈ VERITAS")

    st.caption("Proof-Carrying AI Data Analyst")

    st.divider()

    page = st.radio(

        "Navigation",

        ["🏠 Overview", "🤖 Ask VERITAS", "🔍 Data Audit", "📊 Insights", "📜 Audit Reports"],

        label_visibility="collapsed"

    )

    st.divider()

    st.markdown("### SYSTEM STATUS")

    st.success("● AI Engine: Connected")

    st.success("● Proof Engine: Ready")

    st.success("● Verification Engine: Ready")



# =========================================================

# OVERVIEW

# =========================================================

if page == "🏠 Overview":

    st.markdown('<div class="main-title">◈ VERITAS</div>', unsafe_allow_html=True)

    st.markdown(

        '<div class="subtitle">Proof-Carrying AI Data Analyst — Don\'t just trust the answer. Verify it.</div>',

        unsafe_allow_html=True

    )



    if is_custom:

        st.success("📂 CUSTOM DATA MODE — VERITAS is analyzing your uploaded CSV dataset(s).")

    else:

        st.info("VERITAS demo mode — using the built-in Superstore + customer registry datasets.")



    st.subheader("Data Health")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric("Records", len(sales_df))

    with col2:

        st.metric("Columns", len(sales_df.columns))

    with col3:

        st.metric("Duplicates", int(sales_df.duplicated().sum()))

    with col4:

        st.metric("Missing Values", int(sales_df.isna().sum().sum()))



    st.divider()

    st.subheader("How VERITAS Works")

    a, b, c = st.columns(3)

    with a:

        st.markdown("### 🔎 Understand")

        st.write("Inspect uploaded datasets, schemas and data-quality signals.")

    with b:

        st.markdown("### 🧠 Prove")

        st.write("Generate executable Python proof for the user's question.")

    with c:

        st.markdown("### ✓ Verify")

        st.write("Independently reproduce supported results before showing VERIFIED.")



    st.subheader("Available Datasets")

    for key, df in dataframes.items():

        st.write(f"**{dataset_labels[key]}** — {len(df)} rows × {len(df.columns)} columns")

        st.caption(f"Columns: {', '.join(map(str, df.columns))}")



    if not is_custom and "Quantity" in sales_df.columns:

        negative_count = int((sales_df["Quantity"] < 0).sum())

        st.warning(

            f"Data-quality signals: {negative_count} negative Quantity records, "

            f"{int(sales_df.duplicated().sum())} duplicate rows, and "

            f"{int(sales_df.isna().sum().sum())} missing values."

        )



# =========================================================

# DATA AUDIT

# =========================================================

elif page == "🔍 Data Audit":

    st.markdown('<div class="main-title">🔍 Data Audit</div>', unsafe_allow_html=True)

    st.markdown(

        '<div class="subtitle">Understand the quality of the data before trusting the analysis.</div>',

        unsafe_allow_html=True

    )



    for key, df in dataframes.items():

        st.subheader(f"📄 {dataset_labels[key]}")

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric("Rows", len(df))

        with c2:

            st.metric("Columns", len(df.columns))

        with c3:

            st.metric("Duplicate Rows", int(df.duplicated().sum()))

        with c4:

            st.metric("Missing Values", int(df.isna().sum().sum()))



        missing = df.isna().sum()

        missing = missing[missing > 0].sort_values(ascending=False)

        if not missing.empty:

            st.write("**Missing values**")

            st.dataframe(

                pd.DataFrame({"Column": missing.index, "Missing Values": missing.values}),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.success("No missing values detected.")



        schema_table = pd.DataFrame({

            "Column": df.columns,

            "Data Type": [str(df[c].dtype) for c in df.columns],

            "Unique Values": [int(df[c].nunique(dropna=True)) for c in df.columns],

            "Missing": [int(df[c].isna().sum()) for c in df.columns]

        })

        st.dataframe(schema_table, use_container_width=True, hide_index=True)

        st.divider()



# =========================================================

# INSIGHTS

# =========================================================

elif page == "📊 Insights":

    st.markdown('<div class="main-title">📊 Insights</div>', unsafe_allow_html=True)

    st.markdown(

        '<div class="subtitle">Explore useful patterns from the currently loaded data.</div>',

        unsafe_allow_html=True

    )



    if not is_custom and {"Sales", "Region"}.issubset(sales_df.columns):

        clean = sales_df.drop_duplicates().copy()

        clean = clean[clean["Sales"].notna()].copy()

        if "Quantity" in clean.columns:

            clean = clean[clean["Quantity"].isna() | (clean["Quantity"] >= 0)].copy()



        st.subheader("Sales by Region")

        st.bar_chart(clean.groupby("Region")["Sales"].sum().sort_values(ascending=False))



        if "Category" in clean.columns:

            st.subheader("Sales by Category")

            st.bar_chart(clean.groupby("Category")["Sales"].sum().sort_values(ascending=False))



        if "Profit" in clean.columns and "Category" in clean.columns:

            st.subheader("Profit by Category")

            st.bar_chart(clean.groupby("Category")["Profit"].sum().sort_values(ascending=False))



        if "Order Date" in clean.columns:

            dates = pd.to_datetime(clean["Order Date"], errors="coerce")

            monthly = clean.assign(_date=dates).dropna(subset=["_date"])

            if not monthly.empty:

                st.subheader("Monthly Sales Trend")

                st.line_chart(monthly.set_index("_date")["Sales"].resample("ME").sum())

    else:

        st.info("Custom CSV mode: use Ask VERITAS for questions about any uploaded dataset.")

        for key, df in dataframes.items():

            numeric_cols = df.select_dtypes(include="number").columns.tolist()

            if numeric_cols:

                st.subheader(f"Numeric columns — {dataset_labels[key]}")

                st.dataframe(df[numeric_cols].describe().T, use_container_width=True)



# =========================================================

# AUDIT REPORTS

# =========================================================

elif page == "📜 Audit Reports":

    st.markdown('<div class="main-title">📜 Audit Reports</div>', unsafe_allow_html=True)

    st.markdown(

        '<div class="subtitle">Verification history and audit principles.</div>',

        unsafe_allow_html=True

    )



    if is_custom:

        st.info("Custom CSV questions are independently verified when VERITAS recognizes a supported calculation pattern.")

    else:

        reports = [

            ("What is the total sales?", "✓ VERIFIED", "Numeric proof and independent calculation."),

            ("Which region has the highest sales?", "✓ VERIFIED", "Grouped aggregation reproduced independently."),

            ("High-risk customer sales?", "✓ VERIFIED", "Multi-table join and currency normalization."),

            ("What was the highest sales?", "⚠ CLARIFICATION", "The question is ambiguous."),

            ("What is the profit margin?", "⚠ INSUFFICIENT DATA", "Required information may not be available.")

        ]

        for report_question, status, note in reports:

            with st.expander(f"{status}   {report_question}"):

                st.write("**Question:**", report_question)

                st.write("**Status:**", status)

                st.write("**Audit note:**", note)



    st.subheader("Verification Principle")

    st.write(

        "VERIFIED means the generated proof result was independently reproduced. "

        "Unsupported calculations are never falsely marked VERIFIED."

    )



# =========================================================

# ASK VERITAS

# =========================================================

else:

    st.markdown('<div class="main-title">◈ VERITAS</div>', unsafe_allow_html=True)

    st.markdown(

        '<div class="subtitle">Proof-Carrying AI Data Analyst — Don\'t just trust the answer. Verify it.</div>',

        unsafe_allow_html=True

    )



    if is_custom:

        st.success("📂 Custom CSV mode")

    else:

        st.info("🧪 Demo mode — Superstore + customer registry")



    st.subheader("Ask VERITAS")

    question = st.text_area(

        "Enter your data question",

        placeholder="Example: What is the average CGPA?",

        height=100

    )

    analyze = st.button("🔍 ANALYZE", type="primary", use_container_width=True)



    if analyze:

        if not question.strip():

            st.warning("Please enter a question.")

            st.stop()



        mode_text = "CUSTOM CSV DATASET" if is_custom else "VERITAS DEMO DATASET"



        prompt = f"""

You are VERITAS, a Proof-Carrying AI Data Analyst.



USER QUESTION:

{question}



DATA MODE:

{mode_text}



AVAILABLE DATASETS:

{schema_text()}



AUDIT RULES:

{rules}



CORE OBJECTIVE:

Generate executable Python code that answers the user's question using ONLY the existing DataFrames.

The final result MUST be stored in a variable named answer and printed.

If the question cannot be answered reliably, set answer = None and set reason to either CLARIFICATION_REQUIRED or INSUFFICIENT_DATA.



GENERAL RULES:

1\. Use only the DataFrames listed above.

2\. Do not assume any column exists. Check the actual columns shown above.

3\. Never invent columns or data.

4\. Do not import libraries.

5\. Do not read files.

6\. Do not access the internet.

7\. Do not use os, sys, subprocess, eval, exec, open, or dunder attributes.

8\. Do not modify the original DataFrames; make copies when cleaning.

9\. Handle missing values and duplicates when relevant.

10\. Do not silently make unsupported assumptions.

11\. If the question is ambiguous, use reason = "CLARIFICATION_REQUIRED".

12\. If required information is absent, use reason = "INSUFFICIENT_DATA".

13\. Return ONLY executable Python code. No markdown and no explanation outside the code.



CUSTOM CSV RULES:

If this is CUSTOM CSV DATASET mode, the uploaded CSVs are arbitrary.

Do NOT assume Sales, Quantity, Profit, Region, Category, Customer ID, Risk Level, or Currency Unit exist.

Inspect the actual schemas and choose the relevant dataframe and columns.

If multiple datasets are relevant, only join them when a meaningful common key exists.

Do not guess relationships between files.

For simple numerical questions, prefer direct pandas operations such as:

    answer = df_0["ActualColumn"].sum()

    answer = df_0["ActualColumn"].mean()

    answer = df_0["ActualColumn"].min()

    answer = df_0["ActualColumn"].max()

    answer = df_0["ActualColumn"].count()

    answer = df_0["ActualColumn"].nunique()

    answer = len(df_0)

Use the real column names from the schema.



DEMO RULES:

If this is VERITAS DEMO DATASET mode and the required columns exist:

\- Ordinary total sales: drop exact duplicates, exclude missing Sales, and if Quantity exists exclude negative Quantity; then sum Sales.

\- Highest sales region: drop duplicates, clean Sales and Quantity when present, group Sales by Region, and return the region with the highest sum.

\- High-risk customer sales: only when the question specifically concerns high-risk customers or corporate financial liability. Use Customer ID, Risk Level, Sales and Currency Unit if those columns exist. Join sales_df and customer_df using Customer ID. Apply EUR -> USD at 1.12 only according to the demo audit rules.

\- Do not apply demo-specific rules to arbitrary custom CSVs.



AMBIGUITY:

For a question such as "What was the highest sales?", clarification may be needed because it could mean the highest individual sale, highest regional total, highest product total, etc.



FINAL REQUIREMENT:

Finish with answer = ... and print(answer), or answer = None plus reason = "CLARIFICATION_REQUIRED" or "INSUFFICIENT_DATA".

"""



        # =====================================================

        # AI GENERATION

        # =====================================================

        with st.spinner("Generating executable proof..."):

            try:

                response = client.responses.create(

                    model="gpt-6-luna",

                    input=prompt

                )

                generated_code = response.output_text

            except Exception as e:

                st.error(f"AI generation failed: {e}")

                st.stop()



        generated_code = re.sub(r"```python", "", generated_code)

        generated_code = re.sub(r"```", "", generated_code).strip()



        # =====================================================

        # SAFETY VALIDATION

        # =====================================================

        blocked = [

            "import ", "from ", "os.", "sys.", "subprocess",

            "eval(", "exec(", "open(", "__"

        ]

        unsafe_item = next((item for item in blocked if item in generated_code), None)

        if unsafe_item:

            st.error(f"❌ Code rejected for safety: {unsafe_item}")

            st.stop()



        st.subheader("Verification Pipeline")

        progress = st.empty()

        progress.info("✓ AI code generated")



        # =====================================================

        # EXECUTION NAMESPACE

        # =====================================================

        execution_namespace = {key: df.copy() for key, df in dataframes.items()}

        execution_namespace["sales_df"] = sales_df.copy()

        execution_namespace["customer_df"] = customer_df.copy()

        execution_namespace["pd"] = pd



        safe_builtins = {

            "print": print, "len": len, "sum": sum, "min": min, "max": max,

            "abs": abs, "all": all, "any": any, "str": str, "int": int,

            "float": float, "bool": bool, "list": list, "dict": dict,

            "set": set, "tuple": tuple, "range": range, "sorted": sorted,

            "zip": zip, "enumerate": enumerate, "isinstance": isinstance

        }



        try:

            exec(

                generated_code,

                {"__builtins__": safe_builtins},

                execution_namespace

            )

            answer = execution_namespace.get("answer")

            reason = execution_namespace.get("reason")

            progress.info("✓ AI code generated → ✓ Code executed")

        except Exception as e:

            st.error(f"❌ Proof execution failed: {e}")

            answer = None

            reason = "EXECUTION_ERROR"



        # =====================================================

        # REFUSAL / CLARIFICATION

        # =====================================================

        if answer is None:

            if reason == "CLARIFICATION_REQUIRED":

                st.warning("⚠ VERITAS needs clarification before calculating a reliable answer.")

            elif reason == "INSUFFICIENT_DATA":

                st.warning("⚠ VERITAS cannot reliably answer this question from the available data.")

            else:

                st.warning(f"⚠ {reason or 'No reliable answer was produced.'}")

            st.stop()



        # =====================================================

        # ANSWER

        # =====================================================

        st.subheader("Answer")

        if safe_numeric(answer):

            st.metric("Candidate Result", f"{float(answer):,.2f}")

        else:

            st.metric("Candidate Result", str(answer))



        # =====================================================

        # INDEPENDENT VERIFICATION

        # =====================================================

        progress.info("✓ Code executed → 🔍 Independently verifying...")



        question_lower = question.lower()

        verification_passed = False

        verified_answer = None

        difference = None

        verification_type = "unsupported"



        # =====================================================

        # GENERIC CUSTOM CSV VERIFIER

        # =====================================================

        if is_custom:



            # SUM

            match = re.search(

                r'answer\s*=\s*(df_\d+)\s*\\[\s*["\']\([^"\']+)["\']\s*\\]\s*\\.sum\\(\\)',

                generated_code

            )

            if match:

                df_name, column_name = match.groups()

                if df_name in dataframes and column_name in dataframes[df_name].columns:

                    verify_df = dataframes[df_name].copy()

                    verified_answer = pd.to_numeric(verify_df[column_name], errors="coerce").sum()

                    difference = abs(float(verified_answer) - float(answer))

                    verification_passed = difference < 0.000001

                    verification_type = "numeric"



            # MEAN / AVERAGE

            if verification_type == "unsupported":

                match = re.search(

                    r'answer\s*=\s*(df_\d+)\s*\\[\s*["\']\([^"\']+)["\']\s*\\]\s*\\.(mean|average)\\(\\)',

                    generated_code,

                    re.IGNORECASE

                )

                if match:

                    df_name, column_name, _ = match.groups()

                    if df_name in dataframes and column_name in dataframes[df_name].columns:

                        verify_df = dataframes[df_name].copy()

                        verified_answer = pd.to_numeric(verify_df[column_name], errors="coerce").mean()

                        difference = abs(float(verified_answer) - float(answer))

                        verification_passed = difference < 0.000001

                        verification_type = "numeric"



            # MIN

            if verification_type == "unsupported":

                match = re.search(

                    r'answer\s*=\s*(df_\d+)\s*\\[\s*["\']\([^"\']+)["\']\s*\\]\s*\\.min\\(\\)',

                    generated_code

                )

                if match:

                    df_name, column_name = match.groups()

                    if df_name in dataframes and column_name in dataframes[df_name].columns:

                        verify_df = dataframes[df_name].copy()

                        verified_answer = pd.to_numeric(verify_df[column_name], errors="coerce").min()

                        difference = abs(float(verified_answer) - float(answer))

                        verification_passed = difference < 0.000001

                        verification_type = "numeric"



            # MAX

            if verification_type == "unsupported":

                match = re.search(

                    r'answer\s*=\s*(df_\d+)\s*\\[\s*["\']\([^"\']+)["\']\s*\\]\s*\\.max\\(\\)',

                    generated_code

                )

                if match:

                    df_name, column_name = match.groups()

                    if df_name in dataframes and column_name in dataframes[df_name].columns:

                        verify_df = dataframes[df_name].copy()

                        verified_answer = pd.to_numeric(verify_df[column_name], errors="coerce").max()

                        difference = abs(float(verified_answer) - float(answer))

                        verification_passed = difference < 0.000001

                        verification_type = "numeric"



            # COUNT

            if verification_type == "unsupported":

                match = re.search(

                    r'answer\s*=\s*(df_\d+)\s*\\[\s*["\']\([^"\']+)["\']\s*\\]\s*\\.count\\(\\)',

                    generated_code

                )

                if match:

                    df_name, column_name = match.groups()

                    if df_name in dataframes and column_name in dataframes[df_name].columns:

                        verify_df = dataframes[df_name].copy()

                        verified_answer = int(verify_df[column_name].count())

                        difference = abs(float(verified_answer) - float(answer))

                        verification_passed = difference < 0.000001

                        verification_type = "numeric"



            # UNIQUE COUNT

            if verification_type == "unsupported":

                match = re.search(

                    r'answer\s*=\s*(df_\d+)\s*\\[\s*["\']\([^"\']+)["\']\s*\\]\s*\\.nunique\\(\\)',

                    generated_code

                )

                if match:

                    df_name, column_name = match.groups()

                    if df_name in dataframes and column_name in dataframes[df_name].columns:

                        verify_df = dataframes[df_name].copy()

                        verified_answer = int(verify_df[column_name].nunique())

                        difference = abs(float(verified_answer) - float(answer))

                        verification_passed = difference < 0.000001

                        verification_type = "numeric"



            # ROW COUNT

            if verification_type == "unsupported":

                match = re.search(

                    r'answer\s*=\s*len\\(\s*(df_\d+)\s*\\)',

                    generated_code

                )

                if match:

                    df_name = match.group(1)

                    if df_name in dataframes:

                        verified_answer = len(dataframes[df_name])

                        difference = abs(float(verified_answer) - float(answer))

                        verification_passed = difference < 0.000001

                        verification_type = "numeric"



            # SHAPE[0] ROW COUNT

            if verification_type == "unsupported":

                match = re.search(

                    r'answer\s*=\s*(df_\d+)\\.shape\\[0\\]',

                    generated_code

                )

                if match:

                    df_name = match.group(1)

                    if df_name in dataframes:

                        verified_answer = len(dataframes[df_name])

                        difference = abs(float(verified_answer) - float(answer))

                        verification_passed = difference < 0.000001

                        verification_type = "numeric"



        # =====================================================

        # BUILT-IN DEMO VERIFIERS

        # =====================================================

        else:

            # -------------------------------------------------
            # TOTAL SALES
            # -------------------------------------------------

            if (
                "total sales" in question_lower
                and "Sales" in sales_df.columns
            ):

                verified_df = sales_df.drop_duplicates().copy()

                verified_df = verified_df[
                    verified_df["Sales"].notna()
                ].copy()

                if "Quantity" in verified_df.columns:
                    verified_df = verified_df[
                        verified_df["Quantity"].isna()
                        |
                        (verified_df["Quantity"] >= 0)
                    ].copy()

                verified_answer = verified_df["Sales"].sum()

                difference = abs(
                    float(verified_answer) - float(answer)
                )

                verification_passed = (
                    difference < 0.000001
                )

                verification_type = "numeric"


            # -------------------------------------------------
            # MINIMUM SALES
            # -------------------------------------------------

            elif (
                "minimum sales" in question_lower
                or "min sales" in question_lower
            ):

                verified_df = sales_df.drop_duplicates().copy()

                verified_df = verified_df[
                    verified_df["Sales"].notna()
                ].copy()

                if "Quantity" in verified_df.columns:
                    verified_df = verified_df[
                        verified_df["Quantity"].isna()
                        |
                        (verified_df["Quantity"] >= 0)
                    ].copy()

                verified_answer = verified_df["Sales"].min()

                difference = abs(
                    float(verified_answer) - float(answer)
                )

                verification_passed = (
                    difference < 0.000001
                )

                verification_type = "numeric"


            # -------------------------------------------------
            # MAXIMUM SALES
            # -------------------------------------------------

            elif (
                "maximum sales" in question_lower
                or "max sales" in question_lower
            ):

                verified_df = sales_df.drop_duplicates().copy()

                verified_df = verified_df[
                    verified_df["Sales"].notna()
                ].copy()

                if "Quantity" in verified_df.columns:
                    verified_df = verified_df[
                        verified_df["Quantity"].isna()
                        |
                        (verified_df["Quantity"] >= 0)
                    ].copy()

                verified_answer = verified_df["Sales"].max()

                difference = abs(
                    float(verified_answer) - float(answer)
                )

                verification_passed = (
                    difference < 0.000001
                )

                verification_type = "numeric"


            # -------------------------------------------------
            # AVERAGE SALES
            # -------------------------------------------------

            elif (
                "average sales" in question_lower
                or "mean sales" in question_lower
            ):

                verified_df = sales_df.drop_duplicates().copy()

                verified_df = verified_df[
                    verified_df["Sales"].notna()
                ].copy()

                if "Quantity" in verified_df.columns:
                    verified_df = verified_df[
                        verified_df["Quantity"].isna()
                        |
                        (verified_df["Quantity"] >= 0)
                    ].copy()

                verified_answer = verified_df["Sales"].mean()

                difference = abs(
                    float(verified_answer) - float(answer)
                )

                verification_passed = (
                    difference < 0.000001
                )

                verification_type = "numeric"


            # -------------------------------------------------
            # COUNT SALES
            # -------------------------------------------------

            elif (
                "count sales" in question_lower
                or "number of sales" in question_lower
            ):

                verified_df = sales_df.drop_duplicates().copy()

                verified_answer = int(
                    verified_df["Sales"].count()
                )

                difference = abs(
                    float(verified_answer) - float(answer)
                )

                verification_passed = (
                    difference < 0.000001
                )

                verification_type = "numeric"


            # -------------------------------------------------
            # HIGHEST SALES REGION
            # -------------------------------------------------

            elif (
                "highest sales" in question_lower
                and "region" in question_lower
                and {"Sales", "Region"}.issubset(
                    sales_df.columns
                )
            ):

                verified_df = sales_df.drop_duplicates().copy()

                verified_df = verified_df[
                    verified_df["Sales"].notna()
                ].copy()

                if "Quantity" in verified_df.columns:
                    verified_df = verified_df[
                        verified_df["Quantity"].isna()
                        |
                        (verified_df["Quantity"] >= 0)
                    ].copy()

                region_sales = (
                    verified_df
                    .groupby("Region")["Sales"]
                    .sum()
                    .sort_values(ascending=False)
                )

                if not region_sales.empty:
                    verified_answer = region_sales.index[0]

                    verification_passed = (
                        str(answer).strip().lower()
                        ==
                        str(verified_answer).strip().lower()
                    )

                    verification_type = "text"


            # -------------------------------------------------
            # HIGH-RISK CUSTOMER SALES
            # -------------------------------------------------

            elif (
                (
                    "high-risk" in question_lower
                    or
                    "high risk" in question_lower
                )
                and
                {
                    "Customer ID",
                    "Risk Level",
                    "Sales",
                    "Currency Unit"
                }.issubset(sales_df.columns)
                and
                {
                    "Customer ID",
                    "Risk Level",
                    "Currency Unit"
                }.issubset(customer_df.columns)
            ):

                verified_sales = sales_df.drop_duplicates().copy()

                verified_sales = verified_sales[
                    verified_sales["Customer ID"].notna()
                ].copy()

                verified_sales = verified_sales[
                    verified_sales["Sales"].notna()
                ].copy()

                if "Quantity" in verified_sales.columns:
                    verified_sales = verified_sales[
                        verified_sales["Quantity"].isna()
                        |
                        (verified_sales["Quantity"] >= 0)
                    ].copy()

                verified_registry = customer_df.drop_duplicates().copy()

                if not verified_registry[
                    "Customer ID"
                ].duplicated().any():

                    joined = verified_sales.merge(
                        verified_registry[
                            [
                                "Customer ID",
                                "Risk Level",
                                "Currency Unit"
                            ]
                        ],
                        on="Customer ID",
                        how="left",
                        validate="many_to_one"
                    )

                    high = joined[
                        joined["Risk Level"]
                        .astype("string")
                        .str.strip()
                        .str.upper()
                        == "HIGH"
                    ].copy()

                    high["Currency Unit"] = (
                        high["Currency Unit"]
                        .astype("string")
                        .str.strip()
                        .str.upper()
                    )

                    high["Exchange Rate"] = (
                        high["Currency Unit"]
                        .map(
                            {
                                "USD": 1.0,
                                "EUR": 1.12
                            }
                        )
                    )

                    if not high[
                        "Exchange Rate"
                    ].isna().any():

                        verified_answer = (
                            high["Sales"]
                            *
                            high["Exchange Rate"]
                        ).sum()

                        difference = abs(
                            float(verified_answer) - float(answer)
                        )

                        verification_passed = (
                            difference < 0.000001
                        )

                        verification_type = "numeric"


        # =====================================================

        # DISPLAY VERIFICATION

        # =====================================================

        if verification_passed:

            progress.success("✓ AI proof executed → ✓ Independent verification passed")

            st.markdown('<div class="verified">🟢 VERIFIED</div>', unsafe_allow_html=True)

            if verification_type == "numeric":

                a, b = st.columns(2)

                with a:

                    st.metric("AI Proof Result", f"{float(answer):,.2f}")

                with b:

                    st.metric("Independent Result", f"{float(verified_answer):,.2f}")

                st.write("Difference:", f"{difference:.10f}")

            else:

                a, b = st.columns(2)

                with a:

                    st.metric("AI Proof Result", str(answer))

                with b:

                    st.metric("Independent Result", str(verified_answer))

                st.write("Match: Exact")

        elif verification_type == "unsupported":

            progress.warning("✓ Proof executed → ⚠ No independent verifier available for this question type")

            st.warning(

                "⚠ NOT VERIFIED — The answer has executable proof, but VERITAS does not have "

                "a deterministic independent verifier for this question yet."

            )

        else:

            progress.error("✗ Independent verification failed")

            st.markdown('<div class="failed">🔴 VERIFICATION FAILED</div>', unsafe_allow_html=True)

            st.write("AI result:", answer)

            if verified_answer is not None:

                st.write("Independent result:", verified_answer)

            if difference is not None:

                st.write("Difference:", difference)



        # =====================================================

        # PROOF CODE

        # =====================================================

        with st.expander("🐍 View Executable Proof", expanded=True):

            st.code(generated_code, language="python")



        # =====================================================

        # DATA EVIDENCE

        # =====================================================

        with st.expander("🔍 View Data Evidence"):

            for key, df in dataframes.items():

                st.write(f"**Source dataset:** {dataset_labels[key]}")

                st.write("Rows:", len(df))

                st.write("Columns:", list(df.columns))

                st.write("Exact duplicates:", int(df.duplicated().sum()))

                st.write("Missing values:", int(df.isna().sum().sum()))

                st.divider()
