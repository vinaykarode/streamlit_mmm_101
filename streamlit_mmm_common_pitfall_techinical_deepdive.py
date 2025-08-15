import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, Lasso
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="MMM Pitfalls Technical Guide",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🎯 6 Common MMM Pitfalls: Technical Deep Dive")
st.markdown("### Complete guide with algorithms, diagnostics, and solutions")

# Sidebar
st.sidebar.markdown("## 📚 Quick Navigation")
st.sidebar.markdown("""
**Easy to Grasp:**
1. Data Quality Issues
2. External Factor Omission

**Tricky to Understand:**
3. Multicollinearity
4. Attribution Windows  
5. Saturation Misspecification
6. Baseline Drift
""")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1️⃣ Data Quality",
    "2️⃣ External Factors", 
    "3️⃣ Multicollinearity",
    "4️⃣ Attribution Windows",
    "5️⃣ Saturation",
    "6️⃣ Baseline Drift"
])

# Tab 1: Data Quality Issues
with tab1:
    st.header("Data Quality Issues")
    st.markdown("**Category:** Easy to Grasp | **Impact:** High | **Frequency:** Very Common")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 The Problem: Multiple Data Sources")
        
        # Create data discrepancy visualization
        data_sources = pd.DataFrame({
            'Source': ['Meta Platform', 'Finance Dept', 'Agency', 'Data Warehouse'],
            'Facebook Spend': [55000, 50000, 60000, 52500],
            'Google Spend': [80000, 78000, 85000, 79000],
            'TV Spend': [120000, 125000, np.nan, 122000]
        })
        
        fig = go.Figure()
        for col in ['Facebook Spend', 'Google Spend', 'TV Spend']:
            fig.add_trace(go.Bar(
                name=col,
                x=data_sources['Source'],
                y=data_sources[col],
                text=data_sources[col].apply(lambda x: f'${x/1000:.0f}K' if pd.notna(x) else 'Missing'),
                textposition='auto',
            ))
        
        fig.update_layout(
            title="Same Data, Different Numbers Across Sources",
            xaxis_title="Data Source",
            yaxis_title="Reported Spend ($)",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show discrepancy metrics
        st.markdown("### 🔍 Discrepancy Analysis")
        discrepancy_df = pd.DataFrame({
            'Channel': ['Facebook', 'Google', 'TV'],
            'Max-Min Difference': ['$10K (18%)', '$7K (9%)', '$5K (4%)'],
            'CV (Coefficient of Variation)': ['8.2%', '4.1%', '2.3%'],
            'Missing Data Points': ['0', '0', '1 (Agency)']
        })
        st.dataframe(discrepancy_df, use_container_width=True)
    
    with col2:
        st.subheader("🛠️ Technical Solutions")
        
        st.markdown("""
        **1. Data Validation Pipeline**
        ```python
        # Automated validation checks
        def validate_data(df):
            checks = {
                'duplicates': df.duplicated().sum(),
                'missing': df.isnull().sum(),
                'outliers': detect_outliers(df),
                'date_gaps': find_date_gaps(df),
                'negative_values': (df < 0).sum()
            }
            return checks
        ```
        """)
        
        st.markdown("""
        **2. Statistical Reconciliation Methods:**
        - **Dempster-Shafer Theory**: Combine evidence from multiple sources
        - **Kalman Filtering**: Optimal estimation from noisy sources
        - **Robust PCA**: Identify and correct systematic biases
        """)
        
        st.markdown("""
        **3. Source Priority Matrix:**
        | Priority | Source Type | Use Case |
        |----------|------------|----------|
        | 1 | Platform APIs | Ground truth |
        | 2 | Data Warehouse | Consolidated |
        | 3 | Finance Systems | Invoice-based |
        | 4 | Agency Reports | Reference only |
        """)
        
        st.info("""
        **📈 Best Practice Algorithm:**
        1. Extract from all sources
        2. Calculate correlation matrix between sources
        3. If correlation > 0.95: Use primary source
        4. If correlation < 0.95: Investigate discrepancy
        5. Apply weighted average based on source reliability
        """)

# Tab 2: External Factor Omission
with tab2:
    st.header("External Factor Omission (Confounders)")
    st.markdown("**Category:** Easy to Grasp | **Impact:** High | **Frequency:** Common")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📉 Impact of Omitted Variables")
        
        # Simulate data with and without external factors
        np.random.seed(42)
        weeks = pd.date_range('2020-01-01', periods=104, freq='W')
        
        # Generate synthetic data
        base_sales = 1000000
        marketing_effect = np.sin(np.arange(104) * 0.1) * 50000 + np.random.normal(0, 10000, 104)
        covid_effect = np.concatenate([np.zeros(10), 
                                      -np.ones(20) * 300000,
                                      np.linspace(-300000, 0, 74)])
        competitor_effect = np.where((np.arange(104) > 30) & (np.arange(104) < 60), -100000, 0)
        economy_effect = np.linspace(0, -50000, 104)
        
        true_sales = base_sales + marketing_effect + covid_effect + competitor_effect + economy_effect
        
        # Create plot
        fig = make_subplots(rows=2, cols=1, 
                           subplot_titles=("Sales Decomposition with External Factors",
                                         "Model Performance: With vs Without External Factors"))
        
        # Top plot - decomposition
        fig.add_trace(go.Scatter(x=weeks, y=true_sales, name='Actual Sales', 
                                line=dict(color='black', width=3)), row=1, col=1)
        fig.add_trace(go.Scatter(x=weeks, y=base_sales + marketing_effect, 
                                name='Marketing Only Model', 
                                line=dict(color='blue', dash='dash')), row=1, col=1)
        
        # Bottom plot - residuals
        residuals_without = true_sales - (base_sales + marketing_effect)
        residuals_with = np.random.normal(0, 20000, 104)  # Simulated good fit
        
        fig.add_trace(go.Scatter(x=weeks, y=residuals_without, 
                                name='Residuals (No External Factors)', 
                                line=dict(color='red')), row=2, col=1)
        fig.add_trace(go.Scatter(x=weeks, y=residuals_with, 
                                name='Residuals (With External Factors)', 
                                line=dict(color='green')), row=2, col=1)
        
        fig.update_layout(height=600, showlegend=True)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Sales ($)", row=1, col=1)
        fig.update_yaxes(title_text="Residuals ($)", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show bias metrics
        st.markdown("### 📊 Omitted Variable Bias")
        bias_df = pd.DataFrame({
            'Metric': ['Marketing ROI (True)', 'Marketing ROI (Biased)', 'Bias', 'MAPE'],
            'Without External': ['2.5x', '0.8x', '-68%', '24.3%'],
            'With External': ['2.5x', '2.4x', '-4%', '3.2%']
        })
        st.dataframe(bias_df, use_container_width=True)
    
    with col2:
        st.subheader("🔬 Technical Detection & Solutions")
        
        st.markdown("""
        **1. Ramsey RESET Test for Omitted Variables**
        ```python
        from statsmodels.stats.diagnostic import linear_reset
        
        # Test for omitted variables
        reset_test = linear_reset(model, power=3)
        p_value = reset_test.pvalue
        
        if p_value < 0.05:
            print("Evidence of omitted variables")
        ```
        """)
        
        st.markdown("""
        **2. External Factors to Include:**
        
        | Factor | Data Source | Transformation |
        |--------|-------------|----------------|
        | COVID-19 | Google Mobility | Log transform |
        | Competition | SEMrush/Similar | Market share % |
        | Economy | FRED API | First difference |
        | Weather | NOAA API | Rolling average |
        | Seasonality | Prophet | Fourier terms |
        | Holidays | Custom calendar | Binary dummies |
        """)
        
        st.markdown("""
        **3. Causal Inference Methods:**
        - **Instrumental Variables (IV)**: 2SLS estimation
        - **Regression Discontinuity**: Sharp cutoff events
        - **Synthetic Control**: Create counterfactual
        - **Double ML**: Machine learning + causality
        """)
        
        st.success("""
        **🎯 Implementation Framework:**
        1. List all potential confounders (brainstorm)
        2. Test correlation with sales & marketing
        3. Apply Granger causality tests
        4. Include if p-value < 0.10
        5. Use LASSO for feature selection
        """)

# Tab 3: Multicollinearity
with tab3:
    st.header("Multicollinearity")
    st.markdown("**Category:** Tricky | **Impact:** Very High | **Frequency:** Very Common")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔗 The Problem: Correlated Channels")
        
        # Generate correlated data
        np.random.seed(42)
        n_weeks = 52
        tv_spend = np.random.normal(100, 20, n_weeks)
        radio_spend = 0.9 * tv_spend + np.random.normal(0, 5, n_weeks)  # High correlation
        digital_spend = np.random.normal(50, 15, n_weeks)  # Independent
        
        # Create correlation matrix
        corr_matrix = np.corrcoef([tv_spend, radio_spend, digital_spend])
        
        # Heatmap
        fig1 = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=['TV', 'Radio', 'Digital'],
            y=['TV', 'Radio', 'Digital'],
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix, 2),
            texttemplate='%{text}',
            textfont={"size": 14},
            colorbar=dict(title="Correlation")
        ))
        fig1.update_layout(title="Channel Correlation Matrix", height=400)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Time series plot
        weeks = list(range(1, n_weeks + 1))
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=weeks, y=tv_spend, name='TV', line=dict(width=3)))
        fig2.add_trace(go.Scatter(x=weeks, y=radio_spend, name='Radio', 
                                 line=dict(width=3, dash='dash')))
        fig2.add_trace(go.Scatter(x=weeks, y=digital_spend, name='Digital', 
                                 line=dict(width=2)))
        fig2.update_layout(
            title="TV and Radio Move Together (r=0.92)",
            xaxis_title="Week",
            yaxis_title="Spend ($K)",
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # VIF Calculation
        st.markdown("### 📈 Variance Inflation Factor (VIF)")
        vif_df = pd.DataFrame({
            'Channel': ['TV', 'Radio', 'Digital'],
            'VIF Score': [12.5, 11.8, 1.3],
            'Interpretation': ['🔴 Severe', '🔴 Severe', '🟢 No issue']
        })
        st.dataframe(vif_df, use_container_width=True)
        
        st.warning("""
        **Impact of Multicollinearity:**
        - TV coefficient: 5.2 (inflated)
        - Radio coefficient: -1.3 (wrong sign!)
        - Standard errors: 3x larger
        - Confidence intervals: Unreliable
        """)
    
    with col2:
        st.subheader("🛠️ Advanced Solutions")
        
        st.markdown("""
        **1. Detection Methods:**
        ```python
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        
        # Calculate VIF
        def calculate_vif(df):
            vif = pd.DataFrame()
    vif["Variable"] = df.columns
    vif["VIF"] = [variance_inflation_factor(df.values, i) 
                  for i in range(df.shape[1])]
    return vif
        
        # Condition Number
        condition_number = np.linalg.cond(X)
        # > 30 indicates multicollinearity
        ```
        """)
        
        tab_sol1, tab_sol2, tab_sol3 = st.tabs(["Ridge/LASSO", "PCA", "Other Methods"])
        
        with tab_sol1:
            st.markdown("""
            **Ridge Regression (L2 Regularization)**
            ```python
            from sklearn.linear_model import RidgeCV
            
            alphas = np.logspace(-6, 6, 13)
            ridge = RidgeCV(alphas=alphas, cv=5)
            ridge.fit(X, y)
            
            # Optimal alpha: 0.1
            # Reduces coefficient variance
            ```
            
            **LASSO (L1 Regularization)**
            ```python
            from sklearn.linear_model import LassoCV
            
            lasso = LassoCV(cv=5, random_state=42)
            lasso.fit(X, y)
            
            # Can set coefficients to zero
            # Automatic feature selection
            ```
            """)
        
        with tab_sol2:
            st.markdown("""
            **Principal Component Analysis**
            ```python
            from sklearn.decomposition import PCA
            
            pca = PCA(n_components=0.95)  # Keep 95% variance
            X_pca = pca.fit_transform(X)
            
            # Transform back for interpretation
            coefficients = pca.inverse_transform(
                model.coef_
            )
            ```
            
            **Partial Least Squares**
            ```python
            from sklearn.cross_decomposition import PLSRegression
            
            pls = PLSRegression(n_components=2)
            pls.fit(X, y)
            ```
            """)
        
        with tab_sol3:
            st.markdown("""
            **Other Advanced Methods:**
            
            1. **Elastic Net** (Ridge + LASSO)
            2. **Orthogonalization** (Gram-Schmidt)
            3. **Variable Clustering** (merge similar)
            4. **Instrumental Variables** (2SLS)
            5. **Bayesian Priors** (informative priors)
            6. **Time-varying Parameters** (DLM)
            """)
        
        st.info("""
        **📊 Recommended Approach:**
        1. Check VIF for all variables (threshold: 10)
        2. Check condition number (threshold: 30)
        3. If high: Try Ridge with CV for alpha
        4. Compare OLS vs Ridge coefficients
        5. Validate with holdout test
        """)

# Tab 4: Attribution Windows
with tab4:
    st.header("Attribution Windows (Adstock)")
    st.markdown("**Category:** Tricky | **Impact:** High | **Frequency:** Very Common")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⏱️ The Problem: How Long Do Effects Last?")
        
        # Adstock decay visualization
        weeks = np.arange(0, 13)
        
        # Different decay rates
        decay_fast = 0.1  # Digital
        decay_medium = 0.5  # Social
        decay_slow = 0.8  # TV
        
        adstock_fast = 100 * (decay_fast ** weeks)
        adstock_medium = 100 * (decay_medium ** weeks)
        adstock_slow = 100 * (decay_slow ** weeks)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weeks, y=adstock_slow, name=f'TV (λ={decay_slow})',
                                line=dict(width=3), fill='tonexty'))
        fig.add_trace(go.Scatter(x=weeks, y=adstock_medium, name=f'Social (λ={decay_medium})',
                                line=dict(width=3), fill='tonexty'))
        fig.add_trace(go.Scatter(x=weeks, y=adstock_fast, name=f'Search (λ={decay_fast})',
                                line=dict(width=3), fill='tonexty'))
        
        fig.update_layout(
            title="Adstock Decay Patterns by Channel",
            xaxis_title="Weeks After Campaign",
            yaxis_title="Remaining Effect (%)",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ROI by window length
        st.markdown("### 📊 ROI Changes with Attribution Window")
        
        window_lengths = [1, 2, 4, 8, 13, 26]
        roi_values = [1.2, 1.8, 2.8, 3.5, 3.8, 3.9]
        cumulative_capture = [30, 50, 70, 85, 95, 99]
        
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig2.add_trace(
            go.Bar(x=window_lengths, y=roi_values, name="ROI",
                  marker_color='lightblue'),
            secondary_y=False,
        )
        
        fig2.add_trace(
            go.Scatter(x=window_lengths, y=cumulative_capture, name="% Effect Captured",
                      line=dict(color='red', width=3)),
            secondary_y=True,
        )
        
        fig2.update_xaxes(title_text="Attribution Window (Weeks)")
        fig2.update_yaxes(title_text="ROI (x)", secondary_y=False)
        fig2.update_yaxes(title_text="Effect Captured (%)", secondary_y=True)
        fig2.update_layout(title="Same Campaign, Different ROI", height=400)
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Comparison table
        comparison_df = pd.DataFrame({
            'Window': ['2 weeks', '8 weeks', '13 weeks'],
            'Revenue Attributed': ['$200K', '$450K', '$480K'],
            'ROI': ['2.0x', '4.5x', '4.8x'],
            'Decision': ['Stop campaign', 'Scale up', 'Optimize']
        })
        st.dataframe(comparison_df, use_container_width=True)
    
    with col2:
        st.subheader("🔬 Technical Solutions")
        
        st.markdown("""
        **1. Adstock Transformations:**
        """)
        
        tab_geo, tab_weibull, tab_delayed = st.tabs(["Geometric", "Weibull", "Delayed"])
        
        with tab_geo:
            st.markdown("""
            **Geometric Adstock** (Most Common)
            ```python
            def geometric_adstock(x, theta):
                x_adstocked = np.zeros_like(x)
                x_adstocked[0] = x[0]
                for i in range(1, len(x)):
                    x_adstocked[i] = x[i] + theta * x_adstocked[i-1]
                return x_adstocked
            
            # Theta (decay rate): 0-1
            # Half-life = -ln(2) / ln(theta)
            ```
            
            **Parameters:**
            - TV: θ = 0.4-0.7
            - Radio: θ = 0.3-0.6  
            - Digital: θ = 0.0-0.3
            - OOH: θ = 0.2-0.5
            """)
        
        with tab_weibull:
            st.markdown("""
            **Weibull Adstock** (Flexible Shape)
            ```python
            def weibull_adstock(x, shape, scale):
                n = len(x)
                convolve_window = np.arange(n)
                convolve_window = (shape/scale) * (convolve_window/scale)**(shape-1) * 
                                 np.exp(-(convolve_window/scale)**shape)
                convolve_window = convolve_window / convolve_window.sum()
                return np.convolve(x, convolve_window)[:n]
            
            # Shape < 1: L-shaped decay
            # Shape > 1: Peak then decay
            ```
            """)
        
        with tab_delayed:
            st.markdown("""
            **Delayed Adstock** (Peak Delay)
            ```python
            def delayed_adstock(x, theta, delay):
                x_delayed = np.zeros_like(x)
                x_delayed[delay:] = x[:-delay]
                return geometric_adstock(x_delayed, theta)
            
            # Delay: 1-3 weeks typical
            # Good for: TV, OOH
            ```
            """)
        
        st.markdown("""
        **2. Selection Methods:**
        
        | Method | Description | Pros | Cons |
        |--------|-------------|------|------|
        | Grid Search | Test multiple θ values | Simple | Computationally expensive |
        | AIC/BIC | Information criteria | Balances fit & complexity | May overfit |
        | Cross-validation | Out-of-sample testing | Robust | Requires lots of data |
        | Business knowledge | Use campaign duration | Practical | May be biased |
        | Experiments | Measure actual decay | Ground truth | Expensive |
        """)
        
        st.success("""
        **🎯 Best Practice:**
        1. Start with industry benchmarks
        2. Grid search θ from 0.0 to 0.9 (step 0.1)
        3. Compare AIC/BIC across models
        4. Validate with holdout period
        5. Sanity check with business knowledge
        """)

# Tab 5: Saturation Misspecification
with tab5:
    st.header("Saturation Misspecification")
    st.markdown("**Category:** Tricky | **Impact:** Very High | **Frequency:** Common")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📈 The Problem: Wrong Curve Shape")
        
        # Generate different saturation curves
        spend = np.linspace(0, 3000, 100)
        
        # Hill transformation (S-curve)
        def hill_transform(x, alpha, gamma):
            return alpha * (x**gamma) / (1 + x**gamma)
        
        # Adbudg transformation
        def adbudg_transform(x, alpha, gamma):
            return alpha * (1 - np.exp(-gamma * x))
        
        # Wrong curve (too early saturation)
        wrong_curve = hill_transform(spend/500, 100, 0.8)
        
        # Correct curve
        correct_curve = hill_transform(spend/2000, 100, 1.5)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=spend, y=wrong_curve, 
                                name='Wrong Model (Saturates at $500K)',
                                line=dict(color='red', width=3, dash='dash')))
        fig.add_trace(go.Scatter(x=spend, y=correct_curve, 
                                name='Reality (Saturates at $2M)',
                                line=dict(color='green', width=3)))
        
        # Add current spend marker
        fig.add_trace(go.Scatter(x=[500], y=[65], 
                                mode='markers',
                                name='Current Spend',
                                marker=dict(size=15, color='blue', symbol='star')))
        
        fig.update_layout(
            title="Saturation Misspecification: Missing Growth Opportunity",
            xaxis_title="Monthly Spend ($K)",
            yaxis_title="Response (%)",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ROI at different spend levels
        st.markdown("### 💰 Business Impact")
        
        impact_df = pd.DataFrame({
            'Spend Level': ['$500K', '$1M', '$2M'],
            'Wrong Model ROI': ['1.3x', '1.1x', '1.0x'],
            'Correct Model ROI': ['2.5x', '2.2x', '1.8x'],
            'Decision (Wrong)': ['Stop here', 'Cut budget', 'Way too much'],
            'Decision (Correct)': ['Keep going', 'Optimal', 'Near max']
        })
        st.dataframe(impact_df, use_container_width=True)
        
        st.error("""
        **Cost of Wrong Saturation:**
        - Lost Revenue: $1.5M/year
        - Missed Growth: 10x opportunity
        - Market Share Loss: -8%
        """)
    
    with col2:
        st.subheader("🔬 Saturation Functions")
        
        tab_hill, tab_adbudg, tab_michaelis = st.tabs(["Hill", "Adbudg", "Michaelis-Menten"])
        
        with tab_hill:
            st.markdown("""
            **Hill Saturation (S-Curve)**
            ```python
            def hill_saturation(x, alpha, gamma):
                # alpha: maximum effect
                # gamma: shape parameter
                return alpha * (x**gamma) / (1 + x**gamma)
            
            # gamma < 1: Concave (diminishing returns)
            # gamma = 1: Michaelis-Menten
            # gamma > 1: S-shaped (slow start)
            ```
            
            **When to use:**
            - TV, Radio, OOH (brand building)
            - Channels with threshold effects
            - Long purchase cycles
            """)
        
        with tab_adbudg:
            st.markdown("""
            **Adbudg Saturation**
            ```python
            def adbudg_saturation(x, alpha, gamma):
                # alpha: maximum effect
                # gamma: rate of saturation
                return alpha * (1 - np.exp(-gamma * x))
            
            # Higher gamma = faster saturation
            ```
            
            **When to use:**
            - Digital channels
            - Direct response
            - Quick saturation expected
            """)
        
        with tab_michaelis:
            st.markdown("""
            **Michaelis-Menten**
            ```python
            def michaelis_menten(x, vmax, km):
                # vmax: maximum response
                # km: half-saturation constant
                return (vmax * x) / (km + x)
            
            # km = spend at 50% of max effect
            ```
            
            **When to use:**
            - Simple, interpretable
            - One parameter for saturation point
            - Good default choice
            """)
        
        st.markdown("""
        **3. Model Selection Framework:**
        
        ```python
        from scipy.optimize import curve_fit
        import numpy as np
        
        # Test multiple saturations
        saturations = {
            'linear': lambda x, a: a * x,
            'sqrt': lambda x, a: a * np.sqrt(x),
            'log': lambda x, a: a * np.log1p(x),
            'hill': lambda x, a, g: hill_saturation(x, a, g),
            'adbudg': lambda x, a, g: adbudg_saturation(x, a, g)
        }
        
        # Fit each and compare AIC
        best_aic = np.inf
        best_model = None
        
        for name, func in saturations.items():
            params, _ = curve_fit(func, X, y)
            predictions = func(X, *params)
            aic = calculate_aic(y, predictions, len(params))
            
            if aic < best_aic:
                best_aic = aic
                best_model = name
        ```
        """)
        
        st.info("""
        **📊 Validation Checklist:**
        ✅ Compare saturation point to competitors
        ✅ Check marginal ROI at current spend (should be > 1)
        ✅ Validate with lift tests at 2x spend
        ✅ Industry benchmarks (TV: $1-3M, Digital: $200-500K)
        ✅ Business logic (can't exceed market size)
        """)

# Tab 6: Baseline Drift
with tab6:
    st.header("Baseline Drift")
    st.markdown("**Category:** Tricky | **Impact:** High | **Frequency:** Common")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 The Problem: Changing Baseline")
        
        # Generate data with baseline drift
        np.random.seed(42)
        weeks = pd.date_range('2023-01-01', periods=52, freq='W')
        
        # Components
        baseline_start = 100
        baseline_trend = np.linspace(100, 120, 52)  # 20% growth
        marketing_spend = np.ones(52) * 100  # Flat spend
        marketing_effect = marketing_spend * 0.5 + np.random.normal(0, 5, 52)
        total_sales = baseline_trend + marketing_effect
        
        # Create plot
        fig = go.Figure()
        
        # Add traces
        fig.add_trace(go.Scatter(x=weeks, y=total_sales, 
                                name='Total Sales', 
                                line=dict(color='black', width=3)))
        fig.add_trace(go.Scatter(x=weeks, y=baseline_trend, 
                                name='True Baseline (Hidden)', 
                                line=dict(color='green', width=2, dash='dash')))
        fig.add_trace(go.Scatter(x=weeks, y=marketing_spend, 
                                name='Marketing Spend (Flat)', 
                                line=dict(color='red', width=2),
                                yaxis='y2'))
        
        fig.update_layout(
            title="Sales Growing 20% While Marketing Flat - Who Gets Credit?",
            xaxis_title="Date",
            yaxis_title="Sales Index",
            yaxis2=dict(
                title="Marketing Spend Index",
                overlaying='y',
                side='right'
            ),
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Model comparison
        st.markdown("### 🔍 Model Comparison")
        
        model_comparison = pd.DataFrame({
            'Model': ['Without Trend', 'With Linear Trend', 'With Spline Trend'],
            'Marketing ROI': ['5.2x (inflated)', '2.5x (correct)', '2.4x (correct)'],
            'R²': [0.45, 0.89, 0.92],
            'MAPE': ['18.5%', '4.2%', '3.8%'],
            'Baseline Growth': ['Not captured', '1.5% monthly', 'Variable']
        })
        st.dataframe(model_comparison, use_container_width=True)
    
    with col2:
        st.subheader("🔬 Detection & Solutions")
        
        st.markdown("""
        **1. Statistical Tests for Drift:**
        """)
        
        tab_chow, tab_cusum, tab_kalman = st.tabs(["Chow Test", "CUSUM", "Kalman Filter"])
        
        with tab_chow:
            st.markdown("""
            **Chow Test for Structural Break**
            ```python
            from statsmodels.stats.diagnostic import breaks_cusumolsresid
            
            def chow_test(y, X, break_point):
                n = len(y)
                X1, y1 = X[:break_point], y[:break_point]
                X2, y2 = X[break_point:], y[break_point:]
                
                # Fit separate models
                RSS_pooled = OLS(y, X).fit().ssr
                RSS_1 = OLS(y1, X1).fit().ssr
                RSS_2 = OLS(y2, X2).fit().ssr
                
                # F-statistic
                k = X.shape[1]
                F = ((RSS_pooled - (RSS_1 + RSS_2)) / k) / 
                    ((RSS_1 + RSS_2) / (n - 2*k))
                
                p_value = 1 - stats.f.cdf(F, k, n-2*k)
                return F, p_value
            ```
            """)
        
        with tab_cusum:
            st.markdown("""
            **CUSUM Test**
            ```python
            def cusum_test(residuals):
                cusum = np.cumsum(residuals) / np.std(residuals)
                
                # Critical bounds (5% significance)
                n = len(residuals)
                bounds = 0.948 * np.sqrt(n) * np.array([1, -1])
                
                # Check if CUSUM exceeds bounds
                drift_detected = np.any(np.abs(cusum) > bounds[0])
                return cusum, bounds, drift_detected
            ```
            
            **Interpretation:**
            - Within bounds: No drift
            - Exceeds bounds: Parameter instability
            """)
        
        with tab_kalman:
            st.markdown("""
            **Kalman Filter (Time-Varying Parameters)**
            ```python
            from pykalman import KalmanFilter
            
            # State space model
            kf = KalmanFilter(
                transition_matrices=[[1, 1], [0, 1]],
                observation_matrices=[[1, 0]],
                initial_state_mean=[sales[0], 0],
                initial_state_covariance=np.eye(2),
                transition_covariance=0.01*np.eye(2),
                observation_covariance=1
            )
            
            # Estimate time-varying baseline
            state_means, _ = kf.filter(sales)
            baseline = state_means[:, 0]
            trend = state_means[:, 1]
            ```
            """)
        
        st.markdown("""
        **2. Trend Specifications:**
        
        | Type | Formula | Use Case |
        |------|---------|----------|
        | Linear | β₀ + β₁t | Steady growth |
        | Quadratic | β₀ + β₁t + β₂t² | Acceleration |
        | Log | β₀ + β₁ln(t) | Slowing growth |
        | Spline | Σβᵢ·basis_i(t) | Flexible |
        | Prophet | g(t) + s(t) + h(t) | Complex patterns |
        """)
        
        st.success("""
        **🎯 Implementation Steps:**
        1. Plot sales vs marketing over time
        2. Test for structural breaks (Chow test)
        3. Check residuals for trends (CUSUM)
        4. Add appropriate trend specification
        5. Compare models with/without trend (AIC)
        6. Validate on holdout period
        """)

# Add footer
st.markdown("---")
st.markdown("""
### 📚 Key Takeaways

| Pitfall | Detection | Primary Solution | Validation |
|---------|-----------|-----------------|------------|
| Data Quality | Compare sources | Use platform data | Correlation > 0.95 |
| External Factors | RESET test | Include confounders | Check residuals |
| Multicollinearity | VIF > 10 | Ridge regression | Cross-validation |
| Attribution Windows | Compare windows | Grid search decay | Business knowledge |
| Saturation | Compare curves | Test multiple forms | Competitor benchmarks |
| Baseline Drift | CUSUM test | Add trend terms | Holdout test |

**Remember:** These pitfalls often occur together. Always check for all six in your MMM projects!
""")