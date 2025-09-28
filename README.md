[![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/probalsaha404)
[![GitHub Follow](https://img.shields.io/github/followers/probalintel?label=Follow&style=for-the-badge&logo=github)](https://github.com/probalintel)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-Profile-black?style=for-the-badge&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/ProbalSecOps)
[![X Follow](https://img.shields.io/badge/Follow%20on-X-blue?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/contact_probal)

# 🧞‍♂️ T0P0Genie  
T0P0Genie is an automated network topology generation and auditing tool that converts raw router/switch configuration files into structured insights.The tool analyzes routing protocols (like OSPF), MTU, and security settings to identify misconfigurations and provide best-practice recommendations.
Use it to save time, reduce human error, and gain clear visibility into your network’s design and security posture. ✅

> *Your network’s genie — from configs to topology, instantly.*  

---

## 🔹 Overview  
**T0P0Genie** is an automated **network topology generation and analysis tool**.  
It takes exported **router/switch configuration files** as input and produces:  

- 📌 A **JSON** representation of your network topology  
- 🌐 A **visual topology diagram** (`.png`)  
- 📝 A **detailed text report** with analysis & recommendations  
- 📑 A **professional PDF report** (`.pdf`)  
- 🌍 An **interactive web dashboard** (Flask-based)  

This tool helps in **auditing**, **visualizing**, and **securing** your network by detecting misconfigurations, analyzing routing protocols (like OSPF), checking MTU and bandwidth usage, and suggesting the best routing protocol for your setup.  

---

## ⚙️ Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/probalintel/T0P0Genie.git
cd T0P0Genie
```
### 2️⃣ Upload all the Router & Switch Configuration files into *"src/configs"* directory 
### 3️⃣ Run the Python files
```bash
python3 main.py
python3 export_pdf.py
```
*It will generate all the result inside newly **/output** directory.
### 4️⃣ Now you can see each report 
Go to /output
```bash
cd output
ls
```
### Now see the each output-
```bash
vim recomandations.txt
vim report.txt
open topology.png
open final_report.pdf
```
### 5️⃣ You can also see the whole summary in a web view
```bash
cd ..
python3 webapp.py
```
Click on the given link 🔗

## 📄 License
This project is licensed under a Proprietary License.  
All rights reserved © 2025 Probal Saha.


## 📬 Connect With Me

🚀 Check out my Portfolio: [Probal Saha - Portfolio](https://probalintel.github.io)  
📧 Email me at: [contact.probalsaha@gmail.com](mailto:contact.probalsaha@gmail.com)

   I love connecting with people! Feel free to reach out! 😊

---

⭐ Designed & Developed with ❤ by [@probalintel](https://github.com/probalintel)
