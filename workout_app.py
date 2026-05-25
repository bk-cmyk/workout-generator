# ==========================================
# 2. Data Connection (Updated)
# ==========================================
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSaHE0jUfiF6TrlsS2Trkhw1IRLu6vMQHdVOGHtvANQm5TUPQUHJf7XBYaLOwvRKjTox5P1xmfLa7ME/pub?output=csv'

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        
        # Clean column headers: remove leading/trailing spaces
        df.columns = df.columns.str.strip()
        
        # Clean text cells: remove hidden spaces
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        # If there's an error loading, show it in the app logs or a safe warning
        st.sidebar.error(f"Error loading data: {e}")
        return pd.DataFrame()

data = load_data()

# Quick debug check: if the app is still failing, uncomment the line below 
# to see exactly what columns Pandas is reading from your sheet:
# st.write("Columns found:", data.columns.tolist())


# ==========================================
# 4. Main UI: Shuffle and Equipment (Updated)
# ==========================================
st.divider()

if st.button('🎲 SHUFFLE WORKOUT', use_container_width=True):
    st.session_state.workout_seed = time.time()
    st.rerun()

if 'workout_seed' not in st.session_state:
    st.session_state.workout_seed = time.time()

# Check if data loaded successfully and the expected column exists
if not data.empty and 'Equipment' in data.columns:
    equipment_list = sorted(data['Equipment'].unique().tolist())
    
    selected_equip = st.multiselect(
        "Filter Equipment", 
        options=equipment_list, 
        default=equipment_list
    )
else:
    selected_equip = []


# ==========================================
# 6. Generate Blocks (Updated with Safety Check)
# ==========================================
# Wrap everything in a check to make sure data exists before filtering
if not data.empty and 'Equipment' in data.columns:
    filtered_data = data[data['Equipment'].isin(selected_equip)]
    block_emojis = {"Lower Body": "🦵", "Upper Body": "💪", "Core": "🧘"}

    for block, emoji in block_emojis.items():
        st.header(f"{emoji} {block}")
        
        # Ensure 'Block' column also exists before filtering
        if 'Block' in filtered_data.columns:
            block_df = filtered_data[filtered_data['Block'] == block]
            
            if not block_df.empty:
                sample = block_df.sample(n=min(3, len(block_df)), random_state=int(st.session_state.workout_seed % 1000))
                for _, row in sample.iterrows():
                    if st.checkbox(f"**{row['Exercise']}**", key=f"{block}_{row['Exercise']}"):
                        completed_count += 1
                    
                    st.write(f"🔢 **Reps:** {row['Reps']} | 🛠️ **Equip:** {row['Equipment']}")
                    st.caption(f"🎯 Targets: {row.get('Primary Muscle Focus', 'N/A')}")
                    st.write("---")
else:
    st.warning("⚠️ Unable to load exercises. Please check your Google Sheets connection or column headers.")
