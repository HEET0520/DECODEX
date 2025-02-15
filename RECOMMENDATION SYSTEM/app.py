# Import necessary libraries
import streamlit as st
import pandas as pd

# Load the dataset (Ensure the file is in the same directory as the script)
df = pd.read_csv('surveyor_data.csv')

# Function to recommend parts based on a list of selected parts
def hybrid_recommendation(selected_parts):
    # Historical Data Recommendation: Most frequent parts from claims mentioning the selected parts
    relevant_claims = df[df['TXT_PARTS_NAME'].isin(selected_parts)]
    
    # Get claim IDs for the relevant claims
    claim_ids = relevant_claims['CLAIMNO']
    
    # Find the most frequent parts mentioned in these claims
    historical_recommendations = df[df['CLAIMNO'].isin(claim_ids)]['TXT_PARTS_NAME'].value_counts()
    
    # Exclude all selected parts from the recommendations
    historical_recommendations = historical_recommendations[~historical_recommendations.index.isin(selected_parts)]
    
    # Get the top 5 historical recom4mended parts
    top_5_historical = historical_recommendations.head(5)

    # Recent Input Recommendation: Parts mentioned in the most recent claims
    recent_claims = df.sort_values(by='CLAIMNO', ascending=False).head(10)
    
    # Get the top 5 most mentioned parts in recent claims
    recent_recommendations = recent_claims['TXT_PARTS_NAME'].value_counts().head(5)
    
    # Combine historical and recent recommendations, giving priority to recent ones
    hybrid_recommendations = pd.concat([recent_recommendations, top_5_historical])
    
    # Combine the results and return the top 5 unique recommendations
    hybrid_recommendations = hybrid_recommendations.groupby(hybrid_recommendations.index).sum().sort_values(ascending=False)
    
    # Exclude all selected parts and return the top 5
    return hybrid_recommendations[~hybrid_recommendations.index.isin(selected_parts)].head(5)

# Streamlit App Layout
st.title("Hybrid Parts Recommendation System")
st.markdown("Enter a damaged part to get the top 5 recommended parts. Continue entering parts for updated recommendations.")

# Initialize session state to store selected parts and recommendations
if 'selected_parts' not in st.session_state:
    st.session_state.selected_parts = []

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

# Display the selected parts so far
st.subheader("Selected Parts:")
st.write(st.session_state.selected_parts)

# Display the top 5 hybrid recommended parts
st.subheader("Top 5 Hybrid Recommended Parts (Historical + Recent):")
st.write(st.session_state.recommendations)

# Function to handle new input and update recommendations
def get_new_recommendations():
    # Text Input for entering one part at a time
    input_part = st.text_input("Enter Damaged Part", value="", key=len(st.session_state.selected_parts) + 1)

    # Update and get recommendations only if a part is entered
    if input_part:
        if input_part not in st.session_state.selected_parts:
            st.session_state.selected_parts.append(input_part)
            
            # Get top 5 recommendations for the current selection
            recommendations = hybrid_recommendation(st.session_state.selected_parts)
            
            # Update recommendations in session state
            st.session_state.recommendations = recommendations
            
            # Trigger a rerun to generate a new input field
            st.experimental_rerun()
        else:
            st.warning("This part is already selected. Please enter a different one.")
    else:
        st.info("Please enter a part name to get recommendations.")

# Continuously ask for new input after each recommendation
get_new_recommendations()




