import streamlit as st
import pandas as pd
import time

# 1. Page Setup
st.set_page_config(page_title="Bonnie's Workout Generator", page_icon="🏋️")

# Title and Subtitle
st.title("🏋️ Daily Workout Generator")
st.markdown("### *Dumbbells, Resistance Bands, and Bodyweight workouts.*")
st.markdown("#### *Three sets for each block*")

# 2. Data Connection
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTDv8hjERkT7bcQ6MfJqDnKGxwtqvJE6KRnaK0oMQeT0v07Df0e1JMu0Ne-ZxiFu7kvunfkY3t2xDO3/pub?gid=1238381494&single=true&output=csv'

@st.cache_data(ttl=600)  # Caches for 10 minutes so updates pull through automatically
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        # Force all column headers to lowercase and strip whitespace to prevent casing bugs
        df.columns = df.columns.str.strip().str.lower()
        # Clean text cells: remove hidden spaces from text cells
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        return pd.DataFrame()

data = load_data()

# 3. Sidebar: Stopwatch and Rest Timer
st.sidebar.header("🏃 Workout Tools")

# --- Workout Stopwatch ---
st.sidebar.subheader("Total Time")
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

sw_col1, sw_col2 = st.sidebar.columns(2)
if sw_col1.button("▶️ Start"):
    st.session_state.start_time = time.time()
if sw_col2.button("⏹️ Reset"):
    st.session_state.start_time = None
    st.rerun()

clock_placeholder = st.sidebar.empty()

st.sidebar.divider()

# --- Rest Timer ---
st.sidebar.subheader("⏲️ Rest Timer")
rest_seconds = st.sidebar.number_input("Seconds", min_value=5, max_value=300, value=60, step=5)

if st.sidebar.button("⏱️ Start Rest"):
    timer_placeholder = st.sidebar.empty()
    for t in range(rest_seconds, -1, -1):
        m, s = divmod(t, 60)
        timer_placeholder.metric("Rest Remaining", f"{m:02d}:{s:02d}")
        time.sleep(1)
    
    timer_placeholder.success("Time's up! Back to work! 🔥")
    st.toast("Rest Complete!", icon="💪")

# 4. Main UI: Shuffle and Equipment
st.divider()

# Shuffle Button
if st.button('🎲 SHUFFLE WORKOUT', use_container_width=True):
    st.session_state.workout_seed = time.time()
    st.rerun()

# Ensure we have a seed for the first load
if 'workout_seed' not in st.session_state:
    st.session_state.workout_seed = time.time()

# Equipment Filter (checks for lowercase key)
if not data.empty and 'equipment' in data.columns:
    equipment_list = sorted(data['equipment'].unique().tolist())
    
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

# 6. Generate Blocks (Using robust lowercase column references)
if not data.empty and 'equipment' in data.columns and 'block' in data.columns:
    filtered_data = data[data['equipment'].isin(selected_equip)]
    block_emojis = {"Lower Body": "🦵", "Upper Body": "💪", "Core": "🧘"}

    for block_name, emoji in block_emojis.items():
        st.header(f"{emoji} {block_name}")
        
        # Match case-insensitively against your sheet's values
        block_df = filtered_data[filtered_data['block'].str.lower() == block_name.lower()]
        
        if not block_df.empty:
            sample = block_df.sample(n=min(3, len(block_df)), random_state=int(st.session_state.workout_seed % 1000))
            for _, row in sample.iterrows():
                exercise_name = row['exercise']
                # Checkbox persistence
                if st.checkbox(f"**{exercise_name}**", key=f"{block_name}_{exercise_name}"):
                    completed_count += 1
                
                st.write(f"🔢 **Reps:** {row['reps']} | 🛠️ **Equip:** {row['equipment']}")
                
                # Resolves variations like 'target muscle', 'target muscle focus', etc.
                muscle_focus = row.get('target muscle', row.get('primary muscle focus', 'N/A'))
                st.caption(f"🎯 Targets: {muscle_focus}")
                st.write("---")
else:
    st.warning("⚠️ Unable to generate workout blocks. Please verify that your Google Sheet includes columns for 'Block', 'Equipment', 'Exercise', and 'Reps'.")

# 7. Update Progress
if total_exercises > 0:
    percent = int((completed_count / total_exercises) * 100)
    progress_placeholder.markdown(f"## Progress: {percent}%")
    p_bar.progress(completed_count / total_exercises)

    if percent == 100:
        st.success("Workout Complete! 🎉")

# 8. Ticking Clock Logic
if st.session_state.start_time:
    elapsed = int(time.time() - st.session_state.start_time)
    m, s = divmod(elapsed, 60)
    h, m = divmod(m, 60)
    clock_placeholder.metric("Elapsed Time", f"{h:02d}:{m:02d}:{s:02d}")
    time.sleep(1)
    st.rerun()
