from application.worker import celery
from datetime import datetime
from celery.schedules import crontab
from application.data.models import AdRequest, User, Campaign
from application.utils.mail_service import send_mail

@celery.task
def just_say_hello():
    print("Hello World at " + str(datetime.now()))

@celery.task
def send_daily_reminders():
    # Check if ad request status is pending
    ads_list = AdRequest.query.filter_by(status=1).all()
    emails = ['arnavkohli31@gmail.com']
    for ad in ads_list:
        if ad.influencer_id is not None and ad.influencer_id != 0:
            emails.append(User.query.filter_by(id=ad.influencer_id).first().email)
        campaign_sponsor = Campaign.query.filter_by(id=ad.campaign_id).first().sponsor_id
        emails.append(User.query.filter_by(id=campaign_sponsor).first().email)
    print(emails)
    send_mail(emails, 'Ad Request Reminder')

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0,just_say_hello.s(), name='add every 10s')
    sender.add_periodic_task(crontab(minute=11, hour=16), send_daily_reminders.s(), name='add every midnight')