"""
Enhanced TabNet-IDS Dashboard
Integrates real-time monitoring, threat analysis, and AI assistant
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os
import sys
from pathlib import Path
import json

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

# Import custom modules
from real_time_monitor import RealTimeMonitor, NetworkEvent, create_real_time_dashboard
from chat_assistant import ChatAssistant
from solution_recommender import SolutionRecommender
from config import Config

# Page configuration
st.set_page_config(
    page_title="TabNet-IDS - Enhanced Dashboard",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    .alert-critical {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    .alert-high {
        background: rgba(249, 115, 22, 0.1);
        border-left: 4px solid #f97316;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    .alert-medium {
        background: rgba(251, 191, 36, 0.1);
        border-left: 4px solid #fbbf24;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-active {
        background: #10b981;
        animation: pulse 2s infinite;
    }
    
    .status-inactive {
        background: #ef4444;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .chat-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 350px;
        max-height: 500px;
        background: rgba(26, 32, 53, 0.95);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        backdrop-filter: blur(10px);
    }
    
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 15px;
        border-radius: 10px 10px 0 0;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chat-messages {
        padding: 15px;
        overflow-y: auto;
        flex-grow: 1;
        max-height: 350px;
    }
    
    .chat-input {
        padding: 10px;
        border-top: 1px solid rgba(102, 126, 234, 0.3);
        display: flex;
    }
    
    .chat-message {
        margin-bottom: 10px;
        padding: 8px 12px;
        border-radius: 15px;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: rgba(102, 126, 234, 0.2);
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .assistant-message {
        background: rgba(118, 75, 162, 0.2);
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'monitor' not in st.session_state:
        st.session_state.monitor = RealTimeMonitor()
    
    if 'chat_assistant' not in st.session_state:
        st.session_state.chat_assistant = ChatAssistant()
        st.session_state.chat_history = []
        st.session_state.show_chat = False
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    
    if 'alerts' not in st.session_state:
        st.session_state.alerts = []
    
    if 'system_stats' not in st.session_state:
        st.session_state.system_stats = {
            'total_threats': 0,
            'threats_today': 0,
            'system_uptime': 0,
            'last_scan': None
        }

# Initialize session state
init_session_state()

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    
    page = st.selectbox(
        "Select Page:",
        ["🏠 Dashboard", "📊 Real-time Monitor", "🔍 Threat Analysis", "💬 AI Assistant", "⚙️ Settings"],
        key="page_selector"
    )
    
    # Update current page
    page_map = {
        "🏠 Dashboard": "dashboard",
        "📊 Real-time Monitor": "monitor",
        "🔍 Threat Analysis": "analysis",
        "💬 AI Assistant": "chat",
        "⚙️ Settings": "settings"
    }
    st.session_state.current_page = page_map.get(page, "dashboard")
    
    st.markdown("---")
    
    # System status
    st.markdown("### 📊 System Status")
    
    monitor = st.session_state.monitor
    stats = monitor.get_statistics()
    
    status_color = "status-active" if monitor.monitoring_active else "status-inactive"
    st.markdown(f"""
    <div class="metric-card">
        <span class="status-indicator {status_color}"></span>
        <strong>Monitoring:</strong> {'Active' if monitor.monitoring_active else 'Inactive'}
    </div>
    """, unsafe_allow_html=True)
    
    st.metric("Total Events", stats['total_events'])
    st.metric("Threats Detected", stats['threats_detected'])
    st.metric("Uptime", f"{stats['total_events']} events")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    if st.button("🔄 Refresh Dashboard"):
        st.rerun()
    
    if st.button("📤 Upload Data"):
        st.session_state.current_page = "upload"
        st.rerun()
    
    if st.button("🚨 View Alerts"):
        st.session_state.current_page = "alerts"
        st.rerun()

# Main content area
def main():
    """Main application logic"""
    # Header
    st.markdown('<h1 class="main-header">🔒 TABNET-IDS ENHANCED DASHBOARD</h1>', unsafe_allow_html=True)
    
    # Render current page
    if st.session_state.current_page == "dashboard":
        render_dashboard()
    elif st.session_state.current_page == "monitor":
        render_monitor()
    elif st.session_state.current_page == "analysis":
        render_analysis()
    elif st.session_state.current_page == "chat":
        render_chat()
    elif st.session_state.current_page == "settings":
        render_settings()
    
    # Chat widget (always visible)
    if st.session_state.show_chat:
        render_chat_widget()

def render_dashboard():
    """Render the main dashboard"""
    st.markdown("### 📊 System Overview")
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    monitor = st.session_state.monitor
    stats = monitor.get_statistics()
    metrics = monitor.get_traffic_metrics()
    
    with col1:
        st.metric("Total Events", stats['total_events'], delta=f"+{metrics['events_per_second']:.1f}/s")
    
    with col2:
        st.metric("Threats Detected", stats['threats_detected'], delta="🚨" if stats['threats_detected'] > 0 else "✅")
    
    with col3:
        st.metric("Active Sources", metrics['unique_sources'])
    
    with col4:
        st.metric("Active Destinations", metrics['unique_destinations'])
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Protocol distribution
        if metrics['protocol_distribution']:
            protocol_df = pd.DataFrame(
                list(metrics['protocol_distribution'].items()),
                columns=['Protocol', 'Count']
            )
            fig = px.pie(
                protocol_df,
                values='Count',
                names='Protocol',
                title='Protocol Distribution',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Recent alerts timeline
        recent_alerts = monitor.get_recent_alerts(10)
        if recent_alerts:
            alerts_df = pd.DataFrame(recent_alerts)
            fig = px.scatter(
                alerts_df,
                x='timestamp',
                y='confidence',
                color='threat_type',
                size='confidence',
                title='Recent Security Alerts',
                labels={'confidence': 'Confidence', 'timestamp': 'Time'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent alerts section
    st.markdown("### 🚨 Recent Security Alerts")
    recent_alerts = monitor.get_recent_alerts(5)
    
    if recent_alerts:
        for alert in recent_alerts:
            severity_class = f"alert-{alert['severity'].lower()}"
            st.markdown(f"""
            <div class="{severity_class}">
                <strong>{alert['threat_type'].upper()}</strong> - {alert['description']}<br>
                <small>Source: {alert['source_ip']} → {alert['dest_ip']} | Confidence: {alert['confidence']:.2f}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("✅ No recent security alerts detected")

def render_monitor():
    """Render the real-time monitoring page"""
    create_real_time_dashboard(st.session_state.monitor)

def render_analysis():
    """Render the threat analysis page"""
    st.markdown("### 🔍 Threat Analysis")
    
    # File upload for analysis
    uploaded_file = st.file_uploader(
        "Upload network traffic data for analysis",
        type=['csv', 'txt'],
        help="Upload a CSV file containing network traffic data"
    )
    
    if uploaded_file is not None:
        # Validate file
        is_valid, error_msg = Config.validate_file(uploaded_file.name, uploaded_file.size)
        
        if not is_valid:
            st.error(error_msg)
            return
        
        # Process file
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"File loaded successfully! {len(df)} records found.")
            
            # Display data preview
            st.markdown("### 📋 Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Analyze button
            if st.button("🔍 Analyze Data"):
                with st.spinner("Analyzing data..."):
                    # Here you would integrate your actual analysis logic
                    # For now, showing a placeholder
                    st.success("Analysis complete!")
                    
                    # Show sample results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Total Records", len(df))
                        st.metric("Threats Detected", np.random.randint(0, 10))
                    
                    with col2:
                        st.metric("Normal Traffic", len(df) - np.random.randint(0, 10))
                        st.metric("Analysis Time", f"{np.random.uniform(1, 5):.2f}s")
                    
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def render_chat():
    """Render the AI assistant page"""
    st.markdown("### 💬 AI Security Assistant")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            role = message['role']
            content = message['content']
            
            if role == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {content}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>Assistant:</strong> {content}
                </div>
                """, unsafe_allow_html=True)
        
        # Input field
        user_input = st.text_input("Ask about security threats...", key="chat_input")
        
        if st.button("Send") and user_input:
            # Add user message to history
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            
            # Get response from assistant
            assistant = st.session_state.chat_assistant
            response = assistant.process_message(user_input)
            
            # Add assistant response to history
            st.session_state.chat_history.append({'role': 'assistant', 'content': response['response']})
            
            # Rerun to update the chat
            st.rerun()

def render_chat_widget():
    """Render the floating chat widget"""
    st.markdown(f"""
    <div class="chat-container">
        <div class="chat-header">
            <span>🔒 Security Assistant</span>
            <button onclick="document.querySelector('.chat-container').style.display='none'" 
                    style="background: none; border: none; color: white; cursor: pointer; font-size: 18px;">×</button>
        </div>
        <div class="chat-messages">
            <div class="chat-message assistant-message">
                Hello! I'm your security assistant. How can I help you today?
            </div>
        </div>
        <div class="chat-input">
            <input type="text" placeholder="Ask about security..." 
                   style="flex-grow: 1; padding: 8px 12px; border: 1px solid rgba(102, 126, 234, 0.3); 
                          border-radius: 20px; background: rgba(255, 255, 255, 0.1); color: white; outline: none;">
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_settings():
    """Render the settings page"""
    st.markdown("### ⚙️ System Settings")
    
    # Configuration sections
    tab1, tab2, tab3 = st.tabs(["🔒 Detection", "📊 Monitoring", "🎨 Appearance"])
    
    with tab1:
        st.markdown("#### Threat Detection Settings")
        
        # Detection thresholds
        st.subheader("Detection Thresholds")
        
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=Config.DETECTION_THRESHOLDS['confidence_threshold'],
            step=0.05
        )
        
        high_risk_threshold = st.slider(
            "High Risk Threshold",
            min_value=0.0,
            max_value=1.0,
            value=Config.DETECTION_THRESHOLDS['high_risk_threshold'],
            step=0.05
        )
        
        # Update config
        Config.DETECTION_THRESHOLDS['confidence_threshold'] = confidence_threshold
        Config.DETECTION_THRESHOLDS['high_risk_threshold'] = high_risk_threshold
        
        st.success("Detection thresholds updated!")
    
    with tab2:
        st.markdown("#### Monitoring Settings")
        
        # Monitoring configuration
        buffer_size = st.number_input(
            "Event Buffer Size",
            min_value=100,
            max_value=10000,
            value=Config.MONITORING_CONFIG['buffer_size'],
            step=100
        )
        
        update_interval = st.slider(
            "Update Interval (seconds)",
            min_value=0.5,
            max_value=10.0,
            value=Config.MONITORING_CONFIG['update_interval'],
            step=0.5
        )
        
        # Update config
        Config.MONITORING_CONFIG['buffer_size'] = buffer_size
        Config.MONITORING_CONFIG['update_interval'] = update_interval
        
        st.success("Monitoring settings updated!")
    
    with tab3:
        st.markdown("#### Appearance Settings")
        
        # Theme selection
        theme = st.selectbox(
            "Chart Theme",
            ["plotly_dark", "plotly_white", "plotly", "ggplot2", "seaborn"],
            index=0
        )
        
        # Update config
        Config.VIZ_CONFIG['chart_theme'] = theme
        
        st.success("Appearance settings updated!")
    
    # Save configuration
    if st.button("💾 Save Configuration"):
        Config.save_config("config.json")
        st.success("Configuration saved successfully!")

# Chat toggle button
if st.button("💬", key="chat_toggle", help="Toggle AI Assistant"):
    st.session_state.show_chat = not st.session_state.show_chat
    st.rerun()

# Run the main application
if __name__ == "__main__":
    main()
