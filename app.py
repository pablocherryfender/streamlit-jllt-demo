import streamlit as st
import pandas as pd
import datetime
import random
import openai
import plotly.express as px
import plotly.graph_objects as go

# OpenAI API key
openai.api_key = st.secrets["openai"]  # Ensure your API key is stored securely in Streamlit secrets

# Set corporate colors for JLL
jll_colors = {
    "red": "#bf1e2e",
    "grey": "#555555",
    "white": "#ffffff",
    "black": "#000000"
}

# Function to display section headers with styled background
def section_header(title):
    st.markdown(f"### {title}")
    st.markdown("---")

# Function to simulate fetching similar projects from a database
def fetch_similar_projects(project_type):
    # Placeholder function; replace with actual database queries
    return [
        {"name": "Project Alpha", "link": "https://example.com/project_alpha"},
        {"name": "Project Beta", "link": "https://example.com/project_beta"},
        {"name": "Project Gamma", "link": "https://example.com/project_gamma"}
    ]

# Function to generate a solution architecture description
def generate_description(project_params):
    messages = [
        {
            "role": "system",
            "content": "You are an expert in creating concise architecture documentation based on project specifications.Max 1000 characters."
        },
        {
            "role": "user",
            "content": f"""
            Create a high-level solution architecture description based on the following project parameters:
            - Data Sources: {', '.join(project_params.get('data_sources', [])) or 'None'}
            - ETL Type: {project_params.get('etl_type', 'N/A')}
            - Data Warehouse: {project_params.get('data_warehouse', 'N/A')}
            - Solution Type: {project_params.get('solution_type', 'N/A')}
            - BI Dashboard: {project_params.get('dashboard_required', 'N/A')}
            - Storage Requirements: {project_params.get('storage_needs', 'N/A')}
            - Compute Hours: {project_params.get('compute_hours', 'N/A')}
            - Security Level: {project_params.get('security_level', 'N/A')}
            - AI Integration: {'Yes' if project_params.get('ai_integration') else 'No'}
            - API Access Required: {'Yes' if project_params.get('api_access') else 'No'}
            - Monitoring: {project_params.get('monitoring', 'N/A')}
            - Support: {project_params.get('support', 'N/A')}
            """
        }
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=300,
            temperature=0.5,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"An error occurred while generating the description: {str(e)}")
        return None

# Sidebar Menu for Tab Selection
with st.sidebar:
    st.image("jll_logo.png", use_column_width=True)
    # st.title("Navigation")
    selected = st.radio(
        "",
        ["Home", "Client Overview", "Cost Estimator", "Sales Pipeline"],
        index=0
    )
    st.markdown("---")
    st.markdown("**Client Overview**")
    st.caption("Contracts, Change Requests, Current Products")
    st.markdown("**Cost Estimator**")
    st.caption("Simulate Project Implementation & Ongoing Costs")
    st.markdown("**Sales Pipeline**")
    st.caption("Opportunities & Sales Activities Overview")

# ------------------- Home Tab -------------------
if selected == "Home":
    st.title("Welcome to the BI Solutions Management App")
    st.write(
        """
        This application is designed to assist sales managers in managing client relationships and estimating project costs for BI solutions with AI-powered insights.
        Navigate through the tabs on the left to explore different functionalities.
        """
    )
    # st.image("jll_logo.png", use_column_width=True)

# ------------------- Client Overview Tab -------------------
elif selected == "Client Overview":
    st.title("Client Relationship Overview")

    # Sample data for clients
    clients_data = {
        "Client Name": [
            "ACME Corp", "Globex Inc", "Initech", "Umbrella Corp", "Hooli",
            "Stark Industries", "Wayne Enterprises", "Soylent Corp", "Massive Dynamic", "Vandelay Industries"
        ],
        "Contract Start": [
            "2022-01-01", "2021-06-15", "2023-03-01", "2020-11-11", "2022-05-20",
            "2021-09-30", "2022-01-15", "2023-02-01", "2020-07-01", "2021-12-01"
        ],
        "Contract End": [
            "2024-12-31", "2023-06-14", "2025-03-01", "2023-11-10", "2024-05-19",
            "2024-09-29", "2025-01-14", "2024-02-01", "2023-07-01", "2023-12-01"
        ],
        "Solutions": [
            ["Data Warehouse", "Tableau Dashboards"], ["ETL Pipeline", "Real-time Data Sync"],
            ["Operational Reporting", "Machine Learning"], ["IoT Integration", "Data Lake"],
            ["Data Pipeline", "Custom Visualizations"], ["AI/ML Integration", "Data Warehouse"],
            ["Real-time Data Sync", "IoT Integration"], ["Data Lake", "ETL Pipeline"],
            ["Machine Learning", "Custom Visualizations"], ["Operational Reporting", "Data Lake"]
        ],
        "CR Count": [5, 3, 7, 4, 6, 8, 2, 3, 5, 4],
        "Renewal Likelihood": ["High", "Medium", "High", "Low", "Medium", "High", "Medium", "Low", "Medium", "Low"]
    }
    clients_df = pd.DataFrame(clients_data)

    # Client Filter Dropdown
    client_name = st.selectbox("Select a Client:", clients_df["Client Name"])

    # Filter data based on selected client
    client_data = clients_df[clients_df["Client Name"] == client_name].iloc[0]

    # Display Tiles for Key Metrics
    st.subheader(f"Overview for {client_name}")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Contract Start Date", client_data["Contract Start"])
        st.metric("Contract End Date", client_data["Contract End"])
        st.metric("CRs Last Year", client_data["CR Count"])

    with col2:
        st.metric("Solutions Used", len(client_data["Solutions"]))
        st.metric("Renewal Likelihood", client_data["Renewal Likelihood"])
        contract_end_date = datetime.datetime.strptime(client_data["Contract End"], "%Y-%m-%d")
        status = "Active" if contract_end_date > datetime.datetime.now() else "Expired"
        st.metric("Current Status", status)

    with col3:
        engagement_score = random.randint(70, 100)
        st.metric("Client Engagement Score", f"{engagement_score}%")
        renewal_date = contract_end_date - datetime.timedelta(days=90)
        st.metric("Suggested Renewal Date", renewal_date.strftime("%Y-%m-%d"))
        st.metric("Data Retention Plan", "5 Years")

    # Descriptive Textual Insights
    st.subheader("Client Insights")
    st.write(
        f"""
        **{client_name}** is currently utilizing the following solutions: {', '.join(client_data['Solutions'])}.
        Based on recent engagements, the client's renewal likelihood is marked as **{client_data['Renewal Likelihood']}**.
        """
    )
    st.info("AI-driven insights suggest focusing on customization to increase engagement.")

    # Graph Data
    months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq='M').strftime('%b %Y')
    cr_counts = [random.randint(0, 3) for _ in months]
    solutions = client_data["Solutions"]
    usage = [random.randint(1, 10) for _ in solutions]
    renewal_likelihood = [random.randint(60, 100) for _ in months]
    engagement_scores = [random.randint(60, 100) for _ in months]

    # Graphs
    st.subheader("Client Engagement Over Time")
    tab1, tab2, tab3, tab4 = st.tabs([
        "CR Requests",
        "Solution Usage",
        "Renewal Likelihood",
        "Engagement Score",
    ])

    with tab1:
        fig1 = px.line(
            x=months,
            y=cr_counts,
            markers=True,
            title="Monthly CR Requests",
            color_discrete_sequence=[jll_colors["red"]],
        )
        fig1.update_layout(
            xaxis_title="Month",
            yaxis_title="CR Count",
            title_x=0.5,
            template="simple_white",
            font=dict(size=12),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.bar(
            x=solutions,
            y=usage,
            title="Solution Usage",
            color=usage,
            color_continuous_scale=[[0, jll_colors["grey"]], [1, jll_colors["red"]]],
        )
        fig2.update_layout(
            xaxis_title="Solutions",
            yaxis_title="Usage Count",
            title_x=0.5,
            template="simple_white",
            font=dict(size=12),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        fig3 = px.area(
            x=months,
            y=renewal_likelihood,
            title="Renewal Likelihood Trend",
            color_discrete_sequence=[jll_colors["red"]],
        )
        fig3.update_layout(
            xaxis_title="Month",
            yaxis_title="Likelihood (%)",
            title_x=0.5,
            template="simple_white",
            font=dict(size=12),
        )
        st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        fig4 = px.bar(
            x=months,
            y=engagement_scores,
            title="Engagement Score Trend",
            color=engagement_scores,
            color_continuous_scale=[[0, jll_colors["grey"]], [1, jll_colors["red"]]],
        )
        fig4.update_layout(
            xaxis_title="Month",
            yaxis_title="Engagement Score (%)",
            title_x=0.5,
            template="simple_white",
            font=dict(size=12),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig4, use_container_width=True)

# ------------------- Cost Estimator Tab -------------------
elif selected == "Cost Estimator":
    st.title("Project Cost Estimator")

    # Define sections and organize parameters
    section_header("Source Data Requirements")
    project_params = {
        "data_sources": st.multiselect("Select Data Sources:", ["Corrigo", "Property Hub", "Custom Source", "API Integration", "File Upload"]),
        "etl_type": st.selectbox("Select Load Type:", ["Batch", "Streaming", "Batch + Streaming"]),
        "refresh_frequency": st.selectbox("Select Refresh Frequency:", ["Daily", "Weekly", "Monthly"]),
        "data_warehouse": st.selectbox("Select Data Warehouse:", ["Snowflake", "Databricks"]),
    }

    section_header("Solution Requirements")
    project_params.update({
        "solution_type": st.selectbox("Select Solution Type:", ["Analytical / Operational Reporting", "IoT", "Advanced Analytics"]),
        "dashboard_required": st.selectbox("BI Dashboard Required:", ["PowerBI", "Tableau", "None"])
    })

    section_header("Additional Requirements")
    project_params.update({
        "transformation_complexity": st.selectbox("Data Transformation Complexity:", ["Simple", "Moderate", "Complex"]),
        "compute_hours": st.number_input("Compute Hours per Month:", 0, 500, 50),
        "storage_needs": st.selectbox("Storage Requirements:", ["10 GB", "100 GB", "1 TB", "10 TB"]),
        "data_retention": st.selectbox("Data Retention Policy:", ["3 Months", "1 Year", "5 Years"]),
        "users": st.slider("Number of Users:", 1, 1000, 50),
        "support": st.selectbox("Support Level:", ["Basic", "Premium", "Enterprise"]),
        "security_level": st.selectbox("Security Level:", ["Standard", "Enhanced", "Enterprise"]),
        "data_compliance": st.selectbox("Data Compliance:", ["GDPR", "HIPAA", "None"]),
        "monitoring": st.selectbox("Monitoring Level:", ["Basic", "Advanced"]),
        "training_sessions": st.selectbox("Training Sessions:", ["None", "One-Time", "Ongoing"]),
        "data_encryption": st.checkbox("Enable Data Encryption"),
        "ai_integration": st.checkbox("Include AI/ML Integration"),
        "api_access": st.checkbox("API Access Required"),
    })
    st.markdown("---")

    # Conditional fields based on IoT solution type
    if project_params["solution_type"] == "IoT":
        st.subheader("IoT Specific Requirements")
        iot_params = {
            "iot_solution": st.selectbox("Select IoT Solution:", ["VergeSense", "Digital Twins", "Other"]),
            "number_of_devices": st.selectbox("Number of Devices:", ["10-100", "100-1000", "1000-5000"]),
        }
        project_params.update(iot_params)

    # Estimated Costs Calculation
    st.subheader("Estimated Costs")
    total_cost = 5000  # Base cost
    total_cost += 500 * len(project_params.get("data_sources", []))
    total_cost += 1000 * (["Simple", "Moderate", "Complex"].index(project_params["transformation_complexity"]) + 1)
    total_cost += 100 * project_params.get("compute_hours", 0)
    total_cost += [10, 100, 1000, 10000][["10 GB", "100 GB", "1 TB", "10 TB"].index(project_params["storage_needs"])]
    total_cost *= [1, 1.5, 2][["3 Months", "1 Year", "5 Years"].index(project_params["data_retention"])]
    total_cost += 10 * project_params.get("users", 1)

    # Additional Costs
    if project_params["security_level"] == "Enhanced":
        total_cost += 2000
    elif project_params["security_level"] == "Enterprise":
        total_cost += 5000

    if project_params["data_compliance"] != "None":
        total_cost += 1500

    if project_params.get("data_encryption", False):
        total_cost += 1000

    if project_params.get("ai_integration", False):
        total_cost += 3000

    if project_params.get("api_access", False):
        total_cost += 1000

    if project_params["monitoring"] == "Advanced":
        total_cost += 2000

    if project_params["support"] == "Premium":
        total_cost += 5000
    elif project_params["support"] == "Enterprise":
        total_cost += 10000

    if project_params["training_sessions"] != "None":
        total_cost += 1000

    # Calculate Monthly and Yearly OPEX
    compute_cost_per_month = 500
    storage_cost_per_month = 200
    monthly_opex = (
        (compute_cost_per_month * project_params.get("compute_hours", 0) / 100) +
        (storage_cost_per_month * (["10 GB", "100 GB", "1 TB", "10 TB"].index(project_params["storage_needs"]) + 1))
    )
    yearly_opex = monthly_opex * 12

    # Display Cost Summary
    cost_summary_data = {
        "Total Implementation Cost": f"${total_cost:,.2f}",
        "Estimated Monthly OpEx": f"${monthly_opex:,.2f}",
        "Estimated Yearly OpEx": f"${yearly_opex:,.2f}",
    }
    st.table(pd.DataFrame.from_dict(cost_summary_data, orient='index', columns=['Cost']))

    # Display Recommended Project Team
    st.subheader("Recommended Project Team")
    team = ["1 Project Manager", "1 Business Analyst"]
    if project_params.get("ai_integration", False):
        team.append("1 AI/ML Specialist")
    if project_params.get("dashboard_required") != "None":
        team.append("1 Front-end Developer")
    if project_params.get("etl_type") == "Batch":
        team.append("1 Backend Developer (Batch Processing)")
    else:
        team.append("1 Backend Developer (Streaming Processing)")

    for member in team:
        st.write(f"- {member}")

    # Display Similar Projects
    st.subheader("Similar Projects for Reference")
    similar_projects = fetch_similar_projects(project_params.get("solution_type", "N/A"))
    if similar_projects:
        for project in similar_projects:
            st.write(f"**{project['name']}**: [View Details]({project['link']})")

    # Generate Solution Description
    if st.button("Generate Solution Description"):
        with st.spinner("Generating description..."):
            description = generate_description(project_params)
        if description:
            st.subheader("High-Level Solution Description")
            st.write(description)

# ------------------- Sales Pipeline Tab -------------------
# ------------------- Sales Pipeline Tab -------------------
elif selected == "Sales Pipeline":
    st.title("Sales Pipeline Overview")

    # Sample data for sales pipeline
    pipeline_data = {
        "Client Name": [
            "ACME Corp", "Globex Inc", "Initech", "Umbrella Corp", "Hooli",
            "Stark Industries", "Wayne Enterprises", "Soylent Corp", "Massive Dynamic", "Vandelay Industries"
        ],
        "Stage": [
            "Proposal", "Negotiation", "Prospecting", "Closed Won", "Proposal",
            "Negotiation", "Prospecting", "Closed Lost", "Proposal", "Negotiation"
        ],
        "Estimated Value": [
            100000, 150000, 80000, 200000, 120000,
            160000, 90000, 75000, 110000, 130000
        ],
        "Probability (%)": [
            60, 70, 30, 100, 60,
            70, 30, 0, 60, 70
        ],
        "Expected Close Date": [
            "2023-12-15", "2023-11-30", "2024-01-20", "2023-10-01", "2023-12-31",
            "2023-11-25", "2024-02-10", "2023-09-15", "2023-12-20", "2023-11-10"
        ]
    }
    pipeline_df = pd.DataFrame(pipeline_data)

    # **Convert Expected Close Date to datetime**
    pipeline_df["Expected Close Date"] = pd.to_datetime(pipeline_df["Expected Close Date"])

    # Display Pipeline Overview
    st.subheader("Pipeline Summary")

    # Calculate total estimated value and weighted value
    pipeline_df["Weighted Value"] = pipeline_df["Estimated Value"] * pipeline_df["Probability (%)"] / 100
    total_estimated_value = pipeline_df["Estimated Value"].sum()
    total_weighted_value = pipeline_df["Weighted Value"].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Estimated Value", f"${total_estimated_value:,.2f}")
    with col2:
        st.metric("Total Weighted Value", f"${total_weighted_value:,.2f}")

    # Display Pipeline Table
    st.subheader("Detailed Pipeline")
    st.dataframe(pipeline_df.style.format({
        "Estimated Value": "${:,.2f}",
        "Weighted Value": "${:,.2f}",
        "Probability (%)": "{:.0f}%",
        "Expected Close Date": "{:%Y-%m-%d}"  # This works now because the column is datetime
    }))


    # Visualize Pipeline Stages
    st.subheader("Pipeline by Stage")
    stage_summary = pipeline_df.groupby("Stage").agg({
        "Estimated Value": "sum"
    }).reset_index()

    # Define color mapping for stages using JLL colors
    stage_colors = {
        "Prospecting": jll_colors["grey"],
        "Proposal": jll_colors["black"],
        "Negotiation": jll_colors["grey"],
        "Closed Won": jll_colors["red"],
        "Closed Lost": jll_colors["black"]
    }

    fig_stage = px.bar(
        stage_summary,
        x="Stage",
        y="Estimated Value",
        color="Stage",
        title="Estimated Value by Stage",
        color_discrete_map=stage_colors
    )
    fig_stage.update_layout(
        xaxis_title="Stage",
        yaxis_title="Estimated Value ($)",
        title_x=0.5,
        template="simple_white",
        font=dict(size=12),
        showlegend=False
    )
    st.plotly_chart(fig_stage, use_container_width=True)

    # Forecasted Revenue Over Time
    st.subheader("Forecasted Revenue Over Time")
    pipeline_df["Expected Close Date"] = pd.to_datetime(pipeline_df["Expected Close Date"])
    pipeline_df["Month"] = pipeline_df["Expected Close Date"].dt.to_period("M").dt.to_timestamp()
    monthly_forecast = pipeline_df.groupby("Month").agg({
        "Weighted Value": "sum"
    }).reset_index()

    fig_forecast = px.bar(
        monthly_forecast,
        x="Month",
        y="Weighted Value",
        title="Monthly Forecasted Revenue",
        color_discrete_sequence=[jll_colors["red"]],
    )
    fig_forecast.update_layout(
        xaxis_title="Month",
        yaxis_title="Weighted Value ($)",
        title_x=0.5,
        template="simple_white",
        font=dict(size=12),
        xaxis_tickformat="%b %Y"
    )
    st.plotly_chart(fig_forecast, use_container_width=True)

    # Top Opportunities
    st.subheader("Top Opportunities")
    top_opportunities = pipeline_df.sort_values(by="Weighted Value", ascending=False).head(5)
    st.table(top_opportunities[[
        "Client Name", "Stage", "Estimated Value", "Probability (%)", "Expected Close Date"
    ]].style.format({
        "Estimated Value": "${:,.2f}",
        "Probability (%)": "{:.0f}%",
        "Expected Close Date": "{:%Y-%m-%d}"
    }))

# ------------------- End of Application -------------------
