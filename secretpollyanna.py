import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import yaml
import random

#Function used to initialize the smtp server, email credentials and send the email
def send_email(to_email, to_name, subject, body, image_path=None):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "thesecretpollyanna@gmail.com"
    sender_password = "ixrqchrmleexuqib"
    app_password_spaces = "ixrq chrm leex uqib"

    message = MIMEText(body)
    message["Subject"] = subject

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)

        try:
            server.sendmail(sender_email, to_email, message.as_string())
            print(f"Email sent to: {to_email}")
        except smtplib.SMTPRecipientsRefused as e:
            print(f"Error sending email to: {to_email}: {e}")

def pair_emails_and_set_items(email_and_list_data):

    emails = []
    items = []
    names = []

    for entry in email_and_list_data:
        email = entry.get('email', '')
        item = entry.get('items', '')
        name = entry.get('name', '')

        emails.append(email)
        items.append(item)
        names.append(name)

        print(emails)
        print(items)
        print(names)
        

    if len(emails) % 2 != 0:
        print("Needs to be an even number of emails for pairing!")
        return

    paired_data = list(zip(emails, names, items))
    random.shuffle(paired_data)

    while paired_data:
        pair1 = paired_data.pop()
        pair2 = random.choice(paired_data)
        paired_data.remove(pair2)

        (email1, name1, items1) = pair1
        (email2, name2, items2) = pair2

        items1_plain_text = '\n'.join(items1)
        items2_plain_text = '\n'.join(items2)

        body1 = f"Dear {name1}, \n\nThis Christmas season you have been matched up with {name2} for this years Pollyanna!\n\nHere is {name2}'s wish list: \n\n{(items2_plain_text)}\n\nMerry Christmas!!!" 
        subject1 = "You've Been Matched!! - Sopko Family Pollyanna"
        send_email(email1, name1, subject1, body1)

        body2 = f"Dear {name2},\n\nThis Christmas season you have been matched up with {name1} for this years Pollyanna!\n\nHere is {name1}'s wish list: \n\n{str(items1_plain_text)}\n\nMerry Christmas!!!"
        subject2 = "You've Been Matched!! - Sopko Family Pollyanna"
        send_email(email2, name2, subject2, body2)


if __name__ == "__main__":

    with open("fields.yaml", "r") as file:
        email_and_list_data = yaml.safe_load(file)

    pair_emails_and_set_items(email_and_list_data)
