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

# --- Feature: Workout Stopwatch ---
st.sidebar.divider()
st.sidebar.subheader("🏃 Total Workout Time")

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

col1, col2 = st.sidebar.columns(2)

if col1.button("▶️ Start"):
    st.session_state.start_time = time.time()

if col2.button("⏹️ Reset"):
    st.session_state.start_time = None
    st.rerun()

# This container will hold the live clock
clock_placeholder = st.sidebar.empty()

if st.session_state.start_time:
    # Calculate and Format Time
    elapsed_seconds = int(time.time() - st.session_state.start_time)
    mins, secs = divmod(elapsed_seconds, 60)
    hours, mins = divmod(mins, 60)
    
    # Display the metric
    clock_placeholder.metric("Elapsed Time", f"{hours:02d}:{mins:02d}:{secs:02d}")
    
    # THE TRICK: Wait 1 second and force the app to refresh
    time.sleep(1)
    st.rerun()
else:
    clock_placeholder.info("Press Start to time your session!")

# 4. Workout Generation Logic
if 'workout_seed' not in st.session_state or st.sidebar.button('🎲 Shuffle New Workout'):
    st.session_state.workout_seed = time.time() # This ensures random selection on shuffle
    st.session_state.completed_tasks = {} # Reset progress on new workout

# Filter data based on equipment
filtered_data = data[data['Equipment'].isin(selected_equip)]

# 5. The Progress Bar and Percentage Label
st.divider()
completed_count = 0
total_exercises = 9 # Adjust this if you change your workout size

# Calculate percentage for display
if total_exercises > 0:
    # We calculate this later, but we initialize the container here
    progress_placeholder = st.empty()
    progress_bar = st.progress(0)

# 6. Generate Blocks
block_emojis = {"Lower Body": "🦵", "Upper Body": "💪", "Core": "🧘"}

for block, emoji in block_emojis.items():
    st.header(f"{emoji} {block}")
    
    block_df = filtered_data[filtered_data['Block'] == block]
    if not block_df.empty:
        sample = block_df.sample(n=min(3, len(block_df)), random_state=int(st.session_state.workout_seed % 1000))
        
        for _, row in sample.iterrows():
            task_key = f"{block}_{row['Exercise']}"
            is_done = st.checkbox(f"**{row['Exercise']}**", key=task_key)
            if is_done:
                completed_count += 1
            
            st.write(f"🔢 **Reps:** {row['Reps']} | 🛠️ **Equip:** {row['Equipment']}")
            st.caption(f"🎯 Targets: {row['Primary Muscle Focus']}")
            st.write("---")

# Update Progress Bar and Percentage Text
if total_exercises > 0:
    percent_val = int((completed_count / total_exercises) * 100)
    progress_bar.progress(completed_count / total_exercises)
    
    # This displays the percentage text right above the bar
    progress_placeholder.markdown(f"### Progress: {percent_val}%")
    
    if percent_val == 100:
        st.success("Workout Complete! 🎉")
        st.balloons()