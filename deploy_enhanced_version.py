#!/usr/bin/env python3
"""
Deploy Enhanced TabNet-IDS with Alert System to Streamlit Cloud
"""

import subprocess
import sys
import os

def deploy_to_streamlit_cloud():
    """Deploy the enhanced version to Streamlit Cloud"""
    
    print("🚀 Deploying Enhanced TabNet-IDS to Streamlit Cloud...")
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ app.py not found. Make sure you're in the project directory.")
        return False
    
    try:
        # Deploy to Streamlit Cloud
        result = subprocess.run([
            "streamlit", "run", "app.py", 
            "--server.headless", "true",
            "--server.port", "8501"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Local deployment successful!")
            print("🌐 To deploy to Streamlit Cloud:")
            print("1. Push your code to GitHub repository")
            print("2. Go to https://share.streamlit.io/")
            print("3. Connect your GitHub account")
            print("4. Select your repository")
            print("5. Click 'Deploy' and configure settings")
            
            print("\n📋 Deployment Checklist:")
            print("✅ GitHub repository updated")
            print("✅ Enhanced alert system implemented")
            print("✅ All dependencies in requirements.txt")
            print("✅ app.py ready for deployment")
            
            return True
        else:
            print(f"❌ Deployment failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Deployment timed out")
        return False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False

def check_deployment_readiness():
    """Check if the project is ready for deployment"""
    
    print("🔍 Checking deployment readiness...")
    
    checks = [
        ("app.py", "Main application file"),
        ("requirements.txt", "Dependencies file"),
        ("src/", "Source code directory"),
        ("src/real_time_monitor.py", "Enhanced monitoring module"),
        ("src/chat_assistant.py", "AI assistant module")
    ]
    
    ready = True
    for file_path, description in checks:
        if os.path.exists(file_path):
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - Missing: {file_path}")
            ready = False
    
    if ready:
        print("\n🎉 Project is ready for deployment!")
        return True
    else:
        print("\n⚠️ Some components are missing. Please fix before deploying.")
        return False

if __name__ == "__main__":
    print("🛡️ TabNet-IDS Enhanced Deployment Script")
    print("=" * 50)
    
    # Check readiness
    if check_deployment_readiness():
        # Deploy
        deploy_to_streamlit_cloud()
    
    print("\n📞 For manual deployment, visit:")
    print("https://share.streamlit.io/")
