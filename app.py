import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta

# Page is often nicer in "wide" for layout demos
st.set_page_config(page_title="Streamlit: Layouts", page_icon="🧱", layout="wide")

st.title("🧱 Streamlit Layouts")
st.caption(
    "Columns, tabs, expanders, containers, and placeholders — build clean app layouts fast."
)

# ------------------------------------------------------------
# 0) Tiny sample data we'll reuse
# ------------------------------------------------------------
rng = np.random.default_rng(42)
today = date.today()
dates = pd.date_range(today - timedelta(days=29), today, freq="D")
sales = (
    rng.integers(80, 220, size=len(dates)) + np.linspace(0, 40, len(dates))
).astype(int)
revenue = sales * (350 + rng.normal(0, 25, size=len(dates)))
df = pd.DataFrame({"date": dates, "sales": sales, "revenue": revenue})
df["weekday"] = df["date"].dt.day_name()

# ------------------------------ Sidebar ------------------------------
# The sidebar *is* a layout area. Keep global controls here.
st.sidebar.header("Global Controls")
show_help = st.sidebar.checkbox("Show inline tips", value=True)
card_count = st.sidebar.slider("Cards to show", 3, 6, 4, help="Controls demo card grid")
use_weighted_cols = st.sidebar.toggle("Use weighted columns", value=True)
st.sidebar.caption("Sidebar is perfect for app-wide filters and knobs.")


# Tip callout toggler
def tip(msg: str):
    if show_help:
        st.info(msg)


st.divider()

# ------------------------------------------------------------
# 1) Columns
# ------------------------------------------------------------
st.header("1) Columns")

st.write("**Metric cards in a row** — a classic dashboard pattern:")
# Equal width columns: st.columns(N)
cols = st.columns(card_count)
kpis = [
    ("Total Sales (30d)", f"{df['sales'].sum():,}"),
    ("Total Revenue (₹)", f"{df['revenue'].sum():,.2f}"),
    ("Avg / Day", f"{df['sales'].mean():.1f}"),
    ("Best Day Sales", f"{df['sales'].max():,}"),
    ("Best Day Revenue (₹)", f"{df['revenue'].max():,.2f}"),
    ("Days", str(len(df))),
][:card_count]

for c, (label, val) in zip(cols, kpis):
    with c:
        st.metric(label, val)

tip(
    "Use `st.columns(N)` for equal widths. For asymmetric layouts, pass ratios like `st.columns([3, 1])`."
)

st.subheader("Weighted columns (content + side panel)")
# Weighted columns: main (wider) + side (narrower)
left, right = st.columns([3, 1]) if use_weighted_cols else st.columns(2)
with left:
    st.write("**Main area**: good for charts, tables, forms, etc.")
    st.line_chart(df.set_index("date")["sales"], use_container_width=True)
with right:
    st.write("**Side panel**: contextual info, quick actions, help.")
    st.write("- Download data")
    st.write("- Notes / annotations")
    st.write("- Filters for just this block")

# Nested columns inside a section
st.subheader("Nested columns")
outer1, outer2 = st.columns(2)
with outer1:
    st.write("Outer left")
    a, b = st.columns(2)
    with a:
        st.write("Nested A")
        st.table(df.head(3)[["date", "sales"]])
    with b:
        st.write("Nested B")
        st.table(df.tail(3)[["date", "sales"]])
with outer2:
    st.write("Outer right")
    st.area_chart(df.set_index("date")[["sales"]], use_container_width=True)

st.divider()

# ------------------------------------------------------------
# 2) Tabs
# ------------------------------------------------------------
st.header("2) Tabs")
st.write("Tabs help you show alternative views without leaving the page.")
tab1, tab2, tab3 = st.tabs(["Overview", "Table", "Chart"])

with tab1:
    st.write("High-level summary (last 7 days):")
    recent = df.tail(7)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Sales (7d)", f"{recent['sales'].sum():,}")
    with c2:
        st.metric("Revenue (7d)", f"₹ {recent['revenue'].sum():,.2f}")
    with c3:
        st.metric("Avg / day", f"{recent['sales'].mean():.1f}")
    tip("Each tab can have its own columns/controls. Tabs don't reset when you switch.")

with tab2:
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab3:
    st.bar_chart(df.set_index("date")["sales"].tail(14), use_container_width=True)
    st.caption("Last 14 days bar chart")

st.divider()

# ------------------------------------------------------------
# 3) Expanders (accordions)
# ------------------------------------------------------------
st.header("3) Expanders (accordions)")
with st.expander("Show FAQ"):
    st.markdown(
        """
        **Q: Where should I put filters?**  
        A: Prefer the **sidebar** for global controls, or a right-hand column for local ones.

        **Q: Can I combine tabs and columns?**  
        A: Yes. Tabs can contain columns, forms, charts, etc.

        **Q: When to use expanders?**  
        A: Hide less-critical details (logs, raw JSON, advanced settings).
        """
    )

with st.expander("Advanced settings"):
    st.checkbox("Enable experimental feature")
    st.text_input("Hidden token", type="password")

st.divider()

# ------------------------------------------------------------
# 4) Containers & placeholders
# ------------------------------------------------------------
st.header("4) Containers & placeholders")

st.write(
    "**Containers** group a section; **placeholders** let you swap content dynamically."
)

# A) Container: build a section progressively
cont = st.container()
cont.write("This text is inside a container.")
cont.line_chart(df.set_index("date")[["sales"]].tail(10), use_container_width=True)

# Later we can continue adding to the same section:
with cont:
    st.caption("Added later to the same container (keeps content grouped).")

# B) Placeholder: swap content on action
slot = st.empty()  # reserve a spot
with slot.container():
    st.subheader("Live slot")
    st.write("Click **Swap content** to replace this block.")

if st.button("Swap content"):
    # Completely replace what's inside `slot`
    with slot:
        st.success("✅ Content swapped!")
        st.write("This replaced the previous block using `st.empty()`.")
        st.table(df.tail(5)[["date", "sales", "revenue"]])

tip(
    "Use `st.empty()` when you need to update/replace a section without redrawing the whole page around it."
)

st.divider()

# ------------------------------------------------------------
# 5) Simple layout patterns
# ------------------------------------------------------------
st.header("5) Patterns")

st.subheader("A) Responsive card grid")
# Create a simple "card" per product using columns
products = [
    ("Engine Oil", 4.6, True),
    ("Spark Plug", 4.3, True),
    ("Brake Pads", 3.9, False),
    ("Wiper Blade", 4.1, True),
    ("Air Filter", 4.4, True),
    ("Coolant", 4.2, True),
][:card_count]

# 3 columns looks nice for cards
cols = st.columns(3)
for i, (name, rating, in_stock) in enumerate(products):
    with cols[i % 3]:
        st.markdown(f"#### {name}")
        st.write(f"⭐ {rating:.1f} / 5.0")
        st.write("In stock: ", "✅ Yes" if in_stock else "❌ No")
        st.button("Add to cart", key=f"add_{i}")

st.subheader("B) Kanban-style lists (3 columns)")
todo, doing, done = st.columns(3)
with todo:
    st.markdown("### To Do")
    st.write("- Build dashboard layout")
    st.write("- Connect to API")
with doing:
    st.markdown("### Doing")
    st.write("- Write data adapter")
    st.progress(60)
with done:
    st.markdown("### Done")
    st.write("- Define schema")
    st.write("- Create sample data")

st.divider()

# ------------------------------------------------------------
# 🧩 Mini-exercise
# ------------------------------------------------------------
st.header("🧩 Mini-exercise")

st.markdown(
    """
**Goal:** Create a clean **Analysis** section using layout primitives.

**Requirements**
1) Build a 2-column layout with ratios **[2, 1]**.  
   - Left: put a `st.subheader("Trend")` and a **line chart** of `sales` for the last **14** days.  
   - Right: put a `st.subheader("Summary")` and show three `st.metric` cards:
       - Sales (14d total)  
       - Revenue (14d total, prefixed with ₹)  
       - Best Day Sales (14d)  
2) Below the 2-column block, create **tabs**: `["By Weekday", "Raw"]`.  
   - In **By Weekday**: show a small table of weekday-wise `sales` sum sorted descending.  
   - In **Raw**: put the full `df` in `st.dataframe` with `use_container_width=True`.  
3) Wrap the whole section in a **container** named `analysis_cont` and add a **button** labeled
   **"Refresh view"** that uses a **placeholder** to briefly show "Refreshing..." and then re-renders the section.

*Hints:*  
- Use `df.tail(14)` to slice, then `.sum()`, `.max()`.  
- For the placeholder, create it with `slot = st.empty()` and write something into it, then overwrite.
"""
)
