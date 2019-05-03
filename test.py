from django.core.mail import send_mail

subject = 'welcome'
message = ''
# html_message = "<a href='http://127.0.0.1:8000/blog/active/%s'>
# http://127.0.0.1:8000/blog/active/%s</a>"%(token, token)
html_message = ''
sender = 'hi'
receiver = ['calste@163.com']
send_mail(subject, message, sender, receiver,html_message=html_message)