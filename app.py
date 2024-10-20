import streamlit as st
import pandas as pd
import datetime
import random
import openai
import time
import matplotlib.pyplot as plt

# openAI key
openai.api_key = st.secrets["openai"]  # Assuming you've saved the API key in Streamlit secrets

# Set corporate colors for Jones Lang LaSalle
jll_colors = {
    "primary": "#0072CE",   # Blue
    "secondary": "#6A737B", # Gray
    "accent": "#FFD100"     # Yellow
}

# Function to display section headers with styled background
def section_header(title):
    st.subheader(title)
    # st.markdown("---")

# Function to simulate fetching similar projects from database
def fetch_similar_projects(project_type):
    # Replace with actual logic to fetch projects from database
    return [
        {"name": "Project A", "link": "https://example.com/project_a"},
        {"name": "Project B", "link": "https://example.com/project_b"},
        {"name": "Project C", "link": "https://example.com/project_c"}
    ]

# Sidebar Menu for Tab Selection
with st.sidebar:
    st.image("jll_logo.png", use_column_width=True)
    selected = st.radio("Navigation", ["Home", "Client Relationship Overview", "Project Cost Estimator"], index=0)

# ------------------- Client Relationship Overview Tab -------------------
if selected == "Home":
    st.title("Welcome to BI Solution Management App")
    st.write("This tool is designed to assist sales managers in managing client relationships and estimating project costs for BI solutions with AI-powered insights.")
    st.write("Navigate through the tabs above to get started.")

elif selected == "Client Relationship Overview":
    st.title("Client Relationship Overview")
    
    # Sample data for 10 clients
    clients_data = {
        "Client Name": ["ACME Corp", "Globex Inc", "Initech", "Umbrella Corp", "Hooli", "Stark Industries", "Wayne Enterprises", "Soylent Corp", "Massive Dynamic", "Vandelay Industries"],
        "Contract Start": ["2022-01-01", "2021-06-15", "2023-03-01", "2020-11-11", "2022-05-20", "2021-09-30", "2022-01-15", "2023-02-01", "2020-07-01", "2021-12-01"],
        "Contract End": ["2024-12-31", "2023-06-14", "2025-03-01", "2023-11-10", "2024-05-19", "2024-09-29", "2025-01-14", "2024-02-01", "2023-07-01", "2023-12-01"],
        "Solutions": [["Data Warehouse", "Tableau Dashboards"], ["ETL Pipeline", "Real-time Data Sync"], ["Operational Reporting", "Machine Learning"], ["IoT Integration", "Data Lake"], ["Data Pipeline", "Custom Visualizations"], ["AI/ML Integration", "Data Warehouse"], ["Real-time Data Sync", "IoT Integration"], ["Data Lake", "ETL Pipeline"], ["Machine Learning", "Custom Visualizations"], ["Operational Reporting", "Data Lake"]],
        "CR Count": [5, 3, 7, 4, 6, 8, 2, 3, 5, 4],
        "Renewal Likelihood": ["High", "Medium", "High", "Low", "Medium", "High", "Medium", "Low", "Medium", "Low"]
    }
    clients_df = pd.DataFrame(clients_data)
    
    # Client Filter Dropdown
    client_name = st.selectbox("Select Client", clients_df["Client Name"])
    
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
        st.metric("Current Status", "Active" if datetime.datetime.strptime(client_data["Contract End"], "%Y-%m-%d") > datetime.datetime.now() else "Expired")
        
    with col3:
        st.metric("Client Engagement Score", f"{random.randint(70, 100)}%")
        st.metric("AI Suggested Renewal Date", (datetime.datetime.strptime(client_data["Contract End"], "%Y-%m-%d") - datetime.timedelta(days=90)).strftime("%Y-%m-%d"))
        st.metric("Data Retention Plan", "5 Years")

    # Descriptive Textual Insights
    st.subheader("Client Insights")
    st.write(f"**{client_name}** is currently using solutions like {', '.join(client_data['Solutions'])}.")
    st.write(f"Based on recent engagements, the client’s renewal likelihood is marked as **{client_data['Renewal Likelihood']}**.")
    st.write("AI-driven insights suggest focusing on customization to increase engagement.")

    # Graphs
    st.subheader("Client Engagement Over Time")
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))
    
    # Graph 1: CR Count Trend
    months = list(range(12))
    cr_counts = [random.randint(0, 3) for _ in months]
    ax[0, 0].plot(months, cr_counts, marker="o")
    ax[0, 0].set_title("Monthly CR Requests")
    ax[0, 0].set_xlabel("Months")
    ax[0, 0].set_ylabel("CR Count")
    
    # Graph 2: Solution Usage Distribution
    solutions = client_data["Solutions"]
    usage = [random.randint(1, 10) for _ in solutions]
    ax[0, 1].bar(solutions, usage, color="skyblue")
    ax[0, 1].set_title("Solution Usage")
    
    # Graph 3: Renewal Likelihood Over Time
    ax[1, 0].plot(months, [random.randint(60, 100) for _ in months], color="green", marker="o")
    ax[1, 0].set_title("Renewal Likelihood Trend")
    
    # Graph 4: Engagement Score
    ax[1, 1].plot(months, [random.randint(60, 100) for _ in months], color="orange", marker="o")
    ax[1, 1].set_title("Engagement Score Trend")
    
    # Display graphs in Streamlit
    st.pyplot(fig)

# ------------------- Project Cost Estimator Tab -------------------
if selected == "Project Cost Estimator":
    st.title("Project Cost Estimator")

    # Define sections and organize parameters
    section_header("Source Data Requirements")
    project_params = {
        "data_sources": st.multiselect("Data Sources", ["Corrigo", "Property Hub", "Custom Source", "API Integration", "File Upload"]),
        "etl_type": st.selectbox("Load Type", ["Batch", "Streaming", "Batch + Streaming"]),
        "refresh_frequency": st.selectbox("Refresh Frequency", ["Daily", "Weekly", "Monthly"]),
        "data_warehouse": st.selectbox("Data Warehouse", ["Snowflake", "Databricks"]),
    }

    section_header("Solution Requirements")
    project_params.update({
        "solution_type": st.radio("Solution Type", ["Analytical / Operational Reporting", "IoT", "Advanced Analytics"]),
        "dashboard_required": st.selectbox("BI Dashboard", ["PowerBI", "Tableau", "None"])
    })

    section_header("Extra Requirements")
    project_params.update({
        "transformation_complexity": st.selectbox("Data Transformation Complexity", ["Simple", "Moderate", "Complex"]),
        "compute_hours": st.number_input("Compute Hours per Month", 0, 500, 50),
        "storage_needs": st.selectbox("Storage Requirements", ["10 GB", "100 GB", "1 TB", "10 TB"]),
        "data_retention": st.selectbox("Data Retention Policy", ["3 Months", "1 Year", "5 Years"]),
        "users": st.slider("Number of Users", 1, 1000, 50),
        "security_level": st.selectbox("Security Level", ["Standard", "Enhanced", "Enterprise"]),
        "data_compliance": st.selectbox("Data Compliance", ["GDPR", "HIPAA", "None"]),
        "data_encryption": st.checkbox("Enable Data Encryption"),
        "ai_integration": st.checkbox("AI/ML Integration"),
        "api_access": st.checkbox("API Access Required"),
        "monitoring": st.selectbox("Monitoring Level", ["Basic", "Advanced"]),
        "support": st.selectbox("Support Level", ["Basic", "Premium", "Enterprise"]),
        "consultant_hours": st.number_input("Consultant Hours Needed", 0, 500, 20),
        "training_sessions": st.selectbox("Training Sessions", ["None", "One-Time", "Ongoing"]),
        # "client_type": st.radio("Client Type", ["External", "Internal"]),
    })

        # Conditional fields based on IoT solution type
    if project_params["solution_type"] == "IoT":
        st.subheader("IoT Specific Requirements")
        iot_params = {
            "iot_solution": st.selectbox("IoT Solution", ["VergeSense", "DT", "Other"]),
            "number_of_devices": st.selectbox("Number of Devices", ["10-100", "100-1000", "1000-5000"]),
        }
        project_params.update(iot_params)

    # Handle default values and AI recommendation
    solution_complexity = "Complex" if project_params["transformation_complexity"] == "Complex" or project_params["compute_hours"] > 100 else "Moderate"

    # Estimated Costs Calculation
    total_cost = 0
    
    # Base cost estimation based on project parameters
    if "project_duration" in project_params:
        if project_params["etl_type"] == "Batch":
            total_cost += 1000 * project_params["project_duration"] # Base cost for batch processing
        else:
            total_cost += 1500 * project_params["project_duration"] # Base cost for streaming processing

    total_cost += 500 * len(project_params.get("data_sources", [])) # Additional cost per data source

    if project_params.get("dashboard_required", False):
        total_cost += 2000 # Additional cost for dashboard creation

    total_cost += 1000 * (["Simple", "Moderate", "Complex"].index(project_params["transformation_complexity"]) + 1) # Transformation cost
    total_cost += 100 * project_params.get("compute_hours", 0) # Compute cost

    total_cost += [10, 100, 1000, 10000][["10 GB", "100 GB", "1 TB", "10 TB"].index(project_params["storage_needs"])] # Storage cost

    total_cost *= [1, 1.5, 2][["3 Months", "1 Year", "5 Years"].index(project_params["data_retention"])] # Data retention cost

    total_cost += 10 * project_params.get("users", 1) # User license cost

    if project_params["security_level"] == "Enhanced":
        total_cost += 2000
    elif project_params["security_level"] == "Enterprise":
        total_cost += 5000

    if project_params["data_compliance"] != "None":
        total_cost += 1500 # Additional cost for compliance

    if project_params.get("data_encryption", False):
        total_cost += 1000 # Additional cost for encryption

    if project_params.get("ai_integration", False):
        total_cost += 3000 # Additional cost for AI/ML integration

    if project_params.get("api_access", False):
        total_cost += 1000 # Additional cost for API access

    if project_params["monitoring"] == "Advanced":
        total_cost += 2000 # Additional cost for advanced monitoring

    if project_params["support"] == "Premium":
        total_cost += 5000
    elif project_params["support"] == "Enterprise":
        total_cost += 10000

    total_cost += 50 * project_params.get("consultant_hours", 0) # Consultant cost

    if project_params["training_sessions"] != "None":
        total_cost += 1000 # Additional cost for training

    # Display AI Recommendations
    st.subheader("Recommendations")
    st.write(f"Based on the project parameters, AI suggests the solution complexity should be **{solution_complexity}**.")
    st.write("AI recommends additional attention to data transformation and compute hours.")

    # Display Estimated Project Cost
    st.subheader("Estimated Project Cost")
    st.write(f"The estimated cost for the project is **${total_cost:,.2f}**.")

    # Display Recommended Project Setup
    st.subheader("Recommended Project Setup")
    st.write("Based on the requirements provided, the project setup could include:")

    if project_params.get("ai_integration", False):
        st.write("- 1 AI/ML Specialist")
    if project_params.get("dashboard_required", False):
        st.write("- 1 Front-end Developer")
    if project_params.get("etl_type") == "Batch":
        st.write("- 1 Backend Developer for Batch Processing")
    else:
        st.write("- 1 Backend Developer for Streaming Processing")
    st.write("- 1 Project Manager")
    st.write("- 1 Business Analyst")

    # Display Similar Projects for Reference
    st.subheader("Similar Projects for Reference")
    similar_projects = fetch_similar_projects(project_params["solution_type"])
    
    if similar_projects:
        for project in similar_projects:
            st.write(f"**{project['name']}**: [Project Details]({project['link']})")

    # Calculate and Display Total Implementation Cost
    st.subheader("Total Implementation Cost")
    implementation_cost = total_cost
    st.write(f"The total implementation cost is **${implementation_cost:,.2f}**.")

    # Calculate and Display Monthly OPEX Cost (Compute and Storage)
    st.subheader("Monthly Operational Expenditure (OPEX)")
    monthly_opex = 0

    # Compute and storage costs (hypothetical placeholders, adjust as per actual costs)
    compute_cost_per_month = 500  # Example compute cost per month
    storage_cost_per_month = 200  # Example storage cost per month

    # Calculate monthly OPEX based on compute hours and storage needs
    monthly_opex += compute_cost_per_month * project_params.get("compute_hours", 0) / 100  # Adjust as per actual compute cost logic
    monthly_opex += storage_cost_per_month * (["10 GB", "100 GB", "1 TB", "10 TB"].index(project_params["storage_needs"]) + 1)  # Adjust as per actual storage cost logic

    st.write(f"The estimated monthly OPEX cost is **${monthly_opex:,.2f}** (Compute + Storage).")

    # Calculate and Display Yearly OPEX Cost (assuming 12 months)
    yearly_opex = monthly_opex * 12
    st.write(f"The estimated yearly OPEX cost is **${yearly_opex:,.2f}** (Compute + Storage).")

    # Display Total Cost and OPEX in a Table
    st.subheader("Summary: Total Cost and OPEX")
    cost_summary_data = {
        "Total Implementation Cost": f"${implementation_cost:,.2f}",
        "Estimated Monthly OPEX": f"${monthly_opex:,.2f}",
        "Estimated Yearly OPEX": f"${yearly_opex:,.2f}",
    }

    st.table(pd.DataFrame.from_dict(cost_summary_data, orient='index', columns=['Cost']))

    # Function to generate a diagram description using the updated API
    # Function to generate a diagram description using the updated API
    def generate_diagram_description(project_params):
        # Define the conversation as messages for the chat model
        messages = [
            {"role": "system", "content": "You are an expert in creating architecture diagrams based on project specifications."},
            {"role": "user", "content": f"""
            Create a solution architecture diagram description based on the following project parameters:
            - Data Sources: {', '.join(project_params.get('data_sources', []))}
            - ETL Type: {project_params['etl_type']}
            - Data Warehouse: {project_params['data_warehouse']}
            - Solution Type: {project_params['solution_type']}
            - BI Dashboard: {project_params['dashboard_required']}
            - Storage Requirements: {project_params['storage_needs']}
            - Compute Hours: {project_params['compute_hours']}
            - Security Level: {project_params['security_level']}
            - AI Integration: {'Yes' if project_params['ai_integration'] else 'No'}
            - API Access Required: {'Yes' if project_params['api_access'] else 'No'}
            - Monitoring: {project_params['monitoring']}
            - Support: {project_params['support']}
            """}
        ]
        
        try:
            # API call to OpenAI Chat API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,  # Use messages instead of prompt
                max_tokens=300,
                temperature=0.5,
            )
            return response['choices'][0]['message']['content'].strip()

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    # Streamlit UI for generating the diagram
    if st.button("Generate Solution Diagram"):
        # Generate diagram when the button is clicked
        diagram_description = generate_diagram_description(project_params)
        st.subheader("Generated Solution Diagram")
        st.write(diagram_description)
# ------------------- End of Tabs -------------------
