"""
Real-time Network Traffic Monitor for TabNet-IDS
Provides continuous monitoring and live threat detection capabilities
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import threading
import queue
import json
from typing import Dict, List, Optional, Tuple
import random
from dataclasses import dataclass
import asyncio
from collections import deque

@dataclass
class NetworkEvent:
    """Represents a network traffic event"""
    timestamp: datetime
    source_ip: str
    dest_ip: str
    protocol: str
    port: int
    bytes_sent: int
    bytes_received: int
    duration: float
    flags: str
    packet_count: int
    features: Dict[str, float]

class RealTimeMonitor:
    """Real-time network traffic monitoring system"""
    
    def __init__(self, model=None, buffer_size=1000):
        """
        Initialize the real-time monitor
        
        Args:
            model: Trained TabNet model for threat detection
            buffer_size: Size of the event buffer
        """
        self.model = model
        self.buffer_size = buffer_size
        self.event_queue = queue.Queue()
        self.event_buffer = deque(maxlen=buffer_size)
        self.alert_queue = queue.Queue()
        self.monitoring_active = False
        self.stats = {
            'total_events': 0,
            'threats_detected': 0,
            'last_update': datetime.now(),
            'alerts': []
        }
        
    def start_monitoring(self):
        """Start the real-time monitoring thread"""
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop the real-time monitoring"""
        self.monitoring_active = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=5)
            
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Generate simulated network events
                event = self._generate_network_event()
                
                # Add to queue and buffer
                self.event_queue.put(event)
                self.event_buffer.append(event)
                
                # Analyze event for threats
                self._analyze_event(event)
                
                # Update statistics
                self.stats['total_events'] += 1
                self.stats['last_update'] = datetime.now()
                
                # Sleep to control event generation rate
                time.sleep(random.uniform(0.1, 0.5))
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(1)
                
    def _generate_network_event(self) -> NetworkEvent:
        """Generate a simulated network event"""
        # Simulate different types of network traffic
        protocols = ['TCP', 'UDP', 'ICMP']
        flags = ['SF', 'S0', 'REJ', 'RSTR', 'RSTO', 'SH']
        
        # Generate random IP addresses
        source_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
        dest_ip = f"10.0.{random.randint(0, 255)}.{random.randint(1, 254)}"
        
        # Generate features for ML model
        features = {
            'duration': random.uniform(0, 1000),
            'src_bytes': random.randint(0, 100000),
            'dst_bytes': random.randint(0, 100000),
            'wrong_fragment': random.randint(0, 3),
            'urgent': random.randint(0, 3),
            'hot': random.randint(0, 100),
            'num_failed_logins': random.randint(0, 5),
            'logged_in': random.randint(0, 1),
            'num_compromised': random.randint(0, 50),
            'count': random.randint(0, 100),
            'srv_count': random.randint(0, 100),
            'serror_rate': random.uniform(0, 1),
            'srv_serror_rate': random.uniform(0, 1),
            'rerror_rate': random.uniform(0, 1),
            'same_srv_rate': random.uniform(0, 1),
            'diff_srv_rate': random.uniform(0, 1)
        }
        
        # Occasionally generate threat events
        if random.random() < 0.1:  # 10% chance of threat
            threat_type = random.choice(['dos', 'probe', 'r2l', 'u2r'])
            features = self._modify_features_for_threat(features, threat_type)
        
        return NetworkEvent(
            timestamp=datetime.now(),
            source_ip=source_ip,
            dest_ip=dest_ip,
            protocol=random.choice(protocols),
            port=random.randint(1, 65535),
            bytes_sent=features['src_bytes'],
            bytes_received=features['dst_bytes'],
            duration=features['duration'],
            flags=random.choice(flags),
            packet_count=random.randint(1, 100),
            features=features
        )
        
    def _modify_features_for_threat(self, features: Dict[str, float], threat_type: str) -> Dict[str, float]:
        """Modify features to simulate specific threat types"""
        modified = features.copy()
        
        if threat_type == 'dos':
            # DOS attacks: high duration, many bytes, failed connections
            modified['duration'] *= 10
            modified['src_bytes'] *= 5
            modified['serror_rate'] = random.uniform(0.5, 1.0)
            modified['count'] = random.randint(50, 100)
            
        elif threat_type == 'probe':
            # Probe attacks: many connection attempts, low bytes
            modified['count'] = random.randint(80, 100)
            modified['srv_count'] = random.randint(80, 100)
            modified['src_bytes'] //= 10
            modified['dst_bytes'] //= 10
            
        elif threat_type == 'r2l':
            # Remote to local: failed logins, compromised systems
            modified['num_failed_logins'] = random.randint(3, 5)
            modified['num_compromised'] = random.randint(10, 30)
            modified['logged_in'] = 1
            
        elif threat_type == 'u2r':
            # User to root: logged in users, compromised systems
            modified['logged_in'] = 1
            modified['num_compromised'] = random.randint(5, 20)
            modified['hot'] = random.randint(50, 100)
            
        return modified
        
    def _analyze_event(self, event: NetworkEvent):
        """Analyze a network event for threats"""
        try:
            if self.model is not None:
                # Prepare features for prediction
                feature_values = list(event.features.values())
                
                # Ensure correct number of features
                if len(feature_values) < 25:
                    feature_values.extend([0] * (25 - len(feature_values)))
                elif len(feature_values) > 25:
                    feature_values = feature_values[:25]
                    
                # Make prediction
                prediction = self.model.predict([feature_values])[0]
                confidence = max(self.model.predict_proba([feature_values])[0])
                
                # Map prediction to attack type
                class_names = ['dos', 'normal', 'probe', 'r2l', 'u2r']
                predicted_class = class_names[prediction] if prediction < len(class_names) else 'unknown'
                
                # If threat detected, create alert
                if predicted_class != 'normal' and confidence > 0.7:
                    alert = {
                        'timestamp': event.timestamp,
                        'threat_type': predicted_class,
                        'confidence': confidence,
                        'source_ip': event.source_ip,
                        'dest_ip': event.dest_ip,
                        'port': event.port,
                        'severity': self._get_severity(predicted_class),
                        'description': self._get_threat_description(predicted_class)
                    }
                    
                    self.alert_queue.put(alert)
                    self.stats['threats_detected'] += 1
                    self.stats['alerts'].append(alert)
                    
                    # Keep only recent alerts (last 100)
                    if len(self.stats['alerts']) > 100:
                        self.stats['alerts'] = self.stats['alerts'][-100:]
                        
        except Exception as e:
            print(f"Error analyzing event: {e}")
            
    def _get_severity(self, threat_type: str) -> str:
        """Get severity level for threat type"""
        severity_map = {
            'dos': 'CRITICAL',
            'probe': 'MEDIUM',
            'r2l': 'HIGH',
            'u2r': 'CRITICAL',
            'unknown': 'MEDIUM'
        }
        return severity_map.get(threat_type, 'LOW')
        
    def _get_threat_description(self, threat_type: str) -> str:
        """Get description for threat type"""
        descriptions = {
            'dos': 'Denial of Service attack detected',
            'probe': 'Network probe/scanning activity detected',
            'r2l': 'Remote to Local attack detected',
            'u2r': 'User to Root privilege escalation detected',
            'unknown': 'Suspicious activity detected'
        }
        return descriptions.get(threat_type, 'Unknown threat detected')
        
    def get_recent_events(self, count: int = 50) -> List[NetworkEvent]:
        """Get recent network events"""
        return list(self.event_buffer)[-count:]
        
    def get_recent_alerts(self, count: int = 20) -> List[Dict]:
        """Get recent security alerts"""
        return self.stats['alerts'][-count:]
        
    def get_statistics(self) -> Dict:
        """Get current monitoring statistics"""
        return self.stats.copy()
        
    def get_traffic_metrics(self, time_window: int = 60) -> Dict:
        """
        Get traffic metrics for the last time_window seconds
        
        Args:
            time_window: Time window in seconds
            
        Returns:
            Dictionary with traffic metrics
        """
        cutoff_time = datetime.now() - timedelta(seconds=time_window)
        recent_events = [e for e in self.event_buffer if e.timestamp > cutoff_time]
        
        if not recent_events:
            return {
                'events_per_second': 0,
                'bytes_per_second': 0,
                'unique_sources': 0,
                'unique_destinations': 0,
                'protocol_distribution': {}
            }
            
        # Calculate metrics
        events_per_second = len(recent_events) / time_window
        total_bytes = sum(e.bytes_sent + e.bytes_received for e in recent_events)
        bytes_per_second = total_bytes / time_window
        
        unique_sources = len(set(e.source_ip for e in recent_events))
        unique_destinations = len(set(e.dest_ip for e in recent_events))
        
        # Protocol distribution
        protocol_counts = {}
        for event in recent_events:
            protocol_counts[event.protocol] = protocol_counts.get(event.protocol, 0) + 1
            
        return {
            'events_per_second': events_per_second,
            'bytes_per_second': bytes_per_second,
            'unique_sources': unique_sources,
            'unique_destinations': unique_destinations,
            'protocol_distribution': protocol_counts
        }

def create_real_time_dashboard(monitor: RealTimeMonitor):
    """Create the real-time monitoring dashboard"""
    st.markdown("### 🔄 REAL-TIME NETWORK MONITORING")
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("▶️ Start Monitoring", key="start_monitor"):
            monitor.start_monitoring()
            st.success("Monitoring started!")
            
    with col2:
        if st.button("⏸️ Stop Monitoring", key="stop_monitor"):
            monitor.stop_monitoring()
            st.warning("Monitoring stopped!")
            
    with col3:
        if st.button("🔄 Clear Data", key="clear_monitor"):
            monitor.event_buffer.clear()
            monitor.stats['alerts'] = []
            st.info("Data cleared!")
    
    # Status indicator
    status_color = "🟢" if monitor.monitoring_active else "🔴"
    st.markdown(f"**Status:** {status_color} {'Active' if monitor.monitoring_active else 'Inactive'}")
    
    # Main metrics
    stats = monitor.get_statistics()
    metrics = monitor.get_traffic_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Events", stats['total_events'])
        
    with col2:
        st.metric("Threats Detected", stats['threats_detected'])
        
    with col3:
        st.metric("Events/sec", f"{metrics['events_per_second']:.1f}")
        
    with col4:
        st.metric("Bytes/sec", f"{metrics['bytes_per_second']:.0f}")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Protocol distribution chart
        if metrics['protocol_distribution']:
            protocol_df = pd.DataFrame(
                list(metrics['protocol_distribution'].items()),
                columns=['Protocol', 'Count']
            )
            fig = px.pie(
                protocol_df,
                values='Count',
                names='Protocol',
                title='Protocol Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No protocol data available")
            
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
        else:
            st.info("No recent alerts")
    
    # Recent alerts table
    st.markdown("### 🚨 Recent Security Alerts")
    recent_alerts = monitor.get_recent_alerts(10)
    
    if recent_alerts:
        alerts_df = pd.DataFrame(recent_alerts)
        alerts_df['timestamp'] = alerts_df['timestamp'].dt.strftime('%H:%M:%S')
        
        # Style the dataframe
        def highlight_severity(val):
            color_map = {
                'CRITICAL': 'background-color: #ffcccc',
                'HIGH': 'background-color: #fff3cd',
                'MEDIUM': 'background-color: #d1ecf1',
                'LOW': 'background-color: #d4edda'
            }
            return color_map.get(val, '')
            
        styled_df = alerts_df.style.applymap(
            highlight_severity,
            subset=['severity']
        )
        
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("No security alerts detected")
    
    # Auto-refresh
    if monitor.monitoring_active:
        st.rerun()

# Example usage
if __name__ == "__main__":
    # This would be integrated into the main Streamlit app
    monitor = RealTimeMonitor()
    create_real_time_dashboard(monitor)
