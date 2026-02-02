import streamlit as st
import pandas as pd
import time  # <--- Make sure this line is here!

# 1. Page Setup
st.set_page_config(page_title="Workout Generator", page_icon="💪")

# Title and Subtitle
st.title("🏋️ Daily Workout Generator")
st.markdown("### *Dumbbells, Resistance Bands, and Bodyweight workouts. Three sets for each block*") # This adds the instruction right under the title

# 2. Data Connection (Replace with your link)
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSaHE0jUfiF6TrlsS2Trkhw1IRLu6vMQHdVOGHtvANQm5TUPQUHJf7XBYaLOwvRKjTox5P1xmfLa7ME/pub?output=csv'

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except:
        return pd.DataFrame()

data = load_data()

# 3. Sidebar Features (Timer & Filters)
st.sidebar.header("🛠️ Training Tools")

# --- Feature: Equipment Filter ---
if not data.empty:
    equipment_list = data['Equipment'].unique().tolist()
    selected_equip = st.sidebar.multiselect("Filter by Equipment", options=equipment_list, default=equipment_list)
else:
    selected_equip = []

# --- Feature: Rest Timer ---
st.sidebar.divider()
st.sidebar.subheader("⏲️ Rest Timer")
rest_time = st.sidebar.number_input("Seconds", min_value=5, max_value=300, value=60, step=5)
if st.sidebar.button("⏱️ Start Timer"):
    t_holder = st.sidebar.empty()
    for t in range(rest_time, -1, -1):
        t_holder.metric("Rest Remaining", f"{t}s")
        time.sleep(1)
    st.sidebar.success("Go! 🔥")
    st.balloons()

# 4. Workout Generation Logic
if 'workout_seed' not in st.session_state or st.sidebar.button('🎲 Shuffle New Workout'):
    st.session_state.workout_seed = time.time() # This ensures random selection on shuffle
    st.session_state.completed_tasks = {} # Reset progress on new workout

# Filter data based on equipment
filtered_data = data[data['Equipment'].isin(selected_equip)]

# 5. The Progress Bar
st.divider()
cols = st.columns([1, 4])
with cols[0]:
    st.write("### Progress")
progress_bar = st.progress(0)

# 6. Generate Blocks
block_emojis = {"Lower Body": "🦵", "Upper Body": "💪", "Core": "🧘"}
total_exercises = 9 # 3 per block
completed_count = 0

for block, emoji in block_emojis.items():
    st.header(f"{emoji} {block}")
    
    # Logic to pick 3 random exercises based on our 'seed'
    block_df = filtered_data[filtered_data['Block'] == block]
    if not block_df.empty:
        # Use a consistent sample based on seed so checkboxes don't vanish
        sample = block_df.sample(n=min(3, len(block_df)), random_state=int(st.session_state.workout_seed % 1000))
        
        for _, row in sample.iterrows():
            # Create unique key for the checkbox
            task_key = f"{block}_{row['Exercise']}"
            
            # Checkbox logic
            is_done = st.checkbox(f"**{row['Exercise']}**", key=task_key)
            if is_done:
                completed_count += 1
            
            st.write(f"🔢 **Reps:** {row['Reps']} | 🛠️ **Equip:** {row['Equipment']}")
            st.caption(f"🎯 Targets: {row['Primary Muscle Focus']}")
            st.write("---")

# Update Progress Bar
if total_exercises > 0:
    progress_percent = completed_count / total_exercises
    progress_bar.progress(progress_percent)
    if completed_count == total_exercises:
        st.success("Workout Complete! 🎉")