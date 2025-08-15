import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="MMM Common Pitfalls 101",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better visuals
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Cards and sections */
    .stExpander {
        background-color: #ffffff;
        border: 1px solid #e3e6e9;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Headers styling */
    h1 {
        color: #1e3a5f;
        font-weight: 700;
        padding-bottom: 1rem;
        border-bottom: 3px solid #4c78a8;
    }
    
    h2 {
        color: #2c5282;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #3d5a80;
        font-weight: 500;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4c78a8;
        margin: 1rem 0;
    }
    
    .beginner-note {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
        font-size: 0.95rem;
    }
    
    .solution-box {
        background: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #ffebee;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #f44336;
        margin: 1rem 0;
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Category badges */
    .easy-badge {
        background: #4caf50;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .tricky-badge {
        background: #ff9800;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 📊 MMM Common Pitfalls 101: A Beginner's Guide")
st.markdown("""
<div class="info-box">
<h4>🎯 Welcome to Your MMM Troubleshooting Guide!</h4>
<p>Think of Marketing Mix Modeling (MMM) as detective work - you're trying to figure out which marketing channels are actually driving sales. 
But there are 6 common traps that can fool even experienced detectives. This guide will help you spot and fix them!</p>
<p><strong>How to use this guide:</strong> Scroll through each section to understand the problem, see real examples, and learn solutions. 
Green boxes = helpful tips, Orange boxes = beginner notes, Red boxes = warnings.</p>
</div>
""", unsafe_allow_html=True)

# Quick overview
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Easy to Understand", "2 Pitfalls", "But tricky to fix")
with col2:
    st.metric("Tricky to Understand", "4 Pitfalls", "Need technical knowledge")
with col3:
    st.metric("Business Impact", "$1-10M", "Per mistake!")

st.markdown("---")

# =============================================================================
# PITFALL 1: DATA QUALITY ISSUES
# =============================================================================

st.markdown("## 1️⃣ Data Quality Issues")
st.markdown('<span class="easy-badge">EASY TO UNDERSTAND</span>', unsafe_allow_html=True)

st.markdown("""
<div class="beginner-note">
<strong>🔰 Beginner's Note:</strong> This is the "garbage in, garbage out" problem. Imagine trying to bake a cake but your recipe says 
"2 cups" in one place and "3 cups" in another place for the same ingredient. Which do you trust? That's what happens when different 
departments report different numbers for the same marketing spend.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📊 The Problem Visualized")
    
    # Create data discrepancy visualization
    data_sources = pd.DataFrame({
        'Source': ['Meta Platform', 'Finance Dept', 'Agency', 'Data Warehouse'],
        'Facebook Spend': [55000, 50000, 60000, 52500],
        'Google Spend': [80000, 78000, 85000, 79000],
        'TV Spend': [120000, 125000, np.nan, 122000]
    })
    
    fig = go.Figure()
    colors = ['#4c78a8', '#f28e2c', '#e15759']
    for i, col in enumerate(['Facebook Spend', 'Google Spend', 'TV Spend']):
        fig.add_trace(go.Bar(
            name=col.replace(' Spend', ''),
            x=data_sources['Source'],
            y=data_sources[col],
            text=data_sources[col].apply(lambda x: f'${x/1000:.0f}K' if pd.notna(x) else 'Missing'),
            textposition='auto',
            marker_color=colors[i],
            opacity=0.8
        ))
    
    fig.update_layout(
        title="Same Data, Different Numbers - Who's Right?",
        xaxis_title="Where You Get The Data",
        yaxis_title="How Much They Say You Spent ($)",
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="beginner-note">
    <strong>What you're seeing:</strong> Four different sources reporting different numbers for the same thing! 
    Facebook spend varies by $10K depending on who you ask. The Agency doesn't even have TV data (that's the "Missing" bar).
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🔍 Why This Happens")
    
    st.markdown("""
    <div class="warning-box">
    <strong>Common Causes:</strong>
    <ul>
    <li><strong>Time zones:</strong> Platform uses PST, Finance uses EST</li>
    <li><strong>Date ranges:</strong> Calendar month vs 30-day rolling</li>
    <li><strong>Currency:</strong> Some in USD, others in local currency</li>
    <li><strong>Taxes:</strong> Some include VAT, others don't</li>
    <li><strong>Credits:</strong> Platform credits not reflected in finance</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✅ The Solution")
    
    st.markdown("""
    <div class="solution-box">
    <strong>Simple Fix:</strong>
    <ol>
    <li><strong>Pick ONE source of truth</strong> (usually the platform itself)</li>
    <li><strong>Document your choice</strong> so everyone knows</li>
    <li><strong>Check monthly</strong> that sources still match</li>
    <li><strong>Create a data dictionary</strong> defining each metric</li>
    </ol>
    
    <strong>Pro tip:</strong> Platform data (like Facebook Ads Manager) is usually most accurate because 
    that's where the spending actually happens!
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# PITFALL 2: EXTERNAL FACTOR OMISSION
# =============================================================================

st.markdown("## 2️⃣ External Factor Omission (Confounders)")
st.markdown('<span class="easy-badge">EASY TO UNDERSTAND</span>', unsafe_allow_html=True)

st.markdown("""
<div class="beginner-note">
<strong>🔰 Beginner's Note:</strong> Imagine your ice cream sales dropped 50% in winter. Was it bad marketing or just cold weather? 
External factors are things outside marketing that affect sales - like COVID, competitors, economy, weather. If you don't account 
for them, marketing gets unfairly blamed (or praised) for things it didn't do.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📉 What Happens When You Forget External Factors")
    
    # Create a simple visualization showing sales drop
    dates = pd.date_range('2020-01-01', periods=24, freq='M')
    sales_with_covid = [100, 102, 98, 60, 55, 50, 55, 60, 70, 75, 80, 85, 
                        88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110]
    marketing_spend = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
                      50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=sales_with_covid,
        name='Sales',
        line=dict(color='#4c78a8', width=3),
        fill='tozeroy',
        fillcolor='rgba(76, 120, 168, 0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=marketing_spend,
        name='Marketing Spend (Constant)',
        line=dict(color='#e15759', width=2, dash='dash')
    ))
    
    # Add COVID annotation
    fig.add_annotation(
        x='2020-04-01', y=60,
        text="COVID hits",
        showarrow=True,
        arrowhead=2,
        arrowcolor='red',
        ax=-50, ay=-30
    )
    
    fig.update_layout(
        title="Sales Crashed But Marketing Didn't Change - What Happened?",
        xaxis_title="Date",
        yaxis_title="Index (Jan 2020 = 100)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="beginner-note">
    <strong>What you're seeing:</strong> Sales dropped 50% in April 2020 (COVID) while marketing spend stayed the same. 
    Without modeling COVID as an external factor, your model would think marketing suddenly became terrible!
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🌍 Common External Factors to Include")
    
    factors_df = pd.DataFrame({
        'Factor': ['🦠 COVID-19', '💰 Economy', '🏢 Competitors', '☀️ Weather', 
                   '📅 Holidays', '📰 PR Events'],
        'Example Impact': ['-40% sales', '±15% sales', '-20% share', '±10% sales', 
                          '+30% sales', '±25% sales'],
        'How to Measure': ['Google Mobility', 'GDP/Unemployment', 'Their ad spend', 
                          'Temperature', 'Calendar', 'Google Trends']
    })
    st.dataframe(factors_df, use_container_width=True, hide_index=True)
    
    st.markdown("### ✅ The Solution")
    
    st.markdown("""
    <div class="solution-box">
    <strong>How to Fix It:</strong>
    <ol>
    <li><strong>List everything</strong> that could affect sales (brainstorm with team)</li>
    <li><strong>Get the data</strong> (most is free - Google Trends, weather, economic data)</li>
    <li><strong>Add to your model</strong> as control variables</li>
    <li><strong>Check if it matters</strong> (if correlation > 0.3 with sales, keep it)</li>
    </ol>
    
    <strong>Remember:</strong> It's better to include too many factors than too few. 
    You can always remove ones that don't matter!
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# PITFALL 3: MULTICOLLINEARITY
# =============================================================================

st.markdown("## 3️⃣ Multicollinearity")
st.markdown('<span class="tricky-badge">TRICKY TO UNDERSTAND</span>', unsafe_allow_html=True)

st.markdown("""
<div class="beginner-note">
<strong>🔰 Beginner's Note:</strong> Imagine Batman and Robin always fight crime together. If crime goes down, who gets the credit? 
It's impossible to tell! That's multicollinearity - when two marketing channels always run together (like TV and Radio), 
the model can't figure out which one is actually working.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🔗 The Problem: Channels Moving Together")
    
    # Generate correlated data
    np.random.seed(42)
    weeks = list(range(1, 13))
    tv_spend = [10, 20, 15, 25, 30, 20, 35, 25, 18, 22, 28, 15]
    radio_spend = [9, 19, 14, 24, 29, 19, 34, 24, 17, 21, 27, 14]  # Almost same as TV
    digital_spend = [30, 25, 35, 20, 28, 32, 25, 30, 35, 28, 22, 30]  # Independent
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks, y=tv_spend, name='TV', 
                            line=dict(color='#4c78a8', width=3),
                            mode='lines+markers'))
    fig.add_trace(go.Scatter(x=weeks, y=radio_spend, name='Radio', 
                            line=dict(color='#e15759', width=3, dash='dash'),
                            mode='lines+markers'))
    fig.add_trace(go.Scatter(x=weeks, y=digital_spend, name='Digital', 
                            line=dict(color='#54a24b', width=2),
                            mode='lines+markers'))
    
    fig.update_layout(
        title="TV and Radio Move Together - Model Gets Confused!",
        xaxis_title="Week",
        yaxis_title="Spend ($K)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="beginner-note">
    <strong>What you're seeing:</strong> TV (blue) and Radio (red) follow almost the same pattern - when one goes up, 
    the other goes up. Digital (green) does its own thing. The model can't tell if sales increases are from TV or Radio!
    </div>
    """, unsafe_allow_html=True)
    
    # Show the problem
    st.markdown("### ⚠️ What Goes Wrong")
    
    problem_df = pd.DataFrame({
        'Channel': ['TV', 'Radio', 'Digital'],
        'True Effect': ['+$2.50 per $1', '+$2.00 per $1', '+$3.00 per $1'],
        'Model Says': ['+$5.00 per $1 😱', '-$1.00 per $1 ❌', '+$3.00 per $1 ✅'],
        'Problem?': ['Gets all credit!', 'Looks harmful!', 'Correct']
    })
    st.dataframe(problem_df, use_container_width=True, hide_index=True)

with col2:
    st.markdown("### 🔬 How to Detect It")
    
    # Create correlation heatmap
    corr_matrix = [[1.0, 0.95, 0.2],
                   [0.95, 1.0, 0.15],
                   [0.2, 0.15, 1.0]]
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=['TV', 'Radio', 'Digital'],
        y=['TV', 'Radio', 'Digital'],
        colorscale='RdBu',
        zmid=0,
        text=[[f'{val:.2f}' for val in row] for row in corr_matrix],
        texttemplate='%{text}',
        textfont={"size": 14},
        colorbar=dict(title="Correlation"),
        reversescale=True
    ))
    
    fig.update_layout(
        title="Correlation Matrix - Red = Problem!",
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="beginner-note">
    <strong>Reading this chart:</strong> Numbers close to 1 (red) mean channels move together. 
    TV-Radio = 0.95 is BAD (too similar). TV-Digital = 0.2 is GOOD (independent).
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✅ Solutions")
    
    st.markdown("""
    <div class="solution-box">
    <strong>How to Fix It:</strong>
    <ol>
    <li><strong>Quick fix:</strong> Combine TV + Radio into "Traditional Media"</li>
    <li><strong>Better fix:</strong> Run them at different times (TV only in Q1, Radio only in Q2)</li>
    <li><strong>Technical fix:</strong> Use Ridge Regression (handles correlation better)</li>
    <li><strong>Best fix:</strong> Design tests where they don't overlap</li>
    </ol>
    
    <strong>Rule of thumb:</strong> If correlation > 0.7, you have a problem!
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# PITFALL 4: ATTRIBUTION WINDOWS
# =============================================================================

st.markdown("## 4️⃣ Attribution Windows (Adstock)")
st.markdown('<span class="tricky-badge">TRICKY TO UNDERSTAND</span>', unsafe_allow_html=True)

st.markdown("""
<div class="beginner-note">
<strong>🔰 Beginner's Note:</strong> When you see a TV ad today, do you buy immediately or next week? Attribution windows 
answer "how long does advertising keep working?" It's like asking how long medicine stays in your system - some work 
instantly and fade fast (like coffee), others build up over time (like vitamins).
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### ⏱️ Same Campaign, Different Windows, Different ROI!")
    
    # Create bar chart showing different ROIs
    windows = ['1 Week', '2 Weeks', '4 Weeks', '8 Weeks', '13 Weeks']
    revenue = [120, 200, 350, 450, 480]
    roi = [1.2, 2.0, 3.5, 4.5, 4.8]
    colors = ['#e15759', '#e15759', '#f28e2c', '#54a24b', '#54a24b']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=windows,
        y=revenue,
        text=[f'${r}K<br>ROI: {roi[i]}x' for i, r in enumerate(revenue)],
        textposition='outside',
        marker_color=colors,
        name='Revenue'
    ))
    
    fig.update_layout(
        title="Same $100K TV Campaign - Measured Different Ways",
        xaxis_title="How Long You Measure",
        yaxis_title="Revenue Attributed ($K)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="beginner-note">
    <strong>What you're seeing:</strong> The SAME campaign shows 2x ROI if you only measure 2 weeks, 
    but 4.5x ROI if you measure 8 weeks! Most of TV's impact comes later. It's like planting a tree - 
    you don't see all the fruit on day one.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📊 How Effects Decay Over Time")
    
    # Show decay curves
    weeks = np.arange(0, 13)
    tv_decay = 100 * (0.7 ** weeks)  # Slow decay
    digital_decay = 100 * (0.2 ** weeks)  # Fast decay
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weeks, y=tv_decay,
        name='TV (Slow decay)',
        line=dict(color='#4c78a8', width=3),
        fill='tozeroy',
        fillcolor='rgba(76, 120, 168, 0.2)'
    ))
    fig.add_trace(go.Scatter(
        x=weeks, y=digital_decay,
        name='Search (Fast decay)',
        line=dict(color='#e15759', width=3),
        fill='tozeroy',
        fillcolor='rgba(225, 87, 89, 0.2)'
    ))
    
    fig.update_layout(
        title="Different Channels Decay at Different Speeds",
        xaxis_title="Weeks After Ad",
        yaxis_title="Effect Remaining (%)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### ✅ Typical Decay Rates by Channel")
    
    decay_df = pd.DataFrame({
        'Channel': ['🔍 Search', '📱 Social', '📺 TV', '📻 Radio'],
        'Decay Speed': ['Very Fast', 'Fast', 'Slow', 'Medium'],
        'Lasts For': ['1-2 weeks', '2-4 weeks', '8-13 weeks', '4-8 weeks'],
        'Why?': ['Intent-based', 'Engagement fades', 'Brand building', 'Reminder effect']
    })
    st.dataframe(decay_df, use_container_width=True, hide_index=True)
    
    st.markdown("""
    <div class="solution-box">
    <strong>How to Get It Right:</strong>
    <ol>
    <li><strong>Start with benchmarks</strong> (TV: 8-13 weeks, Digital: 1-4 weeks)</li>
    <li><strong>Test different windows</strong> and see which fits best</li>
    <li><strong>Use business sense</strong> (B2B = longer, B2C = shorter)</li>
    <li><strong>Validate with tests</strong> (turn off channel, see how long effect lasts)</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# PITFALL 5: SATURATION MISSPECIFICATION
# =============================================================================

st.markdown("## 5️⃣ Saturation Misspecification")
st.markdown('<span class="tricky-badge">TRICKY TO UNDERSTAND</span>', unsafe_allow_html=True)

st.markdown("""
<div class="beginner-note">
<strong>🔰 Beginner's Note:</strong> Imagine filling a sponge with water. At first, it absorbs everything. 
Then it starts dripping. Finally, it can't hold anymore - that's saturation! In marketing, it's the point where 
spending more doesn't help. The problem? If your model thinks the sponge is full at 25%, you'll stop way too early!
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📈 Wrong Saturation = Missed Opportunity")
    
    # Generate saturation curves
    spend = np.linspace(0, 3000, 100)
    wrong_curve = 75 * (1 - np.exp(-spend/200))  # Saturates early
    right_curve = 95 * (1 - np.exp(-spend/1500))  # Saturates later
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=spend, y=wrong_curve,
        name='Wrong Model (Saturates at $500K)',
        line=dict(color='#e15759', width=3, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=spend, y=right_curve,
        name='Reality (Saturates at $2M)',
        line=dict(color='#54a24b', width=3)
    ))
    
    # Add markers
    fig.add_trace(go.Scatter(
        x=[500], y=[65],
        mode='markers',
        name='Your Current Spend',
        marker=dict(size=15, color='#4c78a8', symbol='star')
    ))
    fig.add_trace(go.Scatter(
        x=[2000], y=[85],
        mode='markers',
        name='Competitor Spend',
        marker=dict(size=15, color='#f28e2c', symbol='diamond')
    ))
    
    fig.update_layout(
        title="Model Says Stop at $500K, But Competitors Succeed at $2M!",
        xaxis_title="Monthly Spend ($K)",
        yaxis_title="Sales Response (%)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="beginner-note">
    <strong>What you're seeing:</strong> The red line (wrong model) flattens at $500K, suggesting more spend is wasteful. 
    But the green line (reality) keeps growing! You're at the blue star, competitors at orange diamond. 
    You're leaving money on the table!
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 💰 The Business Impact")
    
    impact_df = pd.DataFrame({
        'Spend Level': ['$500K (You)', '$1M', '$2M (Competitor)'],
        'Wrong Model Says': ['✅ Optimal', '🚫 Wasteful', '🚫 Terrible'],
        'Reality Is': ['⚠️ Too Low', '✅ Good', '✅ Near Optimal'],
        'Lost Revenue': ['$0', '$500K/year', '$1.5M/year']
    })
    st.dataframe(impact_df, use_container_width=True, hide_index=True)
    
    st.markdown("### 🎯 Common Saturation Points")
    
    st.markdown("""
    <div class="solution-box">
    <strong>Industry Benchmarks (Monthly):</strong>
    <ul>
    <li>📺 <strong>TV:</strong> $1-3M (builds brand slowly)</li>
    <li>🔍 <strong>Search:</strong> $50-200K (limited search volume)</li>
    <li>📱 <strong>Social:</strong> $200-800K (audience gets tired)</li>
    <li>📻 <strong>Radio:</strong> $300K-1M (regional limits)</li>
    </ul>
    
    <strong>How to Fix:</strong>
    <ol>
    <li><strong>Check competitors:</strong> If they spend 4x more successfully, your curve is wrong</li>
    <li><strong>Test higher spend:</strong> Try 2x spend in one market</li>
    <li><strong>Try different curves:</strong> S-curve, logarithmic, linear-to-plateau</li>
    <li><strong>Use common sense:</strong> Can't exceed total market size!</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# PITFALL 6: BASELINE DRIFT
# =============================================================================

st.markdown("## 6️⃣ Baseline Drift")
st.markdown('<span class="tricky-badge">TRICKY TO UNDERSTAND</span>', unsafe_allow_html=True)

st.markdown("""
<div class="beginner-note">
<strong>🔰 Beginner's Note:</strong> Your business has "baseline" sales - what you'd sell with zero marketing. 
But this baseline changes! Maybe your brand is getting stronger, or the market is growing. It's like a rising tide 
lifting all boats. The problem: if sales go up 20% but marketing stays flat, who gets credit? Without accounting 
for baseline drift, marketing might claim success it didn't earn (or get blamed for failure it didn't cause).
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📊 Sales Growing, Marketing Flat - What's Happening?")
    
    # Generate baseline drift data
    months = pd.date_range('2023-01-01', periods=12, freq='M')
    baseline = np.linspace(100, 120, 12)  # Growing baseline
    marketing_contribution = [5, 4, 6, 5, 5, 4, 6, 5, 5, 4, 5, 5]  # Flat
    total_sales = baseline + marketing_contribution
    marketing_spend_index = [100] * 12  # Flat spend
    
    fig = go.Figure()
    
    # Add stacked area chart
    fig.add_trace(go.Scatter(
        x=months, y=baseline,
        name='Baseline (Hidden)',
        line=dict(color='#54a24b', width=2),
        fill='tozeroy',
        fillcolor='rgba(84, 162, 75, 0.2)',
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=months, y=marketing_contribution,
        name='Marketing Effect',
        line=dict(color='#4c78a8', width=2),
        fill='tonexty',
        fillcolor='rgba(76, 120, 168, 0.2)',
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=months, y=marketing_spend_index,
        name='Marketing Spend (Flat)',
        line=dict(color='#e15759', width=3, dash='dash'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Sales Up 20%, Marketing Flat - Is Marketing a Hero or Just Lucky?",
        xaxis_title="Month",
        yaxis_title="Sales Index",
        yaxis2=dict(
            title="Marketing Spend Index",
            overlaying='y',
            side='right',
            range=[90, 130]
        ),
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="beginner-note">
    <strong>What you're seeing:</strong> Total sales (green + blue) grew 20%. Marketing spend (red dashed) stayed flat. 
    The green area (baseline) is growing naturally - maybe brand strength, market growth, or word-of-mouth. 
    Without modeling this drift, marketing looks like a superstar when it's really just riding the wave!
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🌊 What Causes Baseline to Drift?")
    
    causes_df = pd.DataFrame({
        'Cause': ['📈 Brand Building', '🌍 Market Growth', '🏪 Distribution', 
                  '💬 Word of Mouth', '🏢 Less Competition'],
        'Direction': ['↗️ Up', '↗️ Up', '↗️ Up', '↗️ Up', '↗️ Up'],
        'Example': ['+2% monthly', '+5% yearly', 'New stores', 'Going viral', 'Competitor left'],
        'Impact': ['Slow & steady', 'Industry-wide', 'Step change', 'Exponential', 'Sudden jump']
    })
    st.dataframe(causes_df, use_container_width=True, hide_index=True)
    
    st.markdown("### ⚠️ What Goes Wrong Without Drift Modeling")
    
    st.markdown("""
    <div class="warning-box">
    <strong>Scenario 1:</strong> Baseline growing (brand getting stronger)
    <ul>
    <li>Marketing gets credit for organic growth</li>
    <li>ROI looks inflated (5x instead of true 2x)</li>
    <li>You overspend thinking marketing is amazing</li>
    </ul>
    
    <strong>Scenario 2:</strong> Baseline declining (market shrinking)
    <ul>
    <li>Marketing blamed for market decline</li>
    <li>ROI looks terrible (0.5x instead of true 2x)</li>
    <li>You cut budget when marketing is actually working</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✅ The Solution")
    
    st.markdown("""
    <div class="solution-box">
    <strong>How to Account for Drift:</strong>
    <ol>
    <li><strong>Add a trend line</strong> (growing/declining baseline)</li>
    <li><strong>Include time as a variable</strong> in your model</li>
    <li><strong>Track brand metrics</strong> (awareness, consideration)</li>
    <li><strong>Model step changes</strong> (new store openings, competitor exits)</li>
    <li><strong>Refresh models quarterly</strong> (baselines change!)</li>
    </ol>
    
    <strong>Simple test:</strong> Plot sales vs marketing over time. If they diverge, you have drift!
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# SUMMARY SECTION
# =============================================================================

st.markdown("## 🎯 Quick Reference Guide")

st.markdown("""
<div class="info-box">
<h4>Your MMM Pitfall Checklist</h4>
<p>Run through this list before trusting any MMM results:</p>
</div>
""", unsafe_allow_html=True)

# Create summary table
summary_df = pd.DataFrame({
    'Pitfall': ['Data Quality', 'External Factors', 'Multicollinearity', 
                'Attribution Windows', 'Saturation', 'Baseline Drift'],
    'Quick Test': ['Compare 3 data sources', 'List 5 external events', 'Check correlation > 0.7',
                   'Try 2, 8, 13 week windows', 'Compare to competitors', 'Plot sales vs spend trend'],
    'Red Flag': ['Numbers differ by >10%', 'Major event not modeled', 'Negative coefficients',
                 'ROI changes by >2x', 'Saturating too early', 'Lines diverging'],
    'Quick Fix': ['Use platform data', 'Add COVID dummy', 'Combine channels',
                  'Use 8-week default', 'Test higher spend', 'Add trend line']
})

st.dataframe(summary_df, use_container_width=True, hide_index=True)

st.markdown("""
<div class="solution-box">
<h4>🚀 Next Steps:</h4>
<ol>
<li><strong>Start with data quality</strong> - it's the foundation</li>
<li><strong>Check for multicollinearity</strong> - it can flip results completely</li>
<li><strong>Test different windows and curves</strong> - assumptions matter</li>
<li><strong>Always include external factors</strong> - context is crucial</li>
<li><strong>Monitor for drift</strong> - baselines change over time</li>
</ol>

<strong>Remember:</strong> These pitfalls often occur together. A model with bad data AND wrong saturation AND missing COVID 
will be completely useless. Fix them one by one!
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
<p><strong>MMM Common Pitfalls 101</strong> | A Beginner's Guide to Marketing Mix Modeling</p>
</div>
""", unsafe_allow_html=True)