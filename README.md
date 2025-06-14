# 🔒 NFC-Based Security System with Android App  
**Secure access control using Raspberry Pi, NFC tags, and Firebase.**  

---

## 📋 Table of Contents
- [Features](#-features)
- [Hardware Setup](#-hardware-setup)
- [Installation](#-installation)
- [Configuration](#%EF%B8%8F-configuration)
- [Workflow](#-workflow)
- [Troubleshooting](#-troubleshooting)
- [Files Overview](#-files-overview)

---

## ✨ Features
- **Dual Operational Modes**:  
  - 📖 *Read Mode*: Verify NFC tags (Yellow LED active)  
  - ✏️ *Write Mode*: Register/Reset tags (Red LED active)  
- **Firebase Integration**: Real-time authentication & logging  
- **Encrypted Communication**: AES using Fernet for encryption  
- **Remote Management**: Android app control via SocketXP tunneling  

---

## 🔩 Hardware Setup
| Component       | GPIO Pin |
|-----------------|----------|
| Red LED         | 24       |
| Blue LED        | 25       |
| Yellow LED      | 23       |
| Solenoid Lock   | 16       |
| Buzzer          | 26       |
| PN532 NFC Module| SPI Interface |

---

## ⚡ Installation

### Prerequisites
- Raspberry Pi OS (64-bit recommended)
- Enabled SPI interface (`sudo raspi-config`)
- Firebase project with Realtime Database

### Step-by-Step Setup
1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/NFCserver.git
   cd NFCserver
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Firebase Configuration**
   - Download service account JSON from Firebase Console  
   - Rename to `firebase_credentials.json` and place in project root  
   - **Update Database URL** in 2 files:  
     ```python
     # In firebasecmp.py AND firebaselog.py:
     firebase_admin.initialize_app(login, {
         'databaseURL': 'https://your-project-id.firebaseio.com/'  # ← Replace this
     })
     ```

4. **Auto-Start Services**
   ```bash
   # 1. Add to .bashrc
   cat bashrc.txt >> ~/.bashrc
   source ~/.bashrc

   # 2. Setup systemd service
   sudo cp readservice.txt /lib/systemd/system/readservice.service
   sudo systemctl daemon-reload
   sudo systemctl enable readservice.service
   ```

5. **Set Permissions**
   ```bash
   chmod +x wsgi.sh starttunnel.sh
   ```

---

## ⚙️ Configuration

### Critical Files
| File               | Purpose                              |
|--------------------|--------------------------------------|
| `app.py`           | Flask server endpoints               |
| `readcard.py`      | NFC read operations                  |
| `writecard.py`     | NFC write operations                 |
| `firebasecmp.py`   | Firebase credential validation       |
| `firebaselog.py`   | Access logging to Firebase           |

### NFC Module Setup
- Default authentication key: `FFFFFFFFFFFF`  
- Block numbers for read/write operations are defined in `readcard.py` and `writecard.py`.

### Tunneling Setup
Replace placeholder in `starttunnel.sh`:
```bash
# Replace <YOUR TOKEN> with actual SocketXP token
-H "Authorization: Bearer <YOUR TOKEN>" 
```

---

## 🔄 Workflow
1. **Boot Sequence**  
   - `readservice.service` starts (Yellow LED on)  
   - Flask server launches via `wsgi.sh`

2. **Android App Interaction**  
   - *Register Tag*: App request → Write Mode (Red LED) → `writecard.py` executes  
   - *Reset Tag*: Similar workflow with data overwrite  

3. **Access Control**  
   - Successful NFC read → Solenoid unlock + Firebase log  
   - Invalid tag → Buzzer alert  

---

## 🚨 Troubleshooting
**Common Issues**:
1. **Firebase Connection Failed**  
   - Verify `firebase_credentials.json` exists  
   - Confirm database URL in both `firebasecmp.py` and `firebaselog.py`  

2. **NFC Not Responding**  
   ```bash
   python read_test.py  # Test NFC module functionality
   ```

3. **Service Failures**  
   ```bash
   journalctl -u readservice.service -b  # View service logs
   ```

4. **Path Errors**  
   Update all instances of `/home/karthik/NFCserver` to your actual project path in:  
   - `wsgi.sh`  
   - `readservice.txt`  
   - `app.py`  

---

## 📂 Files Overview
```
├── app.py               # Flask server core
├── firebasecmp.py       # Firebase authentication
├── firebaselog.py       # Activity logging
├── encrypt.py           # Fernet encryption
├── decrypt.py           # AES decryption
├── readservice.txt      # Systemd service template
├── starttunnel.sh       # Internet tunneling
└── requirements.txt     # Python dependencies
```

---

## 📜 License
MIT License - See [LICENSE](LICENSE) for details.  

---

> **Note**: Uncomment the authentication logic in `readcard.py` (lines 52-75) after initial setup.  
> Always test with `read_test.py` before full deployment!

---
