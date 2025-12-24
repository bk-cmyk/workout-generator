{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww14520\viewh11320\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
\
# 1. Page Setup\
st.set_page_config(page_title="My Workout Generator", page_icon="\uc0\u55357 \u56490 ")\
st.title("\uc0\u55356 \u57291 \u65039  Daily Workout Generator")\
\
# 2. Load Data from your Live CSV link\
# Replace 'YOUR_CSV_URL' with the link you copied from Google Sheets\
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSaHE0jUfiF6TrlsS2Trkhw1IRLu6vMQHdVOGHtvANQm5TUPQUHJf7XBYaLOwvRKjTox5P1xmfLa7ME/pub?output=csv'\
\
def load_data():\
    df = pd.read_csv(CSV_URL)\
    return df\
\
data = load_data()\
\
# 3. Create a Shuffle Button\
if st.button('\uc0\u55356 \u57266  Shuffle New Workout'):\
    # This button triggers a re-run of the script\
    st.rerun()\
\
# 4. Generate the Blocks (3 Exercises Each)\
blocks = ["Lower Body", "Upper Body", "Core"]\
\
for block in blocks:\
    st.subheader(f"\uc0\u55358 \u56757  \{block\}")\
    \
    # Filter for the specific block\
    filtered_df = data[data['Block'] == block]\
    \
    # Randomly pick 3 exercises\
    if not filtered_df.empty:\
        # We sample 3 random rows\
        sample = filtered_df.sample(n=min(3, len(filtered_df)))\
        \
        # Display them in a clean table or as individual cards\
        for index, row in sample.iterrows():\
            st.markdown(f"**\{row['Exercise']\}**")\
            st.caption(f"\uc0\u55356 \u57263  Targets: \{row['Primary Muscle Focus']\} | \u55357 \u57056 \u65039  Equipment: \{row['Equipment']\}")\
    else:\
        st.write("No exercises found for this block.")\
    \
    st.divider()}