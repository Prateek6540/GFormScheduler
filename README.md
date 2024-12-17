# GFormScheduler

## Description  
GFormScheduler is a web-based tool that allows users to schedule emails containing Google Form responses in CSV and PDF formats. With a simple interface, users can submit their Google Sheet URL, select file formats, and specify a schedule to receive their files automatically via email.  

---

## Features  

- **Google Form Integration**: Automatically fetch responses from Google Form-linked spreadsheets.  
- **File Generation**: Generate CSV and PDF files of the responses.  
- **Email Scheduling**: Schedule the delivery of files via email at a user-specified time.  
- **Error Handling**: Includes validation for Google Sheet access and scheduled times.  
- **Lightweight UI**: Simple and intuitive user interface for ease of use.  

---

## Tech Stack  

- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Flask (Python)  
- **Scheduling**: APScheduler  
- **Email Services**: smtplib  
- **Google Sheet Integration**: gspread  
- **PDF Generation**: ReportLab  

---

## Setup and Installation  

### 1. Prerequisites  
- Python 3.8 or higher  
- Google Service Account for API access  
- SMTP Server credentials for sending emails  

### 2. Clone the Repository  
```bash
git clone <repository-url>
cd GFormScheduler
