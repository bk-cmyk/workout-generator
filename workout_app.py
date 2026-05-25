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
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSaHE0jUfiF6TrlsS2Trkhw1IRLu6vMQHdVOGHtvANQm5TUPQUHJf7XBYaLOwvRKjTox5P1xmfLa7ME/pub?output=csv'

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        # Clean column headers: remove accidental leading/trailing spaces
        df.columns = df.columns.str.strip()
        # Clean text cells: remove hidden spaces from the start/end of every text cell
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        # Failsafe fallback if Google Sheets is unreachable
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

# Equipment Filter (with safety check to see if column exists)
if not data.empty and 'Equipment' in data.columns:
    equipment_list = sorted(data['Equipment'].unique().tolist())
    
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

# 6. Generate Blocks (Safely guarded against KeyErrors)
if not data.empty and 'Equipment' in data.columns and 'Block' in data.columns:
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
                # Using .get() for optional columns prevents future KeyErrors
                st.caption(f"🎯 Targets: {row.get('Primary Muscle Focus', 'N/A')}")
                st.write("---")
else:
    st.warning("⚠️ Unable to generate workout blocks. Please check that your Google Sheet is published and contains the required 'Block' and 'Equipment' columns.")

# 7. Update Progress
if total_exercises > 0:
    percent = int((
