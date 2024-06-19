from django.core.mail import send_mail

def send_m():
    send_mail(
        'Master Subject',
        'Your first mail',
        'deepakgariya0975@gmail.com',
        ['deepak@onetechway.in'],
        fail_silently=False,
    )
