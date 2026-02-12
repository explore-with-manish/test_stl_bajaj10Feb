import streamlit as st
import pandas as pd
from datetime import date, time

st.set_page_config(
    page_title="treamlit: Widgets & Interactivity", page_icon="🧩", layout="wide"
)

st.title("🧩 Streamlit: Widgets & Interactivity")
st.caption(
    "Change widgets and watch the page update instantly. Use session_state for memory across re-runs."
)

st.divider()

st.header("1. Text Input")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Text & Toggles")
    name = st.text_input(
        "Enter your name:", value="Manish", help="Please enter your name"
    )
    window_updates = st.toggle("Email me updates", value=True)
    show_extras = st.checkbox("Show advance options")

    st.write(f"Hello, {name}")
    if show_extras:
        st.info("Advance options, just for example")

with col2:
    st.subheader("Numbers & Ranges")
    age = st.number_input("Age", min_value=0, max_value=120, value=42, step=1)
    rating = st.slider("Satisfaction (1-10)", 0, 10, 7)
    window = st.slider("Select range", 0, 100, (25, 75))
    st.write(f"Age: {age}, Rating: {rating}, Window: {window}")

with col3:
    st.subheader("Choices and Time")
    color = st.selectbox("Favorite color", ["Red", "Green", "Blue", "Black"], index=2)
    toppings = st.multiselect(
        "Pizza toppings", ["Onion", "Corn", "Paneer", "Mushroom"], default=["Paneer"]
    )
    size = st.radio("T-shirt size", ["S", "M", "L", "XL"], index=2, horizontal=True)
    dob = st.date_input("Date of birth", value=date(2000, 1, 1))
    alarm = st.time_input("Alarm time", value=time(7, 30))
    st.write(f"Color={color}, Size={size}, DOB={dob}, Alarm={alarm}")
    st.caption(f"Toppings chosen: {', '.join(toppings) or 'None'}")

st.divider()

st.header("2_Buttons and State")

if "counter" not in st.session_state:
    st.session_state.counter = 0

c1, c2, c3, c4 = st.columns([1, 1, 1, 4])


def inc():
    st.session_state.counter += 1


def dec():
    st.session_state.counter -= 1


def reset():
    st.session_state.counter = 0


with c1:
    st.button("Increment", on_click=inc, help="Increase the value of Counter by 1")

with c2:
    st.button("Decrement", on_click=dec, help="Decrease the value of Counter by 1")

with c3:
    st.button("Reset", on_click=reset, help="Decrease the value of Counter to 0")

with c4:
    st.metric("Counter", value=st.session_state.counter)

st.divider()

st.header("3) File upload (CSV preview)")

uploaded = st.file_uploader(
    "Upload a CSV file", type=["csv"], help="Try any small CSV to preview"
)

if uploaded:
    try:
        df = pd.read_csv(uploaded)
        st.success(f"Loaded {df.shape[0]} rows × {df.shape[1]} cols")
        st.dataframe(df.head(10), use_container_width=True)
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        st.error(f"Failed to read CSV: {e}")
else:
    st.info("No file uploaded yet. Try uploading a CSV file to preview it here.")

st.divider()

st.header("4) Forms (submit-once pattern)")
st.write("Use forms when you want to collect multiple inputs and submit them together.")

with st.form("loan_form", clear_on_submit=False):
    st.subheader("Simple EMI Calculator")
    P = st.number_input(
        "Principal (₹)", min_value=0.0, value=500000.0, step=10000.0, format="%.2f"
    )
    annual_rate = st.number_input(
        "Annual interest rate (%)", min_value=0.0, value=9.0, step=0.1, format="%.2f"
    )
    months = st.number_input("Tenure (months)", min_value=1, value=60, step=1)
    submitted = st.form_submit_button("Calculate EMI")

if submitted:
    r = annual_rate / 1200.0
    if r == 0:
        emi = P / months
    else:
        emi = P * r * (1 + r) ** months / ((1 + r) ** months - 1)

    st.success(f"Estimated EMI: ₹{emi:,.2f}")

st.divider()
# ------------------------------------------------------------
# 🧩 Mini-exercise
# ------------------------------------------------------------
st.header("🧩 Mini-exercise")

st.markdown(
    """
**Build a tiny To-Do list using widgets + session state:**

**Requirements**
1. Create a text input labeled **"New task"** and an **"Add"** button.  
2. Store tasks in `st.session_state["todos"]` as a list of dicts like `{"text": "...", "done": False}`.  
3. Render each task with a checkbox to mark it **done/undone**.  
4. Add a **"Clear completed"** button to remove tasks where `done == True`.  
"""
)

# 1) Initialize storage for todos
if "todos" not in st.session_state:
    st.session_state.todos = []

# 2) Input row
new_task_col, add_btn_col = st.columns([4, 1])

with new_task_col:
    new_task = st.text_input("New Task", placeholder="Enter Todo Task")

with add_btn_col:
    # if st.button("Add"):
    #     txt = new_task.strip()
    #     if txt:
    #         st.session_state.todos.append({"text": txt, "done": False})
    st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
    if st.button("Add"):
        txt = new_task.strip()
        if txt:
            st.session_state.todos.append({"text": txt, "done": False})
    st.markdown("</div>", unsafe_allow_html=True)

# 3) Render tasks with checkboxes (use index-based unique keys)
for i, todo in enumerate(st.session_state.todos):
    checked = st.checkbox(todo["text"], value=todo["done"], key=f"todo_{i}")
    st.session_state.todos[i]["done"] = checked

# 4) Clear completed
if st.button("Clear Completed"):
    st.session_state.todos = [t for t in st.session_state.todos if not t["done"]]
    st.rerun()
