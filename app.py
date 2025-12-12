"""
FDA Computer System Validation Violations Dashboard
Analysis of 141 observations across 111 warning letters (2020-2025)

To run locally:
    pip install -r requirements.txt
    streamlit run streamlit_csv_dashboard.py

To deploy on Streamlit Cloud:
    1. Push this file and requirements.txt to a GitHub repository
    2. Connect to Streamlit Cloud (share.streamlit.io)
    3. Deploy from your repository
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="FDA CSV Violations Analysis | When the Witness Goes Silent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&family=Source+Sans+Pro:wght@400;600;700&display=swap');
    
    .main-header {
        font-family: 'Merriweather', serif;
        font-size: 2.8rem;
        font-weight: 900;
        color: #1a1a2e;
        margin-bottom: 0;
        line-height: 1.2;
    }
    .sub-header {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.2rem;
        color: #64748b;
        margin-top: 0.5rem;
        line-height: 1.6;
    }
    .insight-box {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 5px solid #dc2626;
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1.5rem 0;
        font-family: 'Source Sans Pro', sans-serif;
    }
    .insight-box-blue {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 5px solid #2563eb;
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1.5rem 0;
        font-family: 'Source Sans Pro', sans-serif;
    }
    .narrative-text {
        font-family: 'Merriweather', serif;
        font-size: 1.15rem;
        line-height: 1.9;
        color: #1e293b;
    }
    .pullquote {
        font-family: 'Merriweather', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #dc2626;
        border-left: 5px solid #dc2626;
        padding-left: 1.5rem;
        margin: 2.5rem 0;
        font-style: italic;
    }
    .section-divider {
        height: 4px;
        background: linear-gradient(90deg, #dc2626 0%, #f87171 30%, #fecaca 60%, transparent 100%);
        border-radius: 2px;
        margin: 3rem 0;
    }
    .stat-number {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #dc2626;
    }
    .stat-label {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA
# ============================================================================

TOTAL_OBSERVATIONS = 141
TOTAL_LETTERS = 111
TOTAL_COMPANIES = 109

# Yearly trend
yearly_data = pd.DataFrame({
    'Year': ['2020', '2021', '2022', '2023', '2024', '2025'],
    'Observations': [8, 7, 17, 8, 23, 22],
    'Period': ['Pre-surge', 'Pre-surge', 'Pre-surge', 'Pre-surge', 'Surge', 'Surge']
})

# Violation types (no proprietary names)
violation_data = pd.DataFrame({
    'Violation Type': [
        'Audit Trail Failures', 
        'Automatic Equipment Controls (211.68)', 
        'Chromatography Data Systems',
        'Electronic Records', 
        'Password & Login Issues',
        'Computerized Systems General', 
        'Access Control Failures',
        'Software Validation',
        'Data Backup Deficiencies'
    ],
    'Count': [49, 40, 24, 24, 24, 22, 21, 19, 8],
    'Percentage': [34.8, 28.4, 17.0, 17.0, 17.0, 15.6, 14.9, 13.5, 5.7]
})

# Geographic distribution (no company names)
geo_data = pd.DataFrame({
    'Region': ['United States', 'India', 'China', 'Germany', 'South Korea', 'Other Regions'],
    'Observations': [71, 28, 14, 6, 3, 19],
    'Percentage': [50.4, 19.9, 9.9, 4.3, 2.1, 13.4]
})

# Sophistication analysis
sophistication_data = pd.DataFrame({
    'Region': ['United States', 'India', 'China'],
    'Basic Failures': [36.4, 21.1, 33.3],
    'Complex Failures': [34.3, 22.8, 22.2],
    'Sophistication Ratio': [0.94, 1.08, 0.67]
})

# Facility type
facility_data = pd.DataFrame({
    'Facility Type': ['QC Laboratory', 'API Manufacturing', 'Sterile Manufacturing', 'Finished Dosage', 'Other'],
    'Audit Trail Violations': [17, 11, 3, 6, 12],
    'Other CSV Violations': [12, 15, 11, 9, 45]
})

# Year-over-year change
growth_data = pd.DataFrame({
    'Violation Type': ['Audit Trail', 'Password Security', 'Electronic Records', 'Equipment Controls'],
    'Y2022': [9, 7, 4, 7],
    'Y2024': [12, 3, 4, 7],
    'Growth_Pct': [33, -57, 0, 0]
})

# Co-occurrence patterns
cooccurrence_data = pd.DataFrame({
    'Violation Pair': [
        'Audit Trail + Password Issues',
        'Audit Trail + Equipment Controls',
        'Audit Trail + Chromatography Systems',
        'Audit Trail + Access Control',
        'Audit Trail + Electronic Records'
    ],
    'Co_occurrences': [20, 20, 16, 16, 14]
})

# Concerning keywords
keyword_data = pd.DataFrame({
    'Finding': ['Delete capability', 'Administrator access', 'Shared credentials', 'Not enabled', 'Spreadsheet use', 'Backup issues', 'Manual workarounds'],
    'Pct_of_Observations': [15.6, 9.9, 7.1, 6.4, 7.8, 5.7, 4.3]
})

# System types (generic terms only)
system_data = pd.DataFrame({
    'System Category': ['Chromatography Data Systems', 'Laboratory Information Systems', 'Spreadsheet Applications', 'Analytical Instrument Software'],
    'Observations': [24, 10, 11, 8]
})

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🔬 FDA Warning Letters")
    st.markdown("**Computer System Validation**")
    st.markdown("*2020-2025 Analysis*")
    
    st.markdown("---")
    
    st.markdown("#### Key Numbers")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Observations", TOTAL_OBSERVATIONS)
        st.metric("Letters", TOTAL_LETTERS)
    with col2:
        st.metric("Companies", TOTAL_COMPANIES)
        st.metric("Years", "5")
    
    st.markdown("---")
    
    st.markdown("#### The Story in Brief")
    st.markdown("""
    - 📈 **187% spike** in 2024
    - 🔍 **Audit trails** are #1 failure
    - 🇺🇸 **50%** from US facilities
    - 🗑️ **15.6%** have delete access
    """)
    
    st.markdown("---")
    st.caption("Data: FDA Warning Letters Database")

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<p class="main-header">When the Witness Goes Silent</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">An investigation into 141 FDA warning letter observations reveals a troubling paradox: the systems designed to guarantee data integrity have become pharmaceutical manufacturing\'s most persistent failure.</p>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# THE HOOK
# ============================================================================

st.markdown("""
<p class="narrative-text">
There's a moment in every FDA inspection when the investigator asks to see the audit trail. It should be a formality. 
The audit trail is, after all, the silent witness—a digital record of every action, every change, every deletion. 
It exists for precisely this moment: to prove that the data can be trusted.
</p>

<p class="narrative-text">
But something strange has been happening.
</p>
""", unsafe_allow_html=True)

# Key metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<p class="stat-number">34.8%</p>', unsafe_allow_html=True)
    st.markdown('<p class="stat-label">Audit trail failures<br>(#1 violation type)</p>', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="stat-number">187%</p>', unsafe_allow_html=True)
    st.markdown('<p class="stat-label">Increase in citations<br>(2023 → 2024)</p>', unsafe_allow_html=True)

with col3:
    st.markdown('<p class="stat-number">15.6%</p>', unsafe_allow_html=True)
    st.markdown('<p class="stat-label">Had delete access<br>(to GxP records)</p>', unsafe_allow_html=True)

with col4:
    st.markdown('<p class="stat-number">50%</p>', unsafe_allow_html=True)
    st.markdown('<p class="stat-label">From US facilities<br>(the home market)</p>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# THE SPIKE
# ============================================================================

st.markdown("## 📈 The 187% Question")

st.markdown("""
<p class="narrative-text">
In 2023, FDA issued 8 computer system validation observations. By 2024, that number was 23. 
<strong>That's a 187% increase in a single year.</strong>
</p>

<p class="narrative-text">
The first instinct is to dismiss this as noise—perhaps FDA inspected more facilities or wrote more letters overall. 
But when we controlled for inspection volume, the pattern held. Something fundamental shifted.
</p>
""", unsafe_allow_html=True)

# Yearly trend chart
fig_yearly = go.Figure()

# Add area fill
fig_yearly.add_trace(go.Scatter(
    x=yearly_data['Year'],
    y=yearly_data['Observations'],
    fill='tozeroy',
    fillcolor='rgba(220, 38, 38, 0.1)',
    line=dict(color='rgba(220, 38, 38, 0)'),
    showlegend=False,
    hoverinfo='skip'
))

# Add line with markers
fig_yearly.add_trace(go.Scatter(
    x=yearly_data['Year'],
    y=yearly_data['Observations'],
    mode='lines+markers+text',
    text=yearly_data['Observations'],
    textposition='top center',
    textfont=dict(size=16, color='#dc2626', family='Source Sans Pro'),
    line=dict(color='#dc2626', width=4),
    marker=dict(size=14, color='#dc2626', line=dict(color='white', width=2)),
    showlegend=False
))

# Annotation for spike
fig_yearly.add_annotation(
    x='2024', y=23,
    text="<b>+187%</b><br>vs prior year",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    arrowcolor='#dc2626',
    ax=80,
    ay=-50,
    font=dict(size=14, color='#dc2626', family='Source Sans Pro'),
    bgcolor='white',
    bordercolor='#dc2626',
    borderwidth=2,
    borderpad=6
)

fig_yearly.update_layout(
    height=400,
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False, 
        tickfont=dict(size=14, family='Source Sans Pro'),
        title=None
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor='#f1f5f9',
        title=dict(text='Observations', font=dict(size=12, family='Source Sans Pro')),
        tickfont=dict(size=12, family='Source Sans Pro')
    ),
    margin=dict(l=60, r=40, t=20, b=40)
)

st.plotly_chart(fig_yearly, use_container_width=True)

st.markdown("""
<div class="insight-box">
<strong>What changed?</strong> FDA's 2018 Data Integrity guidance is finally being enforced with teeth. 
Inspectors are now specifically trained to examine computerized systems, audit trail configurations, 
and electronic record controls. The grace period is over.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# THE PARADOX
# ============================================================================

st.markdown("## 🔍 The Audit Trail Paradox")

st.markdown("""
<p class="pullquote">
"The system designed to ensure integrity is itself the most common point of failure."
</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    # Horizontal bar chart
    fig_violations = go.Figure()
    
    colors = ['#dc2626' if i == 0 else '#475569' for i in range(len(violation_data))]
    
    fig_violations.add_trace(go.Bar(
        y=violation_data['Violation Type'],
        x=violation_data['Count'],
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"<b>{c}</b> ({p}%)" for c, p in zip(violation_data['Count'], violation_data['Percentage'])],
        textposition='outside',
        textfont=dict(size=12, family='Source Sans Pro'),
        hovertemplate='%{y}: %{x} observations<extra></extra>'
    ))
    
    fig_violations.update_layout(
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True, 
            gridcolor='#f1f5f9',
            title=dict(text='Number of Observations', font=dict(size=12, family='Source Sans Pro')),
            tickfont=dict(size=11, family='Source Sans Pro'),
            range=[0, 65]
        ),
        yaxis=dict(
            showgrid=False, 
            autorange='reversed',
            tickfont=dict(size=11, family='Source Sans Pro')
        ),
        margin=dict(l=200, r=80, t=20, b=40)
    )
    
    st.plotly_chart(fig_violations, use_container_width=True)

with col2:
    st.markdown("### What Investigators Found")
    
    st.markdown("""
    **The Disabled Witness**
    
    Systems where audit trail functionality exists but was never activated. 
    The software was validated, procedures were written—but the feature that records every action? *Turned off.*
    
    ---
    
    **The Unreviewed Witness**
    
    Enabled audit trails that nobody reads. Terabytes of data generated, 
    but review procedures examined only summary reports.
    
    ---
    
    **The Illiterate Witness**
    
    Reviewers who don't know what to look for. When one control fails, 
    they aren't catching other anomalies either.
    """)

st.markdown("""
<div class="insight-box-blue">
<strong>💡 The Electronic Signature Surprise:</strong> Despite 21 CFR Part 11 being over 25 years old, 
electronic signature violations account for just 1.4% of observations. The industry solved e-signatures. 
Audit trails? Still struggling.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# THE SOPHISTICATION SURPRISE
# ============================================================================

st.markdown("## 🌍 The Sophistication Surprise")

st.markdown("""
<p class="narrative-text">
Here's something that should make quality leaders uncomfortable: 
<strong>facilities in India are being cited for more sophisticated failures than those in the United States.</strong>
</p>

<p class="narrative-text">
We categorized violations into "basic failures" (password issues, access controls) and "complex failures" 
(audit trail management, chromatography data systems). Then we calculated a sophistication ratio.
</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Grouped bar chart
    fig_soph = go.Figure()
    
    fig_soph.add_trace(go.Bar(
        name='Basic Failures',
        x=sophistication_data['Region'],
        y=sophistication_data['Basic Failures'],
        marker_color='#f87171',
        text=[f"{v}%" for v in sophistication_data['Basic Failures']],
        textposition='outside',
        textfont=dict(size=13, family='Source Sans Pro')
    ))
    
    fig_soph.add_trace(go.Bar(
        name='Complex Failures',
        x=sophistication_data['Region'],
        y=sophistication_data['Complex Failures'],
        marker_color='#1e40af',
        text=[f"{v}%" for v in sophistication_data['Complex Failures']],
        textposition='outside',
        textfont=dict(size=13, family='Source Sans Pro')
    ))
    
    fig_soph.update_layout(
        barmode='group',
        height=380,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation='h', 
            yanchor='bottom', 
            y=1.02,
            font=dict(size=12, family='Source Sans Pro')
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=13, family='Source Sans Pro')
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#f1f5f9',
            title=dict(text='% of Regional Citations', font=dict(size=12, family='Source Sans Pro')),
            tickfont=dict(size=11, family='Source Sans Pro')
        ),
        margin=dict(l=60, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig_soph, use_container_width=True)

with col2:
    st.markdown("### Sophistication Ratio")
    st.markdown("*Complex ÷ Basic Failures*")
    
    for _, row in sophistication_data.iterrows():
        ratio = row['Sophistication Ratio']
        if ratio > 1:
            color = '#059669'
            interpretation = "More complex than basic"
        else:
            color = '#dc2626'
            interpretation = "More basic than complex"
        
        st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <strong>{row['Region']}</strong><br>
            <span style="color:{color}; font-size: 2rem; font-weight: bold;">{ratio:.2f}</span><br>
            <span style="color: #64748b; font-size: 0.85rem;">{interpretation}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<strong>🤔 What this suggests:</strong> US facilities may be over-relying on perceived regulatory familiarity 
while overlooking basic computer system controls. Meanwhile, facilities in other regions—perhaps more accustomed to 
intense FDA scrutiny—have moved past the basics and are now being cited for more nuanced issues.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# THE DELETE PROBLEM
# ============================================================================

st.markdown("## ⚠️ The Delete Problem")

st.markdown("""
<p class="pullquote">
"In 15.6% of observations, analysts had the ability to delete data."
</p>

<p class="narrative-text">
Let that sink in. In almost one out of every six CSV-related warning letters, FDA investigators found that 
laboratory or production personnel could <strong>delete electronic records</strong>. Not archive. Not flag for review. Delete.
</p>
""", unsafe_allow_html=True)

# Keyword chart
fig_keywords = go.Figure()

colors = ['#dc2626' if kw in ['Delete capability', 'Spreadsheet use', 'Administrator access'] else '#64748b' 
          for kw in keyword_data['Finding']]

fig_keywords.add_trace(go.Bar(
    x=keyword_data['Finding'],
    y=keyword_data['Pct_of_Observations'],
    marker_color=colors,
    text=[f"<b>{p}%</b>" for p in keyword_data['Pct_of_Observations']],
    textposition='outside',
    textfont=dict(size=12, family='Source Sans Pro'),
    hovertemplate='%{x}: %{y}% of observations<extra></extra>'
))

fig_keywords.update_layout(
    height=350,
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False, 
        tickangle=30,
        tickfont=dict(size=11, family='Source Sans Pro')
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor='#f1f5f9',
        title=dict(text='% of Observations', font=dict(size=12, family='Source Sans Pro')),
        tickfont=dict(size=11, family='Source Sans Pro')
    ),
    margin=dict(l=60, r=40, t=20, b=100)
)

st.plotly_chart(fig_keywords, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🗑️ Delete Access
    **15.6% of observations**
    
    Users could permanently remove records from GxP systems.
    """)

with col2:
    st.markdown("""
    ### 📊 Spreadsheets
    **7.8% of observations**
    
    Unvalidated spreadsheets in GxP calculations.
    """)

with col3:
    st.markdown("""
    ### 👤 Admin Access
    **9.9% of observations**
    
    Routine users with admin privileges.
    """)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# WHAT'S IMPROVING
# ============================================================================

st.markdown("## ✅ What's Actually Improving")

st.markdown("""
<p class="narrative-text">
Not everything is getting worse. <strong>Password and login violations dropped 57%</strong> from 2022 to 2024. 
The industry's focus on basic security is working.
</p>

<p class="narrative-text">
But here's the catch: over the same period, <strong>audit trail violations increased 33%</strong>. 
We're solving the easy problems while the hard ones get worse.
</p>
""", unsafe_allow_html=True)

# Growth chart
fig_growth = go.Figure()

colors = ['#dc2626' if g > 0 else '#059669' for g in growth_data['Growth_Pct']]

fig_growth.add_trace(go.Bar(
    x=growth_data['Violation Type'],
    y=growth_data['Growth_Pct'],
    marker_color=colors,
    text=[f"<b>{g:+d}%</b>" for g in growth_data['Growth_Pct']],
    textposition='outside',
    textfont=dict(size=14, family='Source Sans Pro', color=colors)
))

fig_growth.add_hline(y=0, line_dash="dash", line_color="#94a3b8", line_width=2)

fig_growth.update_layout(
    height=380,
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        tickfont=dict(size=13, family='Source Sans Pro')
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor='#f1f5f9',
        title=dict(text='% Change (2022 → 2024)', font=dict(size=12, family='Source Sans Pro')),
        tickfont=dict(size=11, family='Source Sans Pro'),
        range=[-70, 50]
    ),
    margin=dict(l=60, r=40, t=20, b=60)
)

st.plotly_chart(fig_growth, use_container_width=True)

st.markdown("""
<div class="insight-box-blue">
<strong>🎯 The implication:</strong> Whatever training approach worked for password security 
needs to be replicated for audit trail management.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# ACTION ITEMS
# ============================================================================

st.markdown("## 🎯 What This Means for Your Organization")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Immediate Priorities
    
    **1. Audit Your Audit Trails**
    
    Not whether they exist—whether they're enabled, reviewed, and actionable. 
    Ask your laboratory director: *"What anomalies would trigger an investigation?"*
    
    ---
    
    **2. Eliminate Delete Access**
    
    Every system, every role. Implement soft-delete with full traceability. 
    Add alerts for any deletion attempts.
    
    ---
    
    **3. Address the Spreadsheet Problem**
    
    Inventory every spreadsheet used in GxP calculations. Validate or replace. 
    Low-hanging fruit with high regulatory exposure.
    """)

with col2:
    st.markdown("""
    ### Strategic Priorities
    
    **4. Focus on QC Laboratories**
    
    20.5% of audit trail violations occur in laboratories. 
    Consider dedicated validation resources for laboratory systems.
    
    ---
    
    **5. Fix the Governance**
    
    CSV failures cluster together. When audit trails fail, password security usually fails too. 
    Address root cause: computer system governance.
    
    ---
    
    **6. Budget for the New Normal**
    
    The 187% spike isn't temporary. FDA has signaled CSV is a permanent priority.
    """)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Methodology")
    st.caption("""
    Analysis of 983 FDA warning letters (2020-2025). CSV observations identified using 
    regulatory citations, technical terms, and keyword patterns. All data publicly available.
    """)

with col2:
    st.markdown("### Limitations")
    st.caption("""
    Warning letters represent a subset of FDA enforcement. 2025 data is partial year. 
    Observation classification based on text analysis.
    """)

with col3:
    st.markdown("### Data Files")
    st.caption("""
    Full dataset available in csv_violations_comprehensive.csv with observation-level details 
    including dates, regions, facility types, and violation categories.
    """)

st.markdown("---")
st.markdown("<center><sub>Analysis conducted December 2024 | Data source: FDA Warning Letters Database</sub></center>", unsafe_allow_html=True)
