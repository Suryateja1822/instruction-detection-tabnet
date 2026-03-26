"""
User-Friendly Output Module for TabNet-IDS
Makes the system more understandable for non-technical customers
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

class UserFriendlyOutput:
    """Makes TabNet-IDS output more user-friendly"""
    
    def __init__(self):
        self.explanations = {
            'normal': {
                'title': '✅ Normal Network Activity',
                'description': 'Regular network traffic detected. No security threats found.',
                'color': '#10b981',
                'icon': '🟢',
                'action': 'Continue monitoring'
            },
            'dos': {
                'title': '🚨 DDoS Attack Detected',
                'description': 'Multiple computers are overwhelming your network with traffic, making it unavailable.',
                'color': '#dc2626',
                'icon': '🔴',
                'action': 'Block source IP immediately'
            },
            'probe': {
                'title': '🔍 Network Probe Detected',
                'description': 'Someone is scanning your network for vulnerabilities.',
                'color': '#f59e0b',
                'icon': '🟠',
                'action': 'Investigate source and update firewall'
            },
            'r2l': {
                'title': '⚠️ Remote Attack Detected',
                'description': 'Unauthorized access attempt from remote location detected.',
                'color': '#ea580c',
                'icon': '🟡',
                'action': 'Change compromised passwords immediately'
            },
            'u2r': {
                'title': '🚨 Privilege Escalation Detected',
                'description': 'User gained unauthorized administrator access.',
                'color': '#dc2626',
                'icon': '🔴',
                'action': 'Isolate affected system immediately'
            },
            'unknown': {
                'title': '❓ Suspicious Activity Detected',
                'description': 'Unusual network pattern detected. Manual review recommended.',
                'color': '#6b7280',
                'icon': '🟡',
                'action': 'Investigate network traffic patterns'
            }
        }
    
    def get_friendly_explanation(self, threat_type: str, confidence: float) -> dict:
        """Get user-friendly explanation for detected threat"""
        base_info = self.explanations.get(threat_type.lower(), self.explanations['unknown'])
        
        # Add confidence-based messaging
        if confidence > 0.9:
            certainty = "Very High"
            urgency = "IMMEDIATE"
        elif confidence > 0.7:
            certainty = "High"
            urgency = "URGENT"
        elif confidence > 0.5:
            certainty = "Medium"
            urgency = "ATTENTION"
        else:
            certainty = "Low"
            urgency = "MONITOR"
        
        # Create user-friendly response
        response = {
            'threat_type': threat_type,
            'title': base_info['title'],
            'description': base_info['description'],
            'color': base_info['color'],
            'icon': base_info['icon'],
            'action': base_info['action'],
            'confidence': confidence,
            'certainty': certainty,
            'urgency': urgency,
            'what_this_means': self._get_simple_explanation(threat_type),
            'what_to_do': self._get_action_plan(threat_type),
            'risk_level': self._get_risk_assessment(confidence)
        }
        
        return response
    
    def _get_simple_explanation(self, threat_type: str) -> str:
        """Get simple explanation of what the threat means"""
        explanations = {
            'dos': 'A DDoS attack is like thousands of cars trying to enter a highway at once, causing a traffic jam that blocks legitimate traffic.',
            'probe': 'Network probing is like someone trying all the doors and windows of your building to find an unlocked entrance.',
            'r2l': 'A remote-to-local attack is like a burglar breaking into your house from outside.',
            'u2r': 'A user-to-root attack is like a guest finding the master keys and taking control of your entire building.',
            'normal': 'Normal traffic is like regular customers entering and leaving your store normally.'
        }
        return explanations.get(threat_type.lower(), 'Unusual network activity that needs investigation.')
    
    def _get_action_plan(self, threat_type: str) -> str:
        """Get simple action plan for the threat"""
        actions = {
            'dos': '1. Block the attacking IP addresses\n2. Contact your internet provider\n3. Use traffic filtering services',
            'probe': '1. Check firewall logs\n2. Update security rules\n3. Monitor for repeated patterns',
            'r2l': '1. Change all user passwords\n2. Review access logs\n3. Scan for malware',
            'u2r': '1. Disconnect affected systems\n2. Review all user permissions\n3. Audit administrator accounts',
            'normal': 'Continue normal monitoring. No action needed.'
        }
        return actions.get(threat_type.lower(), 'Investigate the network activity and consult security team.')
    
    def _get_risk_assessment(self, confidence: float) -> str:
        """Get risk assessment based on confidence"""
        if confidence > 0.9:
            return "CRITICAL - Immediate action required"
        elif confidence > 0.7:
            return "HIGH - Action recommended within 1 hour"
        elif confidence > 0.5:
            return "MEDIUM - Monitor closely, investigate within 24 hours"
        else:
            return "LOW - Continue monitoring, investigate if pattern continues"
    
    def create_user_friendly_alert_card(self, alert_data: dict) -> str:
        """Create a user-friendly alert card"""
        explanation = self.get_friendly_explanation(
            alert_data.get('threat_type', 'unknown'),
            alert_data.get('confidence', 0.0)
        )
        
        return f"""
        <div style="background: {explanation['color']}; 
                   padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                   border: 3px solid rgba(255,255,255,0.2); box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-right: 1rem;">{explanation['icon']}</div>
                <div style="flex: 1;">
                    <div style="color: white; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem;">
                        {explanation['title']}
                    </div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 1rem; margin-bottom: 0.5rem;">
                        {explanation['description']}
                    </div>
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                    <div>
                        <div style="font-weight: 600; color: #333; margin-bottom: 0.3rem;">📊 Detection Confidence</div>
                        <div style="font-size: 1.2rem; color: {explanation['color']}; font-weight: 700;">
                            {explanation['certainty']} ({alert_data.get('confidence', 0):.1%})
                        </div>
                    </div>
                    <div>
                        <div style="font-weight: 600; color: #333; margin-bottom: 0.3rem;">⚡ Urgency Level</div>
                        <div style="font-size: 1.1rem; color: {explanation['color']}; font-weight: 600;">
                            {explanation['urgency']}
                        </div>
                    </div>
                </div>
                
                <div style="margin-bottom: 1rem;">
                    <div style="font-weight: 600; color: #333; margin-bottom: 0.3rem;">🎯 What This Means</div>
                    <div style="background: rgba(255,255,255,0.8); padding: 0.8rem; border-radius: 8px; font-size: 0.95rem;">
                        {explanation['what_this_means']}
                    </div>
                </div>
                
                <div style="margin-bottom: 1rem;">
                    <div style="font-weight: 600; color: #333; margin-bottom: 0.3rem;">🛡️ What To Do</div>
                    <div style="background: rgba(255,255,255,0.8); padding: 0.8rem; border-radius: 8px; font-size: 0.95rem;">
                        {explanation['what_to_do']}
                    </div>
                </div>
                
                <div style="margin-bottom: 1rem;">
                    <div style="font-weight: 600; color: #333; margin-bottom: 0.3rem;">⚠️ Risk Assessment</div>
                    <div style="background: rgba(255,255,255,0.8); padding: 0.8rem; border-radius: 8px; font-size: 0.95rem; font-weight: 600; color: {explanation['color']};">
                        {explanation['risk_level']}
                    </div>
                </div>
            </div>
        </div>
        """
    
    def create_simple_status_dashboard(self, monitoring_data: pd.DataFrame) -> str:
        """Create a simple, easy-to-understand status dashboard"""
        if len(monitoring_data) == 0:
            return """
            <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
                <div style="font-size: 1.5rem; margin-bottom: 1rem;">🔍</div>
                <div style="font-size: 1.2rem; color: #666; margin-bottom: 1rem;">No network activity detected</div>
                <div style="font-size: 1rem; color: #999;">Start monitoring to see network activity</div>
            </div>
            """
        
        # Count different types of activity
        total_events = len(monitoring_data)
        if 'threat_level' in monitoring_data.columns:
            threat_counts = monitoring_data['threat_level'].value_counts()
            normal_count = threat_counts.get('Normal', 0)
            threat_count = total_events - normal_count
        else:
            threat_count = 0
            normal_count = total_events
        
        # Create status message
        if threat_count > 0:
            status_color = '#dc2626'
            status_icon = '🚨'
            status_text = f'{threat_count} threat(s) detected'
            status_detail = 'Security alerts require attention'
        else:
            status_color = '#10b981'
            status_icon = '✅'
            status_text = 'Network operating normally'
            status_detail = f'{normal_count} normal activities monitored'
        
        return f"""
        <div style="background: {status_color}; color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{status_icon}</div>
            <div style="font-size: 1.3rem; font-weight: 700;">{status_text}</div>
            <div style="font-size: 1rem; opacity: 0.9;">{status_detail}</div>
        </div>
        """
    
    def create_traffic_summary_chart(self, monitoring_data: pd.DataFrame) -> str:
        """Create a simple traffic summary chart"""
        if len(monitoring_data) == 0:
            return ""
        
        # Create simple summary
        summary_data = {
            'Time': ['Last 5 min', 'Last 10 min', 'Last 30 min'],
            'Normal Traffic': [0, 0, 0],
            'Suspicious': [0, 0, 0],
            'Threats': [0, 0, 0]
        }
        
        # Simulate some data for demonstration
        import numpy as np
        summary_data['Normal Traffic'] = np.random.randint(50, 100, 3)
        summary_data['Suspicious'] = np.random.randint(5, 15, 3)
        summary_data['Threats'] = np.random.randint(1, 5, 3)
        
        df_summary = pd.DataFrame(summary_data)
        
        fig = px.bar(
            df_summary,
            x='Time',
            y=['Normal Traffic', 'Suspicious', 'Threats'],
            title='Network Activity Summary',
            color_discrete_map=['Normal Traffic', 'Suspicious', 'Threats'],
            color_continuous_scale=['#10b981', '#f59e0b', '#dc2626']
        )
        
        fig.update_layout(
            showlegend=True,
            height=300,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id="traffic-summary-chart")

# Streamlit helper functions
def display_user_friendly_dashboard(monitoring_data: pd.DataFrame):
    """Display user-friendly dashboard in Streamlit"""
    friendly_output = UserFriendlyOutput()
    
    st.markdown("### 📊 Network Status Overview")
    
    # Status card
    status_html = friendly_output.create_simple_status_dashboard(monitoring_data)
    st.markdown(status_html, unsafe_allow_html=True)
    
    # Traffic summary chart
    if len(monitoring_data) > 0:
        st.markdown("### 📈 Activity Summary")
        chart_html = friendly_output.create_traffic_summary_chart(monitoring_data)
        st.markdown(chart_html, unsafe_allow_html=True)
    
    # Recent activity in simple terms
    st.markdown("### 📋 Recent Activity")
    if len(monitoring_data) > 0:
        recent_data = monitoring_data.tail(5).copy()
        
        # Make it more readable
        if 'threat_level' in recent_data.columns:
            recent_data['Status'] = recent_data['threat_level'].apply(
                lambda x: '🚨 THREAT' if x != 'Normal' else '✅ OK'
            )
            
            # Display in user-friendly format
            for _, row in recent_data.iterrows():
                status_emoji = '🚨' if row['threat_level'] != 'Normal' else '✅'
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid {'#dc2626' if row['threat_level'] != 'Normal' else '#10b981'};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-weight: 600;">{status_emoji} {row['threat_level']}</div>
                        <div style="text-align: right; color: #666; font-size: 0.9rem;">
                            From: {row.get('source_ip', 'Unknown')}<br>
                            Time: {row.get('timestamp', 'Unknown')}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📋 No recent activity to display")

def display_user_friendly_alerts(alerts_list: list):
    """Display alerts in user-friendly format"""
    if not alerts_list:
        return
    
    friendly_output = UserFriendlyOutput()
    
    st.markdown("### 🚨 Security Alerts")
    
    for alert in alerts_list[-3:]:  # Show last 3 alerts
        alert_card = friendly_output.create_user_friendly_alert_card(alert)
        st.markdown(alert_card, unsafe_allow_html=True)
        
        # Add separator between alerts
        st.markdown("---")

def create_simple_explanation_guide():
    """Create a simple explanation guide for users"""
    guide = """
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: #333; margin-bottom: 1rem;">📖 Understanding Your Network Security</h3>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem;">
            <div>
                <h4 style="color: #10b981;">✅ Normal Activity</h4>
                <p style="color: #666; line-height: 1.5;">
                    Regular network traffic like users visiting websites, sending emails, or using applications normally. 
                    No action needed - this is good traffic!
                </p>
            </div>
            
            <div>
                <h4 style="color: #f59e0b;">🔍 Suspicious Activity</h4>
                <p style="color: #666; line-height: 1.5;">
                    Unusual patterns that might indicate someone probing your network for weaknesses. 
                    Like someone trying different doors to see if they're unlocked.
                </p>
            </div>
            
            <div>
                <h4 style="color: #dc2626;">🚨 Threats Detected</h4>
                <p style="color: #666; line-height: 1.5;">
                    Actual attacks or confirmed security breaches that need immediate attention. 
                    Like someone actually breaking into your systems.
                </p>
            </div>
        </div>
        
        <div style="background: #e3f2fd; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <h4 style="color: #333;">💡 What the Colors Mean</h4>
            <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 150px;">
                    <div style="background: #10b981; color: white; padding: 0.5rem; border-radius: 5px; text-align: center; margin-bottom: 0.5rem;">✅</div>
                    <div style="font-weight: 600;">Normal</div>
                </div>
                <div style="flex: 1; min-width: 150px;">
                    <div style="background: #f59e0b; color: white; padding: 0.5rem; border-radius: 5px; text-align: center; margin-bottom: 0.5rem;">🔍</div>
                    <div style="font-weight: 600;">Suspicious</div>
                </div>
                <div style="flex: 1; min-width: 150px;">
                    <div style="background: #dc2626; color: white; padding: 0.5rem; border-radius: 5px; text-align: center; margin-bottom: 0.5rem;">🚨</div>
                    <div style="font-weight: 600;">Threat</div>
                </div>
            </div>
        </div>
    """
    
    return guide
