# Streamlit Deployment Readiness Plan

The goal is to prepare the `dashboard.py` for deployment to a platform like Streamlit Community Cloud, where it won't have the background simulator or flask server running. To maintain the illusion of live data, we will "replay" existing data from `aiotdb.db` in a loop.

## Changes Required

### 1. Replay Logic in `dashboard.py`
To simulate an actively updating dashboard without live sensors, we will:
- Use `@st.cache_data` to load all historical data from `aiotdb.db` once into memory. It will be loaded in chronological order (oldest to newest).
- Utilize `st.session_state` to track an `offset` index.
- Every time `streamlit_autorefresh` triggers a reload, we increment the `offset`.
- We will construct a "sliding window" (e.g., the last 30 observations). Based on the `offset`, we will slice 30 rows from the cached data. If the offset reaches the end of the data, we loop back to the beginning.

### 2. X-Axis Adjustments
Since the actual timestamps in the database will be static and from the past, plotting them as-is will not feel "live".
- **Proposed approach:** As you requested, we will update the X-axis for the graphs to use a sequential integer representing the "Last N observations" (e.g., changing the axis labels to `Observation #1, #2...` or just plotting against an index range of `-30 to 0`).
- Alternatively, we could generate fake "current" timestamps for the sliced window to maintain the time-series look, but using an observation index is cleaner and fulfills your request. We will drop the historical timestamp on the charts in favor of an "Observation Sequence".

### 3. KPI Updates
- The "Last Updated" KPI block will be updated to show either the actual time of the refresh using `datetime.now()` rather than the static database timestamp so the user sees the page is actually "live", or we just show the "Current Observation Index".

### 4. Deployment Check
- Ensure `requirements.txt` contains all necessary dependencies (`streamlit`, `pandas`, `plotly`, `streamlit-autorefresh`). *Note: Currently present in the project.*
- We only need to push `dashboard.py`, `aiotdb.db`, and `requirements.txt` to the remote Git repository for Streamlit to deploy it.

## User Review Required

> [!IMPORTANT]
> **Data Wrapping:** When the sliding window reaches the end of the database rows, it will instantly loop to the beginning. The chart will temporarily show a jump from the last reading to the first reading.
> **X-Axis Design:** I am proposing replacing the X-axis with exactly what you asked: an integer index showing "Last N observations" instead of the old, static timestamps.

Please let me know if you approve of this replay method and the X-axis changes! Once approved, I will implement the changes in `dashboard.py` and finalize the codebase.
