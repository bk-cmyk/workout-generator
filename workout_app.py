import streamlit as st
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="My Workout Generator", page_icon="💪")

# Title and Subtitle
st.title("🏋️ Daily Workout Generator")
st.markdown("### *Three sets for each block*") # This adds the instruction right under the title

# 2. Load Data from your Live CSV link
# Use your /export?format=csv link here
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSaHE0jUfiF6TrlsS2Trkhw1IRLu6vMQHdVOGHtvANQm5TUPQUHJf7XBYaLOwvRKjTox5P1xmfLa7ME/pub?output=csv'

def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

data = load_data()

# 3. Create a Shuffle Button
if st.button('🎲 Shuffle New Workout'):
    st.rerun()

# 4. Generate the Blocks (3 Exercises Each)
blocks = ["Lower Body", "Upper Body", "Core"]

for block in blocks:
    st.header(f"🔹 {block}") # Changed subheader to header for a cleaner look
    
    # Filter for the specific block
    filtered_df = data[data['Block'] == block]
    
    if not filtered_df.empty:
        # Randomly pick 3 exercises
        sample = filtered_df.sample(n=min(3, len(filtered_df)))
        
        # Display them
        for index, row in sample.iterrows():
            # Bold Exercise Name
            st.markdown(f"#### {row['Exercise']}")
            
            # Display Reps and Equipment clearly
            # Note: Ensure 'Reps' is the exact name of your column in Google Sheets
            st.write(f"🔢 **Reps:** {row['Reps']} | 🛠️ **Equipment:** {row['Equipment']}")
            st.caption(f"🎯 Targets: {row['Primary Muscle Focus']}")
            st.write("") # Adds a tiny bit of spacing
    else:
        st.write("No exercises found for this block.")
    
    st.divider()