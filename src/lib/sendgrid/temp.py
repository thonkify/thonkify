import os
import urllib2

from . import *
from .helpers.mail import *

RESET_PW = '13b8f94f-bcae-4ec6-b752-70d6cb59f932'

SG = sendgrid.SendGridAPIClient(apikey=os.environ['SENDGRID_API_KEY'])


def _send_email(template_id, subject, dst_email, dst_name, src_email, src_name, sub_dict):
	mail = Mail()
	mail.set_subject(subject)
	mail.set_from(Email(src_email, src_name))
	p = Personalization()
	p.add_to(Email(dst_email, dst_name))
	for k, v in sub_dict.items():
		p.add_substitution(Substitution(k, v))
	mail.add_personalization(p)
	mail.set_template_id(template_id)
	tracking_settings = TrackingSettings()
	tracking_settings.set_click_tracking(ClickTracking(enable=False, enable_text=False))
	tracking_settings.set_open_tracking(OpenTracking(enable=False))
	tracking_settings.set_subscription_tracking(SubscriptionTracking(enable=False))
	mail.set_tracking_settings(tracking_settings)
	data = mail.get()
	print(data)
	res = SG.client.mail.send.post(request_body=data)
	return res


if __name__ == '__main__':
	email = 'elmer@sendgrid.com'
	try:
		_send_email(RESET_PW, 'test email', email, "Elmer", "dx@sendgrid.com", "DX",
					{'-name-': 'Elmer', '-card-': 'Test'})
	except urllib2.HTTPError as e:
		print e.read()
