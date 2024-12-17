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

3. Install Dependencies
Create a virtual environment and install the required libraries:

bash
Copy code
python -m venv venv  
source venv/bin/activate   # On Windows use: venv\Scripts\activate  
pip install -r requirements.txt  
4. Configure Environment Variables
Create a .env file in the project root directory with the following variables:

plaintext
Copy code
SENDER_EMAIL=your_email@example.com         # Your SMTP sender email  
SENDER_PASSWORD=your_email_app_password     # App-specific email password  
SERVICE_ACCOUNT_FILE=SECRET_KEY.json        # Google Service Account JSON file  
SECRET_KEY=your_flask_secret_key            # Flask secret key  
5. Generate a Secret Key
To generate a Flask SECRET_KEY securely, create a Python file named secret.py with the following content:

python
Copy code
import secrets  
print(secrets.token_hex(16))  
Run the file:

bash
Copy code
python secret.py  
Copy the generated key and paste it into your .env file as the value for SECRET_KEY.

6. Set Up Google Service Account
Go to the Google Cloud Console.
Enable the Google Sheets API.
Create a Service Account and download the credentials JSON file.
Rename the file to SECRET_KEY.json and place it in the project root directory.
Share your Google Sheet with the service account email provided in the credentials file.
7. Run the Application
Start the Flask server:

bash
Copy code
python app.py  
Access the app in your browser at http://127.0.0.1:5000.

How It Works
Create a Google Form: Link the responses to a Google Sheet.
Share the Google Sheet: Share the spreadsheet with the service account email provided in the app.
Schedule Email Delivery:
Input the Google Sheet URL.
Specify the recipient email.
Choose file formats (CSV, PDF).
Set the schedule for delivery.
Receive Files: The scheduled email will include the selected files as attachments.
Project Structure
plaintext
Copy code
GFormScheduler/  
│  
├── static/                     # CSS, JS, Images  
│   ├── styles.css  
│   ├── script.js  
│   └── images/  
│       ├── clipboard.png  
│       ├── step1.png  
│       ├── step2.png  
│       └── step3.png  
│  
├── templates/                  # HTML Templates  
│   └── index.html  
│  
├── main.py                     # Helper functions (send_email, generate_csv, etc.)  
├── app.py                      # Flask application  
├── SECRET_KEY.json             # Google Service Account Credentials  
├── .env                        # Environment variables  
├── secret.py                   # Generate Flask Secret Key  
└── requirements.txt            # Python dependencies  
Screenshots
1. Share Google Sheet

2. Schedule Email

Future Enhancements
Add support for multiple recipients.
Integrate with cloud storage (Google Drive) for generated files.
Add user authentication for better security.
License
This project is licensed under the MIT License.

Contributing
Feel free to fork the repository and submit pull requests for improvements.

Contact
For any issues or queries, reach out via:
📧 your-email@example.com
