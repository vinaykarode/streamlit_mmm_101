import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import plotly.figure_factory as ff

# Configure page
st.set_page_config(page_title="MMM 101 Interactive Guide", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #A23B72;
        border-bottom: 3px solid #A23B72;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .description-box {
        background-color: #F18F01;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .stDataFrame {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HELPER FUNCTIONS FOR CREATING PLOTS
# =============================================================================

def create_mmm_vs_attribution_plot():
    """Create MMM vs Attribution comparison"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Attribution (Individual Journey)", "MMM (Aggregated View)"),
        specs=[[{"type": "scatter"}, {"type": "pie"}]]
    )
    
    # Attribution journey visualization
    fig.add_trace(
        go.Scatter(
            x=[1, 2, 3], y=[2, 2, 2],
            mode='markers+text',
            text=['FB', 'Google', 'Purchase'],
            textposition="middle center",
            marker=dict(size=50, color=['#FF6B6B', '#4ECDC4', '#45B7D1']),
            name="User A",
            showlegend=False
        ), row=1, col=1
    )
    
    # Add arrows
    fig.add_annotation(x=1.5, y=2, ax=1, ay=2, xref="x", yref="y", axref="x", ayref="y",
                      arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="black", row=1, col=1)
    fig.add_annotation(x=2.5, y=2, ax=2, ay=2, xref="x", yref="y", axref="x", ayref="y",
                      arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="black", row=1, col=1)
    
    # MMM pie chart
    labels = ['TV (35%)', 'Search (25%)', 'Social (20%)', 'Radio (20%)']
    values = [35, 25, 20, 20]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    fig.add_trace(
        go.Pie(labels=labels, values=values, marker_colors=colors, textinfo='label+percent'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False, title_text="MMM vs Attribution Comparison")
    fig.update_xaxes(showgrid=False, showticklabels=False, row=1, col=1)
    fig.update_yaxes(showgrid=False, showticklabels=False, row=1, col=1)
    
    return fig

def create_sales_decomposition_plot():
    """Create sales decomposition stacked area chart"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    baseline = [2.0] * 12
    media = [2.5, 2.3, 2.7, 2.4, 2.6, 2.2, 2.8, 2.5, 2.4, 2.9, 3.2, 3.1]
    external = [0.3, 0.2, 0.4, 0.2, 0.3, 0.1, 0.2, 0.3, 0.2, 0.4, 0.5, 0.3]
    seasonal = [0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.2, 0.3, 0.8, 0.9]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=months, y=baseline, fill='tonexty', name='Baseline (40%)', 
                            line_color='#2E86AB', fillcolor='rgba(46, 134, 171, 0.6)'))
    fig.add_trace(go.Scatter(x=months, y=[b+m for b,m in zip(baseline, media)], fill='tonexty', 
                            name='Media (50%)', line_color='#A23B72', fillcolor='rgba(162, 59, 114, 0.6)'))
    fig.add_trace(go.Scatter(x=months, y=[b+m+e for b,m,e in zip(baseline, media, external)], fill='tonexty',
                            name='External (6%)', line_color='#F18F01', fillcolor='rgba(241, 143, 1, 0.6)'))
    fig.add_trace(go.Scatter(x=months, y=[b+m+e+s for b,m,e,s in zip(baseline, media, external, seasonal)], fill='tonexty',
                            name='Seasonal (4%)', line_color='#C73E1D', fillcolor='rgba(199, 62, 29, 0.6)'))
    
    fig.update_layout(title="Sales Decomposition Over Time", xaxis_title="Month", yaxis_title="Sales ($M)", height=400)
    return fig

def create_saturation_curve():
    """Create channel saturation curve"""
    spend = np.linspace(0, 2000, 100)
    half_sat = 300
    alpha = 0.7
    max_revenue = 3.0
    
    revenue = max_revenue * (spend**alpha) / (spend**alpha + half_sat**alpha)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=spend, y=revenue, mode='lines', name='TV Response',
                            line=dict(color='#2E86AB', width=4)))
    
    # Add zones
    fig.add_vrect(x0=0, x1=500, fillcolor="green", opacity=0.2, layer="below", line_width=0)
    fig.add_vrect(x0=500, x1=1500, fillcolor="yellow", opacity=0.2, layer="below", line_width=0)
    fig.add_vrect(x0=1500, x1=2000, fillcolor="red", opacity=0.2, layer="below", line_width=0)
    
    # Add vertical lines
    fig.add_vline(x=half_sat, line_dash="dash", line_color="gray", annotation_text="Half-Saturation ($300K)")
    fig.add_vline(x=1200, line_dash="dash", line_color="red", annotation_text="Current Spend ($1.2M)")
    
    fig.update_layout(title="TV Channel Saturation Curve", xaxis_title="Spend ($K)", 
                     yaxis_title="Revenue ($M)", height=400)
    return fig

def create_adstock_decay():
    """Create adstock decay comparison"""
    weeks = list(range(1, 9))
    tv_decay = [100 * (0.6 ** (w-1)) for w in weeks]
    search_decay = [100 * (0.1 ** (w-1)) for w in weeks]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=weeks, y=tv_decay, mode='lines+markers', name='TV (λ=0.6)',
                            line=dict(color='#2E86AB', width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=weeks, y=search_decay, mode='lines+markers', name='Search (λ=0.1)',
                            line=dict(color='#F18F01', width=3), marker=dict(size=8)))
    
    fig.update_layout(title="Adstock Decay Patterns by Channel", xaxis_title="Weeks After Ad Exposure",
                     yaxis_title="Impact Retention (%)", height=400)
    return fig

def create_channel_roi_comparison():
    """Create horizontal bar chart for channel ROI"""
    channels = ['Print', 'Radio', 'TV', 'Social', 'Search']
    roi_values = [1.2, 1.9, 2.8, 3.1, 4.2]
    colors = ['#C73E1D', '#F18F01', '#2E86AB', '#A23B72', '#45B7D1']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(y=channels, x=roi_values, orientation='h', 
                        marker_color=colors, text=[f'{roi}:1' for roi in roi_values],
                        textposition='outside'))
    
    fig.add_vline(x=2.0, line_dash="dash", line_color="red", annotation_text="Target ROI (2.0)")
    fig.update_layout(title="Channel ROI Comparison", xaxis_title="ROI (Revenue per $ Spent)",
                     height=400)
    return fig

def create_validation_radar():
    """Create radar chart for validation scorecard"""
    categories = ['Statistical Fit', 'Significance', 'Out-of-Sample', 'Business Logic', 'Residual Analysis']
    scores = [95, 92, 88, 85, 90]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Current Score',
        line_color='#2E86AB',
        fillcolor='rgba(46, 134, 171, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False,
        title="Model Validation Scorecard - Overall: 90%",
        height=400
    )
    return fig

def create_response_curves():
    """Create response curves for optimization"""
    spend_tv = np.linspace(0, 2000, 100)
    spend_search = np.linspace(0, 800, 100)
    
    revenue_tv = 3.5 * (spend_tv**0.7) / (spend_tv**0.7 + 600**0.7)
    revenue_search = 4.0 * (spend_search**0.5) / (spend_search**0.5 + 200**0.5)
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=("TV Response Curve", "Search Response Curve"))
    
    # TV curve
    fig.add_trace(go.Scatter(x=spend_tv, y=revenue_tv, mode='lines', name='TV Response',
                            line=dict(color='#2E86AB', width=3)), row=1, col=1)
    fig.add_vline(x=1200, line_dash="dash", line_color="red", row=1, col=1)
    fig.add_vline(x=800, line_dash="dash", line_color="green", row=1, col=1)
    
    # Search curve
    fig.add_trace(go.Scatter(x=spend_search, y=revenue_search, mode='lines', name='Search Response',
                            line=dict(color='#F18F01', width=3)), row=1, col=2)
    fig.add_vline(x=300, line_dash="dash", line_color="red", row=1, col=2)
    fig.add_vline(x=500, line_dash="dash", line_color="green", row=1, col=2)
    
    fig.update_layout(height=400, showlegend=False, title_text="Response Curves for Budget Optimization")
    fig.update_xaxes(title_text="Spend ($K)")
    fig.update_yaxes(title_text="Revenue ($M)")
    
    return fig

def create_budget_optimization():
    """Create budget optimization comparison"""
    channels = ['TV', 'Search', 'Social', 'Radio', 'Display']
    current_budget = [1200, 300, 450, 450, 350]
    optimal_budget = [1000, 500, 550, 400, 300]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(name='Current Budget', x=channels, y=current_budget, 
                        marker_color='#C73E1D', opacity=0.8))
    fig.add_trace(go.Bar(name='Optimal Budget', x=channels, y=optimal_budget,
                        marker_color='#2E86AB', opacity=0.8))
    
    fig.update_layout(barmode='group', title="Budget Optimization: Current vs Optimal Allocation",
                     xaxis_title="Channel", yaxis_title="Budget ($K)", height=400)
    return fig

def create_industry_benchmarks():
    """Create industry ROI benchmarks"""
    industries = ['Auto', 'CPG', 'Retail', 'Tech B2B', 'FinServ', 'Healthcare']
    roi_low = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
    roi_high = [4.0, 4.5, 5.0, 6.0, 7.0, 8.0]
    roi_avg = [3.0, 3.5, 4.0, 4.8, 5.5, 6.2]
    
    fig = go.Figure()
    
    for i, industry in enumerate(industries):
        fig.add_trace(go.Scatter(
            x=[roi_low[i], roi_avg[i], roi_high[i]], 
            y=[industry, industry, industry],
            mode='lines+markers',
            name=industry,
            line=dict(width=8),
            marker=dict(size=[8, 12, 8])
        ))
    
    fig.update_layout(title="Marketing ROI Benchmarks by Industry", 
                     xaxis_title="ROI Range", yaxis_title="Industry", height=400)
    return fig

def create_kpi_dashboard():
    """Create KPI dashboard"""
    kpis = ['Model Quality', 'Prediction Accuracy', 'Statistical Significance', 
            'Business Impact', 'Stakeholder Adoption', 'ROI Improvement']
    scores = [95, 92, 88, 85, 78, 72]
    targets = [90, 85, 80, 80, 80, 75]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(name='Current Score', x=kpis, y=scores, 
                        marker_color='#2E86AB', opacity=0.8))
    fig.add_trace(go.Bar(name='Target', x=kpis, y=targets,
                        marker_color='#A23B72', opacity=0.6))
    
    fig.update_layout(barmode='group', title="MMM Key Performance Indicators",
                     xaxis_title="KPI Category", yaxis_title="Score (%)", height=400)
    fig.update_xaxes(tickangle=45)
    return fig

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    st.markdown('<h1 class="main-header">📊 MMM 101: Interactive Guide with Live Charts</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
    Complete Media Mix Modeling reference with interactive visualizations and comprehensive tables
    </div>
    """, unsafe_allow_html=True)
    
    # =============================================================================
    # 1. MMM FUNDAMENTALS
    # =============================================================================
    
    st.markdown('<h2 class="section-header">🎯 MMM Fundamentals</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="description-box">
    <strong>Understanding the Basics:</strong> Media Mix Modeling is like having a sophisticated GPS for your marketing budget - it shows you exactly which routes (channels) are getting you to your destination (sales) most efficiently. Unlike digital attribution that tracks individual customer journeys, MMM looks at the big picture using aggregated data.
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for table and chart
    col1, col2 = st.columns([3, 2])
    
    with col1:
        fundamentals_data = {
            'Concept': ['Media Mix Modeling', 'vs Digital Attribution', 'Privacy-First Solution', 'Business Outcome Focus'],
            'Definition': [
                'Statistical technique measuring marketing impact across all channels simultaneously',
                'MMM = big picture view, Attribution = individual user journey tracking',
                'Works without cookies, user IDs, or personal data - perfect for privacy regulations',
                'Directly connects marketing spend to revenue/sales/conversions with statistical confidence'
            ],
            'Key Point': [
                'Privacy-safe, uses aggregated weekly/monthly data instead of individual tracking',
                'MMM shows channel effectiveness over time, attribution shows user click paths',
                'Perfect for iOS 14.5+, GDPR compliance, cookieless future measurement',
                'Shows incremental impact above baseline business performance'
            ],
            'Concrete Example': [
                'Coffee chain: $1M TV, $500K Facebook, $300K Google → MMM shows TV drove 35% of sales',
                'Attribution: "User saw Facebook ad, clicked Google ad, bought product." MMM: "Facebook creates awareness that makes Google 40% more effective"',
                'Uses only: Weekly TV spend ($50K), weekly sales ($200K), external factors (holidays, weather)',
                'Baseline sales: $2M/month. With marketing: $3.5M/month. MMM shows which $1.5M came from which channels'
            ]
        }
        
        df_fundamentals = pd.DataFrame(fundamentals_data)
        st.dataframe(df_fundamentals, use_container_width=True, height=300)
    
    with col2:
        fig_mmm_attribution = create_mmm_vs_attribution_plot()
        st.plotly_chart(fig_mmm_attribution, use_container_width=True)
    
    # =============================================================================
    # 2. CORE MMM EQUATION COMPONENTS
    # =============================================================================
    
    st.markdown('<h2 class="section-header">🧮 Core MMM Equation Components</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="description-box">
    <strong>The Mathematical Foundation:</strong> Think of MMM like a recipe that explains your total sales. Just as a cake recipe shows how flour, sugar, and eggs combine to create the final product, MMM shows how baseline business, marketing activities, external factors, and seasonality combine to create your total sales.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        equation_data = {
            'Component': ['Complete MMM Equation', 'Baseline (β₀)', 'Media Effects', 'External Factors', 'Seasonality'],
            'Formula': [
                'Sales = Baseline + Media + External + Seasonality + Error',
                'β₀ = $2,000,000',
                'β₁×TV + β₂×Digital + β₃×Radio',
                'γ×Economy + δ×Weather + ε×Competitors',
                'α×Holiday + θ×Trend'
            ],
            'What It Measures': [
                'Breaks down every dollar of sales into its root cause',
                'Your organic business strength - sales without any marketing',
                'How much incremental sales each marketing channel drives',
                'Non-marketing business drivers that affect sales',
                'Predictable cyclical patterns and long-term trends'
            ],
            'Concrete Example': [
                'Monthly Sales $5M = $2M baseline + $2.5M marketing + $300K Black Friday + $200K error',
                'Software company: $2M baseline monthly revenue from word-of-mouth, organic search, existing customers',
                'TV coefficient 2.5 × $400K spend = $1M incremental. Google coefficient 3.0 × $200K = $600K incremental',
                '10% GDP growth = +$200K sales. Competitor launch = -$150K. Heat wave = +$100K (ice cream)',
                'Black Friday = +40% sales. December = +25%. 5% annual growth trend'
            ]
        }
        
        df_equation = pd.DataFrame(equation_data)
        st.dataframe(df_equation, use_container_width=True, height=300)
    
    with col2:
        fig_sales_decomp = create_sales_decomposition_plot()
        st.plotly_chart(fig_sales_decomp, use_container_width=True)
    
    # =============================================================================
    # 3. MMM COEFFICIENT TYPES & INTERPRETATION
    # =============================================================================
    
    st.markdown('<h2 class="section-header">🔢 MMM Coefficient Types & Interpretation</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="description-box">
    <strong>Decoding the Numbers:</strong> MMM coefficients are like efficiency ratings for your marketing channels. Just as miles-per-gallon tells you how efficient your car is, MMM coefficients tell you how efficiently each marketing channel converts spend into sales. Understanding these numbers is crucial for budget optimization.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        coefficients_data = {
            'Coefficient Type': ['Media Coefficient (β)', 'Saturation Alpha (α)', 'Half-Saturation Point', 'Adstock Lambda (λ)', 'Peak Delay (P)', 'Baseline Trend'],
            'Formula/Range': ['β = 0.5 to 5.0', 'α = 0.3 to 1.0', '$10K to $1M+', 'λ = 0.1 to 0.8', 'P = 0 to 8 weeks', '+/-2% per month'],
            'What It Measures': [
                'Direct return on investment - dollars in sales per dollar spent',
                'How quickly diminishing returns kick in. Lower α = faster saturation',
                'Spend level where you get 50% of maximum possible effectiveness',
                'How much advertising impact carries over to next period',
                'Time until advertising reaches maximum effectiveness',
                'Underlying business growth/decline independent of marketing'
            ],
            'Detailed Example': [
                'β = 2.5 for TV: Spend $100K on TV → Generate $250K in sales → Net profit depends on margins',
                'α = 0.5: First $100K very effective, next $100K less effective, third $100K much less effective',
                'Half-saturation at $200K: $200K spend gets 50% max impact, $400K gets ~75%, $800K gets ~87%',
                'λ = 0.4: Week 1 impact = 100%, Week 2 = 40%, Week 3 = 16%, Week 4 = 6.4%',
                'P = 3 weeks: TV ad airs Week 1, but peak sales impact occurs in Week 4',
                '+3%/month trend: business growing organically 3% monthly even without marketing changes'
            ]
        }
        
        df_coeffs = pd.DataFrame(coefficients_data)
        st.dataframe(df_coeffs, use_container_width=True, height=350)
    
    with col2:
        # Show saturation curve and adstock decay in tabs
        tab1, tab2, tab3 = st.tabs(["Saturation Curve", "Adstock Decay", "Channel ROI"])
        
        with tab1:
            fig_saturation = create_saturation_curve()
            st.plotly_chart(fig_saturation, use_container_width=True)
        
        with tab2:
            fig_adstock = create_adstock_decay()
            st.plotly_chart(fig_adstock, use_container_width=True)
        
        with tab3:
            fig_roi = create_channel_roi_comparison()
            st.plotly_chart(fig_roi, use_container_width=True)
    
    # =============================================================================
    # 4. CHANNEL-SPECIFIC COEFFICIENT BENCHMARKS
    # =============================================================================
    
    st.markdown('<h2 class="section-header">📺 Channel-Specific Coefficient Benchmarks</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="description-box">
    <strong>Industry Reality Check:</strong> Different marketing channels behave very differently. TV builds awareness slowly but has lasting impact. Search captures immediate demand. Social creates engagement that takes time to convert. Use these benchmarks to validate your model results and set realistic expectations.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        benchmarks_data = {
            'Channel': ['TV', 'Digital Display', 'Paid Search', 'Social Media', 'Radio', 'Print', 'Out-of-Home'],
            'Typical β Range': ['1.5 - 4.0', '0.8 - 2.5', '2.0 - 6.0', '1.2 - 3.5', '1.0 - 2.8', '0.5 - 2.0', '0.8 - 2.2'],
            'Typical Adstock (λ)': ['0.4 - 0.7', '0.1 - 0.3', '0.0 - 0.2', '0.2 - 0.4', '0.3 - 0.6', '0.1 - 0.4', '0.2 - 0.5'],
            'Typical Peak Delay': ['1-3 weeks', '0-1 weeks', '0-1 weeks', '1-2 weeks', '1-2 weeks', '2-4 weeks', '1-3 weeks'],
            'Saturation Point': ['$500K - $2M', '$100K - $500K', '$50K - $200K', '$200K - $800K', '$300K - $1M', '$200K - $600K', '$400K - $1.2M'],
            'Real Example': [
                'National TV: β=2.8, λ=0.6, P=2 weeks. $1M spend → $2.8M sales over 8 weeks',
                'Banner ads: β=1.2, λ=0.2, P=0 weeks. $200K spend → $240K immediate sales',
                'Google Ads: β=4.5, λ=0.1, P=0 weeks. $100K spend → $450K immediate sales',
                'Facebook: β=2.1, λ=0.3, P=1 week. $300K spend → $630K sales over 6 weeks',
                'Local radio: β=1.8, λ=0.4, P=1 week. $400K spend → $720K sales over 10 weeks',
                'Magazine: β=1.3, λ=0.2, P=3 weeks. $250K spend → $325K sales over 12 weeks',
                'Billboards: β=1.5, λ=0.3, P=2 weeks. $600K spend → $900K sales over 8 weeks'
            ]
        }
        
        df_benchmarks = pd.DataFrame(benchmarks_data)
        st.dataframe(df_benchmarks, use_container_width=True, height=400)
    
    with col2:
        fig_industry = create_industry_benchmarks()
        st.plotly_chart(fig_industry, use_container_width=True)
    
    # =============================================================================
    # 5. MODEL VALIDATION CHECKLIST
    # =============================================================================
    
    st.markdown('<h2 class="section-header">✅ Model Validation Checklist</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="description-box">
    <strong>Quality Assurance:</strong> Model validation is like getting a medical second opinion - you need multiple perspectives to ensure your diagnosis (model results) is correct. Each validation check catches different types of problems, from statistical issues to business logic failures. Never skip this step.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        validation_data = {
            'Validation Type': ['Statistical Fit', 'Coefficient Signs', 'Statistical Significance', 'Business Logic', 'Out-of-Sample', 'Residual Analysis', 'Cross-Validation'],
            'Check': ['R-squared goodness of fit', 'All media coefficients positive', 'Confidence intervals/p-values', 'ROI within reasonable ranges', 'Prediction accuracy on holdout', 'Error patterns over time', 'Performance across time periods'],
            'Good Result': ['R² > 0.75', 'All β > 0', '90%+ coefficients significant', 'ROI matches industry benchmarks', 'MAPE < 15% on holdout period', 'Random residuals, no patterns', 'Consistent performance'],
            'Red Flag': ['R² < 0.50', 'Any β < 0', '<70% significant', 'ROI 10× industry average', 'MAPE > 25%', 'Systematic patterns in errors', 'Varies wildly by period'],
            'Concrete Example': [
                'Model explains 83% of sales variation. Residual plots show random scatter',
                'TV β = +2.3, Search β = +4.1, Display β = +1.2 ✓ (all positive)',
                'TV β = 2.3 ± 0.4 (significant), Radio β = 0.8 ± 0.9 (not significant)',
                'Your TV ROI: 2.3. Industry benchmark: 1.5-3.5 ✓. Competitor estimate: 2.1 ✓',
                'Predicted Q4 sales: $8.2M. Actual Q4: $8.5M. Error: 3.7% ✓',
                'Residuals randomly distributed around zero. No correlation with seasonality',
                'Model MAPE: 2019=8%, 2020=12%, 2021=9% (consistent)'
            ]
        }
        
        df_validation = pd.DataFrame(validation_data)
        st.dataframe(df_validation, use_container_width=True, height=400)
    
    with col2:
        fig_validation = create_validation_radar()
        st.plotly_chart(fig_validation, use_container_width=True)
    
    # =============================================================================
    # 6. MMM OUTPUT INTERPRETATION GUIDE
    # =============================================================================
    
    st.markdown('<h2 class="section-header">📊 MMM Output Interpretation Guide</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="description-box">
    <strong>Turning Numbers into Strategy:</strong> MMM outputs are like a financial report for your marketing - they tell you what happened, what's working, and what to do next. Each metric answers specific business questions and drives different types of decisions. Understanding these outputs transforms analysis into action.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        outputs_data = {
            'Output Type': ['Channel ROI', 'Marginal ROI', 'Contribution %', 'Saturation Level', 'Response Curves', 'Scenario Planning'],
            'Formula': [
                '(Incremental Revenue - Media Spend) / Media Spend',
                '∂Revenue/∂Spend at current spending level',
                'Channel Incremental Revenue / Total Incremental Revenue × 100',
                'Current Spend / Half-Saturation Point',
                'Revenue = f(Spend) showing relationship',
                'If spend changes by X%, revenue changes by Y%'
            ],
            'Business Question Answered': [
                'Which channels give best return on investment?',
                'If I spend one more dollar, which channel gives highest return?',
                'How much does each channel contribute to my marketing-driven growth?',
                'How close am I to diminishing returns on each channel?',
                'How does effectiveness change as I spend more or less?',
                'What happens to my business if I reallocate budget?'
            ],
            'Concrete Example': [
                'TV ROI: ($2.8M - $1M) / $1M = 1.8 → $1.80 profit per $1 spent',
                'At current spending: TV marginal ROI = $1.20, Search marginal ROI = $2.80',
                'Total marketing revenue: $5M. TV: $2M (40%), Search: $1.5M (30%), Social: $1M (20%)',
                'TV: $1M spend / $600K half-saturation = 1.67 → In diminishing returns',
                'TV curve shows: $0-500K steep, $500K-1M moderate, $1M+ flat. Current at $1M in flat zone',
                'Scenario: Move $200K from TV to Search. Result: -$180K from TV, +$280K from Search = +$100K net'
            ]
        }
        
        df_outputs = pd.DataFrame(outputs_data)
        st.dataframe(df_outputs, use_container_width=True, height=350)
    
    with col2:
        tab1, tab2 = st.tabs(["Response Curves", "Budget Optimization"])
        
        with tab1:
            fig_response = create_response_curves()
            st.plotly_chart(fig_response, use_container_width=True)
        
        with tab2:
            fig_budget = create_budget_optimization()
            st.plotly_chart(fig_budget, use_container_width=True)
    
    # =============================================================================
    # 7. COMMON MMM CHALLENGES & SOLUTIONS
    # =============================================================================
    
    st.markdown('<h2 class="section-header">⚠️ Common MMM Challenges & Solutions</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="description-box">
    <strong>Troubleshooting Guide:</strong> Every MMM project faces predictable challenges. Like a doctor's diagnostic manual, this guide helps you identify symptoms, understand root causes, and apply proven treatments. Learning from others' mistakes saves months of troubleshooting.
    </div>
    """, unsafe_allow_html=True)
    
    challenges_data = {
        'Challenge': ['Multicollinearity', 'Data Quality Issues', 'Attribution Windows', 'Baseline Drift', 'Saturation Misspecification', 'External Factor Omission'],
        'Problem Description': [
            'Two+ channels always move together, cannot separate their individual effects',
            'Missing data, inconsistent definitions, reporting errors across sources',
            'Unclear how long advertising effects last, impacts ROI calculations significantly',
            'Organic sales changing over time due to brand building, word-of-mouth effects',
            'Wrong curve shape leads to wrong optimization recommendations',
            'Missing important non-marketing drivers biases coefficient results'
        ],
        'Impact on Business': [
            'Wrong budget allocation decisions, over/under-investment in correlated channels',
            'Unreliable model results, wrong business decisions, stakeholder distrust',
            'Wrong ROI calculations, poor budget timing decisions, missed opportunities',
            'Marketing gets wrong credit/blame for organic business changes',
            'Over-investment in saturated channels, missed growth opportunities',
            'Marketing blamed/credited for external factors beyond control'
        ],
        'Concrete Example': [
            'TV and Radio always launch together. Model shows TV β=5.0, Radio β=-1.0 (impossible)',
            'Facebook reports $50K spend, finance shows $65K. Missing 2 weeks TV data due to system change',
            'TV coefficient changes from 2.0 (2-week window) to 4.5 (8-week window). Which is right?',
            'Sales grew 20% but marketing spend flat. Is it marketing effectiveness or brand strength?',
            'Hill curve shows TV saturated at $500K, but business reality suggests $2M saturation point',
            'COVID impact not modeled. Marketing looks ineffective in 2020, super effective in 2021'
        ],
        'Step-by-Step Solution': [
            '1) Check correlation matrix 2) Combine correlated channels 3) Use Ridge regression 4) Plan uncorrelated tests',
            '1) Data audit across sources 2) Create data dictionary 3) Implement validation rules 4) Use proxy metrics',
            '1) Test multiple adstock specifications 2) Use business knowledge 3) Validate with experiments 4) Choose conservative',
            '1) Add time trends to model 2) Include brand health metrics 3) Use hierarchical modeling 4) Regular refresh',
            '1) Test multiple curve types 2) Use business knowledge 3) Validate with experiments 4) Compare to benchmarks',
            '1) Brainstorm all business drivers 2) Collect external data 3) Include systematically 4) Validate impact'
        ]
    }
    
    df_challenges = pd.DataFrame(challenges_data)
    st.dataframe(df_challenges, use_container_width=True, height=400)
    
    # =============================================================================
    # 8. BUDGET OPTIMIZATION QUICK REFERENCE
    # =============================================================================
    
    st.markdown('<h2 class="section-header">💰 Budget Optimization Quick Reference</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="description-box">
    <strong>From Analysis to Action:</strong> Budget optimization is where MMM delivers tangible business value. Like a financial advisor recommending portfolio rebalancing, MMM shows you how to reallocate marketing spend for maximum return. Each optimization type serves different business needs and planning cycles.
    </div>
    """, unsafe_allow_html=True)
    
    optimization_data = {
        'Optimization Type': ['Simple Reallocation', 'Marginal ROI Balancing', 'Response Curve Optimization', 'Scenario Planning', 'Real-time Optimization'],
        'When to Use': [
            'Clear over/under-performers visible in current results',
            'Channels at different saturation levels, diminishing returns visible',
            'Sophisticated budget planning, multiple scenarios needed',
            'Annual budget setting, what-if analysis for different budget levels',
            'Dynamic budget management, weekly/monthly adjustments'
        ],
        'Expected Improvement': ['5-15% efficiency gain', '10-20% efficiency gain', '15-25% efficiency gain', 'Strategic insights, risk assessment', 'Ongoing 3-8% improvements'],
        'Time Required': ['1 week analysis', '2 weeks analysis', '3-4 weeks analysis', '2-3 weeks analysis', 'Continuous process'],
        'Concrete Example': [
            'Radio ROI 0.8, Search ROI 3.2. Move $100K from Radio to Search. Gain: -$80K + $320K = +$240K',
            'TV marginal ROI $1.50, Search marginal ROI $2.80. Shift budget until both equal ~$2.00 marginal ROI',
            'Full optimization across 8 channels with constraints. Current $5M budget → optimal allocation increases revenue 18%',
            'Budget cut 20%: Revenue drops 12%. Budget increase 30%: Revenue increases 18%. Optimal budget: +15% for +25% revenue',
            'Weekly budget adjustments based on performance. Week 12: TV underperforming, shift $50K to Search mid-campaign'
        ],
        'Business Impact': [
            'Quick wins, easy stakeholder buy-in, immediate implementation possible',
            'Optimal efficiency, mathematical foundation, sustainable long-term strategy',
            'Maximum impact, handles complexity, provides strategic competitive advantage',
            'Strategic planning support, risk management, executive-level insights for annual planning',
            'Agile marketing approach, competitive advantage, continuous improvement culture'
        ]
    }
    
    df_optimization = pd.DataFrame(optimization_data)
    st.dataframe(df_optimization, use_container_width=True, height=300)
    
    # =============================================================================
    # 9. KEY PERFORMANCE INDICATORS (KPIS) FOR MMM SUCCESS
    # =============================================================================
    
    st.markdown('<h2 class="section-header">📈 Key Performance Indicators (KPIs) for MMM Success</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="description-box">
    <strong>Measuring Your MMM Program:</strong> Like a health checkup for your MMM, these KPIs help you monitor model performance, business impact, and organizational adoption. Regular monitoring prevents small issues from becoming big problems and ensures your MMM investment delivers sustained value.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        kpi_data = {
            'KPI Category': ['Model Quality', 'Prediction Accuracy', 'Statistical Significance', 'Business Impact', 'Stakeholder Adoption', 'ROI Improvement'],
            'Metric': ['R-squared (model fit)', 'MAPE (Mean Absolute Percentage Error)', '% of coefficients statistically significant', 'Revenue lift from optimization recommendations', '% of budget decisions using MMM insights', 'Year-over-year marketing efficiency gains'],
            'Good Performance': ['R² > 0.75', 'MAPE < 15%', '>80% of channels significant', '>10% efficiency improvement', '>75% of decisions MMM-informed', '>15% YoY efficiency'],
            'Poor Performance': ['R² < 0.50', 'MAPE > 25%', '<60% significant', '<5% improvement', '<50% usage', '<5% improvement'],
            'Concrete Example': [
                'Current model: R² = 0.82 explains 82% of sales variation. Previous model: R² = 0.73',
                'Q1 forecast: Predicted $12.5M, Actual $11.8M. Error: |12.5-11.8|/11.8 = 5.9% ✓',
                '8 channels modeled, 7 have p<0.05 (87.5% significant). Only Radio insignificant',
                'Implemented Q1 recommendations: $5M budget generated $23M revenue vs $20M predicted baseline (+15%)',
                '12 budget decisions in Q1: 10 used MMM insights (83%). 2 ignored due to brand campaign timing',
                '2023 overall ROI: 3.2:1. 2024 ROI: 3.8:1. Improvement: (3.8-3.2)/3.2 = +18.8% ✓'
            ]
        }
        
        df_kpi = pd.DataFrame(kpi_data)
        st.dataframe(df_kpi, use_container_width=True, height=350)
    
    with col2:
        fig_kpi = create_kpi_dashboard()
        st.plotly_chart(fig_kpi, use_container_width=True)
    
    # =============================================================================
    # 10. ADVANCED MMM CONCEPTS
    # =============================================================================
    
    st.markdown('<h2 class="section-header">🚀 Advanced MMM Concepts</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="description-box">
    <strong>Beyond the Basics:</strong> Once you've mastered fundamental MMM, these advanced concepts help you handle complex business situations, improve model accuracy, and extract deeper insights. Like advanced driving techniques, these skills separate MMM practitioners from MMM experts.
    </div>
    """, unsafe_allow_html=True)
    
    advanced_data = {
        'Advanced Concept': ['Interaction Effects', 'Geo-Level Modeling', 'Time-Varying Coefficients', 'Reach & Frequency Optimization', 'Incrementality Integration', 'Competition Modeling'],
        'What It Addresses': [
            'How channels work together vs independently',
            'Different market performance across regions',
            'Channel effectiveness changes over time',
            'Optimizes exposure levels, not just spend',
            'Combines MMM with experiment results',
            'How competitor activity affects your performance'
        ],
        'When to Use': [
            'Channels clearly amplify each other',
            'National brands with regional variations',
            'Market maturity, competitive changes',
            'Channels with reach/frequency data available',
            'MMM results conflict with test results',
            'Highly competitive markets'
        ],
        'Concrete Example': [
            'TV + Search interaction: TV alone β=2.0, Search alone β=3.0, but TV+Search together β=2.5 + 4.2 = 6.7 total',
            'Seattle: TV β=1.8, Search β=4.5. Atlanta: TV β=3.2, Search β=2.1. Optimize by market',
            'TV effectiveness: 2021 β=3.0, 2022 β=2.5, 2023 β=2.0 (declining due to cord-cutting)',
            'TV: Optimal frequency 3.2 exposures/person/week. Current: 2.1. Increase frequency 50%, reduce reach 30%',
            'MMM shows Facebook β=2.5, but geo-test shows β=1.8. Truth likely β=2.0±0.3',
            'When competitor increases TV 50%, your TV effectiveness drops 15%. Include competitor spend as negative coefficient'
        ],
        'Implementation Complexity': ['High - requires interaction terms', 'Very High - hierarchical Bayesian', 'High - dynamic parameter estimation', 'Medium - requires additional data', 'Medium - Bayesian updating', 'Medium - requires competitor data'],
        'Business Benefit': [
            'Reveals channel synergies, optimizes cross-channel timing',
            'Local optimization, market-specific insights, better accuracy',
            'Adapts to market changes, identifies trends, improves forecasting',
            'Fine-tunes campaign delivery, improves creative efficiency',
            'Improves accuracy, builds stakeholder confidence, validates results',
            'Anticipates competitive impact, informs defensive strategies'
        ]
    }
    
    df_advanced = pd.DataFrame(advanced_data)
    st.dataframe(df_advanced, use_container_width=True, height=350)
    
    # =============================================================================
    # FOOTER
    # =============================================================================
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;">
    📊 This comprehensive MMM 101 guide provides everything needed to understand, implement, and excel with Media Mix Modeling.<br>
    Interactive charts powered by Plotly • Tables with real-world examples • Ready for business application
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()