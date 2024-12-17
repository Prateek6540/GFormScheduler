from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from dotenv import load_dotenv
from main import send_email, validate_sheet_access, get_client_email, generate_csv, generate_pdf, fetch_sheet_data
import os
import json
# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

@app.route('/')
def index():
    client_email = get_client_email()
    return render_template("index.html", client_email=client_email)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        sheet_url = request.form['sheet_url']
        receiver_email = request.form['receiver_email']
        schedule_time_str = request.form['schedule_time']
        include_csv = 'include_csv' in request.form
        include_pdf = 'include_pdf' in request.form

        formats = []
        if include_csv:
            formats.append('csv')
        if include_pdf:
            formats.append('pdf')

        # Parse schedule time
        schedule_time = datetime.strptime(schedule_time_str, "%Y-%m-%dT%H:%M")

        # Check if the schedule time is in the past
        if schedule_time < datetime.now():
            flash("Error: The scheduled time must be in the future.", "error")
            return redirect(url_for('index'))

        # Validate sheet access with timeout
        def validate_sheet_with_timeout():
            validate_sheet_access(sheet_url)

        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(validate_sheet_with_timeout)
                future.result(timeout=5)
        except TimeoutError:
            flash("Error: Google Sheet access timed out after 5 seconds. Please try again.", "error")
            return redirect(url_for('index'))

        # Calculate the time when files need to be generated
        generate_time = schedule_time - timedelta(seconds=4)

        # Define the task to generate files and send email
        def generate_and_send_email():
            data = fetch_sheet_data(sheet_url)
            attachments = []
            if 'csv' in formats:
                csv_path = generate_csv(data, "output.csv")
                attachments.append(csv_path)
            if 'pdf' in formats:
                pdf_path = generate_pdf(data, "output.pdf")
                attachments.append(pdf_path)
            send_email(receiver_email, attachments)
            for file_path in attachments:
                if os.path.exists(file_path):
                    os.remove(file_path)

        scheduler.add_job(generate_and_send_email, DateTrigger(run_date=generate_time))
        return render_template("success.html",
                               sheet_url=sheet_url,
                               receiver_email=receiver_email,
                               schedule_time=schedule_time,
                               formats=formats)

    except PermissionError:
        flash("Access denied. Please share the spreadsheet with the service account.", "error")
        return redirect(url_for('index'))
    except ValueError:
        flash("Invalid Google Sheet URL. Please check and try again.", "error")
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"An unexpected error occurred: {e}", "error")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
