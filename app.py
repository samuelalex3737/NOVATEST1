import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    h2 {
        color: #2c3e50;
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function with better error handling
@st.cache_data
def load_data():
    """Load all CSV files from Dataset folder"""
    data_dict = {}
    
    files = {
        'campaign_performance': 'campaign_performance.csv',
        'channel_attribution': 'channel_attribution.csv',
        'correlation_matrix': 'correlation_matrix.csv',
        'customer_data': 'customer_data.csv',
        'customer_journey': 'customer_journey.csv',
        'feature_importance': 'feature_importance.csv',
        'funnel_data': 'funnel_data.csv',
        'geographic_data': 'geographic_data.csv',
        'lead_scoring_results': 'lead_scoring_results.csv',
        'learning_curve': 'learning_curve.csv',
        'product_sales': 'product_sales.csv'
    }
    
    errors = []
    
    for key, filepath in files.items():
        try:
            data_dict[key] = pd.read_csv(filepath)
            st.sidebar.success(f"✅ Loaded {key}")
        except FileNotFoundError:
            errors.append(f"❌ File not found: {filepath}")
            st.sidebar.error(f"❌ Missing: {key}")
        except Exception as e:
            errors.append(f"❌ Error loading {key}: {str(e)}")
            st.sidebar.error(f"❌ Error: {key}")
    
    if errors:
        st.error("### Errors loading data:")
        for error in errors:
            st.error(error)
        
        st.info("""
        ### Troubleshooting:
        1. Check that all CSV files are in the 'Dataset' folder
        2. Verify file names match exactly (case-sensitive)
        3. Ensure files are not corrupted
        """)
        return None
    
    return data_dict

# Load data
with st.spinner("Loading data..."):
    data = load_data()

if data is None or len(data) == 0:
    st.stop()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/000000/business-report.png", width=100)
    st.title("📊 Marketing Analytics")
    st.markdown("---")
    
    st.subheader("Select Analysis View")
    analysis_type = st.selectbox(
        "Choose Analysis Type",
        ["Overview", "Customer Analysis", "Campaign Performance", "Channel Attribution", 
         "Product Sales", "Geographic Analysis", "Customer Journey", "Lead Scoring",
         "Feature Importance", "Correlation Analysis"]
    )
    
    st.markdown("---")
    st.info("💡 **Tip**: Explore different views")

# Main content
st.title("🎯 Marketing Analytics Dashboard")
st.markdown("### Comprehensive Marketing Performance Analysis")

# Helper function to safely get column
def safe_column(df, possible_names):
    """Return first matching column name from list"""
    for name in possible_names:
        if name in df.columns:
            return name
    return None

# Overview Section
if analysis_type == "Overview":
    st.header("📈 Executive Summary")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = len(data['customer_data'])
        st.metric("Total Customers", f"{total_customers:,}")
    
    with col2:
        # Try different column names for revenue/sales
        sales_col = safe_column(data['product_sales'], ['Revenue', 'Sales', 'Total_Sales', 'Amount'])
        if sales_col:
            total_sales = data['product_sales'][sales_col].sum()
            st.metric("Total Sales", f"${total_sales:,.0f}")
        else:
            st.metric("Total Products", len(data['product_sales']))
    
    with col3:
        total_campaigns = len(data['campaign_performance'])
        st.metric("Total Campaigns", total_campaigns)
    
    with col4:
        lead_score_col = safe_column(data['lead_scoring_results'], ['LeadScore', 'Score', 'Lead_Score'])
        if lead_score_col:
            avg_lead_score = data['lead_scoring_results'][lead_score_col].mean()
            st.metric("Avg Lead Score", f"{avg_lead_score:.2f}")
        else:
            st.metric("Total Leads", len(data['lead_scoring_results']))
    
    st.markdown("---")
    
    # Display datasets info
    st.subheader("📊 Available Datasets")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Loaded Datasets:**
        - Campaign Performance: {len(data['campaign_performance'])} rows
        - Customer Data: {len(data['customer_data'])} rows
        - Product Sales: {len(data['product_sales'])} rows
        - Geographic Data: {len(data['geographic_data'])} rows
        - Lead Scoring: {len(data['lead_scoring_results'])} rows
        """)
    
    with col2:
        st.info(f"""
        **Additional Data:**
        - Channel Attribution: {len(data['channel_attribution'])} rows
        - Customer Journey: {len(data['customer_journey'])} rows
        - Funnel Data: {len(data['funnel_data'])} rows
        - Feature Importance: {len(data['feature_importance'])} rows
        """)
    
    # Show sample data
    st.markdown("---")
    st.subheader("📋 Sample Data Preview")
    
    dataset_to_show = st.selectbox("Select dataset to preview:", list(data.keys()))
    st.dataframe(data[dataset_to_show].head(10), use_container_width=True)
    
    # Show column names
    with st.expander("📝 View Column Names"):
        st.write(f"**Columns in {dataset_to_show}:**")
        st.write(list(data[dataset_to_show].columns))

# Customer Analysis
elif analysis_type == "Customer Analysis":
    st.header("👥 Customer Analysis")
    
    df = data['customer_data']
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", len(df))
    
    with col2:
        age_col = safe_column(df, ['Age', 'age', 'Customer_Age'])
        if age_col:
            st.metric("Avg Age", f"{df[age_col].mean():.1f}")
    
    with col3:
        income_col = safe_column(df, ['Income', 'income', 'Annual_Income', 'Salary'])
        if income_col:
            st.metric("Avg Income", f"${df[income_col].mean():,.0f}")
    
    with col4:
        st.metric("Total Columns", len(df.columns))
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Visualizations", "Data Table", "Statistics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            age_col = safe_column(df, ['Age', 'age', 'Customer_Age'])
            if age_col:
                st.subheader("Age Distribution")
                fig = px.histogram(df, x=age_col, nbins=30, 
                                 color_discrete_sequence=['#1f77b4'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Age column not found")
        
        with col2:
            # Income distribution
            income_col = safe_column(df, ['Income', 'income', 'Annual_Income'])
            if income_col:
                st.subheader("Income Distribution")
                fig = px.box(df, y=income_col, color_discrete_sequence=['#2ecc71'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Income column not found")
    
    with tab2:
        st.dataframe(df, use_container_width=True)
    
    with tab3:
        st.dataframe(df.describe(), use_container_width=True)

# Campaign Performance
elif analysis_type == "Campaign Performance":
    st.header("📢 Campaign Performance Analysis")
    
    df = data['campaign_performance']
    
    # Show columns
    with st.expander("📝 Available Columns"):
        st.write(list(df.columns))
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Campaigns", len(df))
    
    with col2:
        budget_col = safe_column(df, ['Budget', 'budget', 'Campaign_Budget', 'Spend'])
        if budget_col:
            st.metric("Total Budget", f"${df[budget_col].sum():,.0f}")
    
    with col3:
        conv_col = safe_column(df, ['Conversions', 'conversions', 'Total_Conversions'])
        if conv_col:
            st.metric("Total Conversions", f"{df[conv_col].sum():,}")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Find campaign name and metric columns
        name_col = safe_column(df, ['CampaignName', 'Campaign_Name', 'Campaign', 'Name'])
        metric_col = safe_column(df, ['Conversions', 'Revenue', 'Sales', 'Clicks'])
        
        if name_col and metric_col:
            st.subheader(f"{metric_col} by Campaign")
            fig = px.bar(df, x=name_col, y=metric_col,
                       color=metric_col,
                       color_continuous_scale='Viridis')
            fig.update_xaxis(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        budget_col = safe_column(df, ['Budget', 'Spend', 'Cost'])
        roi_col = safe_column(df, ['ROI', 'ROAS', 'Return'])
        
        if budget_col and roi_col:
            st.subheader("Budget vs ROI")
            fig = px.scatter(df, x=budget_col, y=roi_col,
                           color=roi_col,
                           color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Campaign Data")
    st.dataframe(df, use_container_width=True)

# Channel Attribution
elif analysis_type == "Channel Attribution":
    st.header("📱 Channel Attribution Analysis")
    
    df = data['channel_attribution']
    
    with st.expander("📝 Available Columns"):
        st.write(list(df.columns))
    
    col1, col2 = st.columns(2)
    
    with col1:
        channel_col = safe_column(df, ['Channel', 'channel', 'Marketing_Channel'])
        conv_col = safe_column(df, ['Conversions', 'conversions', 'Total_Conversions'])
        
        if channel_col and conv_col:
            st.subheader("Conversions by Channel")
            fig = px.bar(df, x=channel_col, y=conv_col,
                       color=conv_col,
                       color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        revenue_col = safe_column(df, ['Revenue', 'revenue', 'Sales', 'Amount'])
        
        if channel_col and revenue_col:
            st.subheader("Revenue by Channel")
            fig = px.pie(df, values=revenue_col, names=channel_col, hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(df, use_container_width=True)

# Product Sales
elif analysis_type == "Product Sales":
    st.header("🛍️ Product Sales Analysis")
    
    df = data['product_sales']
    
    with st.expander("📝 Available Columns"):
        st.write(list(df.columns))
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Products", len(df))
    
    with col2:
        sales_col = safe_column(df, ['Sales', 'Revenue', 'Total_Sales', 'Amount'])
        if sales_col:
            st.metric("Total Sales", f"${df[sales_col].sum():,.0f}")
    
    with col3:
        qty_col = safe_column(df, ['Quantity', 'Units', 'Qty', 'Units_Sold'])
        if qty_col:
            st.metric("Total Units", f"{df[qty_col].sum():,}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_col = safe_column(df, ['Product', 'ProductName', 'Product_Name', 'Item'])
        sales_col = safe_column(df, ['Sales', 'Revenue', 'Amount'])
        
        if product_col and sales_col:
            st.subheader("Top 10 Products")
            top_products = df.nlargest(10, sales_col)
            fig = px.bar(top_products, x=product_col, y=sales_col,
                       color=sales_col,
                       color_continuous_scale='Greens')
            fig.update_xaxis(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        category_col = safe_column(df, ['Category', 'Product_Category', 'Type'])
        
        if category_col and sales_col:
            st.subheader("Sales by Category")
            cat_sales = df.groupby(category_col)[sales_col].sum().reset_index()
            fig = px.pie(cat_sales, values=sales_col, names=category_col)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(df, use_container_width=True)

# Geographic Analysis
elif analysis_type == "Geographic Analysis":
    st.header("🌍 Geographic Analysis")
    
    df = data['geographic_data']
    
    with st.expander("📝 Available Columns"):
        st.write(list(df.columns))
    
    col1, col2 = st.columns(2)
    
    with col1:
        region_col = safe_column(df, ['Region', 'region', 'Area', 'Territory'])
        
        if region_col:
            st.subheader("Distribution by Region")
            region_dist = df[region_col].value_counts().reset_index()
            region_dist.columns = [region_col, 'Count']
            fig = px.bar(region_dist, x=region_col, y='Count',
                       color='Count',
                       color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        country_col = safe_column(df, ['Country', 'country', 'Nation'])
        
        if country_col:
            st.subheader("Top 10 Countries")
            country_dist = df[country_col].value_counts().head(10).reset_index()
            country_dist.columns = [country_col, 'Count']
            fig = px.pie(country_dist, values='Count', names=country_col)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(df, use_container_width=True)

# Customer Journey
elif analysis_type == "Customer Journey":
    st.header("🛤️ Customer Journey Analysis")
    
    # Funnel Data
    funnel_df = data['funnel_data']
    
    with st.expander("📝 Funnel Data Columns"):
        st.write(list(funnel_df.columns))
    
    st.subheader("Conversion Funnel")
    
    stage_col = safe_column(funnel_df, ['Stage', 'stage', 'Step', 'Funnel_Stage'])
    count_col = safe_column(funnel_df, ['Count', 'count', 'Users', 'Visitors'])
    
    if stage_col and count_col:
        fig = go.Figure(go.Funnel(
            y=funnel_df[stage_col],
            x=funnel_df[count_col],
            textinfo="value+percent initial"
        ))
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Funnel Data")
        st.dataframe(funnel_df, use_container_width=True)
    
    with col2:
        st.subheader("Journey Data")
        st.dataframe(data['customer_journey'].head(20), use_container_width=True)

# Lead Scoring
elif analysis_type == "Lead Scoring":
    st.header("🎯 Lead Scoring Analysis")
    
    df = data['lead_scoring_results']
    
    with st.expander("📝 Available Columns"):
        st.write(list(df.columns))
    
    score_col = safe_column(df, ['LeadScore', 'Score', 'Lead_Score', 'Probability'])
    
    if score_col:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Avg Score", f"{df[score_col].mean():.2f}")
        
        with col2:
            st.metric("Max Score", f"{df[score_col].max():.2f}")
        
        with col3:
            st.metric("Total Leads", len(df))
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Score Distribution")
            fig = px.histogram(df, x=score_col, nbins=30,
                             color_discrete_sequence=['#9b59b6'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Score Box Plot")
            fig = px.box(df, y=score_col,
                       color_discrete_sequence=['#e74c3c'])
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(df, use_container_width=True)

# Feature Importance
elif analysis_type == "Feature Importance":
    st.header("📊 Feature Importance Analysis")
    
    df = data['feature_importance']
    
    with st.expander("📝 Available Columns"):
        st.write(list(df.columns))
    
    feature_col = safe_column(df, ['Feature', 'feature', 'Variable', 'Column'])
    importance_col = safe_column(df, ['Importance', 'importance', 'Score', 'Weight'])
    
    if feature_col and importance_col:
        st.subheader("Feature Importance Ranking")
        
        sorted_df = df.sort_values(importance_col, ascending=True)
        
        fig = px.bar(sorted_df, x=importance_col, y=feature_col,
                   orientation='h',
                   color=importance_col,
                   color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(df, use_container_width=True)

# Correlation Analysis
elif analysis_type == "Correlation Analysis":
    st.header("🔗 Correlation Analysis")
    
    df = data['correlation_matrix']
    
    st.subheader("Correlation Matrix Heatmap")
    
    try:
        fig = px.imshow(df,
                       text_auto='.2f',
                       aspect="auto",
                       color_continuous_scale='RdBu_r')
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("Correlation matrix format may need adjustment")
    
    st.markdown("---")
    st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p>📊 Marketing Analytics Dashboard | Built with Streamlit & Plotly</p>
        <p>Data-driven insights for better marketing decisions</p>
    </div>
    """, unsafe_allow_html=True)
