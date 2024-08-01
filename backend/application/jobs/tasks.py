from application.worker import celery
from datetime import datetime
from celery.schedules import crontab
from application.data.models import AdRequest, User, Campaign
from application.utils.mail_service import send_mail
from time import time_ns
from application.utils.constants import DAILY_REMINDER_HTML, MONTHLY_REPORT_HTML
from application.utils.utility import make_monthly_report
import datetime

# @celery.task
# def just_say_hello():
#     print("Hello World at " + str(datetime.now()))

@celery.task
def send_daily_reminders():
    # Check if ad request status is pending
    ads_list = AdRequest.query.filter_by(status=1).all()
    emails = ['arnavkohli321@gmail.com']
    for ad in ads_list:
        if ad.influencer_id is not None and ad.influencer_id != 0:
            emails.append(User.query.filter_by(id=ad.influencer_id).first().email)
        campaign_sponsor = Campaign.query.filter_by(id=ad.campaign_id).first().sponsor_id
        emails.append(User.query.filter_by(id=campaign_sponsor).first().email)
    send_mail(emails, "Hi, You have an ad request in pending status", html=DAILY_REMINDER_HTML)

@celery.task
def send_monthly_report():
    for user in User.query.all():
        user_report = make_monthly_report(user.id)
        send_mail([user.email], "Here's Your Monthly Activity Report", html=MONTHLY_REPORT_HTML, dataframe=user_report)



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='*/20', minute='*/45'), send_daily_reminders.s(), name='Daily Reminder')
    sender.add_periodic_task(crontab(hour='*/23', minute='*/19', day_of_month='1'), send_monthly_report.s(), name='Monthly Report')