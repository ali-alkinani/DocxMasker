# 🛡️ DocxMasker

**DocxMasker** is a lightweight desktop tool built with Python and CustomTkinter designed to redact sensitive names or targeted phrases within `.docx` documents and manage recovery mappings with optional AES encryption.

---

## 🛠️ Tech Stack

- **GUI Framework:** CustomTkinter
- **Security:** `cryptography` (PBKDF2HMAC / AES-GCM)
- **Database:** SQLite3
- **Document Engine:** `python-docx`

---

## 🚀 Installation & Setup

### 1. Clone the repository
```
git clone https://github.com/ali-alkinani/DocxMasker.git
cd DocxMasker
```


### 2. Set up a virtual environment (Recommended)
```
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
```
pip install customtkinter cryptography python-docx
```

### 4. Run the application
```
python main.py
```
---

## 📖 How to Use

The application workflow is divided into three main tabs:

### 1. 📦 Database Management
- **Create / Import Database:** Create a new SQLite database (`.db`) by importing a text file containing names separated by commas, or load an existing `.db` file directly.
- **Manual Entry:** Option to manually input terms into the database.

### 2. 🔀 Text Masking & Encryption
- **Select Source Data:** Choose your target `.docx` file and the configured SQLite database.
- **Set Replacement Word:** Define a custom replacement string (e.g., `CODENAME`).
- **Optional High-Grade Encryption:** 
  - If a password is provided, the recovery mapping will be secured as an encrypted `.enc` file. 
  - **Security Note:** It uses **AES-GCM (256-bit)** combined with **PBKDF2 key derivation**—industry-standard algorithms used globally to secure sensitive data. Even if you are unfamiliar with encryption technologies, rest assured that without the correct password, reversing or cracking the recovery file is practically impossible.
  - If left blank, an unencrypted JSON recovery mapping will be output directly for simple use cases.

### 3. 🔑 Recovery & Restoration
- **Step 1 (Decrypt Key):** If your recovery file was encrypted (`.enc`), provide the password to extract the JSON mapping file.
- **Step 2 (Restore Document):** Upload the modified `.docx` file and the JSON mapping file to restore the original document.

---

## 💬 A Note from the Developer

> "I built this tool thinking it would be genuinely useful for anyone needing to redact large sets of keywords in a document automatically, without relying on heavy AI models or cloud services, while maintaining a smooth restoration workflow. Recognizing that users dealing with sensitive files value security, I included high-grade encryption for the recovery file. Please feel free to reach out if you encounter any bugs or have suggestions, as I plan to release updates and fixes based on feedback."

---

## 📄 License

This project is open-source and licensed under the [MIT License](LICENSE).
