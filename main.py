# Supply Chain Sentinel Agent - A Streamlit Demonstration

import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import date, timedelta

# --- App Configuration ---
st.set_page_config(
    page_title="Supply Chain Sentinel Agent",
    page_icon="🤖",
    layout="wide"
)

# --- App Header ---
st.title("🤖 Supply Chain Sentinel Agent - Live Demo")
st.markdown("""
This application demonstrates the core functionality of the **Supply Chain Sentinel Agent**. 

The agent's goal is to maintain supply chain resilience by:
1.  **Perceiving** real-time data and disruptive events.
2.  **Reasoning** to predict potential component shortages.
3.  **Acting** by recommending specific, actionable mitigation strategies.

*This demo is based on the concepts presented in the AI Transformation Workshop.*
""")

# --- Attribution and License ---
st.sidebar.title("About")
st.sidebar.markdown("""
**Designed by Assoc Prof Ts Dr Yu Yong Poh, Tunku Abdul Rahman University of Management and Technology**
<a href="mailto:yuyp@tarc.edu.my">yuyp@tarc.edu.my</a>
""", unsafe_allow_html=True)
st.sidebar.info("""
**Disclaimer:** This is a demonstration application for illustrative purposes only. The data is simulated.
""")
st.sidebar.markdown("""
**License:** This work is licensed under a
<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.
<br/><br/>
<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" />
</a>
""", unsafe_allow_html=True)


# --- Data Simulation ---
def get_initial_data():
    """Creates a DataFrame simulating the company's supply chain status."""
    data = {
        'Component': ['CPU Model A', 'GPU Model X', '16GB DDR5 RAM', '1TB NVMe SSD', 'Power Supply Unit', 'Chassis Type B', 'Motherboard Z', 'Cooling Fan'],
        'Supplier': ['Intel', 'Nvidia', 'Micron', 'Samsung', 'Delta Electronics', 'Foxconn', 'ASUS', 'Nidec'],
        'Origin': ['USA', 'Taiwan', 'Singapore', 'South Korea', 'Taiwan', 'China', 'Taiwan', 'China'],
        'Shipping_Lane': ['Trans-Pacific', 'Taiwan-US', 'Intra-Asia', 'Korea-US', 'Taiwan-US', 'Intra-Asia', 'Taiwan-US', 'Intra-Asia'],
        'Lead_Time_Days': [25, 30, 15, 20, 30, 12, 28, 14],
        'On_Hand_Stock': [15000, 8000, 40000, 25000, 18000, 50000, 12000, 80000],
        'Daily_Consumption': [500, 250, 1200, 800, 600, 1500, 400, 2500],
        'Revenue_Per_Unit': [400, 600, 80, 120, 50, 25, 150, 10],
        'Secondary_Supplier': ['AMD', 'AMD', 'Hynix', 'Kioxia', 'Lite-On', 'Inventec', 'Gigabyte', 'Sunon'],
        'Status': ['Nominal'] * 8,
        'Alerts': ['-'] * 8
    }
    df = pd.DataFrame(data)
    df['Days_of_Supply'] = df['On_Hand_Stock'] / df['Daily_Consumption']
    return df

# --- Event Simulation ---
def simulate_disruptive_events(df):
    """Introduces random disruptive events into the supply chain."""
    events = []
    num_events = random.randint(1, 2) # Reduced number of events for clarity
    
    # UPDATED: Replaced 'Factory Shutdown' with a less severe event
    possible_events = [
        'Port Congestion', 'Geopolitical Tension', 'Production Slowdown', 'Demand Spike'
    ]
    
    for _ in range(num_events):
        event_type = random.choice(possible_events)
        
        if event_type == 'Port Congestion':
            lane = random.choice(df['Shipping_Lane'].unique())
            delay = random.randint(5, 10)
            df.loc[df['Shipping_Lane'] == lane, 'Lead_Time_Days'] += delay
            events.append({
                'type': 'Port Congestion 港口拥堵', 'details': f"Congestion in the **{lane}** lane. Estimated delay: **{delay} days**."
            })

        elif event_type == 'Geopolitical Tension':
            origin = random.choice(df['Origin'].unique())
            delay = random.randint(7, 12)
            df.loc[df['Origin'] == origin, 'Lead_Time_Days'] += delay
            events.append({
                'type': 'Geopolitical Tension 地缘政治紧张', 'details': f"Tensions in **{origin}** causing customs delays. Estimated impact: **{delay} days**."
            })

        # NEW EVENT: More realistic than a full shutdown
        elif event_type == 'Production Slowdown':
            supplier_to_slow = random.choice(df['Supplier'].unique())
            delay = random.randint(4, 8)
            df.loc[df['Supplier'] == supplier_to_slow, 'Lead_Time_Days'] += delay
            events.append({
                'type': 'Production Slowdown 生产放缓', 'details': f"Reports of a production slowdown at **{supplier_to_slow}** due to quality issues. Estimated delay: **{delay} days**."
            })
        
        elif event_type == 'Demand Spike':
            component_to_spike = random.choice(df['Component'].unique())
            spike_factor = random.uniform(1.20, 1.50)
            df.loc[df['Component'] == component_to_spike, 'Daily_Consumption'] = int(df.loc[df['Component'] == component_to_spike, 'Daily_Consumption'] * spike_factor)
            events.append({
                'type': 'Demand Spike 需求激增', 'details': f"Unexpected surge in demand for **{component_to_spike}**. Consumption increased by **{spike_factor:.0%}**."
            })
            
    return df, events

# --- Sentinel Agent Logic ---
def run_sentinel_agent(df):
    """The core agent logic: Perceive, Reason, Act."""
    critical_threshold_days = 15
    df['Days_of_Supply'] = (df['On_Hand_Stock'] / df['Daily_Consumption']).round(1)
    
    for index, row in df.iterrows():
        projected_supply_at_reorder_point = row['Days_of_Supply'] - row['Lead_Time_Days']
        
        if projected_supply_at_reorder_point < 0:
            df.loc[index, 'Status'] = 'CRITICAL'
            df.loc[index, 'Alerts'] = f"ACTION: Projected shortfall of {-projected_supply_at_reorder_point:.1f} days. Expedite next shipment via Air Freight."
        elif row['Days_of_Supply'] < critical_threshold_days:
            df.loc[index, 'Status'] = 'WARNING'
            df.loc[index, 'Alerts'] = f"WARNING: Supply below {critical_threshold_days}-day threshold. Monitor closely."
        else:
            df.loc[index, 'Status'] = 'Nominal'
            df.loc[index, 'Alerts'] = '-'
            
    return df

# --- Business Impact Calculation ---
def calculate_business_impact(df_after_agent):
    """Calculates the financial impact of the agent's actions."""
    AIR_FREIGHT_PREMIUM_PER_SHIPMENT = 120_000 
    
    total_potential_loss = 0
    total_mitigation_cost = 0

    critical_items = df_after_agent[df_after_agent['Status'] == 'CRITICAL']

    for index, row in critical_items.iterrows():
        if "Projected shortfall" in row['Alerts']:
            shortfall_days = row['Lead_Time_Days'] - row['Days_of_Supply']
            if shortfall_days > 0:
                # Calculate potential revenue loss from this specific component shortage
                total_potential_loss += shortfall_days * (row['Daily_Consumption'] * row['Revenue_Per_Unit'])
                total_mitigation_cost += AIR_FREIGHT_PREMIUM_PER_SHIPMENT
        
    net_value_generated = total_potential_loss - total_mitigation_cost
    return total_potential_loss, total_mitigation_cost, net_value_generated

# --- Mitigation Suggestion Logic ---
def get_mitigation_plan(events):
    """Generates high-level mitigation plans for each event."""
    plans = []
    for event in events:
        plan = f"**For the '{event['type']}' event:** "
        if 'Port Congestion' in event['type']:
            plan += "Engage freight forwarder to assess alternative sea/air routes. Increase monitoring frequency."
        elif 'Geopolitical Tension' in event['type']:
            plan += "Review inventory levels for all components from the affected region. Place early orders with secondary suppliers."
        elif 'Production Slowdown' in event['type']:
            plan += "Contact supplier immediately for root cause analysis and a firm recovery timeline. Assess impact on production schedule."
        elif 'Demand Spike' in event['type']:
            plan += "Alert Sales & Operations Planning (S&OP) team. Validate if spike is temporary or a new baseline."
        plans.append(plan)
    return plans

# --- Main App UI ---
# Initialize or load data
if 'supply_data' not in st.session_state:
    st.session_state.supply_data = get_initial_data()
    st.session_state.impact = None
    st.session_state.history = []

st.header("Supply Chain Status Dashboard")
st.dataframe(
    st.session_state.supply_data.style.apply(
        lambda s: ['background-color: #8B0000; color: white' if s == 'CRITICAL' 
                   else 'background-color: #FFD700; color: black' if s == 'WARNING' 
                   else '' for s in s], subset=['Status']
    ), 
    use_container_width=True
)
st.divider()

# --- Simulation Control & Output ---
col1, col2 = st.columns(2)
with col1:
    st.header("Agent Control")
    st.markdown("Trigger a simulation to see the Sentinel Agent in action.")
    if st.button("🚨 Simulate Events & Run Agent", type="primary", use_container_width=True):
        df_after_events, events = simulate_disruptive_events(get_initial_data())
        st.session_state.events = events
        df_after_agent = run_sentinel_agent(df_after_events)
        st.session_state.supply_data = df_after_agent
        st.session_state.impact = calculate_business_impact(df_after_agent)
        
        # Add to history
        run_number = len(st.session_state.history) + 1
        st.session_state.history.append({
            'Run': run_number,
            'Net Value Generated': st.session_state.impact[2] if st.session_state.impact[2] > 0 else 0
        })
        st.rerun()

    if st.button("🔄 Reset Simulation", use_container_width=True):
        st.session_state.supply_data = get_initial_data()
        st.session_state.impact = None
        st.session_state.history = []
        if 'events' in st.session_state:
            del st.session_state['events']
        st.rerun()

with col2:
    st.header("Agent Log & Recommendations")
    if 'events' in st.session_state and st.session_state.events:
        with st.container(border=True):
            st.subheader("Perceived Events")
            for event in st.session_state.events:
                st.warning(f"**{event['type']}:** {event['details']}")
        with st.container(border=True):
            st.subheader("Suggested Mitigation Plan")
            mitigation_plans = get_mitigation_plan(st.session_state.events)
            for plan in mitigation_plans:
                st.info(plan)
    else:
        st.info("Waiting for simulation to be triggered...")

st.divider()

# --- Tangible Benefit Simulation Section ---
st.header("📈 Tangible Benefit Simulation")
if st.session_state.impact:
    potential_loss, mitigation_cost, net_value = st.session_state.impact
    
    st.subheader("Latest Simulation Run Analysis")
    if potential_loss > 0:
        c1, c2, c3 = st.columns(3)
        c1.metric("Potential Revenue Loss Avoided", f"${potential_loss:,.0f}")
        c2.metric("Cost of Recommended Action", f"${mitigation_cost:,.0f}")
        c3.metric("Net Value Generated by Agent", f"${net_value:,.0f}", delta=f"${net_value:,.0f}")
    else:
        st.success("No critical financial risks were identified in the latest run. The supply chain remains resilient.")
    
    # --- Cumulative & Trend Analysis ---
    if len(st.session_state.history) > 0:
        st.subheader("Cumulative & Trend Analysis (All Runs)")
        history_df = pd.DataFrame(st.session_state.history)
        
        c4, c5 = st.columns(2)
        with c4:
            total_net_value = history_df['Net Value Generated'].sum()
            st.metric("Total Net Value Generated (All Runs)", f"${total_net_value:,.0f}")
        with c5:
            st.markdown("**Net Value Trend**")
            st.line_chart(history_df.set_index('Run')['Net Value Generated'])
else:
    st.info("Run a simulation to see the agent's financial impact analysis.")


