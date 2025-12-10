import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function with caching
@st.cache_data
def load_data():
    """Load all CSV files from Dataset folder"""
    try:
        campaign_performance = pd.read_csv('Dataset/campaign_performance.csv')
        channel_attribution = pd.read_csv('Dataset/channel_attribution.csv')
        correlation_matrix = pd.read_csv('Dataset/correlation_matrix.csv')
        customer_data = pd.read_csv('Dataset/customer_data.csv')
        customer_journey = pd.read_csv('Dataset/customer_journey.csv')
        feature_importance = pd.read_csv('Dataset/feature_importance.csv')
        funnel_data = pd.read_csv('Dataset/funnel_data.csv')
        geographic_data = pd.read_csv('Dataset/geographic_data.csv')
        lead_scoring_results = pd.read_csv('Dataset/lead_scoring_results.csv')
        learning_curve = pd.read_csv('Dataset/learning_curve.csv')
        product_sales = pd.read_csv('Dataset/product_sales.csv')
        
        return {
            'campaign_performance': campaign_performance,
            'channel_attribution': channel_attribution,
            'correlation_matrix': correlation_matrix,
            'customer_data': customer_data,
            'customer_journey': customer_journey,
            'feature_importance': feature_importance,
            'funnel_data': funnel_data,
            'geographic_data': geographic_data,
            'lead_scoring_results': lead_scoring_results,
            'learning_curve': learning_curve,
            'product_sales': product_sales
        }
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please ensure all CSV files are in the 'Dataset' folder")
        return None

# Load all data
data = load_data()

if data is None:
    st.stop()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/000000/business-report.png", width=100)
    st.title("📊 Marketing Analytics")
    st.markdown("---")
    
    # Analysis selector
    st.subheader("Select Analysis View")
    analysis_type = st.selectbox(
        "Choose Analysis Type",
        ["Overview", "Customer Analysis", "Campaign Performance", "Channel Attribution", 
         "Product Sales", "Geographic Analysis", "Customer Journey", "Lead Scoring",
         "Feature Importance", "Correlation Analysis"]
    )
    
    st.markdown("---")
    st.info("💡 **Tip**: Explore different views to gain insights")

# Main content
st.title("🎯 Marketing Analytics Dashboard")
st.markdown("### Comprehensive Marketing Performance Analysis")

# Overview Section
if analysis_type == "Overview":
    st.header("📈 Executive Summary")
    
    # KPI Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_customers = len(data['customer_data'])
        st.metric("Total Customers", f"{total_customers:,}")
    
    with col2:
        if 'Revenue' in data['product_sales'].columns:
            total_revenue = data['product_sales']['Revenue'].sum()
            st.metric("Total Revenue", f"${total_revenue:,.0f}")
        elif 'Sales' in data['product_sales'].columns:
            total_sales = data['product_sales']['Sales'].sum()
            st.metric("Total Sales", f"${total_sales:,.0f}")
    
    with col3:
        total_campaigns = len(data['campaign_performance'])
        st.metric("Total Campaigns", total_campaigns)
    
    with col4:
        if 'ConversionRate' in data['funnel_data'].columns:
            avg_conversion = data['funnel_data']['ConversionRate'].mean()
            st.metric("Avg Conversion Rate", f"{avg_conversion:.2f}%")
        elif 'Conversions' in data['funnel_data'].columns:
            total_conversions = data['funnel_data']['Conversions'].sum()
            st.metric("Total Conversions", f"{total_conversions:,}")
    
    with col5:
        if 'LeadScore' in data['lead_scoring_results'].columns:
            avg_lead_score = data['lead_scoring_results']['LeadScore'].mean()
            st.metric("Avg Lead Score", f"{avg_lead_score:.2f}")
    
    st.markdown("---")
    
    # Display sample data from each dataset
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Campaign Performance Overview")
        st.dataframe(data['campaign_performance'].head(10), use_container_width=True)
    
    with col2:
        st.subheader("👥 Customer Data Sample")
        st.dataframe(data['customer_data'].head(10), use_container_width=True)
    
    # Visualizations
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Product Sales Distribution")
        if 'Product' in data['product_sales'].columns and 'Sales' in data['product_sales'].columns:
            fig = px.bar(data['product_sales'].head(10), 
                        x='Product', y='Sales',
                        color='Sales',
                        color_continuous_scale='Blues')
            fig.update_xaxis(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Geographic Distribution")
        if 'Region' in data['geographic_data'].columns:
            region_dist = data['geographic_data']['Region'].value_counts().reset_index()
            region_dist.columns = ['Region', 'Count']
            fig = px.pie(region_dist, values='Count', names='Region', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

# Customer Analysis Section
elif analysis_type == "Customer Analysis":
    st.header("👥 Customer Analysis")
    
    # Display customer data info
    st.subheader("Customer Data Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Customers", len(data['customer_data']))
    
    with col2:
        if 'Age' in data['customer_data'].columns:
            avg_age = data['customer_data']['Age'].mean()
            st.metric("Average Age", f"{avg_age:.1f}")
    
    with col3:
        if 'Income' in data['customer_data'].columns:
            avg_income = data['customer_data']['Income'].mean()
            st.metric("Avg Income", f"${avg_income:,.0f}")
    
    st.markdown("---")
    
    # Tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["Customer Demographics", "Data Table", "Statistics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution if available
            if 'Age' in data['customer_data'].columns:
                st.subheader("Age Distribution")
                fig = px.histogram(data['customer_data'], x='Age', 
                                 nbins=30, color_discrete_sequence=['#1f77b4'])
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Income distribution if available
            if 'Income' in data['customer_data'].columns:
                st.subheader("Income Distribution")
                fig = px.box(data['customer_data'], y='Income',
                           color_discrete_sequence=['#2ecc71'])
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Customer Data Table")
        st.dataframe(data['customer_data'], use_container_width=True)
    
    with tab3:
        st.subheader("Statistical Summary")
        st.dataframe(data['customer_data'].describe(), use_container_width=True)

# Campaign Performance Section
elif analysis_type == "Campaign Performance":
    st.header("📢 Campaign Performance Analysis")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Campaigns", len(data['campaign_performance']))
    
    with col2:
        if 'Budget' in data['campaign_performance'].columns:
            total_budget = data['campaign_performance']['Budget'].sum()
            st.metric("Total Budget", f"${total_budget:,.0f}")
    
    with col3:
        if 'Conversions' in data['campaign_performance'].columns:
            total_conversions = data['campaign_performance']['Conversions'].sum()
            st.metric("Total Conversions", f"{total_conversions:,}")
    
    with col4:
        if 'ROI' in data['campaign_performance'].columns:
            avg_roi = data['campaign_performance']['ROI'].mean()
            st.metric("Average ROI", f"{avg_roi:.2f}%")
    
    st.markdown("---")
    
    # Visualizations
    tab1, tab2, tab3 = st.tabs(["Performance Metrics", "Data Table", "Trends"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            if 'CampaignName' in data['campaign_performance'].columns and 'Conversions' in data['campaign_performance'].columns:
                st.subheader("Conversions by Campaign")
                fig = px.bar(data['campaign_performance'], 
                           x='CampaignName', y='Conversions',
                           color='Conversions',
                           color_continuous_scale='Viridis')
                fig.update_xaxis(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Budget' in data['campaign_performance'].columns and 'ROI' in data['campaign_performance'].columns:
                st.subheader("Budget vs ROI")
                fig = px.scatter(data['campaign_performance'], 
                               x='Budget', y='ROI',
                               size='Conversions' if 'Conversions' in data['campaign_performance'].columns else None,
                               color='ROI',
                               color_continuous_scale='RdYlGn')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Campaign Performance Data")
        st.dataframe(data['campaign_performance'], use_container_width=True)
    
    with tab3:
        st.subheader("Statistical Summary")
        st.dataframe(data['campaign_performance'].describe(), use_container_width=True)

# Channel Attribution Section
elif analysis_type == "Channel Attribution":
    st.header("📱 Channel Attribution Analysis")
    
    st.subheader("Channel Performance Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Channel' in data['channel_attribution'].columns and 'Conversions' in data['channel_attribution'].columns:
            st.subheader("Conversions by Channel")
            fig = px.bar(data['channel_attribution'], 
                       x='Channel', y='Conversions',
                       color='Conversions',
                       color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Channel' in data['channel_attribution'].columns and 'Revenue' in data['channel_attribution'].columns:
            st.subheader("Revenue by Channel")
            fig = px.pie(data['channel_attribution'], 
                       values='Revenue', names='Channel',
                       hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Channel Attribution Data")
    st.dataframe(data['channel_attribution'], use_container_width=True)

# Product Sales Section
elif analysis_type == "Product Sales":
    st.header("🛍️ Product Sales Analysis")
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_products = len(data['product_sales'])
        st.metric("Total Products", total_products)
    
    with col2:
        if 'Sales' in data['product_sales'].columns:
            total_sales = data['product_sales']['Sales'].sum()
            st.metric("Total Sales", f"${total_sales:,.0f}")
    
    with col3:
        if 'Quantity' in data['product_sales'].columns:
            total_quantity = data['product_sales']['Quantity'].sum()
            st.metric("Total Units Sold", f"{total_quantity:,}")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Product' in data['product_sales'].columns and 'Sales' in data['product_sales'].columns:
            st.subheader("Top 10 Products by Sales")
            top_products = data['product_sales'].nlargest(10, 'Sales')
            fig = px.bar(top_products, x='Product', y='Sales',
                       color='Sales',
                       color_continuous_scale='Greens')
            fig.update_xaxis(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Category' in data['product_sales'].columns and 'Sales' in data['product_sales'].columns:
            st.subheader("Sales by Category")
            category_sales = data['product_sales'].groupby('Category')['Sales'].sum().reset_index()
            fig = px.pie(category_sales, values='Sales', names='Category')
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Product Sales Data")
    st.dataframe(data['product_sales'], use_container_width=True)

# Geographic Analysis Section
elif analysis_type == "Geographic Analysis":
    st.header("🌍 Geographic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Region' in data['geographic_data'].columns:
            st.subheader("Distribution by Region")
            region_dist = data['geographic_data']['Region'].value_counts().reset_index()
            region_dist.columns = ['Region', 'Count']
            fig = px.bar(region_dist, x='Region', y='Count',
                       color='Count',
                       color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Country' in data['geographic_data'].columns:
            st.subheader("Distribution by Country")
            country_dist = data['geographic_data']['Country'].value_counts().head(10).reset_index()
            country_dist.columns = ['Country', 'Count']
            fig = px.pie(country_dist, values='Count', names='Country')
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Geographic Data")
    st.dataframe(data['geographic_data'], use_container_width=True)

# Customer Journey Section
elif analysis_type == "Customer Journey":
    st.header("🛤️ Customer Journey Analysis")
    
    # Funnel visualization
    st.subheader("Conversion Funnel")
    
    if 'Stage' in data['funnel_data'].columns and 'Count' in data['funnel_data'].columns:
        fig = go.Figure(go.Funnel(
            y=data['funnel_data']['Stage'],
            x=data['funnel_data']['Count'],
            textinfo="value+percent initial"
        ))
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Funnel Data")
        st.dataframe(data['funnel_data'], use_container_width=True)
    
    with col2:
        st.subheader("Customer Journey Data")
        st.dataframe(data['customer_journey'].head(20), use_container_width=True)

# Lead Scoring Section
elif analysis_type == "Lead Scoring":
    st.header("🎯 Lead Scoring Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'LeadScore' in data['lead_scoring_results'].columns:
            avg_score = data['lead_scoring_results']['LeadScore'].mean()
            st.metric("Average Lead Score", f"{avg_score:.2f}")
    
    with col2:
        if 'LeadScore' in data['lead_scoring_results'].columns:
            max_score = data['lead_scoring_results']['LeadScore'].max()
            st.metric("Max Lead Score", f"{max_score:.2f}")
    
    with col3:
        total_leads = len(data['lead_scoring_results'])
        st.metric("Total Leads", f"{total_leads:,}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'LeadScore' in data['lead_scoring_results'].columns:
            st.subheader("Lead Score Distribution")
            fig = px.histogram(data['lead_scoring_results'], x='LeadScore',
                             nbins=30,
                             color_discrete_sequence=['#9b59b6'])
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'LeadScore' in data['lead_scoring_results'].columns:
            st.subheader("Lead Score Box Plot")
            fig = px.box(data['lead_scoring_results'], y='LeadScore',
                       color_discrete_sequence=['#e74c3c'])
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Lead Scoring Results")
    st.dataframe(data['lead_scoring_results'], use_container_width=True)

# Feature Importance Section
elif analysis_type == "Feature Importance":
    st.header("📊 Feature Importance Analysis")
    
    if 'Feature' in data['feature_importance'].columns and 'Importance' in data['feature_importance'].columns:
        st.subheader("Feature Importance Ranking")
        
        # Sort by importance
        sorted_features = data['feature_importance'].sort_values('Importance', ascending=True)
        
        fig = px.bar(sorted_features, 
                   x='Importance', y='Feature',
                   orientation='h',
                   color='Importance',
                   color_continuous_scale='Viridis',
                   title='Feature Importance Scores')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Feature Importance Data")
    st.dataframe(data['feature_importance'], use_container_width=True)

# Correlation Analysis Section
elif analysis_type == "Correlation Analysis":
    st.header("🔗 Correlation Analysis")
    
    st.subheader("Correlation Matrix Heatmap")
    
    # Create heatmap
    fig = px.imshow(data['correlation_matrix'],
                   text_auto=True,
                   aspect="auto",
                   color_continuous_scale='RdBu_r',
                   title='Feature Correlation Matrix')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Correlation Matrix Data")
    st.dataframe(data['correlation_matrix'], use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p>📊 Marketing Analytics Dashboard | Built with Streamlit & Plotly</p>
        <p>Data-driven insights for better marketing decisions</p>
    </div>
    """, unsafe_allow_html=True)
