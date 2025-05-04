# import streamlit as st
# import pandas as pd
# from query_functions import query_handling_using_LLM_updated

# st.set_page_config(page_title="SHL Assessment Recommendation System", layout="centered")

# st.markdown(
#     """
#     <h1 style='text-align: center; color: #4B8BBE;'>🧠 SHL Assessment Recommendation System</h1>
#     <h4 style='text-align: center; color: #ccc;'>Find the best assessments based on your query using AI!</h4>
#     <hr style="border: 1px solid #333;">
#     """,
#     unsafe_allow_html=True
# )

# query = st.text_input("🔍 Enter your search query here:", placeholder="e.g. Python SQL coding test")

# # On search
# if st.button("Search"):
#     if query.strip() == "":
#         st.warning("Please enter a valid query.")
#     else:
#         with st.spinner("🤖 Thinking... Fetching the best matches for you!"):
#             try:
#                 # Get results
#                 df = query_handling_using_LLM_updated(query)

#                 if isinstance(df, pd.DataFrame) and not df.empty:
#                     if 'Score' in df.columns:
#                         df = df.drop(columns=['Score'])

#                     if "Duration" in df.columns:
#                         df = df.rename(columns={"Duration": "Duration in mins"})

#                     display_cols = ["Assessment Name", "Skills", "Test Type", "Description", "Remote Testing Support", "Adaptive/IRT", "Duration in mins", "URL"]
#                     df = df[[col for col in display_cols if col in df.columns]]

#                     # Make URLs clickable
#                     df['URL'] = df['URL'].apply(lambda x: f"<a href='{x}' target='_blank'>🔗 View</a>" if pd.notna(x) else "")

#                     st.success("✅ Here are your top assessment recommendations:")

#                     # Build styled HTML table
#                     table_html = """
#                     <style>
#                         table.custom-table {
#                             width: 100%;
#                             border-collapse: collapse;
#                             font-family: Arial, sans-serif;
#                         }
#                         table.custom-table thead {
#                             background-color: #2e2e2e;
#                             color: white;
#                         }
#                         table.custom-table th, table.custom-table td {
#                             border: 1px solid #444;
#                             padding: 10px;
#                             text-align: left;
#                             vertical-align: top;
#                             color: #eee;
#                         }
#                         table.custom-table tr:nth-child(even) {
#                             background-color: #1e1e1e;
#                         }
#                         table.custom-table tr:nth-child(odd) {
#                             background-color: #2a2a2a;
#                         }
#                         a {
#                             color: #1a73e8;
#                             text-decoration: none;
#                         }
#                     </style>
#                     <table class="custom-table">
#                         <thead>
#                             <tr>
#                     """

#                     for col in df.columns:
#                         table_html += f"<th>{col}</th>"
#                     table_html += "</tr></thead><tbody>"

#                     for _, row in df.iterrows():
#                         table_html += "<tr>"
#                         for cell in row:
#                             table_html += f"<td>{cell}</td>"
#                         table_html += "</tr>"

#                     table_html += "</tbody></table>"

#                     st.markdown(table_html, unsafe_allow_html=True)

#                 else:
#                     st.warning("😕 No assessments matched your query. Try rephrasing it!")

#             except Exception as e:
#                 st.error(f"🚨 Something went wrong: {e}")

import streamlit as st
import pandas as pd
from query_functions import query_handling_using_LLM_updated

# Set page configuration
st.set_page_config(page_title="SHL Assessment Finder", layout="centered")

# Inject custom CSS for background image
st.markdown(
    """
    <style>
    body {
        background-image: url("https://unsplash.com/photos/a-man-driving-a-car-while-holding-a-cell-phone-k_pYLZE2eIo");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .css-18e3th9 {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 1rem;
    }
    .stApp, .block-container {
    background-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header section
st.markdown(
    """
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #2c3e50;'>🧠 SHL Assessment Finder</h1>
        <p style='color: #555; font-size: 18px;'>Instantly get the best assessments based on your role or skill requirement.</p>
        <hr style="border: 1px solid #ccc;">
    </div>
    """, unsafe_allow_html=True
)

# Input
query = st.text_input("Enter job title or skills to find matching assessments:", placeholder="e.g. Data Analyst, Java, Leadership...")

# On button click
if st.button("🔍 Find Assessments"):
    if not query.strip():
        st.warning("Please enter a valid search query.")
    else:
        with st.spinner("Searching our intelligence library..."):
            try:
                df = query_handling_using_LLM_updated(query)

                if isinstance(df, pd.DataFrame) and not df.empty:
                    if 'Score' in df.columns:
                        df = df.drop(columns=['Score'])

                    if "Duration" in df.columns:
                        df = df.rename(columns={"Duration": "Duration (mins)"})

                    df = df[[
                        "Assessment Name", "Skills", "Test Type", "Description",
                        "Remote Testing Support", "Adaptive/IRT", "Duration (mins)", "URL"
                    ]]

                    st.success("🎯 Found the following recommended assessments:\n")

                    for _, row in df.iterrows():
                        st.markdown(f"""
                        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 20px; background-color: #ffffffcc;">
                            <h4 style="color: #0077b6;">{row['Assessment Name']}</h4>
                            <p><strong>Type:</strong> {row['Test Type']} | <strong>Duration:</strong> {row['Duration (mins)']} mins</p>
                            <p><strong>Skills:</strong> {row['Skills']}</p>
                            <p style="color: #333;">{row['Description']}</p>
                            <p><strong>Adaptive:</strong> {row['Adaptive/IRT']} | <strong>Remote:</strong> {row['Remote Testing Support']}</p>
                            <a href="{row['URL']}" target="_blank" style="text-decoration: none; color: #1a73e8;">🔗 View Assessment</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("🔎 No assessments found for your input. Try refining your search.")

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
