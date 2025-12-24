# 🔓 403 Bypass Practice Lab

A comprehensive bug bounty practice lab demonstrating various 403 Forbidden bypass techniques. Perfect for learning and creating educational content!

<img width="1740" height="956" alt="Screenshot_2025-12-23_20-15-34" src="https://github.com/user-attachments/assets/495e13e3-55f5-4762-bb3f-ec431fd4611d" />

Created by **zack0x01** | [Learn Bug Bounty](https://lureo.shop) | [YouTube](https://youtube.com/@zack0x01) | [Twitter](https://twitter.com/zack0x01)

## 🚀 Quick Installation

### Option 1: Using the Start Script (Recommended)

The easiest way to get started:

```bash
chmod +x start.sh
./start.sh
```

This script will automatically:
- Create a virtual environment
- Install all dependencies
- Start the server

**Note:** If you get an error about `python3-venv`, install it first:
```bash
sudo apt install python3-venv  # For Debian/Ubuntu
```

---

### Option 2: Manual Installation

#### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/403-bypass-lab.git
cd 403-bypass-lab
```

#### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Run the Lab
```bash
python app.py
```

#### Step 5: Open in Browser
Navigate to: **http://localhost:5000**

That's it! 🎉

---

## 🎮 Challenges

This lab contains **8 different 403 bypass challenges**:

1. **HTTP Verb/Method Bypass** - `/admin/secret`
2. **HTTP Header Bypass** - `/internal/data`
3. **Path Encoding Bypass** - `/protected/files`
4. **Path Case Bypass** - `/sensitive/info`
5. **Path Slash Bypass** - `/restricted/area`
6. **Parameter Pollution** - `/api/user?id=123`
7. **Host Header Bypass** - `/local/admin`
8. **Method Override Bypass** - `/api/update`

Each challenge starts with a **403 Forbidden** error. Your goal is to bypass it using various techniques!

---

## 🛠️ Requirements

- Python 3.7 or higher
- pip (Python package manager)
- python3-venv (for virtual environment)

**Install python3-venv if needed:**
```bash
sudo apt install python3-venv  # Debian/Ubuntu
```

---

## 📚 Learning Resources

- [HackTricks 403 Bypass Guide](https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-web/403-and-401-bypasses.html)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)

---

## 🎯 How to Use

1. **Start the server** using the installation steps above
2. **Open the lab** in your browser at `http://localhost:5000`
3. **Read each challenge** description and hints
4. **Try to bypass** the 403 error using the suggested techniques
5. **Get the flag** when you successfully bypass the protection!

### Testing Tools

You can test the challenges using:
- **Browser** - Direct navigation and DevTools
- **Burp Suite** - Intercept and modify requests
- **curl** - Command-line testing
- **Postman** - GUI for testing different methods

---

## 💡 Example Solutions

### Challenge 1: HTTP Verb Bypass
```bash
# Instead of GET, try:
curl -X POST http://localhost:5000/admin/secret
curl -X HEAD http://localhost:5000/admin/secret
```

### Challenge 2: HTTP Header Bypass
```bash
curl -H "X-Forwarded-For: 127.0.0.1" http://localhost:5000/internal/data
```

### Challenge 3: Path Encoding Bypass
```bash
curl 'http://localhost:5000/protected/%2efiles'
```

*Try to solve the rest yourself!*

---

## 📝 License

This project is for **educational purposes only**. Use responsibly and only on systems you own or have permission to test.

---

## 🤝 Contributing

Found a bug or want to add more challenges? Feel free to submit issues or pull requests!

---

## ⭐ Star This Repo

If you find this lab helpful, please give it a star! ⭐

---

**Happy Hacking! 🔓**
