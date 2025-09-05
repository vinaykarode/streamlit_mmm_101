import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Multicollinearity in Marketing Mix Modeling",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #c9d3e3;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
    .plot-container {
        border: 2px solid #e6e9ef;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🎯 Multicollinearity in Marketing Mix Modeling")
st.markdown("### Understanding and Solving the Hidden Challenge in Marketing Analytics")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Choose a section:",
    ["📚 Introduction & Theory", 
     "📊 Generate Marketing Data",
     "🔍 Detect Multicollinearity", 
     "📈 Visualize the Problem",
     "🛠️ Compare Solutions",
     "🎮 Interactive Simulator",
     "💡 Real-World Examples"]
)

# Initialize session state for data persistence
if 'marketing_data' not in st.session_state:
    st.session_state.marketing_data = None
if 'vif_scores' not in st.session_state:
    st.session_state.vif_scores = None

# Section 1: Introduction & Theory
if section == "📚 Introduction & Theory":
    st.header("What is Multicollinearity?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Multicollinearity** occurs when independent variables in your marketing mix model are highly correlated 
        with each other. This creates several problems:
        
        1. **Attribution Confusion**: Can't determine which channel drives sales
        2. **Unstable Coefficients**: Small data changes cause large coefficient swings  
        3. **Inflated Standard Errors**: Reduced statistical significance
        4. **Unreliable Predictions**: Model becomes sensitive to minor variations
        """)
        
        st.info("""
        **🌧️ Real-World Analogy**: It's like trying to determine if umbrella sales or raincoat sales 
        are causing people to stay dry during rain - both increase together, making individual 
        contribution impossible to isolate!
        """)
    
    with col2:
        st.markdown("### Key Metrics")
        st.metric("Dangerous Correlation", "> 0.8", "High Risk")
        st.metric("VIF Threshold", "> 5", "Action Needed")
        st.metric("Critical VIF", "> 10", "Must Fix")
    
    st.markdown("---")
    
    # Common scenarios
    st.subheader("Common Multicollinearity Scenarios in Marketing")
    
    scenarios_df = pd.DataFrame({
        'Scenario': ['Holiday Season', 'Product Launch', 'Brand Campaign', 'Competitive Response'],
        'Correlated Channels': [
            'TV, Digital, Email, Social - all increase together',
            'PR, Social, Paid Search - simultaneous activation',
            'TV, Radio, OOH - traditional media bundle',
            'Price Promotion, Display Ads - defensive spending'
        ],
        'Correlation': [0.92, 0.88, 0.85, 0.90],
        'Business Impact': [
            'Cannot separate channel contributions',
            'PR impact absorbed by paid channels',
            'TV gets all credit, Radio shows negative',
            'Promotion ROI appears inflated'
        ]
    })
    
    st.dataframe(scenarios_df, use_container_width=True)

# Section 2: Generate Marketing Data
elif section == "📊 Generate Marketing Data":
    st.header("Generate Realistic Marketing Mix Data")
    
    # Add introductory explanation
    st.markdown("""
    ### 🎯 What This Tool Does
    This simulator creates **synthetic marketing data** that mimics real-world scenarios where multiple marketing 
    channels (TV, Digital, Social, etc.) are running simultaneously. The tool helps you understand how 
    **multicollinearity** - when marketing channels move together - affects your ability to measure their individual impact.
    
    ### 💡 Why This Matters
    In real marketing campaigns, channels often increase or decrease together (e.g., during holiday sales or product launches).
    This makes it statistically difficult to determine which channel is actually driving sales - a critical problem for 
    marketing budget optimization.
    """)
    
    st.divider()
    
    st.subheader("📊 Configure Your Marketing Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📅 Time Period & Baseline**")
        n_weeks = st.slider(
            "Number of Weeks", 
            52, 208, 104,
            help="🔍 Duration of your marketing campaign. 104 weeks = 2 years of data, typical for MMM analysis."
        )
        base_sales = st.slider(
            "Base Sales (000s)", 
            100, 1000, 500,
            help="🔍 Your baseline sales without any marketing (in thousands). This represents organic demand."
        )
        
    with col2:
        st.markdown("**🔗 Channel Relationships**")
        correlation_level = st.select_slider(
            "Correlation Scenario",
            options=["Low (Ideal)", "Medium", "High (Problem)", "Extreme (Critical)"],
            value="High (Problem)",
            help="""🔍 How closely your marketing channels move together:
            • **Low (Ideal)**: Channels vary independently - easy to measure impact
            • **Medium**: Some channels move together occasionally  
            • **High (Problem)**: Most channels increase/decrease together
            • **Extreme (Critical)**: Nearly impossible to separate channel effects"""
        )
        noise_level = st.slider(
            "Market Noise %", 
            5, 30, 15,
            help="🔍 Random variations in sales from external factors (competitor actions, weather, news events, etc.)"
        )
    
    with col3:
        st.markdown("**📈 Realistic Patterns**")
        seasonality = st.checkbox(
            "Add Seasonality", 
            value=True,
            help="🔍 Adds yearly patterns like summer slumps or holiday peaks"
        )
        trend = st.checkbox(
            "Add Growth Trend", 
            value=True,
            help="🔍 Simulates business growth over time"
        )
        outliers = st.checkbox(
            "Add Outlier Events", 
            value=True,
            help="🔍 Includes special events like Black Friday where all channels spike together"
        )
    
    if st.button("🎲 Generate Marketing Data", type="primary"):
        np.random.seed(42)
        
        # Define correlation matrices for different scenarios
        corr_matrices = {
            "Low (Ideal)": np.array([
                [1.0, 0.3, 0.2, 0.1, 0.15, 0.25],
                [0.3, 1.0, 0.25, 0.2, 0.1, 0.2],
                [0.2, 0.25, 1.0, 0.15, 0.3, 0.1],
                [0.1, 0.2, 0.15, 1.0, 0.35, 0.2],
                [0.15, 0.1, 0.3, 0.35, 1.0, 0.25],
                [0.25, 0.2, 0.1, 0.2, 0.25, 1.0]
            ]),
            "Medium": np.array([
                [1.0, 0.6, 0.5, 0.3, 0.4, 0.45],
                [0.6, 1.0, 0.55, 0.4, 0.35, 0.5],
                [0.5, 0.55, 1.0, 0.45, 0.6, 0.4],
                [0.3, 0.4, 0.45, 1.0, 0.65, 0.5],
                [0.4, 0.35, 0.6, 0.65, 1.0, 0.55],
                [0.45, 0.5, 0.4, 0.5, 0.55, 1.0]
            ]),
            "High (Problem)": np.array([
                [1.0, 0.85, 0.75, 0.6, 0.7, 0.65],
                [0.85, 1.0, 0.8, 0.65, 0.6, 0.7],
                [0.75, 0.8, 1.0, 0.7, 0.85, 0.65],
                [0.6, 0.65, 0.7, 1.0, 0.82, 0.75],
                [0.7, 0.6, 0.85, 0.82, 1.0, 0.8],
                [0.65, 0.7, 0.65, 0.75, 0.8, 1.0]
            ]),
            "Extreme (Critical)": np.array([
                [1.0, 0.95, 0.92, 0.88, 0.9, 0.85],
                [0.95, 1.0, 0.94, 0.89, 0.87, 0.9],
                [0.92, 0.94, 1.0, 0.91, 0.95, 0.88],
                [0.88, 0.89, 0.91, 1.0, 0.93, 0.92],
                [0.9, 0.87, 0.95, 0.93, 1.0, 0.94],
                [0.85, 0.9, 0.88, 0.92, 0.94, 1.0]
            ])
        }
        
        # Generate correlated marketing spend data
        mean = [50, 40, 30, 25, 20, 15]  # Average spend levels
        cov = corr_matrices[correlation_level] * 200  # Scale by variance
        
        channels = ['TV', 'Digital', 'Social', 'Search', 'Email', 'Radio']
        spend_data = np.random.multivariate_normal(mean, cov, n_weeks)
        spend_data = np.maximum(spend_data, 0)  # Ensure non-negative
        
        # Create DataFrame
        dates = pd.date_range(start='2022-01-01', periods=n_weeks, freq='W')
        df = pd.DataFrame(spend_data, columns=channels, index=dates)
        
        # Add realistic patterns
        if seasonality:
            seasonal_pattern = 1 + 0.3 * np.sin(2 * np.pi * np.arange(n_weeks) / 52)
            for col in channels:
                df[col] *= seasonal_pattern
        
        if trend:
            growth = 1 + 0.002 * np.arange(n_weeks)
            for col in channels:
                df[col] *= growth
        
        # Generate sales with realistic channel contributions
        true_coefficients = {
            'TV': 2.5, 'Digital': 3.2, 'Social': 2.8, 
            'Search': 4.1, 'Email': 1.5, 'Radio': 1.8
        }
        
        df['Sales'] = base_sales
        for channel in channels:
            df['Sales'] += df[channel] * true_coefficients[channel]
        
        # Add noise
        df['Sales'] += np.random.normal(0, base_sales * noise_level/100, n_weeks)
        
        if outliers:
            # Add Black Friday/Cyber Monday effect
            black_friday_weeks = [46, 98, 150]  # Approximate weeks
            for week in black_friday_weeks:
                if week < n_weeks:
                    df.iloc[week] *= 2.5
        
        # Round for realism
        for col in channels:
            df[col] = df[col].round(2)
        df['Sales'] = df['Sales'].round(0)
        
        st.session_state.marketing_data = df
        st.success(f"✅ Generated {n_weeks} weeks of marketing data with {correlation_level} correlation")
    
    # Display data if available
    if st.session_state.marketing_data is not None:
        st.divider()
        st.subheader("📊 Your Generated Marketing Data")
        
        # Add explanation of what user is seeing
        st.info("""
        **📖 How to Read This Data:**
        - **Time Series Tab**: Shows how each marketing channel's spend varies over time
        - **Statistics Tab**: Key metrics showing the relationships between channels
        - **Raw Data Tab**: The actual numbers you can download and analyze
        
        **🔍 What to Look For:**
        - In high correlation scenarios, notice how channels tend to peak and dip together
        - Check the Statistics tab to see correlation values between channels
        - Values > 0.7 indicate strong correlation (problematic for analysis)
        """)
        
        tab1, tab2, tab3 = st.tabs(["📈 Time Series", "📊 Statistics", "📋 Raw Data"])
        
        with tab1:
            # Time series plot
            fig = go.Figure()
            for col in st.session_state.marketing_data.columns:
                if col != 'Sales':
                    fig.add_trace(go.Scatter(
                        x=st.session_state.marketing_data.index,
                        y=st.session_state.marketing_data[col],
                        name=col,
                        mode='lines'
                    ))
            
            fig.update_layout(
                title="Marketing Spend Over Time",
                xaxis_title="Date",
                yaxis_title="Spend ($000s)",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("### 📊 Summary Statistics")
            st.markdown("""
            **Understanding These Metrics:**
            - **mean**: Average spend for each channel
            - **std**: Variation in spend (higher = more variable spending)
            - **min/max**: Lowest and highest spend levels
            - **quartiles (25%, 50%, 75%)**: Distribution of spending levels
            """)
            st.dataframe(st.session_state.marketing_data.describe(), use_container_width=True)
            
            # Add correlation matrix
            channels = [col for col in st.session_state.marketing_data.columns if col != 'Sales']
            corr_matrix = st.session_state.marketing_data[channels].corr()
            
            st.markdown("### 🔗 Channel Correlation Matrix")
            st.markdown("""
            **How to Interpret:**
            - Values range from -1 to 1
            - **0.0 - 0.3**: Low correlation ✅ (channels are independent)
            - **0.3 - 0.7**: Moderate correlation ⚠️ (some relationship)
            - **0.7 - 1.0**: High correlation 🔴 (channels move together - problematic!)
            """)
            
            # Create correlation heatmap
            fig = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdYlGn_r',
                title="Channel Correlation Heatmap"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("### 📋 Raw Data Sample")
            st.markdown("""
            **💡 Pro Tip:** Look for patterns where multiple channels increase or decrease together.
            This is the multicollinearity problem we're trying to detect and solve!
            """)
            st.write("**First 10 Weeks of Data**")
            st.dataframe(st.session_state.marketing_data.head(10), use_container_width=True)
            
            # Add download button
            csv = st.session_state.marketing_data.to_csv()
            st.download_button(
                label="📥 Download Full Dataset as CSV",
                data=csv,
                file_name="marketing_data_multicollinearity.csv",
                mime="text/csv"
            )

# Section 3: Detect Multicollinearity
elif section == "🔍 Detect Multicollinearity":
    st.header("Detect Multicollinearity in Your Data")
    
    # Add comprehensive introduction
    st.markdown("""
    ### 🎯 What is Multicollinearity Detection?
    
    Multicollinearity occurs when your marketing channels are **highly correlated** - they increase and decrease together.
    This makes it nearly impossible to determine which channel is actually driving sales.
    
    ### 🔍 Two Key Detection Methods:
    
    1. **Correlation Analysis** - Measures how closely two channels move together (pairwise relationships)
    2. **VIF (Variance Inflation Factor)** - Measures how much a channel's variance is inflated by all other channels combined
    
    ### 📊 Why Both Methods?
    - **Correlation** shows simple two-channel relationships (easy to understand)
    - **VIF** reveals complex multi-channel interactions (more comprehensive)
    - A channel might have moderate correlations but still have high VIF due to combined effects
    """)
    
    st.divider()
    
    if st.session_state.marketing_data is None:
        st.warning("⚠️ Please generate marketing data first in the 'Generate Marketing Data' section")
    else:
        df = st.session_state.marketing_data
        channels = [col for col in df.columns if col != 'Sales']
        
        # Calculate correlation matrix
        corr_matrix = df[channels].corr()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Correlation Heatmap")
            
            st.markdown("""
            **How to Read This Heatmap:**
            - **Diagonal (1.00)**: A channel's correlation with itself
            - **Green values (< 0.7)**: ✅ Good - channels are independent
            - **Yellow values (0.7-0.8)**: ⚠️ Warning - moderate correlation
            - **Red values (> 0.8)**: 🔴 Problem - high correlation
            
            **What to Look For:**
            - Many red/orange squares = multicollinearity problem
            - Mostly green = your channels vary independently
            """)
            fig = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdYlGn_r',
                aspect="auto",
                title="Channel Correlation Matrix"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Identify problematic pairs
            st.divider()
            st.subheader("⚠️ Problematic Correlations (> 0.8)")
            st.markdown("""
            **Why This Matters:**
            Channel pairs with correlation > 0.8 are nearly impossible to separate statistically.
            The model can't tell which channel deserves credit for sales.
            """)
            problem_pairs = []
            for i in range(len(channels)):
                for j in range(i+1, len(channels)):
                    if abs(corr_matrix.iloc[i, j]) > 0.8:
                        problem_pairs.append({
                            'Channel 1': channels[i],
                            'Channel 2': channels[j],
                            'Correlation': f"{corr_matrix.iloc[i, j]:.3f}"
                        })
            
            if problem_pairs:
                problem_df = pd.DataFrame(problem_pairs)
                st.dataframe(problem_df, use_container_width=True)
                st.warning(f"⚠️ Found {len(problem_pairs)} problematic channel pair(s) that need attention!")
            else:
                st.success("✅ No problematic correlations found! Your channels are sufficiently independent.")
        
        with col2:
            st.subheader("📈 VIF Analysis")
            
            st.markdown("""
            **Understanding VIF (Variance Inflation Factor):**
            
            VIF measures how much the variance of a channel's coefficient is inflated due to correlations with other channels.
            
            **Interpretation Guide:**
            - **VIF = 1**: No correlation with other channels (perfect)
            - **VIF < 5**: 🟢 Low multicollinearity (acceptable)
            - **VIF 5-10**: 🟡 Moderate multicollinearity (concerning)
            - **VIF > 10**: 🔴 High multicollinearity (problematic)
            - **VIF > 20**: 🚨 Severe multicollinearity (critical)
            
            **Rule of Thumb:** If VIF > 10, the channel's coefficient is unreliable!
            """)
            
            # Calculate VIF
            X = df[channels].values
            vif_data = []
            for i in range(X.shape[1]):
                vif_value = variance_inflation_factor(X, i)
                vif_data.append({
                    'Channel': channels[i],
                    'VIF': vif_value,
                    'Status': '🟢 Good' if vif_value < 5 else '🟡 Warning' if vif_value < 10 else '🔴 Critical'
                })
            
            vif_df = pd.DataFrame(vif_data)
            st.session_state.vif_scores = vif_df
            
            # VIF bar chart
            fig = go.Figure()
            colors = ['green' if v < 5 else 'orange' if v < 10 else 'red' for v in vif_df['VIF']]
            
            fig.add_trace(go.Bar(
                x=vif_df['Channel'],
                y=vif_df['VIF'],
                marker_color=colors,
                text=vif_df['VIF'].round(2),
                textposition='outside'
            ))
            
            # Add threshold lines
            fig.add_hline(y=5, line_dash="dash", line_color="orange", 
                         annotation_text="Warning Threshold (VIF=5)")
            fig.add_hline(y=10, line_dash="dash", line_color="red", 
                         annotation_text="Critical Threshold (VIF=10)")
            
            fig.update_layout(
                title="Variance Inflation Factor by Channel",
                xaxis_title="Marketing Channel",
                yaxis_title="VIF Score",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # VIF interpretation
            st.divider()
            st.subheader("📋 VIF Detailed Results")
            st.markdown("""
            **How to Read This Table:**
            - Channels are sorted by VIF score (worst first)
            - Status column shows severity at a glance
            - Higher VIF = less reliable marketing attribution
            """)
            # Sort by VIF for better visibility
            vif_df_sorted = vif_df.sort_values('VIF', ascending=False)
            st.dataframe(vif_df_sorted, use_container_width=True)
            
            # Summary metrics with better explanations
            st.divider()
            st.subheader("📊 Summary Metrics")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                max_vif = vif_df['VIF'].max()
                st.metric(
                    "Max VIF", 
                    f"{max_vif:.2f}",
                    help="Highest VIF score across all channels. Values > 10 indicate serious issues."
                )
                if max_vif > 20:
                    st.error("🚨 Severe multicollinearity detected!")
                elif max_vif > 10:
                    st.warning("⚠️ High multicollinearity detected!")
                elif max_vif > 5:
                    st.info("ℹ️ Moderate multicollinearity detected")
                else:
                    st.success("✅ Low multicollinearity - good!")
            
            with col2:
                channels_warning = (vif_df['VIF'] > 5).sum()
                st.metric(
                    "Channels > VIF 5", 
                    f"{channels_warning}",
                    help="Number of channels with concerning VIF scores"
                )
                if channels_warning > 0:
                    st.caption(f"⚠️ {channels_warning}/{len(channels)} channels need attention")
            
            with col3:
                channels_critical = (vif_df['VIF'] > 10).sum()
                st.metric(
                    "Channels > VIF 10", 
                    f"{channels_critical}",
                    help="Number of channels with critical VIF scores"
                )
                if channels_critical > 0:
                    st.caption(f"🔴 {channels_critical}/{len(channels)} channels unreliable")
            
            # Add actionable insights
            st.divider()
            st.subheader("💡 What This Means For You")
            
            if max_vif > 10:
                st.error("""
                **⚠️ Your marketing data has serious multicollinearity issues!**
                
                **Impact:**
                - Marketing ROI estimates are unreliable
                - Channel attribution is essentially guesswork
                - Budget optimization recommendations will be flawed
                
                **Next Steps:**
                1. Check the 'Compare Solutions' tab to see different approaches
                2. Consider running controlled experiments (A/B tests)
                3. Use the 'Interactive Simulator' to understand the problem better
                """)
            elif max_vif > 5:
                st.warning("""
                **⚠️ Moderate multicollinearity detected**
                
                Some channels are correlated enough to affect attribution accuracy.
                Consider reviewing your media planning to ensure channels vary more independently.
                """)
            else:
                st.success("""
                **✅ Your data looks good!**
                
                Low multicollinearity means you can trust your marketing mix model results.
                Channel attribution should be reliable and actionable.
                """)

# Section 4: Visualize the Problem
elif section == "📈 Visualize the Problem":
    st.header("Visualize Multicollinearity Impact")
    
    # Add comprehensive introduction
    st.markdown("""
    ### 🎯 Why Visualize the Problem?
    
    Numbers and statistics can be abstract. This section shows you **visually** how multicollinearity 
    makes your marketing measurements unreliable and unstable.
    
    ### 📊 What You'll See:
    
    **Coefficient Instability**: When multicollinearity is present, your model's estimates for each channel's 
    impact become extremely unstable. Small changes in your data lead to wildly different results.
    
    ### 🔬 The Bootstrap Experiment:
    
    We'll take many random samples from your data (with replacement) and fit a model to each sample.
    In a healthy dataset, coefficients should be consistent. With multicollinearity, they'll be all over the place!
    """)
    
    st.divider()
    
    if st.session_state.marketing_data is None:
        st.warning("⚠️ Please generate marketing data first in the 'Generate Marketing Data' section")
    else:
        df = st.session_state.marketing_data
        channels = [col for col in df.columns if col != 'Sales']
        
        # Create subsamples to show coefficient instability
        st.subheader("🎲 Coefficient Instability Demonstration")
        
        st.markdown("""
        **What This Shows:**
        
        This analysis runs the same model multiple times on slightly different samples of your data.
        Think of it like asking 50 different analysts to measure your marketing impact using slightly different time periods.
        
        **What to Look For:**
        - **Narrow distributions** = Stable, reliable estimates ✅
        - **Wide distributions** = Unstable, unreliable estimates 🔴
        - **Multiple peaks** = Model can't decide on the true value ⚠️
        """)
        
        n_simulations = st.slider(
            "Number of Bootstrap Samples", 
            10, 100, 50,
            help="More samples = more reliable visualization, but takes longer to compute"
        )
        
        if st.button("Run Bootstrap Analysis"):
            coefficients = {channel: [] for channel in channels}
            
            progress_bar = st.progress(0)
            for i in range(n_simulations):
                # Bootstrap sample
                sample_idx = np.random.choice(len(df), size=len(df), replace=True)
                sample_df = df.iloc[sample_idx]
                
                # Fit model
                X = sample_df[channels]
                y = sample_df['Sales']
                
                model = LinearRegression()
                model.fit(X, y)
                
                for j, channel in enumerate(channels):
                    coefficients[channel].append(model.coef_[j])
                
                progress_bar.progress((i + 1) / n_simulations)
            
            # Create coefficient distribution plot
            fig = make_subplots(
                rows=2, cols=3,
                subplot_titles=channels,
                vertical_spacing=0.15,
                horizontal_spacing=0.1
            )
            
            for idx, channel in enumerate(channels):
                row = idx // 3 + 1
                col = idx % 3 + 1
                
                fig.add_trace(
                    go.Histogram(
                        x=coefficients[channel],
                        name=channel,
                        nbinsx=20,
                        marker_color='lightblue',
                        showlegend=False
                    ),
                    row=row, col=col
                )
                
                # Add mean line
                mean_coef = np.mean(coefficients[channel])
                fig.add_vline(
                    x=mean_coef, 
                    line_dash="dash", 
                    line_color="red",
                    row=row, col=col
                )
            
            fig.update_layout(
                title=f"Coefficient Distribution Across {n_simulations} Bootstrap Samples",
                height=600,
                showlegend=False
            )
            
            # Add annotations to explain the histograms
            fig.update_xaxes(title_text="Coefficient Value", row=2, col=2)
            fig.update_yaxes(title_text="Frequency", row=1, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add visual interpretation guide
            st.info("""
            **📖 How to Interpret the Histograms Above:**
            
            Each histogram shows how much a channel's estimated impact varies across different data samples:
            - **Narrow, single peak** = Consistent estimate (good!) ✅
            - **Wide spread** = Uncertain estimate (problematic) ⚠️
            - **Multiple peaks or very wide** = Extremely unreliable (critical) 🔴
            
            The red dashed line shows the average estimate across all samples.
            """)
            
            # Coefficient statistics with enhanced explanations
            st.divider()
            st.subheader("📊 Coefficient Variability Statistics")
            
            st.markdown("""
            **Understanding These Metrics:**
            - **Mean**: Average coefficient across all bootstrap samples
            - **Std Dev**: How much coefficients vary (lower is better)
            - **Min/Max**: Range of coefficient values seen
            - **CV% (Coefficient of Variation)**: Relative variability - the key metric!
                - CV < 20%: Excellent stability ✅
                - CV 20-50%: Moderate stability ⚠️
                - CV > 50%: Poor stability 🔴
            """)
            
            coef_stats = pd.DataFrame({
                'Channel': channels,
                'Mean': [np.mean(coefficients[ch]) for ch in channels],
                'Std Dev': [np.std(coefficients[ch]) for ch in channels],
                'Min': [np.min(coefficients[ch]) for ch in channels],
                'Max': [np.max(coefficients[ch]) for ch in channels],
                'CV%': [100 * np.std(coefficients[ch]) / abs(np.mean(coefficients[ch])) if np.mean(coefficients[ch]) != 0 else 0 for ch in channels]
            })
            
            # Add stability indicator
            def get_stability_indicator(cv):
                if cv < 20:
                    return "✅ Stable"
                elif cv < 50:
                    return "⚠️ Moderate"
                else:
                    return "🔴 Unstable"
            
            coef_stats['Stability'] = coef_stats['CV%'].apply(get_stability_indicator)
            
            st.dataframe(coef_stats.style.format({
                'Mean': '{:.3f}',
                'Std Dev': '{:.3f}',
                'Min': '{:.3f}',
                'Max': '{:.3f}',
                'CV%': '{:.1f}'
            }), use_container_width=True)
            
            # Enhanced interpretation with real-world implications
            st.divider()
            st.subheader("💡 What This Means for Your Marketing")
            
            high_cv_channels = coef_stats[coef_stats['CV%'] > 50]['Channel'].tolist()
            moderate_cv_channels = coef_stats[(coef_stats['CV%'] > 20) & (coef_stats['CV%'] <= 50)]['Channel'].tolist()
            
            if high_cv_channels:
                st.error(f"""
                **🔴 Critical Issue Detected!**
                
                Channels with unstable coefficients: **{', '.join(high_cv_channels)}**
                
                **Real-world Impact:**
                - You could measure the same campaign twice and get completely different ROI numbers
                - Budget recommendations based on these coefficients are essentially random
                - Historical performance analysis is unreliable
                
                **Example:** {high_cv_channels[0]} shows coefficients ranging from {coef_stats[coef_stats['Channel']==high_cv_channels[0]]['Min'].values[0]:.2f} to {coef_stats[coef_stats['Channel']==high_cv_channels[0]]['Max'].values[0]:.2f}.
                This means the model thinks this channel could be anywhere from {'harmful' if coef_stats[coef_stats['Channel']==high_cv_channels[0]]['Min'].values[0] < 0 else 'barely effective'} to highly effective!
                """)
            
            if moderate_cv_channels:
                st.warning(f"""
                **⚠️ Moderate Instability**
                
                Channels with moderate variability: **{', '.join(moderate_cv_channels)}**
                
                These channels show some uncertainty in their impact measurement. 
                Consider additional analysis or controlled experiments for these channels.
                """)
            
            if not high_cv_channels and not moderate_cv_channels:
                st.success("""
                **✅ Excellent Stability!**
                
                All channels show stable coefficient estimates. Your marketing mix model 
                can reliably measure channel performance and guide budget decisions.
                """)
            
            # Add actionable next steps
            st.divider()
            st.subheader("🎯 Recommended Next Steps")
            
            if high_cv_channels or moderate_cv_channels:
                st.markdown("""
                Based on your coefficient instability results:
                
                1. **Immediate Action**: Don't rely solely on these model results for budget decisions
                2. **Data Collection**: Vary channels more independently in future campaigns
                3. **Alternative Methods**: Check the 'Compare Solutions' tab for different approaches
                4. **Experimentation**: Run controlled A/B tests to get cleaner measurements
                5. **Expert Review**: Consider statistical consultation for critical decisions
                """)

# Section 5: Compare Solutions
elif section == "🛠️ Compare Solutions":
    st.header("Compare Multicollinearity Solutions")
    
    # Add comprehensive introduction
    st.markdown("""
    ### 🎯 Finding the Best Solution for Your Data
    
    When multicollinearity makes standard regression unreliable, several statistical techniques can help.
    This section compares different approaches so you can choose the best one for your situation.
    
    ### 📚 Solution Methods Explained:
    
    1. **OLS (Ordinary Least Squares)**: The standard approach - no protection against multicollinearity
    2. **Ridge Regression (L2)**: Shrinks coefficients but keeps all channels
    3. **Lasso Regression (L1)**: Can eliminate less important channels entirely
    4. **Elastic Net**: Combines Ridge and Lasso benefits
    5. **PCA (Principal Components)**: Transforms correlated channels into independent components
    6. **Residualization**: Removes correlation between predictors step-by-step
    
    ### 🎯 What to Look For:
    - **Test R² close to Train R²**: Model generalizes well (not overfitting)
    - **Stable coefficients**: Similar values across methods indicate reliability
    - **Reasonable coefficient magnitudes**: Not extremely large or wildly varying
    """)
    
    st.divider()
    
    if st.session_state.marketing_data is None:
        st.warning("⚠️ Please generate marketing data first in the 'Generate Marketing Data' section")
    else:
        df = st.session_state.marketing_data
        channels = [col for col in df.columns if col != 'Sales']
        
        X = df[channels].values
        y = df['Sales'].values
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Split data
        train_size = int(0.8 * len(X))
        X_train, X_test = X_scaled[:train_size], X_scaled[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        st.subheader("🔬 Regularization Methods Comparison")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Method Settings")
            
            st.markdown("**📊 Ridge Regression (L2)**")
            ridge_alpha = st.slider(
                "Ridge Alpha", 
                0.01, 10.0, 1.0,
                help="Higher values = stronger regularization. Prevents coefficients from becoming too large."
            )
            st.caption("Best for: When you want to keep all channels but reduce their impact")
            
            st.markdown("**✂️ Lasso Regression (L1)**")
            lasso_alpha = st.slider(
                "Lasso Alpha", 
                0.01, 10.0, 0.1,
                help="Higher values = more aggressive channel elimination. Can set some coefficients to exactly zero."
            )
            st.caption("Best for: When you suspect some channels don't matter at all")
            
            st.markdown("**🔄 Elastic Net**")
            elastic_ratio = st.slider(
                "Elastic Net Ratio", 
                0.0, 1.0, 0.5,
                help="0 = Pure Ridge, 1 = Pure Lasso, 0.5 = Equal mix of both"
            )
            st.caption("Best for: Balanced approach between Ridge and Lasso")
            
            st.markdown("**🔀 PCA Components**")
            n_components = st.slider(
                "PCA Components", 
                1, len(channels), 3,
                help="Number of independent components to extract from correlated channels"
            )
            st.caption("Best for: When channels are highly correlated and you want independent factors")
            
            st.markdown("**🔄 Residualization**")
            residual_base_channel = st.selectbox(
                "Base Channel for Residualization",
                channels,
                help="Choose the primary channel. Other channels will be orthogonalized against this one."
            )
            st.caption("Best for: When you have a primary channel and want to measure incremental impact of others")
        
        with col2:
            # Train models
            models = {
                'OLS (No Regularization)': LinearRegression(),
                'Ridge (L2)': Ridge(alpha=ridge_alpha),
                'Lasso (L1)': Lasso(alpha=lasso_alpha),
                'Elastic Net': ElasticNet(alpha=lasso_alpha, l1_ratio=elastic_ratio)
            }
            
            results = []
            coefficients_comparison = pd.DataFrame(index=channels)
            
            for name, model in models.items():
                model.fit(X_train, y_train)
                train_score = model.score(X_train, y_train)
                test_score = model.score(X_test, y_test)
                
                results.append({
                    'Method': name,
                    'Train R²': train_score,
                    'Test R²': test_score,
                    'Overfit Gap': train_score - test_score
                })
                
                coefficients_comparison[name] = model.coef_
            
            # PCA approach
            pca = PCA(n_components=n_components)
            X_train_pca = pca.fit_transform(X_train)
            X_test_pca = pca.transform(X_test)
            
            pca_model = LinearRegression()
            pca_model.fit(X_train_pca, y_train)
            
            results.append({
                'Method': f'PCA ({n_components} components)',
                'Train R²': pca_model.score(X_train_pca, y_train),
                'Test R²': pca_model.score(X_test_pca, y_test),
                'Overfit Gap': pca_model.score(X_train_pca, y_train) - pca_model.score(X_test_pca, y_test)
            })
            
            # Residualization approach
            # Create residualized features
            base_channel_idx = channels.index(residual_base_channel)
            X_train_resid = X_train.copy()
            X_test_resid = X_test.copy()
            
            # For each channel (except base), residualize against base channel
            for i, channel in enumerate(channels):
                if i != base_channel_idx:
                    # Fit linear regression to predict this channel from base channel
                    residual_model = LinearRegression()
                    residual_model.fit(X_train[:, base_channel_idx].reshape(-1, 1), X_train[:, i])
                    
                    # Get residuals (what's left after removing base channel influence)
                    X_train_resid[:, i] = X_train[:, i] - residual_model.predict(X_train[:, base_channel_idx].reshape(-1, 1))
                    X_test_resid[:, i] = X_test[:, i] - residual_model.predict(X_test[:, base_channel_idx].reshape(-1, 1))
            
            # Fit model on residualized features
            resid_model = LinearRegression()
            resid_model.fit(X_train_resid, y_train)
            
            results.append({
                'Method': f'Residualized (base: {residual_base_channel})',
                'Train R²': resid_model.score(X_train_resid, y_train),
                'Test R²': resid_model.score(X_test_resid, y_test),
                'Overfit Gap': resid_model.score(X_train_resid, y_train) - resid_model.score(X_test_resid, y_test)
            })
            
            # Store residualized coefficients for comparison
            residualized_coefs = resid_model.coef_.copy()
            coefficients_comparison[f'Residualized ({residual_base_channel})'] = residualized_coefs
            
            # Display results
            st.markdown("### Model Performance Comparison")
            
            st.info("""
            **📖 How to Read This Chart:**
            - **Train R²**: How well the model fits the training data (higher is better, but...)
            - **Test R²**: How well the model predicts new data (this is what really matters!)
            - **Gap between bars**: Large gap = overfitting (model memorized training data)
            - **Best model**: High Test R² with small gap from Train R²
            """)
            
            results_df = pd.DataFrame(results)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Train R²', x=results_df['Method'], y=results_df['Train R²']))
            fig.add_trace(go.Bar(name='Test R²', x=results_df['Method'], y=results_df['Test R²']))
            
            fig.update_layout(
                title="Model Performance: Train vs Test",
                yaxis_title="R² Score",
                barmode='group',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Add performance interpretation
            best_model = results_df.loc[results_df['Test R²'].idxmax(), 'Method']
            best_score = results_df.loc[results_df['Test R²'].idxmax(), 'Test R²']
            
            st.success(f"""
            **🏆 Best Performing Model: {best_model}**
            - Test R² Score: {best_score:.3f}
            - This model provides the most reliable predictions on new data
            """)
            
        # Coefficient comparison
        st.divider()
        st.subheader("📊 Coefficient Comparison Across Methods")
        
        st.markdown("""
        **What This Shows:**
        
        How each method assigns importance to different marketing channels. Look for:
        - **Consistency**: Similar patterns across methods suggest reliable attribution
        - **Stability**: Regularized methods should show more reasonable coefficient sizes
        - **Sparsity**: Lasso might set some coefficients to zero (channel elimination)
        """)
        
        fig = go.Figure()
        for method in coefficients_comparison.columns:
            fig.add_trace(go.Bar(
                name=method,
                x=channels,
                y=coefficients_comparison[method],
                text=coefficients_comparison[method].round(2),
                textposition='outside'
            ))
        
        fig.update_layout(
            title="Channel Coefficients by Regularization Method",
            xaxis_title="Marketing Channel",
            yaxis_title="Coefficient Value",
            barmode='group',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Residualization explanation
        st.divider()
        st.subheader("🔄 Understanding Residualization")
        
        st.markdown(f"""
        **What is Residualization?**
        
        Residualization removes the influence of one channel from all others, allowing you to measure 
        their **incremental impact** beyond what the base channel already explains.
        
        **Current Setup:**
        - **Base Channel**: {residual_base_channel}
        - **Process**: Other channels are adjusted to remove their correlation with {residual_base_channel}
        - **Result**: Coefficients now show the unique contribution of each channel
        
        **When to Use Residualization:**
        - You have a **primary channel** (e.g., TV) that drives overall awareness
        - You want to measure the **incremental lift** from secondary channels
        - You need to answer: "What does Channel X add beyond what {residual_base_channel} already provides?"
        
        **Interpretation:**
        - **{residual_base_channel} coefficient**: Total impact including correlated effects
        - **Other coefficients**: Additional impact after removing {residual_base_channel}'s influence
        - **Lower coefficients after residualization**: Indicates the channel was riding on {residual_base_channel}'s coattails
        """)
        
        # Feature importance from PCA
        st.divider()
        st.subheader("🔍 PCA Component Analysis")
        
        st.markdown("""
        **Understanding PCA (Principal Component Analysis):**
        
        PCA transforms your correlated marketing channels into **independent components** - 
        think of it as finding the "hidden factors" that drive all channels together.
        
        **How to Interpret the Heatmap Below:**
        - **Red values**: Channel contributes positively to this component
        - **Blue values**: Channel contributes negatively to this component
        - **Near-zero values**: Channel doesn't affect this component
        
        **Example Interpretation:**
        - PC1 might represent "overall marketing intensity"
        - PC2 might capture "digital vs traditional" marketing split
        - PC3 might show "seasonal campaign patterns"
        """)
        
        loadings = pd.DataFrame(
            pca.components_[:n_components].T,
            columns=[f'PC{i+1}' for i in range(n_components)],
            index=channels
        )
        
        fig = px.imshow(
            loadings.T,
            text_auto='.2f',
            color_continuous_scale='RdBu_r',
            aspect='auto',
            title="PCA Component Loadings (How channels contribute to each component)"
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Explained variance with better explanations
        st.divider()
        st.subheader("📊 Variance Explained by Components")
        
        st.markdown("""
        **What These Numbers Mean:**
        - **Total Variance Explained**: How much of the original data's information is captured
        - **PC1, PC2, etc**: How much each component contributes (PC1 is always the most important)
        - **Goal**: Capture 80-90% of variance with fewer components than original channels
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            total_var = pca.explained_variance_ratio_.sum()
            st.metric(
                "Total Variance Explained", 
                f"{total_var:.1%}",
                help="Percentage of original data information retained"
            )
            if total_var < 0.8:
                st.caption("⚠️ Consider more components")
            else:
                st.caption("✅ Good coverage")
        with col2:
            st.metric(
                "PC1 Variance", 
                f"{pca.explained_variance_ratio_[0]:.1%}",
                help="Most important pattern in your data"
            )
        with col3:
            if n_components > 1:
                st.metric(
                    "PC2 Variance", 
                    f"{pca.explained_variance_ratio_[1]:.1%}",
                    help="Second most important pattern"
                )
        
        # Add method selection guidance
        st.divider()
        st.subheader("🎯 Which Method Should You Use?")
        
        # Analyze results and provide recommendation
        if st.session_state.vif_scores is not None:
            max_vif = st.session_state.vif_scores['VIF'].max()
            
            if max_vif > 10:
                st.error("""
                **🔴 Severe Multicollinearity Detected (VIF > 10)**
                
                **Recommended Approaches:**
                1. **Ridge Regression**: Good first choice - reduces coefficient variance
                2. **Elastic Net**: If you want some channel elimination too
                3. **PCA**: If channels are extremely correlated (VIF > 20)
                4. **Residualization**: If you have a clear primary channel (e.g., TV drives awareness for all)
                
                **Avoid:**
                - OLS (standard regression) - will give unreliable results
                - Pure Lasso with low alpha - might eliminate important channels randomly
                """)
            elif max_vif > 5:
                st.warning("""
                **⚠️ Moderate Multicollinearity (VIF 5-10)**
                
                **Recommended Approaches:**
                1. **Elastic Net**: Balanced approach for moderate issues
                2. **Ridge with low alpha**: Gentle regularization
                
                **Consider:**
                - Collecting more varied data
                - Running some channels independently
                """)
            else:
                st.success("""
                **✅ Low Multicollinearity (VIF < 5)**
                
                **Recommended Approach:**
                - **OLS (Standard Regression)**: Your data is clean enough for standard methods
                - Optional: Light Ridge regularization for extra stability
                """)
        
        # Final recommendations
        st.divider()
        st.subheader("📋 Key Takeaways")
        
        st.info("""
        **Remember:**
        1. **No single method is always best** - it depends on your specific data and goals
        2. **Test performance matters more than training performance** - avoid overfitting
        3. **Coefficient stability is as important as model accuracy** - unstable coefficients = unreliable insights
        4. **Consider business context** - some channels might be correlated for good reasons (e.g., holiday campaigns)
        5. **Validate with experiments** - even the best model benefits from A/B test validation
        """)

# Section 6: Interactive Simulator
elif section == "🎮 Interactive Simulator":
    st.header("Interactive Multicollinearity Simulator")
    
    # Add comprehensive introduction
    st.markdown("""
    ### 🎯 Hands-On Learning Experience
    
    This interactive simulator lets you **see multicollinearity in action**! 
    Adjust parameters and watch in real-time how correlation between channels affects your ability to measure their true impact.
    
    ### 🔬 What This Simulates:
    
    Imagine you're running two marketing channels (e.g., TV and Digital) and trying to measure their individual impact on sales.
    This simulator shows what happens when these channels are correlated (run together).
    
    ### 📊 Key Insights to Discover:
    - **Low correlation**: Model estimates are close to true values ✅
    - **High correlation**: Model struggles to separate channel effects ⚠️
    - **Perfect correlation**: Model completely fails (coefficients become random) 🔴
    """)
    
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎛️ Simulation Parameters")
        
        st.markdown("**📊 Channel Relationship**")
        correlation = st.slider(
            "Channel Correlation", 
            -1.0, 1.0, 0.8, 0.05,
            help="""
            -1.0 = Perfect negative correlation (when one goes up, other goes down)
            0.0 = No correlation (channels vary independently)
            0.8 = High positive correlation (channels move together)
            1.0 = Perfect correlation (channels move in lockstep)
            """
        )
        
        # Show correlation interpretation
        if abs(correlation) < 0.3:
            st.success("✅ Low correlation - Good for measurement!")
        elif abs(correlation) < 0.7:
            st.warning("⚠️ Moderate correlation - Some uncertainty")
        elif abs(correlation) < 0.95:
            st.error("🔴 High correlation - Difficult to measure!")
        else:
            st.error("🚨 Near-perfect correlation - Measurement impossible!")
        
        st.markdown("**📈 Data Settings**")
        sample_size = st.slider(
            "Sample Size", 
            20, 500, 100,
            help="More data points = more reliable estimates (like having more weeks of campaign data)"
        )
        
        noise_std = st.slider(
            "Noise Level", 
            0.1, 5.0, 1.0,
            help="Market randomness - higher = more unpredictable sales (like external factors affecting sales)"
        )
        
        st.markdown("**🎯 True Channel Effects**")
        st.caption("Set the actual impact each channel has on sales (what we're trying to measure)")
        
        true_coef1 = st.number_input(
            "True Channel 1 Effect", 
            value=3.0,
            help="For every $1 spent on Channel 1, sales increase by this amount"
        )
        true_coef2 = st.number_input(
            "True Channel 2 Effect", 
            value=2.0,
            help="For every $1 spent on Channel 2, sales increase by this amount"
        )
    
    # Generate correlated data
    mean = [0, 0]
    cov = [[1, correlation], [correlation, 1]]
    
    np.random.seed(42)
    X_sim = np.random.multivariate_normal(mean, cov, sample_size)
    
    # Generate outcome
    y_sim = 10 + true_coef1 * X_sim[:, 0] + true_coef2 * X_sim[:, 1] + np.random.normal(0, noise_std, sample_size)
    
    # Fit model
    model = LinearRegression()
    model.fit(X_sim, y_sim)
    estimated_coef1, estimated_coef2 = model.coef_
    
    # Calculate VIF
    vif = 1 / (1 - correlation**2) if abs(correlation) < 1 else float('inf')
    
    with col2:
        st.markdown("### 📊 Real-Time Visualization")
        
        # Add explanation for the charts
        with st.expander("📖 How to Read These Charts", expanded=False):
            st.markdown("""
            **1. Channel Correlation (Top Left):**
            - Shows how the two channels move together
            - Red line shows the correlation strength
            - Tighter cloud = higher correlation
            
            **2. True vs Estimated Effects (Top Right):**
            - Green bars: The true impact you set
            - Orange bars: What the model thinks the impact is
            - Closer bars = better measurement accuracy
            
            **3. Residual Plot (Bottom Left):**
            - Shows prediction errors
            - Points should be randomly scattered around zero
            - Patterns indicate model problems
            
            **4. Channel Contributions (Bottom Right):**
            - Distribution of each channel's calculated contribution
            - Overlapping distributions = hard to separate effects
            """)
        
        # Create scatter plot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Channel Correlation', 'True vs Estimated Effects', 
                          'Residual Plot', 'Channel Contributions'),
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # Correlation scatter
        fig.add_trace(
            go.Scatter(x=X_sim[:, 0], y=X_sim[:, 1], mode='markers',
                      marker=dict(color='lightblue', size=8),
                      name='Data Points'),
            row=1, col=1
        )
        
        # Add correlation line
        x_range = np.linspace(X_sim[:, 0].min(), X_sim[:, 0].max(), 100)
        y_range = correlation * x_range
        fig.add_trace(
            go.Scatter(x=x_range, y=y_range, mode='lines',
                      line=dict(color='red', dash='dash'),
                      name=f'r = {correlation:.2f}'),
            row=1, col=1
        )
        
        # True vs Estimated coefficients
        fig.add_trace(
            go.Bar(x=['Channel 1', 'Channel 2'], 
                  y=[true_coef1, true_coef2],
                  name='True Effect',
                  marker_color='green'),
            row=1, col=2
        )
        fig.add_trace(
            go.Bar(x=['Channel 1', 'Channel 2'], 
                  y=[estimated_coef1, estimated_coef2],
                  name='Estimated Effect',
                  marker_color='orange'),
            row=1, col=2
        )
        
        # Residual plot
        y_pred = model.predict(X_sim)
        residuals = y_sim - y_pred
        fig.add_trace(
            go.Scatter(x=y_pred, y=residuals, mode='markers',
                      marker=dict(color='purple', size=6),
                      name='Residuals'),
            row=2, col=1
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)
        
        # Channel contributions
        contributions = pd.DataFrame({
            'Channel 1': X_sim[:, 0] * estimated_coef1,
            'Channel 2': X_sim[:, 1] * estimated_coef2
        })
        
        fig.add_trace(
            go.Histogram(x=contributions['Channel 1'], name='Channel 1',
                        marker_color='blue', opacity=0.7),
            row=2, col=2
        )
        fig.add_trace(
            go.Histogram(x=contributions['Channel 2'], name='Channel 2',
                        marker_color='red', opacity=0.7),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Metrics with enhanced explanations
    st.divider()
    st.markdown("### 📈 Key Performance Metrics")
    
    st.markdown("""
    **Understanding These Metrics:**
    - **VIF Score**: Variance Inflation Factor - measures multicollinearity severity
    - **Channel Errors**: How far off the model's estimates are from true values
    - **Model R²**: Overall model fit (but can be misleading with multicollinearity!)
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "VIF Score", 
            f"{vif:.2f}" if vif != float('inf') else "∞",
            "⚠️ High" if vif > 5 else "✅ Good",
            help="VIF > 5 indicates problematic multicollinearity"
        )
        if vif > 10:
            st.caption("🔴 Severe issue!")
        elif vif > 5:
            st.caption("⚠️ Concerning")
        else:
            st.caption("✅ Acceptable")
    
    with col2:
        error1 = abs(estimated_coef1 - true_coef1) / abs(true_coef1) * 100 if true_coef1 != 0 else 0
        st.metric(
            "Channel 1 Error", 
            f"{error1:.1f}%",
            "High" if error1 > 20 else "Low",
            help="Percentage difference between true and estimated effect"
        )
        st.caption(f"True: {true_coef1:.1f}")
        st.caption(f"Est: {estimated_coef1:.1f}")
    
    with col3:
        error2 = abs(estimated_coef2 - true_coef2) / abs(true_coef2) * 100 if true_coef2 != 0 else 0
        st.metric(
            "Channel 2 Error", 
            f"{error2:.1f}%",
            "High" if error2 > 20 else "Low",
            help="Percentage difference between true and estimated effect"
        )
        st.caption(f"True: {true_coef2:.1f}")
        st.caption(f"Est: {estimated_coef2:.1f}")
    
    with col4:
        r2 = model.score(X_sim, y_sim)
        st.metric(
            "Model R²", 
            f"{r2:.3f}",
            help="Proportion of variance explained - can be high even with wrong coefficients!"
        )
        st.caption("⚠️ R² can mislead with multicollinearity")
    
    # Enhanced Interpretation
    st.divider()
    st.markdown("### 🎯 What This Means")
    
    if vif > 10:
        st.error(f"""
        🚨 **Critical Multicollinearity Detected!**
        
        **Your Simulation Results:**
        - VIF Score: {vif:.2f} (anything > 10 is critical)
        - Channel 1 estimation error: {error1:.1f}%
        - Channel 2 estimation error: {error2:.1f}%
        
        **What's Happening:**
        With correlation = {correlation:.2f}, the two channels are moving almost in lockstep.
        The model sees them increase and decrease together, making it impossible to determine 
        which channel is actually driving sales.
        
        **Real-World Impact:**
        - Marketing ROI calculations are essentially meaningless
        - Budget optimization will give random recommendations
        - You might invest in the wrong channel entirely
        
        **Try This:**
        Move the correlation slider below 0.7 and watch the estimates improve!
        """)
    elif vif > 5:
        st.warning(f"""
        ⚠️ **High Multicollinearity Warning**
        
        **Your Simulation Results:**
        - VIF Score: {vif:.2f} (5-10 range is concerning)
        - Average estimation error: {(error1 + error2)/2:.1f}%
        
        **What's Happening:**
        The channels are correlated enough that the model struggles to accurately 
        separate their individual impacts. Notice how the orange bars (estimates) 
        don't quite match the green bars (true values).
        
        **Real-World Impact:**
        - ROI estimates have significant uncertainty
        - Budget decisions based on these numbers are risky
        - You need more data or different methods
        
        **Solutions:**
        - Use regularization methods (Ridge, Lasso)
        - Collect data where channels vary more independently
        - Run controlled experiments
        """)
    else:
        st.success(f"""
        ✅ **Good News - Low Multicollinearity!**
        
        **Your Simulation Results:**
        - VIF Score: {vif:.2f} (< 5 is good!)
        - Average estimation error: {(error1 + error2)/2:.1f}%
        - Model R²: {r2:.3f}
        
        **What's Happening:**
        With correlation = {correlation:.2f}, the channels vary independently enough 
        that the model can distinguish their separate effects. Notice how the orange bars 
        (estimates) closely match the green bars (true values)!
        
        **Real-World Implication:**
        - You can trust your marketing attribution
        - ROI calculations are reliable
        - Budget optimization recommendations are sound
        
        **Key Insight:**
        This is what you want to see in your real marketing data - 
        channels that don't always move together!
        """)
    
    # Add learning exercises
    st.divider()
    st.markdown("### 🎓 Learning Exercises")
    
    with st.expander("🔬 Try These Experiments"):
        st.markdown("""
        **Experiment 1: The Correlation Effect**
        1. Set correlation to 0.0 (no correlation)
        2. Note the estimation errors
        3. Gradually increase to 0.9
        4. Watch how errors increase dramatically!
        
        **Experiment 2: Sample Size Impact**
        1. Set correlation to 0.8 (high)
        2. Try sample size = 50 (small dataset)
        3. Increase to 500 (large dataset)
        4. Notice: More data helps, but doesn't solve high correlation!
        
        **Experiment 3: Noise Sensitivity**
        1. Set correlation to 0.7
        2. Vary noise from 0.1 to 5.0
        3. Observe: High noise makes estimation harder
        4. But correlation is still the bigger problem!
        
        **Experiment 4: The Perfect Storm**
        1. Set correlation to 0.95 (near perfect)
        2. Set sample size to 30 (small)
        3. Set noise to 3.0 (high)
        4. This is the worst-case scenario - completely unreliable!
        """)
    
    with st.expander("💡 Key Takeaways"):
        st.markdown("""
        **What You've Learned:**
        
        1. **Correlation Kills Attribution**
           - Even 0.8 correlation causes major problems
           - Above 0.9 is essentially unmeasurable
        
        2. **More Data Isn't Always the Answer**
           - Sample size helps, but can't overcome high correlation
           - Need data where channels vary independently
        
        3. **R² Can Be Misleading**
           - High R² doesn't mean accurate coefficients
           - Model can fit well but still get attribution wrong
        
        4. **VIF is Your Friend**
           - Quick way to spot multicollinearity
           - VIF > 5 = start worrying
           - VIF > 10 = serious problem
        
        5. **Business Implications**
           - Bad attribution = bad budget decisions
           - Might invest heavily in wrong channel
           - Need to fix before trusting results
        """)

# Section 7: Real-World Examples
elif section == "💡 Real-World Examples":
    st.header("Real-World Examples & Case Studies")
    
    # Add comprehensive introduction
    st.markdown("""
    ### 🎯 Learning from Real Marketing Scenarios
    
    These case studies show how multicollinearity appears in actual marketing campaigns.
    Each example represents a common situation where companies struggle to measure marketing effectiveness.
    
    ### 📚 What You'll Learn:
    - How multicollinearity manifests in different industries
    - Why certain marketing practices create measurement problems
    - Practical solutions that real companies have implemented
    - Warning signs to watch for in your own data
    """)
    
    st.divider()
    
    # Example selector with better description
    example = st.selectbox(
        "📂 Choose a case study to explore:",
        ["🛍️ E-commerce: Black Friday Campaign"],
        help="Real-world example demonstrating multicollinearity in action"
    )
    
    if example == "🛍️ E-commerce: Black Friday Campaign":
        st.subheader("🛍️ E-commerce: Black Friday Campaign Analysis")
        
        # Add case study overview
        st.info("""
        **📖 Case Study Overview:**
        
        This is a classic example of **event-driven multicollinearity**. During major sales events like 
        Black Friday, companies typically increase all marketing channels simultaneously, making it 
        impossible to determine which channel actually drove the sales increase.
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 📊 The Problem
            
            **Company**: Major online retailer
            **Event**: Black Friday / Cyber Monday 2023
            
            **What Happened:**
            The marketing team increased all channels for Black Friday week:
            - **Google Ads**: +400% spend increase
            - **Facebook Ads**: +380% spend increase
            - **Email**: +350% campaign volume
            - **Display**: +420% impression buying
            
            **Result**: Sales increased by 600% 🎉
            
            **The Challenge**: 
            Which channel deserves credit? The MMM couldn't tell because all channels moved together!
            
            ### 📈 The Data Pattern
            
            **Notice the Problem:**
            Look how all channels spike together at Black Friday (red line).
            This perfect correlation makes attribution impossible!
            """)
            
            # Generate example data
            weeks = pd.date_range(start='2023-10-01', periods=12, freq='W')
            black_friday_week = 8
            
            data = {
                'Google_Ads': [20]*8 + [100] + [25]*3,
                'Facebook_Ads': [18]*8 + [86] + [22]*3,
                'Email': [15]*8 + [67] + [18]*3,
                'Display': [12]*8 + [62] + [15]*3,
                'Sales': [100]*8 + [700] + [120]*3
            }
            
            df_example = pd.DataFrame(data, index=weeks)
            
            fig = go.Figure()
            
            for col in ['Google_Ads', 'Facebook_Ads', 'Email', 'Display']:
                fig.add_trace(go.Scatter(
                    x=df_example.index,
                    y=df_example[col],
                    name=col,
                    mode='lines+markers'
                ))
            
            # Add vertical line for Black Friday using add_shape (more reliable with dates)
            black_friday_date = df_example.index[black_friday_week]
            fig.add_shape(
                type="line",
                x0=black_friday_date, x1=black_friday_date,
                y0=0, y1=1,
                yref="paper",
                line=dict(color="red", dash="dash", width=2)
            )
            fig.add_annotation(
                x=black_friday_date,
                y=1.05,
                yref="paper",
                text="Black Friday",
                showarrow=False,
                font=dict(color="red")
            )
            
            fig.update_layout(
                title="Marketing Spend Pattern",
                xaxis_title="Week",
                yaxis_title="Spend ($000s)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Key Metrics")
            
            st.metric(
                "Channel Correlation", 
                "0.98",
                "🔴 Critical",
                help="Nearly perfect correlation during Black Friday"
            )
            st.metric(
                "Max VIF", 
                "47.3",
                "🔴 Severe",
                help="VIF > 10 means unreliable attribution"
            )
            st.metric(
                "Model R²", 
                "0.92",
                "✅ High",
                help="Model fits well but coefficients are wrong!"
            )
            st.metric(
                "Attribution Confidence", 
                "12%",
                "🔴 Very Low",
                help="How confident we are in channel attribution"
            )
            
            st.warning("""
            **⚠️ The Trap:**
            High R² (0.92) looks good but is misleading!
            The model fits well but can't separate channel effects.
            """)
        
        st.divider()
        st.markdown("### 💡 The Solution")
        
        solution_tabs = st.tabs(["🎯 Approach", "💻 Implementation", "📈 Results", "📚 Lessons Learned"])
        
        with solution_tabs[0]:
            st.markdown("""
            **How This Company Solved It:**
            
            They realized they couldn't measure individual channels during Black Friday, 
            so they used a **multi-method approach**:
            
            #### 1️⃣ **Aggregate Modeling**
            - Combined all digital channels into "Total Digital Spend"
            - Measured overall digital effectiveness vs baseline
            - Avoided trying to separate inseparable channels
            
            #### 2️⃣ **Alternative Data Sources**
            - **Google Analytics**: Last-click attribution data
            - **Customer Surveys**: "Which ad made you buy?"
            - **Platform Data**: Facebook/Google conversion tracking
            - **Historical Ratios**: Pre-Black Friday channel performance
            
            #### 3️⃣ **Controlled Testing**
            - Ran A/B tests in January when spending was normal
            - Geo-experiments: Different channel mix by region
            - Incrementality tests: Turned channels on/off systematically
            
            #### 4️⃣ **Business Rules**
            - Applied known industry benchmarks
            - Used historical performance ratios
            - Incorporated marketing team expertise
            """)
        
        with solution_tabs[1]:
            st.markdown("**📝 Practical Implementation:**")
            
            st.code("""
# Stage 1: Combined Digital Model (avoiding multicollinearity)
df['Total_Digital'] = df[['Google_Ads', 'Facebook_Ads', 'Email', 'Display']].sum(axis=1)
df['Baseline'] = df[['TV', 'Radio', 'Print']].sum(axis=1)

# Fit model with aggregated channels
model_stage1 = Ridge(alpha=1.0)
model_stage1.fit(df[['Total_Digital', 'Baseline']], df['Sales'])

# Stage 2: Attribution weights from multiple sources
last_click_data = {
    'Google_Ads': 0.40,    # From Google Analytics
    'Facebook_Ads': 0.25,  # From GA4 + Facebook Attribution
    'Email': 0.20,         # From email platform tracking
    'Display': 0.15        # From display platform
}

survey_data = {
    'Google_Ads': 0.30,    # "I searched on Google"
    'Facebook_Ads': 0.35,  # "I saw it on Facebook"
    'Email': 0.25,         # "Got an email"
    'Display': 0.10        # "Saw a banner ad"
}

# Stage 3: Weighted average of different methods
final_weights = {}
for channel in ['Google_Ads', 'Facebook_Ads', 'Email', 'Display']:
    final_weights[channel] = (
        0.4 * last_click_data[channel] +  # 40% weight to last-click
        0.3 * survey_data[channel] +       # 30% weight to surveys
        0.3 * (1/4)                        # 30% equal distribution
    )

# Stage 3: Final attribution
total_digital_contribution = model_stage1.coef_[0] * df['Total_Digital'].sum()
channel_contributions = {
    channel: total_digital_contribution * weight 
    for channel, weight in weights.items()
}
            """, language='python')
        
        with solution_tabs[2]:
            st.markdown("**📊 Results & Impact:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Before Fix (Standard MMM):**
                - ❌ VIF scores: 40-50 (critical)
                - ❌ Confidence intervals: ±200%
                - ❌ Unstable coefficients
                - ❌ Different results each model run
                
                **After Fix (Multi-Method):**
                - ✅ No VIF issues (aggregated)
                - ✅ Confidence intervals: ±15%
                - ✅ Stable attribution
                - ✅ Consistent results
                """)
            
            with col2:
                st.markdown("""
                **📈 Final ROI Estimates:**
                - **Email**: $4.50 per $1 (highest)
                - **Google Ads**: $3.20 per $1
                - **Facebook**: $2.80 per $1
                - **Display**: $1.90 per $1 (lowest)
                
                **💰 Business Impact:**
                - Shifted $2M from Display to Email
                - 23% improvement in overall ROI
                - Saved $500K in wasted spend
                """)
            
            st.success("""
            **✅ Key Success:** By accepting they couldn't perfectly measure during Black Friday,
            they built a practical solution that was "good enough" for decision-making.
            """)
        
        with solution_tabs[3]:
            st.markdown("**🎓 Lessons Learned:**")
            
            with st.expander("📖 Key Takeaways for Your Business"):
                st.markdown("""
                **1. Don't Fight Perfect Correlation**
                - When channels move together, accept you can't separate them
                - Focus on measuring aggregate impact instead
                - Use other data sources to split credit
                
                **2. Prevention is Better Than Cure**
                - Plan marketing calendars to avoid simultaneous launches
                - Stagger channel increases when possible
                - Build in test periods with varied spending
                
                **3. Multiple Methods > Perfect Model**
                - No single attribution method is perfect
                - Combine MMM, digital tracking, surveys, and tests
                - Weight different methods based on reliability
                
                **4. Business Logic Matters**
                - Sometimes equal attribution is fine
                - Use historical performance as a guide
                - Don't over-engineer the solution
                """)
            
            with st.expander("⚠️ Warning Signs to Watch"):
                st.markdown("""
                **Red Flags in Your Data:**
                - 📍 All channels spike on the same dates
                - 📍 Channels always increase/decrease together
                - 📍 Major events drive all marketing simultaneously
                - 📍 VIF scores > 10 for multiple channels
                - 📍 Model coefficients change drastically with small data changes
                
                **When You See These Signs:**
                1. Check correlation matrix immediately
                2. Calculate VIF scores
                3. Consider aggregating channels
                4. Plan for alternative measurement
                """)
            
            with st.expander("🛠️ Action Plan Template"):
                st.markdown("""
                **If You Face Similar Issues:**
                
                **Week 1: Diagnose**
                - [ ] Calculate correlation matrix
                - [ ] Compute VIF scores
                - [ ] Identify problematic channel pairs
                
                **Week 2: Quick Fixes**
                - [ ] Try Ridge regression
                - [ ] Aggregate highly correlated channels
                - [ ] Apply business rules for attribution
                
                **Week 3-4: Additional Data**
                - [ ] Pull platform attribution reports
                - [ ] Design customer survey
                - [ ] Analyze historical patterns
                
                **Month 2: Testing**
                - [ ] Design geo-experiments
                - [ ] Plan staggered campaigns
                - [ ] Implement holdout tests
                
                **Month 3: Long-term Solution**
                - [ ] Update marketing calendar
                - [ ] Build attribution framework
                - [ ] Document methodology
                """)
    
    # Summary section for the case study
    st.divider()
    st.markdown("### 🎯 Key Takeaways from This Case Study")
    
    st.success("""
    **What We Learned:**
    
    1. **Multicollinearity is Common**: Major sales events create perfect correlation scenarios
    2. **Perfect Attribution is Impossible**: When channels move together, accept the limitation
    3. **Multiple Methods Work**: Combine MMM, digital tracking, surveys, and experiments
    4. **Prevention is Key**: Plan marketing calendars to avoid simultaneous spikes
    5. **Business Logic Helps**: Sometimes simple rules (like equal attribution) are good enough
    
    **Remember:** The goal isn't perfect measurement - it's actionable insights that improve ROI.
    """)
