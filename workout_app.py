import streamlit as st
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="My Workout Generator", page_icon="💪")
st.title("🏋️ Daily Workout Generator")

# 2. Load Data from your Live CSV link
# Replace 'YOUR_CSV_URL' with the link you copied from Google Sheets
CSV_URL = 'YOUR_CSV_URL'

def load_data():
    df = pd.read_csv(CSV_URL)
    return df

data = load_data()

# 3. Create a Shuffle Button
if st.button('🎲 Shuffle New Workout'):
    # This button triggers a re-run of the script
    st.rerun()

# 4. Generate the Blocks (3 Exercises Each)
blocks = ["Lower Body", "Upper Body", "Core"]

for block in blocks:
    st.subheader(f"🦵 {block}")
    
    # Filter for the specific block
    filtered_df = data[data['Block'] == block]
    
    # Randomly pick 3 exercises
    if not filtered_df.empty:
        # We sample 3 random rows
        sample = filtered_df.sample(n=min(3, len(filtered_df)))
        
        # Display them in a clean table or as individual cards
        for index, row in sample.iterrows():
            st.markdown(f"**{row['Exercise']}**")
            st.caption(f"🎯 Targets: {row['Primary Muscle Focus']} | 🛠️ Equipment: {row['Equipment']}")
    else:
        st.write("No exercises found for this block.")
    
    st.divider()