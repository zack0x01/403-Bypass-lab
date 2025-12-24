# 🔓 403 Bypass Practice Lab

<img width="1740" height="956" alt="Screenshot_2025-12-23_20-15-34" src="https://github.com/user-attachments/assets/ca351c79-3258-41b4-95a3-aa1fcb3a7d9e" />

A bug bounty practice lab demonstrating various 403 Forbidden bypass techniques.

Created by **zack0x01** | [Learn Bug Bounty](https://lureo.shop) | [YouTube](https://youtube.com/@zack0x01) | [Twitter](https://twitter.com/zack0x01)

## 🚀 Installation

**Quick Start:**
```bash
chmod +x start.sh
./start.sh
```

**Manual Installation:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000** in your browser.

## 🎮 Challenges

8 different 403 bypass challenges:

1. **HTTP Verb Bypass** - `/admin/secret`
2. **HTTP Header Bypass** - `/internal/data`
3. **Path Encoding Bypass** - `/protected/files`
4. **Path Case Bypass** - `/sensitive/info`
5. **Path Slash Bypass** - `/restricted/area`
6. **Parameter Pollution** - `/api/user?id=123`
7. **Host Header Bypass** - `/local/admin`
8. **Method Override Bypass** - `/api/update`

Each challenge returns **403 Forbidden** - bypass it to get the flag!

## 📚 Resources

- [HackTricks 403 Bypass Guide](https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-web/403-and-401-bypasses.html)

## 📝 License

Educational purposes only. Use responsibly.
