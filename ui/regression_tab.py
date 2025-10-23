import streamlit as st
from models.regression_model import run_regression


def render():
    """
    Render the Regression Analysis tab for the Digital Transformation & GDP Growth Dashboard.
    Runs an OLS regression to evaluate the impact of DTI on Vietnam's GDP growth.
    """

    # --- Page title & description ---
    st.title("📊 Regression Analysis: Impact of DTI on GDP Growth")
    st.markdown(
        """
        This section presents an **Ordinary Least Squares (OLS)** regression 
        examining how the **Digital Transformation Index (DTI)** influences 
        Vietnam's GDP growth rate.
        """
    )

    # --- Run regression ---
    try:
        result = run_regression()

        # Display model summary in a collapsible box
        with st.expander("📈 View Detailed Regression Summary", expanded=True):
            st.text(result)

        # Optional interpretation section
        st.markdown("---")
        st.markdown("### 📘 Interpretation Guide")
        st.markdown(
            """
            - **Coefficient (β₁):** Measures how a one-unit increase in DTI affects GDP growth.  
            - **Intercept (β₀):** Expected GDP growth when DTI = 0.  
            - **R-squared:** Explains the proportion of variance in GDP growth explained by DTI.  
            - **P-value:** Tests the statistical significance of the DTI variable.  
            """
        )

    except Exception as e:
        st.error(f"⚠️ Error running regression: {e}")
        st.info("Please make sure `data/vietnam_dti_gdp.csv` contains the columns `DTI` and `GDP_growth`.")
