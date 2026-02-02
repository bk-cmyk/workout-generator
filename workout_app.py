import streamlit as st
import pandas as pd
import time

# 1. Page Setup
st.set_page_config(page_title="Workout Generator", page_icon="💪")

# Title and Subtitle
st.title("🏋️ Daily Workout Generator")
st.markdown("### *Dumbbells, Resistance Bands, and Bodyweight workouts.*")
st.markdown("#### *Three sets for each block*")

# 2. Data Connection
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSaHE0jUfiF6TrlsS2Trkhw1IRLu6vMQHdVOGHtvANQm5TUPQUHJf7XBYaLOwvRKjTox5P1xmfLa7ME/pub?output=csv'

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        # NEW: This line removes hidden spaces from the start/end of every text cell
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except:
        return pd.DataFrame()

data = load_data()

# 3. Sidebar: Stopwatch Only
st.sidebar.header("🏃 Workout Timer")

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

col1, col2 = st.sidebar.columns(2)
if col1.button("▶️ Start"):
    st.session_state.start_time = time.time()
if col2.button("⏹️ Reset"):
    st.session_state.start_time = None
    st.rerun()

clock_placeholder = st.sidebar.empty()

# 4. Main UI: Shuffle and Equipment
sst.divider()

# 1. Shuffle Button (Full Width at the Top)
if st.button('🎲 SHUFFLE WORKOUT', use_container_width=True):
    # Update the seed and clear checkboxes by resetting session state keys
    st.session_state.workout_seed = time.time()
    st.rerun()

# Ensure we have a seed for the first load
if 'workout_seed' not in st.session_state:
    st.session_state.workout_seed = time.time()

# 2. Equipment Filter (Full Width directly below)
if not data.empty:
    # Use .strip() to fix the "double dumbbells" issue if not already fixed in load_data
    equipment_list = sorted(data['Equipment'].str.strip().unique().tolist())
    
    selected_equip = st.multiselect(
        "Filter Equipment", 
        options=equipment_list, 
        default=equipment_list
    )
else:
    selected_equip = []

# 5. Progress Bar Setup
progress_placeholder = st.empty()
p_bar = st.empty()
completed_count = 0
total_exercises = 9 

# 6. Generate Blocks
filtered_data = data[data['Equipment'].isin(selected_equip)]
block_emojis = {"Lower Body": "🦵", "Upper Body": "💪", "Core": "🧘"}

for block, emoji in block_emojis.items():
    st.header(f"{emoji} {block}")
    block_df = filtered_data[filtered_data['Block'] == block]
    
    if not block_df.empty:
        sample = block_df.sample(n=min(3, len(block_df)), random_state=int(st.session_state.workout_seed % 1000))
        for _, row in sample.iterrows():
            # Checkbox persistence
            if st.checkbox(f"**{row['Exercise']}**", key=f"{block}_{row['Exercise']}"):
                completed_count += 1
            
            st.write(f"🔢 **Reps:** {row['Reps']} | 🛠️ **Equip:** {row['Equipment']}")
            st.caption(f"🎯 Targets: {row['Primary Muscle Focus']}")
            st.write("---")

# 7. Update Progress (Calculated after loop to prevent glitch)
percent = int((completed_count / total_exercises) * 100)
progress_placeholder.markdown(f"## Progress: {percent}%")
p_bar.progress(completed_count / total_exercises)

if percent == 100:
    st.success("Workout Complete! 🎉")
    st.balloons()

# 8. Ticking Clock Logic (At the very bottom so it doesn't interrupt calculation)
if st.session_state.start_time:
    elapsed = int(time.time() - st.session_state.start_time)
    m, s = divmod(elapsed, 60)
    h, m = divmod(m, 60)
    clock_placeholder.metric("Elapsed Time", f"{h:02d}:{m:02d}:{s:02d}")
    time.sleep(1)
    st.rerun()