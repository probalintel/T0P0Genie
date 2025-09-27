# 🧞‍♂️ TopoGenie  
*Your network’s genie — from configs to topology, instantly.*  

---

## 🔹 Overview  
**TopoGenie** is an automated **network topology generation and analysis tool**.  
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
### 2️⃣ Upload all the Router & Switch Configuration files into **"scr/configs"* directory 
3️⃣ Run the Python files
```bash
python3 main.py
python3 export_pdf.py
```
*It will generate all the result inside newly **/output** directory.
4️⃣ Now you can see each report 
Go to /output
```bash
cd output
ls
```
Now see the ach output-
```bash
vim recomandations.txt
vim report.txt
open topology.png
open final_report.pdf
```
5️⃣You can also see the whole summary in a web view
```bash
cd ..
python3 webapp.py
```
Click on the given link 🔗
