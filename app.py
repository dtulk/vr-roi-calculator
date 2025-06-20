import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="VR Software ROI Calculator", page_icon="🥽", layout="wide")

# Title and description
st.title("🥽 VR Software ROI Calculator")
st.markdown("Calculate the Return on Investment for VR training software implementation")

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["📊 Calculator", "📈 Analysis", "📋 Report"])

with tab1:
    # Create columns for inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("👥 Company Parameters")
        num_employees = st.number_input("Number of Employees", min_value=1, value=400, step=10)
        pay_per_hour = st.number_input("Pay per Hour ($)", min_value=0.0, value=25.0, step=0.5, format="%.2f")
        
        st.header("💰 Investment Costs")
        vr_content_dev = st.number_input("VR Content Development ($)", min_value=0, value=60000, step=1000)
        licensing_maintenance = st.number_input("Annual Licensing & Maintenance ($)", min_value=0, value=24000, step=1000)
        hardware = st.number_input("Hardware ($)", min_value=0, value=10000, step=1000)
        internal_resources = st.number_input("Internal Resources ($)", min_value=0, value=25000, step=1000)
        materials = st.number_input("Materials ($)", min_value=0, value=5000, step=500)
        hardware_refresh_cost = st.number_input("Hardware Refresh Cost (Year 4) ($)", min_value=0, value=14000, step=1000)
    
    with col2:
        st.header("✈️ Travel Parameters")
        trip_reductions = st.number_input("Trip Reductions per Year", min_value=0, value=4, step=1)
        cost_per_trip = st.number_input("Cost per Trip ($)", min_value=0, value=1600, step=100)
        work_hours_lost_per_trip = st.number_input("Work Hours Lost per Trip", min_value=0.0, value=54.0, step=1.0)
        
        st.header("⚠️ Incident Parameters")
        incident_count = st.number_input("Current Incidents per Year", min_value=0, value=2, step=1)
        incident_frequency = st.number_input("Incident Frequency Reduction (%)", min_value=0, value=10, step=5)
        productivity_loss_per_incident = st.number_input("Productivity Loss per Incident (hours)", min_value=0.0, value=45.0, step=5.0)
        
        st.header("💡 Additional Savings")
        travel_productivity_savings = st.number_input("Travel Productivity Savings ($)", min_value=0, value=21600, step=1000)
        incident_savings = st.number_input("Incident Reduction Savings ($)", min_value=0, value=12000, step=1000)
        year4_bonus_savings = st.number_input("Year 4 Additional Savings ($)", min_value=0, value=47000, step=1000)

# Calculations
def calculate_vr_roi():
    # Yearly costs
    year1_cost = vr_content_dev + licensing_maintenance + hardware + internal_resources + materials
    year2_cost = licensing_maintenance
    year3_cost = licensing_maintenance
    year4_cost = licensing_maintenance + hardware_refresh_cost
    
    # Savings calculations
    travel_cost_savings = trip_reductions * cost_per_trip
    materials_savings = materials  # Assuming all materials are saved
    
    # Base yearly savings
    yearly_savings = travel_cost_savings + travel_productivity_savings + materials_savings + incident_savings
    
    # Year 4 has additional savings
    year4_savings = yearly_savings + year4_bonus_savings
    
    # Calculate net savings for each year
    results = {
        'Year': [1, 2, 3, 4],
        'Savings': [yearly_savings, yearly_savings, yearly_savings, year4_savings],
        'Costs': [year1_cost, year2_cost, year3_cost, year4_cost],
        'Net_Savings': [
            yearly_savings - year1_cost,
            yearly_savings - year2_cost,
            yearly_savings - year3_cost,
            year4_savings - year4_cost
        ]
    }
    
    return results, yearly_savings, year4_savings

results, base_yearly_savings, year4_total_savings = calculate_vr_roi()

# Display key metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

total_4_year_savings = sum(results['Savings'])
total_4_year_costs = sum(results['Costs'])
total_net_savings = sum(results['Net_Savings'])
roi_percentage = (total_net_savings / total_4_year_costs) * 100

with col1:
    st.metric("4-Year Total Savings", f"${total_4_year_savings:,}")

with col2:
    st.metric("4-Year Total Costs", f"${total_4_year_costs:,}")

with col3:
    st.metric("4-Year Net Savings", f"${total_net_savings:,}")

with col4:
    st.metric("4-Year ROI", f"{roi_percentage:.1f}%")

# Results table
st.header("📋 Year-by-Year Breakdown")
df = pd.DataFrame(results)
df['Savings'] = df['Savings'].apply(lambda x: f"${x:,}")
df['Costs'] = df['Costs'].apply(lambda x: f"${x:,}")
df['Net_Savings'] = df['Net_Savings'].apply(lambda x: f"${x:,}")
st.table(df)

with tab2:
    st.header("📈 Financial Analysis")
    
    # Create visualization of savings vs costs
    fig = go.Figure()
    
    # Add savings bars
    fig.add_trace(go.Bar(
        x=results['Year'],
        y=results['Savings'],
        name='Savings',
        marker_color='green',
        opacity=0.7
    ))
    
    # Add costs bars
    fig.add_trace(go.Bar(
        x=results['Year'],
        y=results['Costs'],
        name='Costs',
        marker_color='red',
        opacity=0.7
    ))
    
    fig.update_layout(
        title='Annual Savings vs Costs',
        xaxis_title='Year',
        yaxis_title='Amount ($)',
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cumulative savings chart
    cumulative_net = []
    running_total = 0
    for net in results['Net_Savings']:
        running_total += net
        cumulative_net.append(running_total)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=results['Year'],
        y=cumulative_net,
        mode='lines+markers',
        name='Cumulative Net Savings',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))
    
    fig2.update_layout(
        title='Cumulative Net Savings Over Time',
        xaxis_title='Year',
        yaxis_title='Cumulative Net Savings ($)',
        height=400
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Savings breakdown
    st.subheader("💰 Savings Breakdown (Annual)")
    savings_breakdown = {
        'Category': ['Travel Cost Savings', 'Travel Productivity Savings', 'Materials Savings', 'Incident Reduction Savings'],
        'Amount': [
            trip_reductions * cost_per_trip,
            travel_productivity_savings,
            materials,
            incident_savings
        ]
    }
    
    fig3 = px.pie(
        values=savings_breakdown['Amount'],
        names=savings_breakdown['Category'],
        title='Annual Savings Sources'
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.header("📋 Detailed Report")
    
    # Investment summary
    st.subheader("💰 Investment Summary")
    investment_data = {
        'Component': ['VR Content Development', 'Annual Licensing & Maintenance', 'Hardware', 'Internal Resources', 'Materials', 'Hardware Refresh (Year 4)'],
        'Cost': [f"${vr_content_dev:,}", f"${licensing_maintenance:,}", f"${hardware:,}", f"${internal_resources:,}", f"${materials:,}", f"${hardware_refresh_cost:,}"]
    }
    st.table(pd.DataFrame(investment_data))
    
    # Savings summary
    st.subheader("💡 Savings Summary")
    savings_data = {
        'Savings Source': ['Travel Cost Reduction', 'Travel Productivity Gains', 'Materials Savings', 'Incident Reduction'],
        'Annual Amount': [
            f"${trip_reductions * cost_per_trip:,}",
            f"${travel_productivity_savings:,}",
            f"${materials:,}",
            f"${incident_savings:,}"
        ],
        'Calculation': [
            f"{trip_reductions} trips × ${cost_per_trip:,}",
            "Custom input",
            f"Materials cost saved",
            "Custom input"
        ]
    }
    st.table(pd.DataFrame(savings_data))
    
    # ROI Analysis
    st.subheader("📊 ROI Analysis")
    if total_net_savings > 0:
        payback_period = None
        cumulative = 0
        for i, net in enumerate(results['Net_Savings']):
            cumulative += net
            if cumulative > 0 and payback_period is None:
                payback_period = i + 1
                break
        
        st.success(f"✅ Positive ROI of {roi_percentage:.1f}% over 4 years")
        if payback_period:
            st.info(f"💡 Payback period: {payback_period} year(s)")
        else:
            st.warning("⚠️ Payback period exceeds 4 years")
    else:
        st.error(f"❌ Negative ROI of {roi_percentage:.1f}% over 4 years")
    
    # Export functionality
    st.subheader("📥 Export Data")
    
    # Prepare export data
    export_df = pd.DataFrame({
        'Year': results['Year'],
        'Savings ($)': results['Savings'],
        'Costs ($)': results['Costs'],
        'Net Savings ($)': results['Net_Savings']
    })
    
    csv = export_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="vr_roi_analysis.csv",
        mime="text/csv"
    )
