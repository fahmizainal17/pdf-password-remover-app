# PDF Password Remover

**Quickly strip passwords from your encrypted PDF files with an intuitive Streamlit UI**

---

<p align="center">
  <img src="https://img.shields.io/badge/last%20commit-today-blue" alt="last commit">
  <img src="https://img.shields.io/badge/python-100%25-brightgreen" alt="python coverage">
  <img src="https://img.shields.io/badge/languages-1-lightgrey" alt="languages">
</p>

## Built With

- **Markdown** • **Streamlit** • **Python** • **pypdf**

---

## Overview

This repository hosts a Streamlit app that lets you:

1. **Upload** one or more password-protected PDF files  
2. **Enter** the password(s) (single or per-file)  
3. **Unlock** your PDFs at the click of a button  
4. **Download** the decrypted PDFs individually or in a ZIP archive  

No command-line fiddling—everything runs in your browser.

### Demo

<div align="center">
  <img src="assets/main_app_pic.png" width="600px" alt="Main App Interface">
  <p><em>Main upload screen</em></p>
</div>

---

## Workflow

```mermaid
flowchart TD
    U[User] -->|Uploads PDFs & passwords| A[Streamlit App]
    A --> B[unlock_pdf() function]
    B --> C[PdfReader → PdfWriter]
    C --> D[Unlocked PDF bytes]
    D --> A
    A -->|Downloads| U
````

---

## Features

* **Bulk PDF handling**: Upload multiple files at once
* **Flexible passwords**: Use one password for all files or individual per-file entry
* **Progress feedback**: See a progress bar and status messages
* **Session persistence**: Download UI stays alive even after reruns
* **Single-click download**: Grab individual PDFs or a ZIP of all unlocked files

---

## Screenshots

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="assets/remove_password_pic.png" width="300px" alt="Removing Passwords">
        <p><em>Entering password & processing</em></p>
      </td>
      <td align="center">
        <img src="assets/result_pic.png" width="300px" alt="Results & Downloads">
        <p><em>Results summary & download options</em></p>
      </td>
    </tr>
  </table>
</div>

---

## Project Structure

```
pdf-password-remover-app/
├─ assets/
│  ├─ main_app_pic.png
│  ├─ remove_password_pic.png
│  └─ result_pic.png
├─ component.py       # Styling & sidebar UI
├─ main.py            # Streamlit app entrypoint
├─ requirements.txt
└─ README.md
```

---

## Installation

```bash
git clone https://github.com/yourusername/pdf-password-remover-app.git
cd pdf-password-remover-app
python3 -m venv .venv
source .venv/bin/activate       # macOS/Linux
# or .venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

## Usage

```bash
streamlit run main.py --server.fileWatcherType none
```

1. Open the URL shown in your terminal.
2. Upload your encrypted PDFs.
3. Enter the password(s).
4. Click **Remove Passwords**.
5. Download unlocked PDFs individually or as a ZIP.

---

## License

License © 2025 Fahmi Zainal
