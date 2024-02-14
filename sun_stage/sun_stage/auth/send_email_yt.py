import os 
#mniq gzgf hntl rasc
import ssl
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader



email_sender = "lindasiewe6@gmail.com"
#email_password = os.environ.get("EMAIL_PASSWORD")
email_password = "mniq gzgf hntl rasc"
email_receiver = 'siewe.stephanie@gmail.com'



def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def render_html_template(template_path, **kwargs):
    template_dir = os.path.dirname(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(os.path.basename(template_path))
    return template.render(**kwargs)

def send_simple_email(newbody):
   subject = 'Test Sending Mail'
   body = newbody
   em = EmailMessage()
   em['From'] = email_sender
   em['To'] = email_receiver
   em['Subject'] = subject
   
   em.set_content(body)

   context = ssl.create_default_context()

   with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
      smtp.login(email_sender, email_password)
      smtp.sendmail(email_sender, email_receiver, em.as_string())
      
def send_simple_html_email(file_path):
   subject = 'Test Sending Mail'
   body = read_html_file(file_path)
   em = EmailMessage()
   em['From'] = email_sender
   em['To'] = email_receiver
   em['Subject'] = subject
   em.add_alternative(body,subtype='html')
   

   context = ssl.create_default_context()

   with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
      smtp.login(email_sender, email_password)
      smtp.sendmail(email_sender, email_receiver, em.as_string())
      
      
      
def send_dynamic_email(receiver_email, kwargs):
 
    file_path = 'sun_stage/auth/templates/email_otp.html'
    
    # Utilisez Jinja2 pour rendre le modèle HTML avec des variables dynamiques
    body = render_html_template(file_path, **kwargs)
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = receiver_email
    em['Subject'] = kwargs['subject']
    em.add_alternative(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiver_email, em.as_string())
        return print("response send email",{"status": "Ok", "content": "mail_send"})
        
nbody = {'otpcode': "0v0tgtg", 'subject': "Test Sending Mail", 'fullname': "lola", 'validtime': '15'}
#send_dynamic_email(email_receiver,nbody)
#send_simple_email('Test Testing Test')