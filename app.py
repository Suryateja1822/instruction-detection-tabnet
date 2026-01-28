"""
TabNet-IDS Advanced Threat Detection System
Next-generation network intrusion detection with AI-powered analysis and real-time monitoring
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime, timedelta
import time
import os
import io
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

# Import TabNet and other ML components
from pytorch_tabnet.tab_model import TabNetClassifier

# Import custom modules with error handling
try:
    from chat_assistant import ChatAssistant
except ImportError:
    st.warning("Chat assistant module not available")
    ChatAssistant = None

try:
    from solution_recommender import SolutionRecommender, ThreatSolution
except ImportError:
    st.warning("Solution recommender module not available")
    SolutionRecommender = None
    ThreatSolution = None

try:
    from predict import predict_threats
except ImportError:
    st.warning("Predict module not available")
    predict_threats = None

try:
    from preprocessing import preprocess_data
except ImportError:
    st.warning("Preprocessing module not available")
    preprocess_data = None

try:
    from explainability import generate_shap_explanations
except ImportError:
    st.warning("Explainability module not available")
    generate_shap_explanations = None

# Page configuration
st.set_page_config(
    page_title="TabNet-IDS - Advanced Threat Detection",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/tabnet-ids',
        'Report a bug': 'https://github.com/yourusername/tabnet-ids/issues',
        'About': "# TabNet-IDS\nAdvanced Network Intrusion Detection System\n\nPowered by TabNet and Streamlit"
    }
)

# Initialize session state for chat
if 'chat_assistant' not in st.session_state and ChatAssistant is not None:
    st.session_state.chat_assistant = ChatAssistant()
    st.session_state.chat_history = []
    st.session_state.show_chat = False
elif 'chat_assistant' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.show_chat = False

# Premium Dark Theme CSS (same as executive)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Hide sidebar completely or style it dark */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent;
    }
    
    /* Style sidebar text */
    section[data-testid="stSidebar"] * {
        color: #e0e7ff !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .executive-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
        animation: glow 2s ease-in-out infinite alternate;
        letter-spacing: 3px;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.5)); }
        to { filter: drop-shadow(0 0 20px rgba(118, 75, 162, 0.8)); }
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #667eea;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.8);
    }
    
    .alert-critical {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
        backdrop-filter: blur(10px);
        border-left: 4px solid #ef4444;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #fecaca;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
        animation: pulse-red 2s infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3); }
        50% { box-shadow: 0 4px 30px rgba(239, 68, 68, 0.6); }
    }
    
    .alert-warning {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(245, 158, 11, 0.2) 100%);
        backdrop-filter: blur(10px);
        border-left: 4px solid #fbbf24;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #fef3c7;
        box-shadow: 0 4px 20px rgba(251, 191, 36, 0.3);
    }
    
    .alert-info {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
        backdrop-filter: blur(10px);
        border-left: 4px solid #10b981;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #d1fae5;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 700;
        border-radius: 10px;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .upload-box {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: rgba(102, 126, 234, 0.05);
        transition: all 0.3s ease;
    }
    
    .upload-box:hover {
        border-color: #764ba2;
        background: rgba(102, 126, 234, 0.1);
    }
    
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

def start_real_time_monitoring():
    """Start real-time monitoring functionality"""
    try:
        # Initialize real-time monitor if not already done
        if 'real_time_monitor' not in st.session_state:
            try:
                from real_time_monitor import RealTimeMonitor
                st.session_state.real_time_monitor = RealTimeMonitor()
            except ImportError:
                st.error("❌ Real-time monitoring module not available")
                return False
        
        # Start monitoring
        st.session_state.real_time_monitor.start_monitoring()
        st.session_state.monitoring_active = True
        
        st.success("🔄 Real-time monitoring started!")
        return True
        
    except Exception as e:
        st.error(f"❌ Failed to start real-time monitoring: {str(e)}")
        st.session_state.monitoring_active = False
        return False

def stop_real_time_monitoring():
    """Stop real-time monitoring functionality"""
    try:
        if 'real_time_monitor' in st.session_state:
            st.session_state.real_time_monitor.stop_monitoring()
        
        st.session_state.monitoring_active = False
        st.session_state.real_time_monitoring = False
        
        st.info("⏹️ Real-time monitoring stopped")
        return True
        
    except Exception as e:
        st.error(f"❌ Failed to stop real-time monitoring: {str(e)}")
        return False

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
    st.session_state.uploaded_file = None
    st.session_state.uploaded_data = None
    st.session_state.model_loaded = False
    st.session_state.processing = False
    st.session_state.completed_analysis = False
    st.session_state.threats_detected = 0
    st.session_state.benign_count = 0
    st.session_state.threat_categories = {}
    st.session_state.threat_timeline = []
    st.session_state.prediction_time = 0
    st.session_state.upload_time = None
    st.session_state.show_advanced = False
    st.session_state.active_tab = "dashboard"
    st.session_state.real_time_monitoring = False
    
# Initialize threat database
if 'threat_db' not in st.session_state:
    st.session_state.threat_db = SolutionRecommender() if SolutionRecommender is not None else None
    
# Initialize real-time monitoring
if 'monitoring_data' not in st.session_state:
    st.session_state.monitoring_data = pd.DataFrame()
    st.session_state.monitoring_active = False

# Attack type information
ATTACK_INFO = {
    'dos': {'name': 'Denial of Service', 'severity': 'CRITICAL', 'icon': '💥', 'color': '#ef4444'},
    'probe': {'name': 'Network Probe', 'severity': 'WARNING', 'icon': '🔍', 'color': '#fbbf24'},
    'r2l': {'name': 'Remote to Local', 'severity': 'CRITICAL', 'icon': '🚨', 'color': '#ef4444'},
    'u2r': {'name': 'User to Root', 'severity': 'CRITICAL', 'icon': '⚠️', 'color': '#ef4444'},
    'normal': {'name': 'Normal Traffic', 'severity': 'INFO', 'icon': '✅', 'color': '#10b981'}
}

@st.cache_resource
def load_model():
    """Load the trained TabNet-IDS model"""
    model_path = "models/tabnet_ids_model.zip"
    if not os.path.exists(model_path):
        return None
    
    clf = TabNetClassifier()
    clf.load_model(model_path)
    return clf

def preprocess_uploaded_data(df):
    """
    Preprocess uploaded data for prediction
    Handles various CSV formats and matches training preprocessing
    """
    from sklearn.preprocessing import StandardScaler
    
    # Expected numeric columns for the model
    expected_numeric_cols = [
        'duration', 'src_bytes', 'dst_bytes', 'wrong_fragment', 'urgent',
        'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
        'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
        'rerror_rate', 'same_srv_rate', 'diff_srv_rate'
    ]
    
    # Categorical columns that need one-hot encoding
    categorical_cols = ['protocol_type', 'service', 'flag']
    
    # Extract numeric features
    available_numeric = [col for col in expected_numeric_cols if col in df.columns]
    
    if len(available_numeric) >= 10:
        # Use available numeric columns
        X_numeric = df[available_numeric].values
    else:
        # Use all numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        X_numeric = numeric_df.values
    
    # Handle categorical features if present
    categorical_features = []
    for col in categorical_cols:
        if col in df.columns:
            # One-hot encode
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
            categorical_features.append(dummies.values)
    
    # Combine numeric and categorical features
    if categorical_features:
        X = np.hstack([X_numeric] + categorical_features)
    else:
        X = X_numeric
    
    # Ensure we have exactly 25 features (matching training)
    # The model was trained with 25 features after one-hot encoding
    if X.shape[1] < 25:
        # Pad with zeros
        padding = np.zeros((X.shape[0], 25 - X.shape[1]))
        X = np.hstack([X, padding])
    elif X.shape[1] > 25:
        # Truncate to 25 features
        X = X[:, :25]
    
    # Normalize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    return X

def analyze_uploaded_data(df, model):
    """Analyze uploaded data and return results"""
    
    # Preprocess data
    X = preprocess_uploaded_data(df)
    
    # Make predictions
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    
    # Map predictions to attack types
    class_names = ['dos', 'normal', 'probe', 'r2l', 'u2r']
    
    # Add predictions to dataframe
    df['prediction'] = [class_names[p] if p < len(class_names) else 'unknown' for p in predictions]
    df['confidence'] = [max(prob) for prob in probabilities]
    df['threat_level'] = df['prediction'].apply(
        lambda x: ATTACK_INFO.get(x, {}).get('severity', 'INFO')
    )
    
    # Calculate statistics
    total_packets = len(df)
    threats = len(df[df['prediction'] != 'normal'])
    normal = total_packets - threats
    threat_percentage = (threats / total_packets * 100) if total_packets > 0 else 0
    
    # Attack type distribution
    attack_dist = df['prediction'].value_counts().to_dict()
    
    # Severity distribution
    severity_dist = df['threat_level'].value_counts().to_dict()
    
    results = {
        'dataframe': df,
        'total_packets': total_packets,
        'threats': threats,
        'normal': normal,
        'threat_percentage': threat_percentage,
        'attack_distribution': attack_dist,
        'severity_distribution': severity_dist,
        'high_confidence_threats': df[(df['prediction'] != 'normal') & (df['confidence'] > 0.8)]
    }
    
    return results

# Main Dashboard Header
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("💬 AI Security Assistant", key="chat_toggle"):
        st.session_state.show_chat = not st.session_state.show_chat

with col2:
    st.markdown('<h1 class="executive-header">🔒 TABNET-IDS THREAT DETECTION</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #a0aec0; font-size: 1.2rem; margin-top: -1rem;">Advanced Network Intrusion Detection with AI-Powered Analysis</p>', unsafe_allow_html=True)

with col3:
    if st.button("🔄 Real-time Monitoring", key="monitor_toggle"):
        st.session_state.real_time_monitoring = not st.session_state.real_time_monitoring
        if st.session_state.real_time_monitoring:
            st.session_state.monitoring_active = True
            start_real_time_monitoring()
        else:
            stop_real_time_monitoring()

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ CONTROL CENTER")
    st.markdown("---")
    
    # Model status
    model = load_model()
    if model:
        st.markdown('<div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1rem; border-radius: 10px; text-align: center; color: white; font-weight: 700;">🟢 MODEL READY</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 1rem; border-radius: 10px; text-align: center; color: white; font-weight: 700;">🔴 MODEL OFFLINE</div>', unsafe_allow_html=True)
        st.error("⚠️ Train model first:\n`python src/train_ids.py`")
    
    st.markdown("---")
    
    # Instructions
    st.markdown("### 📋 HOW TO USE")
    st.info("""
    **1.** Upload CSV file with network traffic
    
    **2.** Click 'Analyze Data'
    
    **3.** View results and threats
    
    **4.** Download report
    """)
    
    st.markdown("---")
    
    # Sample data format
    st.markdown("### 📄 DATA FORMAT")
    st.code("""
CSV with columns like:
- duration
- src_bytes
- dst_bytes
- protocol_type
- service
- flag
... (network features)
    """, language="text")
    
    if st.button("📥 Download Sample CSV"):
        # Generate sample data
        sample_data = {
            'duration': [10, 5, 15, 20, 8],
            'src_bytes': [1000, 500, 1500, 2000, 800],
            'dst_bytes': [500, 200, 800, 1000, 400],
            'wrong_fragment': [0, 0, 1, 0, 0],
            'urgent': [0, 0, 0, 1, 0],
            'hot': [1, 0, 2, 1, 0],
            'num_failed_logins': [0, 0, 0, 1, 0],
            'logged_in': [1, 1, 1, 0, 1],
            'num_compromised': [0, 0, 0, 1, 0],
            'count': [50, 30, 60, 40, 35],
            'srv_count': [30, 20, 35, 25, 22],
            'serror_rate': [0.1, 0.05, 0.15, 0.2, 0.08],
            'srv_serror_rate': [0.08, 0.04, 0.12, 0.18, 0.06],
            'rerror_rate': [0.05, 0.02, 0.08, 0.1, 0.04],
            'same_srv_rate': [0.8, 0.9, 0.75, 0.7, 0.85],
            'diff_srv_rate': [0.2, 0.1, 0.25, 0.3, 0.15]
        }
        sample_df = pd.DataFrame(sample_data)
        csv = sample_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download",
            data=csv,
            file_name="sample_network_traffic.csv",
            mime="text/csv"
        )

# Main content
tab1, tab2, tab3 = st.tabs(["📤 UPLOAD & ANALYZE", "📊 ANALYSIS RESULTS", "📈 DETAILED REPORT"])

# Tab 1: Upload
with tab1:
    st.markdown("### 📤 UPLOAD NETWORK TRAFFIC DATA")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h4>📁 Upload Your CSV File</h4>
            <p>Upload network traffic data in CSV format for AI-powered threat analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload network traffic data in CSV format"
        )
        
        if uploaded_file is not None:
            try:
                # Read the uploaded file
                df = pd.read_csv(uploaded_file)
                st.session_state.uploaded_data = df
                
                st.success(f"✅ File uploaded successfully! {len(df)} packets loaded.")
                
                # Show preview
                st.markdown("#### 👀 Data Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Show statistics
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Total Rows", len(df))
                col_b.metric("Total Columns", len(df.columns))
                col_c.metric("Numeric Columns", len(df.select_dtypes(include=[np.number]).columns))
                
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h4>ℹ️ Requirements</h4>
            <ul>
                <li>CSV format</li>
                <li>Network traffic features</li>
                <li>At least 10 numeric columns</li>
                <li>No missing values (preferred)</li>
            </ul>
            <br>
            <h4>✨ What We Detect</h4>
            <ul>
                <li>💥 DoS Attacks</li>
                <li>🔍 Network Probes</li>
                <li>🚨 Unauthorized Access</li>
                <li>⚠️ Privilege Escalation</li>
                <li>✅ Normal Traffic</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analyze button
    if st.session_state.uploaded_data is not None and model is not None:
        if st.button("🔍 ANALYZE DATA", use_container_width=True):
            with st.spinner("🔄 Analyzing network traffic with TabNet AI..."):
                results = analyze_uploaded_data(st.session_state.uploaded_data, model)
                st.session_state.analysis_results = results
                st.success("✅ Analysis complete!")
                st.balloons()
                time.sleep(1)
                st.rerun()

# Tab 2: Results
with tab2:
    if st.session_state.analysis_results is None:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem;">📊</div>
            <div style="font-size: 1.5rem; margin-top: 1rem;">No Analysis Yet</div>
            <div style="color: #a0aec0; margin-top: 0.5rem;">Upload data and click 'Analyze' to see results</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        results = st.session_state.analysis_results
        
        # Top metrics
        st.markdown("### 📊 ANALYSIS SUMMARY")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['total_packets']}</div>
            <div style="color: #a0aec0; font-size: 1rem; margin-top: 0.5rem;">TOTAL PACKETS</div>
        </div>
        """, unsafe_allow_html=True)
        
        col2.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #ef4444;">{results['threats']}</div>
            <div style="color: #a0aec0; font-size: 1rem; margin-top: 0.5rem;">THREATS FOUND</div>
        </div>
        """, unsafe_allow_html=True)
        
        col3.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #10b981;">{results['normal']}</div>
            <div style="color: #a0aec0; font-size: 1rem; margin-top: 0.5rem;">NORMAL TRAFFIC</div>
        </div>
        """, unsafe_allow_html=True)
        
        col4.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #fbbf24;">{results['threat_percentage']:.1f}%</div>
            <div style="color: #a0aec0; font-size: 1rem; margin-top: 0.5rem;">THREAT RATE</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Attack distribution
            attack_data = results['attack_distribution']
            fig = go.Figure(data=[go.Pie(
                labels=list(attack_data.keys()),
                values=list(attack_data.values()),
                hole=0.4,
                marker=dict(colors=['#ef4444', '#10b981', '#fbbf24', '#667eea', '#764ba2'])
            )])
            fig.update_layout(
                title="Attack Type Distribution",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=14)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Severity distribution
            severity_data = results['severity_distribution']
            fig = go.Figure(data=[go.Bar(
                x=list(severity_data.keys()),
                y=list(severity_data.values()),
                marker=dict(color=['#ef4444', '#fbbf24', '#10b981'])
            )])
            fig.update_layout(
                title="Severity Distribution",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=14),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # High confidence threats
        st.markdown("### 🚨 HIGH CONFIDENCE THREATS")
        high_threats = results['high_confidence_threats']
        
        if len(high_threats) > 0:
            for idx, row in high_threats.head(10).iterrows():
                threat_info = ATTACK_INFO.get(row['prediction'], {})
                severity_class = {
                    'CRITICAL': 'alert-critical',
                    'WARNING': 'alert-warning',
                    'INFO': 'alert-info'
                }.get(threat_info.get('severity', 'INFO'), 'alert-info')
                
                st.markdown(f"""
                <div class="{severity_class}">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <strong style="font-size: 1.2rem;">{threat_info.get('icon', '🔔')} {threat_info.get('name', 'Unknown')}</strong>
                            <div style="margin-top: 0.5rem;">Row #{idx} | Confidence: {row['confidence']:.1%}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.5rem; font-weight: 900;">{threat_info.get('severity', 'INFO')}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No high-confidence threats detected!")

# Tab 3: Detailed Report
with tab3:
    if st.session_state.analysis_results is None:
        st.info("📊 Upload and analyze data to see detailed report")
    else:
        results = st.session_state.analysis_results
        df = results['dataframe']
        
        st.markdown("### 📋 COMPLETE ANALYSIS REPORT")
        
        # Full dataframe with predictions
        st.markdown("#### 🔍 All Packets with Predictions")
        st.dataframe(
            df[['prediction', 'confidence', 'threat_level']].head(100),
            use_container_width=True
        )
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Report (CSV)",
            data=csv,
            file_name=f"tabnet_ids_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Statistics
        st.markdown("#### 📊 Detailed Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Attack Type Breakdown:**")
            for attack_type, count in results['attack_distribution'].items():
                percentage = (count / results['total_packets'] * 100)
                st.write(f"- {ATTACK_INFO.get(attack_type, {}).get('name', attack_type)}: {count} ({percentage:.1f}%)")
        
        with col2:
            st.markdown("**Severity Breakdown:**")
            for severity, count in results['severity_distribution'].items():
                percentage = (count / results['total_packets'] * 100)
                st.write(f"- {severity}: {count} ({percentage:.1f}%)")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <div style='font-size: 1.5rem; font-weight: 700; color: #667eea; font-family: "Orbitron", sans-serif;'>
        🛡️ TABNET-IDS ANALYSIS CENTER
    </div>
    <div style='color: #a0aec0; margin-top: 0.5rem;'>
        AI-Powered Network Threat Detection | Upload, Analyze, Protect
    </div>
</div>
""", unsafe_allow_html=True)
