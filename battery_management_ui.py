import streamlit as st
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Battery Management System",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .task-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        color: white;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        animation: slideInLeft 0.6s ease-out;
    }
    
    .cell-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        color: white;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        animation: slideInRight 0.6s ease-out;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-active {
        background: #10b981;
        color: white;
    }
    
    .status-idle {
        background: #f59e0b;
        color: white;
    }
    
    .status-charging {
        background: #3b82f6;
        color: white;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .sidebar .stSelectbox > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'tasks_data' not in st.session_state:
    st.session_state.tasks_data = {}
if 'task_list' not in st.session_state:
    st.session_state.task_list = []

def create_cell_data(cell_type, idx):
    """Create cell data based on type"""
    voltage = 3.2 if cell_type == "lfp" else 3.6
    min_voltage = 2.8 if cell_type == "lfp" else 3.2
    max_voltage = 3.6 if cell_type == "lfp" else 4.0
    current = round(random.uniform(0, 5), 2)
    temp = round(random.uniform(25, 40), 1)
    capacity = round(voltage * current, 2)
    
    return {
        "voltage": voltage,
        "current": current,
        "temp": temp,
        "capacity": capacity,
        "min_voltage": min_voltage,
        "max_voltage": max_voltage,
        "health": round(random.uniform(85, 100), 1),
        "cycles": random.randint(50, 500)
    }

def create_voltage_chart(cells_data):
    """Create voltage monitoring chart"""
    if not cells_data:
        return None
    
    fig = go.Figure()
    
    for cell_key, data in cells_data.items():
        time_points = list(range(0, 61, 5))  
        base_voltage = data['voltage']
        voltages = [base_voltage + random.uniform(-0.1, 0.1) for _ in time_points]
        
        fig.add_trace(go.Scatter(
            x=time_points,
            y=voltages,
            mode='lines+markers',
            name=cell_key.replace('_', ' ').title(),
            line=dict(width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title="Real-time Voltage Monitoring",
        xaxis_title="Time (seconds)",
        yaxis_title="Voltage (V)",
        template="plotly_white",
        height=400,
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig

def create_temperature_gauge(temp):
    """Create temperature gauge"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = temp,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Temperature (°C)"},
        delta = {'reference': 25},
        gauge = {
            'axis': {'range': [None, 50]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 35], 'color': "yellow"},
                {'range': [35, 50], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 40
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

st.markdown("""
<div class="main-header">
    <h1>🔋 Battery Management System</h1>
    <p>Advanced Cell Monitoring & Task Management Platform</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Configuration Panel")
    
    st.markdown("#### 🔋 Cell Configuration")
    
    num_cells = st.number_input(
        "Number of Cells",
        min_value=1,
        max_value=20,
        value=3,
        help="Enter the number of battery cells to monitor"
    )
    
    cell_types = []
    for i in range(num_cells):
        cell_type = st.selectbox(
            f"Cell {i+1} Type",
            ["lfp", "nmc", "lto"],
            key=f"cell_type_{i}",
            help="Select the chemistry type for this cell"
        )
        cell_types.append(cell_type)
    
    if st.button("🔄 Initialize Cells", type="primary"):
        st.session_state.cells_data = {}
        for idx, cell_type in enumerate(cell_types, start=1):
            cell_key = f"cell_{idx}_{cell_type}"
            st.session_state.cells_data[cell_key] = create_cell_data(cell_type, idx)
        st.success("✅ Cells initialized successfully!")
        time.sleep(1)
        st.rerun()

if st.session_state.cells_data:
    col1, col2, col3, col4 = st.columns(4)
    
    total_voltage = sum(data['voltage'] for data in st.session_state.cells_data.values())
    avg_temp = sum(data['temp'] for data in st.session_state.cells_data.values()) / len(st.session_state.cells_data)
    total_current = sum(data['current'] for data in st.session_state.cells_data.values())
    avg_health = sum(data['health'] for data in st.session_state.cells_data.values()) / len(st.session_state.cells_data)
    
    with col1:
        st.metric(
            label="🔋 Total Voltage",
            value=f"{total_voltage:.2f} V",
            delta=f"{random.uniform(-0.1, 0.1):.2f}"
        )
    
    with col2:
        st.metric(
            label="🌡️ Avg Temperature",
            value=f"{avg_temp:.1f} °C",
            delta=f"{random.uniform(-1, 1):.1f}"
        )
    
    with col3:
        st.metric(
            label="⚡ Total Current",
            value=f"{total_current:.2f} A",
            delta=f"{random.uniform(-0.5, 0.5):.2f}"
        )
    
    with col4:
        st.metric(
            label="💚 Avg Health",
            value=f"{avg_health:.1f}%",
            delta=f"{random.uniform(-1, 1):.1f}"
        )
    
    st.markdown("### 📈 Real-time Monitoring")
    voltage_chart = create_voltage_chart(st.session_state.cells_data)
    if voltage_chart:
        st.plotly_chart(voltage_chart, use_container_width=True)
    
    st.markdown("### 🔋 Cell Details")
    
    cols = st.columns(min(3, len(st.session_state.cells_data)))
    for idx, (cell_key, cell_data) in enumerate(st.session_state.cells_data.items()):
        with cols[idx % 3]:
            with st.expander(f"📱 {cell_key.replace('_', ' ').title()}", expanded=True):
                temp_gauge = create_temperature_gauge(cell_data['temp'])
                st.plotly_chart(temp_gauge, use_container_width=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Voltage", f"{cell_data['voltage']:.2f} V")
                    st.metric("Current", f"{cell_data['current']:.2f} A")
                    st.metric("Temperature", f"{cell_data['temp']:.1f} °C")
                
                with col_b:
                    st.metric("Capacity", f"{cell_data['capacity']:.2f} Wh")
                    st.metric("Health", f"{cell_data['health']:.1f}%")
                    st.metric("Cycles", f"{cell_data['cycles']}")
                
                st.progress(
                    (cell_data['voltage'] - cell_data['min_voltage']) / 
                    (cell_data['max_voltage'] - cell_data['min_voltage'])
                )
                st.caption(f"Range: {cell_data['min_voltage']}V - {cell_data['max_voltage']}V")

st.markdown("### 📋 Task Management")

with st.expander("➕ Add New Task", expanded=False):
    task_type = st.selectbox(
        "Task Type",
        ["CC_CV", "IDLE", "CC_CD"],
        help="Select the type of task to create"
    )
    
    col1, col2 = st.columns(2)
    
    if task_type == "CC_CV":
        with col1:
            cc_input = st.text_input("CC/CP Value", placeholder="e.g., 5A or 10W")
            cv_voltage = st.number_input("CV Voltage (V)", min_value=0.0, step=0.1)
            current = st.number_input("Current (A)", min_value=0.0, step=0.1)
        
        with col2:
            capacity = st.number_input("Capacity", min_value=0.0, step=0.1)
            time_seconds = st.number_input("Time (seconds)", min_value=1, step=1)
        
        task_data = {
            "task_type": "CC_CV",
            "cc_cp": cc_input,
            "cv_voltage": cv_voltage,
            "current": current,
            "capacity": capacity,
            "time_seconds": time_seconds
        }
    
    elif task_type == "IDLE":
        time_seconds = st.number_input("Time (seconds)", min_value=1, step=1)
        task_data = {
            "task_type": "IDLE",
            "time_seconds": time_seconds
        }
    
    elif task_type == "CC_CD":
        with col1:
            cc_input = st.text_input("CC/CP Value", placeholder="e.g., 5A or 10W")
            voltage = st.number_input("Voltage (V)", min_value=0.0, step=0.1)
        
        with col2:
            capacity = st.number_input("Capacity", min_value=0.0, step=0.1)
            time_seconds = st.number_input("Time (seconds)", min_value=1, step=1)
        
        task_data = {
            "task_type": "CC_CD",
            "cc_cp": cc_input,
            "voltage": voltage,
            "capacity": capacity,
            "time_seconds": time_seconds
        }
    
    if st.button("➕ Add Task", type="primary"):
        task_key = f"task_{len(st.session_state.tasks_data) + 1}"
        st.session_state.tasks_data[task_key] = task_data
        st.session_state.task_list.append(task_type)
        st.success(f"✅ Task {task_key} added successfully!")
        time.sleep(1)
        st.rerun()

if st.session_state.tasks_data:
    st.markdown("#### 📝 Current Tasks")
    
    for task_key, task_data in st.session_state.tasks_data.items():
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                task_type = task_data["task_type"]
                if task_type == "CC_CV":
                    st.markdown(f"""
                    <div class="task-card">
                        <h4>🔋 {task_key.replace('_', ' ').title()} - Constant Current/Constant Voltage</h4>
                        <p><strong>CC/CP:</strong> {task_data.get('cc_cp', 'N/A')}</p>
                        <p><strong>CV Voltage:</strong> {task_data.get('cv_voltage', 0)} V</p>
                        <p><strong>Current:</strong> {task_data.get('current', 0)} A</p>
                        <p><strong>Duration:</strong> {task_data.get('time_seconds', 0)} seconds</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif task_type == "IDLE":
                    st.markdown(f"""
                    <div class="task-card">
                        <h4>⏸️ {task_key.replace('_', ' ').title()} - Idle State</h4>
                        <p><strong>Duration:</strong> {task_data.get('time_seconds', 0)} seconds</p>
                        <span class="status-badge status-idle">Idle</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif task_type == "CC_CD":
                    st.markdown(f"""
                    <div class="task-card">
                        <h4>🔽 {task_key.replace('_', ' ').title()} - Constant Current Discharge</h4>
                        <p><strong>CC/CP:</strong> {task_data.get('cc_cp', 'N/A')}</p>
                        <p><strong>Voltage:</strong> {task_data.get('voltage', 0)} V</p>
                        <p><strong>Capacity:</strong> {task_data.get('capacity', 0)}</p>
                        <p><strong>Duration:</strong> {task_data.get('time_seconds', 0)} seconds</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"▶️ Start", key=f"start_{task_key}"):
                    st.success(f"Task {task_key} started!")
            
            with col3:
                if st.button(f"🗑️ Delete", key=f"delete_{task_key}"):
                    del st.session_state.tasks_data[task_key]
                    if task_data["task_type"] in st.session_state.task_list:
                        st.session_state.task_list.remove(task_data["task_type"])
                    st.rerun()

if st.session_state.cells_data or st.session_state.tasks_data:
    st.markdown("### 📊 Data Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📁 Export Cell Data"):
            if st.session_state.cells_data:
                df_cells = pd.DataFrame(st.session_state.cells_data).T
                st.download_button(
                    label="💾 Download Cell Data CSV",
                    data=df_cells.to_csv(),
                    file_name=f"cell_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    with col2:
        if st.button("📁 Export Task Data"):
            if st.session_state.tasks_data:
                df_tasks = pd.DataFrame(st.session_state.tasks_data).T
                st.download_button(
                    label="💾 Download Task Data CSV",
                    data=df_tasks.to_csv(),
                    file_name=f"task_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔄 Auto Refresh")
    auto_refresh = st.checkbox("Enable Auto Refresh", value=False)
    if auto_refresh:
        refresh_interval = st.selectbox("Refresh Interval", [5, 10, 30, 60], index=1)
        st.markdown(f"*Refreshing every {refresh_interval} seconds*")
        time.sleep(refresh_interval)
        st.rerun()

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🔋 Battery Management System v1.0 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
