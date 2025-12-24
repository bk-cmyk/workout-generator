import streamlit as st
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="Workout Generator", page_icon="💪")

# Title and Subtitle
st.title("🏋️ Daily Workout Generator")
st.markdown("### *Dumbbells, Resistance Bands, and Bodyweight workouts. Three sets for each block*") # This adds the instruction right under the title

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

# 4. Define Emojis for each block
block_emojis = {
    "Lower Body": "🦵",
    "Upper Body": "💪",
    "Core": "🧘"
}

# 5. Generate the Blocks (3 Exercises Each)
for block, emoji in block_emojis.items():
    st.header(f"{emoji} {block}")
    
    # Filter for the specific block
    filtered_df = data[data['Block'] == block]
    
    if not filtered_df.empty:
        # Randomly pick 3 exercises
        sample = filtered_df.sample(n=min(3, len(filtered_df)))
        
        # Display them
        for index, row in sample.iterrows():
            st.markdown(f"#### {row['Exercise']}")
            st.write(f"🔢 **Reps:** {row['Reps']} | 🛠️ **Equipment:** {row['Equipment']}")
            st.caption(f"🎯 Primary Muscle Focus: {row['Primary Muscle Focus']}")
            st.write("") 
    else:
        st.write("No exercises found for this block.")
    
    st.divider()