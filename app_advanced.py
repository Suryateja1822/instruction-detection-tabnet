"""
Advanced TabNet-IDS Security Operations Center (SOC) Dashboard
Real-time threat detection with automated response actions
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
    page_title="TabNet-IDS SOC Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .alert-critical {
        background-color: #ff4444;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .alert-warning {
        background-color: #ffaa00;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .alert-info {
        background-color: #00C851;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 5px;
    }
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

# Attack type information
ATTACK_INFO = {
    'dos': {
        'name': 'Denial of Service',
        'severity': 'CRITICAL',
        'description': 'Attempts to make a machine or network resource unavailable',
        'mitigation': ['Rate limiting', 'Traffic filtering', 'Load balancing'],
        'color': '#ff4444'
    },
    'probe': {
        'name': 'Network Probe',
        'severity': 'WARNING',
        'description': 'Reconnaissance activity to gather network information',
        'mitigation': ['Firewall rules', 'IDS alerts', 'Port security'],
        'color': '#ffaa00'
    },
    'r2l': {
        'name': 'Remote to Local',
        'severity': 'CRITICAL',
        'description': 'Unauthorized access from remote machine',
        'mitigation': ['Strong authentication', 'Access control', 'VPN'],
        'color': '#ff4444'
    },
    'u2r': {
        'name': 'User to Root',
        'severity': 'CRITICAL',
        'description': 'Privilege escalation attack',
        'mitigation': ['Least privilege', 'Patch management', 'Monitoring'],
        'color': '#ff4444'
    },
    'normal': {
        'name': 'Normal Traffic',
        'severity': 'INFO',
        'description': 'Legitimate network traffic',
        'mitigation': [],
        'color': '#00C851'
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
    # Select only numeric features for prediction
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
        'description': ATTACK_INFO.get(threat_type, {}).get('description', 'Unknown threat')
    }
    st.session_state.alerts.insert(0, alert)
    st.session_state.threat_log.append(alert)
    
    # Keep only last 50 alerts
    if len(st.session_state.alerts) > 50:
        st.session_state.alerts = st.session_state.alerts[:50]

def block_ip(ip_address):
    """Block an IP address"""
    st.session_state.blocked_ips.add(ip_address)
    st.success(f"🚫 IP {ip_address} has been blocked!")

def unblock_ip(ip_address):
    """Unblock an IP address"""
    if ip_address in st.session_state.blocked_ips:
        st.session_state.blocked_ips.remove(ip_address)
        st.success(f"✅ IP {ip_address} has been unblocked!")

# Main Dashboard
st.markdown('<h1 class="main-header">🛡️ TabNet-IDS Security Operations Center</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/security-checked.png", width=100)
    st.title("⚙️ Control Panel")
    
    # Model status
    model = load_model()
    if model:
        st.success("✅ Model Loaded")
    else:
        st.error("❌ Model Not Found")
        st.info("Train the model first: `python src/train_ids.py`")
    
    st.markdown("---")
    
    # Monitoring controls
    st.subheader("🔍 Real-Time Monitoring")
    if st.button("▶️ Start Monitoring" if not st.session_state.monitoring_active else "⏸️ Pause Monitoring"):
        st.session_state.monitoring_active = not st.session_state.monitoring_active
    
    monitoring_speed = st.slider("Monitoring Speed (seconds)", 1, 10, 3)
    
    st.markdown("---")
    
    # Threat simulation
    st.subheader("🎯 Threat Simulation")
    threat_type = st.selectbox("Simulate Attack", ['normal', 'dos', 'probe', 'r2l', 'u2r'])
    if st.button("🚀 Generate Traffic"):
        st.session_state.simulate_threat = threat_type
    
    st.markdown("---")
    
    # Statistics
    st.subheader("📊 Statistics")
    st.metric("Total Alerts", len(st.session_state.alerts))
    st.metric("Blocked IPs", len(st.session_state.blocked_ips))
    st.metric("Threats Detected", len([a for a in st.session_state.alerts if a['type'] != 'normal']))

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Real-Time Detection",
    "🚨 Active Alerts",
    "🔒 Blocked IPs",
    "📈 Analytics",
    "🛠️ Threat Intelligence"
])

# Tab 1: Real-Time Detection
with tab1:
    st.header("Real-Time Network Traffic Analysis")
    
    if model is None:
        st.warning("⚠️ Please train the model first to enable real-time detection")
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        # Metrics placeholders
        metric_total = col1.empty()
        metric_threats = col2.empty()
        metric_normal = col3.empty()
        metric_blocked = col4.empty()
        
        # Traffic visualization
        chart_placeholder = st.empty()
        
        # Recent detections table
        st.subheader("📋 Recent Detections")
        table_placeholder = st.empty()
        
        # Real-time monitoring loop
        if st.session_state.monitoring_active:
            # Generate traffic
            traffic_df = generate_network_traffic(n_samples=5)
            
            # Preprocess and predict
            X = preprocess_for_prediction(traffic_df)
            predictions = model.predict(X)
            probabilities = model.predict_proba(X)
            
            # Map predictions to attack types
            class_names = ['dos', 'normal', 'probe', 'r2l', 'u2r']
            traffic_df['prediction'] = [class_names[p] if p < len(class_names) else 'unknown' for p in predictions]
            traffic_df['confidence'] = [max(prob) for prob in probabilities]
            
            # Create alerts for threats
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
            total_traffic = len(st.session_state.threat_log)
            threats = len([a for a in st.session_state.threat_log if a['type'] != 'normal'])
            normal = total_traffic - threats
            
            metric_total.metric("Total Traffic", total_traffic, delta=len(traffic_df))
            metric_threats.metric("Threats Detected", threats, delta=len([p for p in predictions if p != 1]))
            metric_normal.metric("Normal Traffic", normal)
            metric_blocked.metric("Blocked IPs", len(st.session_state.blocked_ips))
            
            # Display recent detections
            display_df = traffic_df[['timestamp', 'src_ip', 'dst_ip', 'prediction', 'confidence']].copy()
            display_df['confidence'] = display_df['confidence'].apply(lambda x: f"{x:.2%}")
            
            # Color code by threat level
            def highlight_threats(row):
                if row['prediction'] in ['dos', 'r2l', 'u2r']:
                    return ['background-color: #ff4444; color: white'] * len(row)
                elif row['prediction'] == 'probe':
                    return ['background-color: #ffaa00; color: white'] * len(row)
                else:
                    return ['background-color: #00C851; color: white'] * len(row)
            
            styled_df = display_df.style.apply(highlight_threats, axis=1)
            table_placeholder.dataframe(styled_df, use_container_width=True)
            
            # Auto-refresh
            time.sleep(monitoring_speed)
            st.rerun()

# Tab 2: Active Alerts
with tab2:
    st.header("🚨 Active Security Alerts")
    
    if not st.session_state.alerts:
        st.info("No active alerts. System is secure! 🛡️")
    else:
        # Filter options
        col1, col2 = st.columns(2)
        severity_filter = col1.multiselect(
            "Filter by Severity",
            ['CRITICAL', 'WARNING', 'INFO'],
            default=['CRITICAL', 'WARNING', 'INFO']
        )
        
        # Display alerts
        for alert in st.session_state.alerts:
            if alert['severity'] in severity_filter:
                severity_class = {
                    'CRITICAL': 'alert-critical',
                    'WARNING': 'alert-warning',
                    'INFO': 'alert-info'
                }.get(alert['severity'], 'alert-info')
                
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="{severity_class}">
                            <strong>{alert['severity']}</strong> - {ATTACK_INFO[alert['type']]['name']}<br>
                            <small>{alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</small><br>
                            Source: {alert['src_ip']} → Destination: {alert['dst_ip']}<br>
                            Confidence: {alert['confidence']:.2%}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button(f"🔍 Details", key=f"details_{alert['timestamp']}"):
                            st.info(f"**Description:** {alert['description']}")
                            st.write(f"**Mitigation Steps:**")
                            for step in ATTACK_INFO[alert['type']]['mitigation']:
                                st.write(f"- {step}")
                    
                    with col3:
                        if alert['src_ip'] not in st.session_state.blocked_ips:
                            if st.button(f"🚫 Block IP", key=f"block_{alert['timestamp']}"):
                                block_ip(alert['src_ip'])
                                st.rerun()

# Tab 3: Blocked IPs
with tab3:
    st.header("🔒 Blocked IP Addresses")
    
    if not st.session_state.blocked_ips:
        st.info("No IPs are currently blocked.")
    else:
        blocked_df = pd.DataFrame({
            'IP Address': list(st.session_state.blocked_ips),
            'Status': ['Blocked'] * len(st.session_state.blocked_ips),
            'Action': [''] * len(st.session_state.blocked_ips)
        })
        
        for idx, ip in enumerate(st.session_state.blocked_ips):
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.write(f"🚫 **{ip}**")
            col2.write("Status: Blocked")
            if col3.button(f"✅ Unblock", key=f"unblock_{ip}"):
                unblock_ip(ip)
                st.rerun()
    
    st.markdown("---")
    
    # Manual IP blocking
    st.subheader("Manual IP Management")
    col1, col2 = st.columns(2)
    with col1:
        manual_ip = st.text_input("Enter IP Address to Block")
        if st.button("Block IP"):
            if manual_ip:
                block_ip(manual_ip)
                st.rerun()

# Tab 4: Analytics
with tab4:
    st.header("📈 Security Analytics Dashboard")
    
    if st.session_state.threat_log:
        # Convert to dataframe
        log_df = pd.DataFrame(st.session_state.threat_log)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Attack type distribution
            attack_counts = log_df['type'].value_counts()
            fig = px.pie(
                values=attack_counts.values,
                names=attack_counts.index,
                title="Attack Type Distribution",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Severity distribution
            severity_counts = log_df['severity'].value_counts()
            fig = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                title="Severity Level Distribution",
                labels={'x': 'Severity', 'y': 'Count'},
                color=severity_counts.index,
                color_discrete_map={'CRITICAL': '#ff4444', 'WARNING': '#ffaa00', 'INFO': '#00C851'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Timeline
        st.subheader("Threat Timeline")
        log_df['hour'] = pd.to_datetime(log_df['timestamp']).dt.hour
        hourly_threats = log_df.groupby('hour').size().reset_index(name='count')
        
        fig = px.line(
            hourly_threats,
            x='hour',
            y='count',
            title="Threats Detected Over Time",
            labels={'hour': 'Hour of Day', 'count': 'Number of Threats'}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available yet. Start monitoring to collect analytics.")

# Tab 5: Threat Intelligence
with tab5:
    st.header("🛠️ Threat Intelligence & Mitigation")
    
    for attack_type, info in ATTACK_INFO.items():
        if attack_type != 'normal':
            with st.expander(f"{info['name']} - {info['severity']}"):
                st.markdown(f"**Description:** {info['description']}")
                st.markdown(f"**Severity Level:** `{info['severity']}`")
                st.markdown("**Recommended Mitigation Steps:**")
                for step in info['mitigation']:
                    st.write(f"✓ {step}")
                
                # Show recent occurrences
                if st.session_state.threat_log:
                    recent = [a for a in st.session_state.threat_log if a['type'] == attack_type]
                    if recent:
                        st.write(f"**Recent Occurrences:** {len(recent)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🛡️ TabNet-IDS Security Operations Center | Powered by TabNet Deep Learning</p>
    <p>Real-time Intrusion Detection with Explainable AI</p>
</div>
""", unsafe_allow_html=True)
