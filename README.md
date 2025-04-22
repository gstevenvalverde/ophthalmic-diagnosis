# 🩺 Ophthalmic Diagnosis Management System

## 🧠 Description

A comprehensive clinical management system designed to store, process, and analyze ophthalmic examination data—especially fundus images and diagnostic parameters. The system supports **bilateral (OD/OS) eye examinations** with specialized handling of **retinal images** and **expert contour segmentations**.

This project includes a module for handling medical images and their metadata, leveraging the [**PAPILA Dataset**](https://figshare.com/articles/dataset/PAPILA/14798004/1) for development and validation.

---

## ✨ Key Features

- 🔍 **Dual-eye Examination Support**  
  Manage both OD (right eye) and OS (left eye) clinical records.

- 🧾 **Medical Image Processing**  
  - Fundus image management (`.jpg`, `.png`, `.tiff`, etc.)  
  - Expert contour file handling (`.txt`)  
  - Automatic validation and organization of files  

- 📊 **Clinical Data Tracking**  
  - Diopter & axial length tracking  
  - Astigmatism metrics  
  - Visual field performance (VF MD)

- 🧱 **Modular Architecture**  
  - `DiagnosisService` core logic  
  - Dedicated handlers per eye  
  - Validation and utility modules

- 💻 **Command-Line Interface (CLI)**  
  Interactive and intuitive terminal-based interface for data operations

---

## 🛠️ Technical Structure

```
├── data/
│   └── load_data/
│       ├── ClinicalData/             # Excel sheets with ophthalmic data
│       ├── ExpertsSegmentations/     # Expert contour files and processed outputs
│       └── FundusImages/             # Raw retinal image storage
├── src/
│   ├── cli/                          # CLI components
│   ├── models/                       # Core data models
│   ├── services/                     # Business logic and orchestration
│   └── utils.py                      # Shared utilities
├── main.py                           # Entry point
└── requirements.txt                  # Dependencies version
```

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ophthalmic-diagnosis.git
cd ophthalmic-diagnosis-system

# Set up a Python virtual environment (Python 3.8+)
python -m venv venv
source venv/bin/activate         # Linux/Mac
venv\Scripts\activate            # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Running the System

```bash
python main.py
```

The CLI will guide you through image loading, data management, and diagnostic workflows.

---

## 📁 File Handling System

| **File Type**       | **Destination Path**                                      | **Valid Formats**                      |
|---------------------|------------------------------------------------------------|----------------------------------------|
| Retinal Images      | `data/load_data/FundusImages/`                             | `.jpg`, `.jpeg`, `.png`, `.tiff`, `.bmp` |
| Contour Files       | `data/load_data/ExpertsSegmentations/Contours/`            | `.txt`                                 |
| Processed Images    | `data/load_data/ExpertsSegmentations/ImagesWithContours/`  | `.jpg`, `.jpeg`, `.png`, `.tiff`, `.bmp` |

Files are automatically organized and validated upon loading.

---

## 📬 Contact

**Project Maintainer**  
Grover Steven Valverde Saavedra  
📧 [gstevenvalverde@gmail.com](mailto:gstevenvalverde@gmail.com)  
🔗 [GitHub: @gstevenvalverde](https://github.com/gstevenvalverde)