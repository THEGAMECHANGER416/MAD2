from flask_mail import Mail, Message
from flask import current_app
import io
import pandas as pd

def send_mail(users, subject, html=None, dataframe=None, csv_filename="report.csv"):
    mail = current_app.extensions['mail']
    with mail.connect() as conn:
        for user in users:
            msg = Message(
                sender=("Brandly", "22f3002292@ds.study.iitm.ac.in"),
                subject=subject,
                recipients=[user],
            )
            if html:
                msg.html = html

            # Attach CSV file if DataFrame is provided
            if dataframe is not None:
                # Convert DataFrame to CSV
                csv_buffer = io.StringIO()
                dataframe.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                
                # Attach the CSV file to the email
                msg.attach(
                    filename=csv_filename,
                    content_type='text/csv',
                    data=csv_buffer.getvalue()
                )
                
            conn.send(msg)
