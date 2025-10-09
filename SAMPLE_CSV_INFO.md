# 📄 Sample CSV File Information

## 📁 File Created: `sample_upload_data.csv`

### ✅ What's Inside

**100 network traffic packets** with realistic data including:
- ✅ Normal HTTP traffic
- ✅ DoS attacks (ICMP flooding)
- ✅ Probe attacks (port scanning)
- ✅ Suspicious connections (S0 flags)
- ✅ Failed login attempts

---

## 📊 CSV Structure

### **Columns (21 total):**

#### **Numeric Features (16):**
1. `duration` - Connection duration in seconds
2. `src_bytes` - Bytes sent from source
3. `dst_bytes` - Bytes sent to destination
4. `wrong_fragment` - Number of wrong fragments
5. `urgent` - Number of urgent packets
6. `hot` - Number of "hot" indicators
7. `num_failed_logins` - Failed login attempts
8. `logged_in` - Successfully logged in (1/0)
9. `num_compromised` - Number of compromised conditions
10. `count` - Number of connections to same host
11. `srv_count` - Number of connections to same service
12. `serror_rate` - SYN error rate
13. `srv_serror_rate` - Service SYN error rate
14. `rerror_rate` - REJ error rate
15. `same_srv_rate` - Same service rate
16. `diff_srv_rate` - Different service rate

#### **Categorical Features (5):**
17. `src_ip` - Source IP address
18. `dst_ip` - Destination IP address
19. `protocol_type` - Protocol (tcp, udp, icmp)
20. `service` - Network service (http, ftp, smtp, etc.)
21. `flag` - Connection status flag (SF, S0, REJ)

---

## 🎯 Attack Patterns Included

### **1. Normal Traffic (~60%)**
- HTTP connections with SF flag
- FTP data transfers
- Legitimate services
- Example: Row 1, 3, 5, 7, 9...

### **2. DoS Attacks (~25%)**
- ICMP echo flooding
- High connection counts (254, 511)
- High error rates (0.88-1.0)
- Example: Rows 4, 6, 9, 11, 16...

### **3. Probe Attacks (~10%)**
- Port scanning attempts
- S0 flag (connection attempt, no reply)
- Low duration (30 seconds)
- Example: Rows 7, 18, 24, 32...

### **4. Suspicious Activity (~5%)**
- Failed login attempts
- Telnet with S0 flag
- Compromised indicators
- Example: Rows 24, 40, 54, 80...

---

## 🚀 How to Use This File

### **Step 1: Train Model**
```powershell
python src/train_ids.py
```

### **Step 2: Launch Upload Dashboard**
```powershell
python -m streamlit run app_with_upload.py
```

### **Step 3: Upload the CSV**
1. Click **"Browse files"**
2. Select **`sample_upload_data.csv`**
3. Click **"🔍 ANALYZE DATA"**

### **Step 4: View Results**
- See 100 packets analyzed
- ~25-30 threats detected
- DoS and Probe attacks identified
- Download full report

---

## 📊 Expected Results

### **Metrics:**
- **Total Packets:** 100
- **Threats:** ~25-35
- **Normal:** ~65-75
- **Threat Rate:** ~25-35%

### **Attack Distribution:**
- **DoS:** ~25 packets (ICMP flooding)
- **Probe:** ~10 packets (Port scanning)
- **Normal:** ~65 packets (Legitimate traffic)

### **Severity Levels:**
- **CRITICAL:** ~25 (DoS attacks)
- **WARNING:** ~10 (Probe attacks)
- **INFO:** ~65 (Normal traffic)

---

## 🎨 Sample Data Preview

```csv
duration,src_bytes,dst_bytes,protocol_type,service,flag
5,215,45076,tcp,http,SF          ← Normal HTTP
0,0,0,icmp,eco_i,SF               ← DoS (ICMP flood)
30,0,0,tcp,http,S0                ← Probe (Port scan)
5,1684,1838,tcp,smtp,SF           ← Normal SMTP
30,0,0,tcp,telnet,S0              ← Suspicious (Telnet probe)
```

---

## 💡 Tips for Testing

### **Test Different Scenarios:**

1. **Upload Full File (100 rows)**
   - See complete analysis
   - View all attack types
   - Download full report

2. **Upload First 50 Rows**
   - Quick test
   - Faster processing
   - Partial analysis

3. **Upload Only Suspicious Rows**
   - Filter rows with S0 flag
   - High threat detection rate
   - Test alert system

---

## 🔍 How to Identify Attacks in CSV

### **DoS Indicators:**
```csv
duration,count,serror_rate,protocol_type
0,511,1.0,icmp                    ← High count + ICMP
0,254,0.99,icmp                   ← High error rate
```

### **Probe Indicators:**
```csv
duration,flag,num_failed_logins
30,S0,0                           ← S0 flag (no response)
30,S0,3                           ← Failed logins
```

### **Normal Traffic:**
```csv
duration,flag,logged_in,service
5,SF,1,http                       ← SF flag + logged in
2,SF,1,ftp_data                   ← Successful connection
```

---

## 📥 Create Your Own CSV

### **Minimum Requirements:**
```csv
duration,src_bytes,dst_bytes,count,srv_count,serror_rate,...
10,1000,500,50,30,0.1,...
5,500,200,30,20,0.05,...
```

### **Optional Columns:**
- Add `src_ip`, `dst_ip` for reference
- Add `protocol_type`, `service` for context
- Add `flag` for connection status

---

## 🎯 Quick Test Commands

```powershell
# 1. Train model
python src/train_ids.py

# 2. Launch upload app
python -m streamlit run app_with_upload.py

# 3. Upload: sample_upload_data.csv
# 4. Click: Analyze Data
# 5. View: Results & Charts
# 6. Download: Full Report
```

---

## 📊 What You'll See

### **Tab 1: Upload & Analyze**
- ✅ File uploaded: 100 packets
- ✅ Preview: First 10 rows
- ✅ Stats: 100 rows, 21 columns

### **Tab 2: Analysis Results**
- 📊 Metrics: 100 total, ~30 threats
- 📈 Pie chart: Attack distribution
- 📈 Bar chart: Severity levels
- 🚨 High-confidence threats listed

### **Tab 3: Detailed Report**
- 📋 Full table with predictions
- 📥 Download button
- 📊 Complete statistics

---

## 🎊 Ready to Test!

**The file `sample_upload_data.csv` is ready in your project folder!**

Just upload it to the dashboard and see AI-powered threat detection in action! 🛡️✨
