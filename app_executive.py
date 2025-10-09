"""
TabNet-IDS Executive Security Operations Center
Premium Dark Theme with Glassmorphism Design
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os
from pytorch_tabnet.tab_model import TabNetClassifier
import json

# Page configuration
st.set_page_config(
    page_title="TabNet-IDS Executive SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark Theme CSS with Glassmorphism
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Header */
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
    
    /* Glassmorphism Cards */
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
    
    /* Metric Cards */
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
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
    }
    
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #667eea;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.8);
    }
    
    .metric-label {
        font-size: 1rem;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }
    
    /* Alert Styles */
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
    
    /* Buttons */
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
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.95) 0%, rgba(26, 31, 58, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #667eea;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        color: #a0aec0;
        font-weight: 600;
        padding: 10px 20px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Data Tables */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-radius: 10px;
        color: #e2e8f0 !important;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-online {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
    }
    
    .status-offline {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Text Colors */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #e2e8f0 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        color: #667eea !important;
        font-weight: 700;
    }
    
    /* IP Address Display */
    .ip-display {
        font-family: 'Courier New', monospace;
        background: rgba(102, 126, 234, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border-left: 3px solid #667eea;
        display: inline-block;
    }
    
    /* Threat Level Indicator */
    .threat-indicator {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .threat-critical { background: #ef4444; box-shadow: 0 0 15px #ef4444; }
    .threat-warning { background: #fbbf24; box-shadow: 0 0 15px #fbbf24; }
    .threat-info { background: #10b981; box-shadow: 0 0 15px #10b981; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'blocked_ips' not in st.session_state:
    st.session_state.blocked_ips = set()
if 'threat_log' not in st.session_state:
    st.session_state.threat_log = []
if 'monitoring_active' not in st.session_state:
    st.session_state.monitoring_active = False
if 'total_packets' not in st.session_state:
    st.session_state.total_packets = 0

# Attack type information
ATTACK_INFO = {
    'dos': {
        'name': 'Denial of Service',
        'severity': 'CRITICAL',
        'description': 'Attempts to make a machine or network resource unavailable',
        'mitigation': ['Rate limiting', 'Traffic filtering', 'Load balancing'],
        'icon': '💥',
        'color': '#ef4444'
    },
    'probe': {
        'name': 'Network Probe',
        'severity': 'WARNING',
        'description': 'Reconnaissance activity to gather network information',
        'mitigation': ['Firewall rules', 'IDS alerts', 'Port security'],
        'icon': '🔍',
        'color': '#fbbf24'
    },
    'r2l': {
        'name': 'Remote to Local',
        'severity': 'CRITICAL',
        'description': 'Unauthorized access from remote machine',
        'mitigation': ['Strong authentication', 'Access control', 'VPN'],
        'icon': '🚨',
        'color': '#ef4444'
    },
    'u2r': {
        'name': 'User to Root',
        'severity': 'CRITICAL',
        'description': 'Privilege escalation attack',
        'mitigation': ['Least privilege', 'Patch management', 'Monitoring'],
        'icon': '⚠️',
        'color': '#ef4444'
    },
    'normal': {
        'name': 'Normal Traffic',
        'severity': 'INFO',
        'description': 'Legitimate network traffic',
        'mitigation': [],
        'icon': '✅',
        'color': '#10b981'
    }
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

def generate_network_traffic(n_samples=1):
    """Generate synthetic network traffic for real-time simulation"""
    data = {
        'duration': np.random.exponential(10, n_samples),
        'src_bytes': np.random.exponential(1000, n_samples),
        'dst_bytes': np.random.exponential(1000, n_samples),
        'wrong_fragment': np.random.poisson(0.1, n_samples),
        'urgent': np.random.poisson(0.05, n_samples),
        'hot': np.random.poisson(0.5, n_samples),
        'num_failed_logins': np.random.poisson(0.1, n_samples),
        'logged_in': np.random.binomial(1, 0.7, n_samples),
        'num_compromised': np.random.poisson(0.05, n_samples),
        'count': np.random.poisson(50, n_samples),
        'srv_count': np.random.poisson(30, n_samples),
        'serror_rate': np.random.beta(2, 5, n_samples),
        'srv_serror_rate': np.random.beta(2, 5, n_samples),
        'rerror_rate': np.random.beta(2, 5, n_samples),
        'same_srv_rate': np.random.beta(5, 2, n_samples),
        'diff_srv_rate': np.random.beta(2, 5, n_samples),
    }
    
    # Add source and destination IPs
    data['src_ip'] = [f"192.168.{np.random.randint(1,255)}.{np.random.randint(1,255)}" for _ in range(n_samples)]
    data['dst_ip'] = [f"10.0.{np.random.randint(1,255)}.{np.random.randint(1,255)}" for _ in range(n_samples)]
    data['timestamp'] = [datetime.now() - timedelta(seconds=np.random.randint(0, 300)) for _ in range(n_samples)]
    
    return pd.DataFrame(data)

def preprocess_for_prediction(df):
    """Preprocess data for model prediction"""
    numeric_cols = ['duration', 'src_bytes', 'dst_bytes', 'wrong_fragment', 'urgent',
                   'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
                   'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
                   'rerror_rate', 'same_srv_rate', 'diff_srv_rate']
    
    X = df[numeric_cols].values
    return X

def create_alert(threat_type, src_ip, dst_ip, confidence, timestamp):
    """Create a security alert"""
    alert = {
        'timestamp': timestamp,
        'type': threat_type,
        'severity': ATTACK_INFO.get(threat_type, {}).get('severity', 'INFO'),
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'confidence': confidence,
        'status': 'Active',
        'description': ATTACK_INFO.get(threat_type, {}).get('description', 'Unknown threat'),
        'icon': ATTACK_INFO.get(threat_type, {}).get('icon', '🔔')
    }
    st.session_state.alerts.insert(0, alert)
    st.session_state.threat_log.append(alert)
    
    if len(st.session_state.alerts) > 50:
        st.session_state.alerts = st.session_state.alerts[:50]

def block_ip(ip_address):
    """Block an IP address"""
    st.session_state.blocked_ips.add(ip_address)

def unblock_ip(ip_address):
    """Unblock an IP address"""
    if ip_address in st.session_state.blocked_ips:
        st.session_state.blocked_ips.remove(ip_address)

# Main Dashboard Header
st.markdown('<h1 class="executive-header">🛡️ TABNET-IDS EXECUTIVE SOC</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #a0aec0; font-size: 1.2rem; margin-top: -1rem;">Real-Time Network Intrusion Detection & Response System</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ CONTROL CENTER")
    st.markdown("---")
    
    # Model status with premium styling
    model = load_model()
    if model:
        st.markdown('<div class="status-badge status-online">🟢 SYSTEM ONLINE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-offline">🔴 MODEL OFFLINE</div>', unsafe_allow_html=True)
        st.warning("⚠️ Train model: `python src/train_ids.py`")
    
    st.markdown("---")
    
    # Monitoring controls with premium buttons
    st.markdown("### 🎯 MONITORING")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ START" if not st.session_state.monitoring_active else "⏸️ PAUSE"):
            st.session_state.monitoring_active = not st.session_state.monitoring_active
    
    with col2:
        if st.button("🔄 RESET"):
            st.session_state.alerts = []
            st.session_state.threat_log = []
            st.session_state.total_packets = 0
            st.rerun()
    
    monitoring_speed = st.slider("⚡ Speed (sec)", 1, 10, 2)
    
    st.markdown("---")
    
    # System Statistics
    st.markdown("### 📊 LIVE STATS")
    
    total_threats = len([a for a in st.session_state.threat_log if a['type'] != 'normal'])
    threat_percentage = (total_threats / max(len(st.session_state.threat_log), 1)) * 100
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 1rem; margin: 0.5rem 0;">
        <div style="font-size: 2rem; color: #667eea; font-weight: 900;">{st.session_state.total_packets}</div>
        <div style="color: #a0aec0; font-size: 0.9rem;">TOTAL PACKETS</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 1rem; margin: 0.5rem 0;">
        <div style="font-size: 2rem; color: #ef4444; font-weight: 900;">{total_threats}</div>
        <div style="color: #a0aec0; font-size: 0.9rem;">THREATS DETECTED</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 1rem; margin: 0.5rem 0;">
        <div style="font-size: 2rem; color: #fbbf24; font-weight: 900;">{len(st.session_state.blocked_ips)}</div>
        <div style="color: #a0aec0; font-size: 0.9rem;">BLOCKED IPs</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Threat Level Gauge
    st.markdown("### 🎚️ THREAT LEVEL")
    if threat_percentage < 20:
        threat_level = "LOW"
        threat_color = "#10b981"
    elif threat_percentage < 50:
        threat_level = "MODERATE"
        threat_color = "#fbbf24"
    else:
        threat_level = "HIGH"
        threat_color = "#ef4444"
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 1rem; text-align: center;">
        <div style="font-size: 1.5rem; color: {threat_color}; font-weight: 900;">{threat_level}</div>
        <div style="color: #a0aec0; font-size: 0.9rem;">{threat_percentage:.1f}% MALICIOUS</div>
    </div>
    """, unsafe_allow_html=True)

# Main content tabs with premium styling
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 LIVE DETECTION",
    "🚨 ACTIVE ALERTS",
    "🔒 IP MANAGEMENT",
    "📈 ANALYTICS",
    "🛠️ THREAT INTEL"
])

# Tab 1: Real-Time Detection
with tab1:
    if model is None:
        st.error("⚠️ **SYSTEM OFFLINE** - Please train the model first")
    else:
        # Top Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        metric1 = col1.empty()
        metric2 = col2.empty()
        metric3 = col3.empty()
        metric4 = col4.empty()
        
        st.markdown("---")
        
        # Live Traffic Feed
        st.markdown("### 📡 LIVE NETWORK TRAFFIC")
        traffic_container = st.empty()
        
        # Real-time monitoring loop
        if st.session_state.monitoring_active:
            # Generate traffic
            traffic_df = generate_network_traffic(n_samples=3)
            st.session_state.total_packets += len(traffic_df)
            
            # Preprocess and predict
            X = preprocess_for_prediction(traffic_df)
            predictions = model.predict(X)
            probabilities = model.predict_proba(X)
            
            # Map predictions
            class_names = ['dos', 'normal', 'probe', 'r2l', 'u2r']
            traffic_df['prediction'] = [class_names[p] if p < len(class_names) else 'unknown' for p in predictions]
            traffic_df['confidence'] = [max(prob) for prob in probabilities]
            
            # Create alerts
            for idx, row in traffic_df.iterrows():
                if row['prediction'] != 'normal' and row['confidence'] > 0.7:
                    create_alert(
                        row['prediction'],
                        row['src_ip'],
                        row['dst_ip'],
                        row['confidence'],
                        row['timestamp']
                    )
            
            # Update metrics
            total_traffic = st.session_state.total_packets
            threats = len([a for a in st.session_state.threat_log if a['type'] != 'normal'])
            normal = total_traffic - threats
            blocked = len(st.session_state.blocked_ips)
            
            metric1.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_traffic}</div>
                <div class="metric-label">Total Packets</div>
            </div>
            """, unsafe_allow_html=True)
            
            metric2.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #ef4444;">{threats}</div>
                <div class="metric-label">Threats</div>
            </div>
            """, unsafe_allow_html=True)
            
            metric3.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #10b981;">{normal}</div>
                <div class="metric-label">Normal</div>
            </div>
            """, unsafe_allow_html=True)
            
            metric4.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #fbbf24;">{blocked}</div>
                <div class="metric-label">Blocked</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display traffic with premium styling
            traffic_html = "<div class='glass-card'>"
            for idx, row in traffic_df.iterrows():
                threat_class = 'threat-critical' if row['prediction'] in ['dos', 'r2l', 'u2r'] else ('threat-warning' if row['prediction'] == 'probe' else 'threat-info')
                icon = ATTACK_INFO[row['prediction']]['icon']
                
                traffic_html += f"""
                <div style="padding: 1rem; margin: 0.5rem 0; background: rgba(255,255,255,0.03); border-radius: 10px; border-left: 4px solid {ATTACK_INFO[row['prediction']]['color']};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="threat-indicator {threat_class}"></span>
                            <strong style="font-size: 1.2rem;">{icon} {ATTACK_INFO[row['prediction']]['name']}</strong>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.9rem; color: #a0aec0;">{row['timestamp'].strftime('%H:%M:%S')}</div>
                            <div style="font-size: 1.1rem; color: #667eea; font-weight: 700;">{row['confidence']:.1%} Confidence</div>
                        </div>
                    </div>
                    <div style="margin-top: 0.5rem; font-family: 'Courier New', monospace; font-size: 0.9rem;">
                        <span class="ip-display">{row['src_ip']}</span> → <span class="ip-display">{row['dst_ip']}</span>
                    </div>
                </div>
                """
            traffic_html += "</div>"
            
            traffic_container.markdown(traffic_html, unsafe_allow_html=True)
            
            # Auto-refresh
            time.sleep(monitoring_speed)
            st.rerun()
        else:
            st.info("⏸️ **MONITORING PAUSED** - Click START to begin real-time detection")

# Tab 2: Active Alerts
with tab2:
    st.markdown("### 🚨 ACTIVE SECURITY ALERTS")
    
    if not st.session_state.alerts:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem;">🛡️</div>
            <div style="font-size: 1.5rem; margin-top: 1rem;">ALL SYSTEMS SECURE</div>
            <div style="color: #a0aec0; margin-top: 0.5rem;">No active threats detected</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Filter options
        col1, col2 = st.columns([2, 1])
        severity_filter = col1.multiselect(
            "🔍 Filter by Severity",
            ['CRITICAL', 'WARNING', 'INFO'],
            default=['CRITICAL', 'WARNING']
        )
        
        # Display alerts with premium styling
        for alert in st.session_state.alerts:
            if alert['severity'] in severity_filter:
                severity_class = {
                    'CRITICAL': 'alert-critical',
                    'WARNING': 'alert-warning',
                    'INFO': 'alert-info'
                }.get(alert['severity'], 'alert-info')
                
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="{severity_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 1.5rem; font-weight: 900;">{alert['icon']} {alert['severity']}</div>
                                <div style="font-size: 1.2rem; margin-top: 0.5rem;">{ATTACK_INFO[alert['type']]['name']}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.5rem; font-weight: 900;">{alert['confidence']:.0%}</div>
                                <div style="font-size: 0.9rem; opacity: 0.8;">Confidence</div>
                            </div>
                        </div>
                        <div style="margin-top: 1rem; font-family: 'Courier New', monospace;">
                            <strong>Source:</strong> {alert['src_ip']} → <strong>Target:</strong> {alert['dst_ip']}
                        </div>
                        <div style="margin-top: 0.5rem; font-size: 0.9rem; opacity: 0.8;">
                            {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if alert['src_ip'] not in st.session_state.blocked_ips:
                        if st.button(f"🚫 BLOCK", key=f"block_{alert['timestamp']}"):
                            block_ip(alert['src_ip'])
                            st.success(f"Blocked {alert['src_ip']}")
                            st.rerun()
                    else:
                        st.markdown('<div style="color: #ef4444; font-weight: 700;">🚫 BLOCKED</div>', unsafe_allow_html=True)

# Tab 3: IP Management
with tab3:
    st.markdown("### 🔒 IP ADDRESS MANAGEMENT")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚫 BLOCKED IPs")
        if not st.session_state.blocked_ips:
            st.info("No IPs currently blocked")
        else:
            for ip in st.session_state.blocked_ips:
                col_ip, col_btn = st.columns([3, 1])
                col_ip.markdown(f'<div class="ip-display" style="font-size: 1.1rem;">🚫 {ip}</div>', unsafe_allow_html=True)
                if col_btn.button(f"✅ Unblock", key=f"unblock_{ip}"):
                    unblock_ip(ip)
                    st.success(f"Unblocked {ip}")
                    st.rerun()
    
    with col2:
        st.markdown("#### ➕ MANUAL BLOCKING")
        manual_ip = st.text_input("Enter IP Address", placeholder="192.168.1.100")
        if st.button("🚫 BLOCK IP"):
            if manual_ip:
                block_ip(manual_ip)
                st.success(f"Blocked {manual_ip}")
                st.rerun()

# Tab 4: Analytics
with tab4:
    st.markdown("### 📈 SECURITY ANALYTICS")
    
    if st.session_state.threat_log:
        log_df = pd.DataFrame(st.session_state.threat_log)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Attack distribution
            attack_counts = log_df['type'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=attack_counts.index,
                values=attack_counts.values,
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
            severity_counts = log_df['severity'].value_counts()
            fig = go.Figure(data=[go.Bar(
                x=severity_counts.index,
                y=severity_counts.values,
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
    else:
        st.info("📊 Start monitoring to collect analytics data")

# Tab 5: Threat Intelligence
with tab5:
    st.markdown("### 🛠️ THREAT INTELLIGENCE DATABASE")
    
    for attack_type, info in ATTACK_INFO.items():
        if attack_type != 'normal':
            with st.expander(f"{info['icon']} {info['name']} - {info['severity']}"):
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color: {info['color']};">{info['name']}</h4>
                    <p><strong>Severity:</strong> <span style="color: {info['color']};">{info['severity']}</span></p>
                    <p><strong>Description:</strong> {info['description']}</p>
                    <p><strong>Mitigation Strategies:</strong></p>
                    <ul>
                        {''.join([f'<li>{step}</li>' for step in info['mitigation']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <div style='font-size: 1.5rem; font-weight: 700; color: #667eea; font-family: "Orbitron", sans-serif;'>
        🛡️ TABNET-IDS EXECUTIVE SOC
    </div>
    <div style='color: #a0aec0; margin-top: 0.5rem;'>
        Powered by TabNet Deep Learning | Real-Time Intrusion Detection with Explainable AI
    </div>
    <div style='color: #667eea; margin-top: 1rem; font-size: 0.9rem;'>
        © 2025 Advanced Network Security Solutions
    </div>
</div>
""", unsafe_allow_html=True)
