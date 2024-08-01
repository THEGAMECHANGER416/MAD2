import pandas as pd
from application.data.models import User, Sponsor, Influencer, AdRequest, Campaign

def make_monthly_report(user_id):
    columns = ['Date','AdRequest_id','campaign_id','influencer_id','goal','platform','requirements','payment_amount','status']

    user_type = User.query.filter_by(id=user_id).first().role
    ad_reqs = None
    if user_type == 'Sponsor':
        user_campaigns = Sponsor.query.filter_by(id=user_id).first().campaigns
        ad_reqs = []
        for campaign in user_campaigns:
            ad_reqs.extend(AdRequest.query.filter_by(campaign_id=campaign.id).all())
    elif user_type == 'Influencer':
        ad_reqs = AdRequest.query.filter_by(influencer_id=user_id).all()
    else:
        ad_reqs = AdRequest.query.all()

    rows = []
    for ad_req in ad_reqs:
        row = []
        row.append(ad_req.created_at)
        row.append(ad_req.id)
        row.append(ad_req.campaign_id)
        row.append(ad_req.influencer_id)
        row.append(ad_req.goal)
        row.append(ad_req.platform)
        row.append(ad_req.requirements)
        row.append(ad_req.payment_amount)
        row.append(ad_req.status)
        rows.append(row)

    # create a dataframe
    df = pd.DataFrame(rows,columns=columns)
    return df
