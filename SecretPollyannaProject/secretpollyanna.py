import smtplib
import argparse
import yaml
import random
import itertools
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

IMAGE_PATH = "C:/Users/Jake/Documents/SecretPollyanna/8bitsanta-01.png"

#Function used to initialize the smtp server, email credentials and send the email
def send_email(to_email, to_name, subject, body, image_path=None):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = ""
    sender_password = ""

    message = MIMEMultipart()
    message["Subject"] = subject
    message.attach(MIMEText(body, 'plain'))

    #Opens up an image and adds it to the message 
    if image_path:

        with open(image_path, "rb") as image_file:
            image = MIMEImage(image_file.read(), name = "image.jpg")
            message.attach(image)

    #Open up the SMTP server and log into it 
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        #Sends the email
        try:
            server.sendmail(sender_email, to_email, message.as_string())
            print(f"Email sent to: {to_email}")
        except smtplib.SMTPRecipientsRefused as e:
            print(f"Error sending email to: {to_email}: {e}")


#function to randomly pair people together for secret santa
def pair_emails_randomly(email_and_list_data):

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
        
    #Checks to make sure that their will be even matches for pairing
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

        print(f"Processing pair: {name1} - {name2}")

        body1 = f"Dear {name1}, \n\nThis Christmas season you have been matched up with {name2} for this years Pollyanna!\n\nHere is {name2}'s wish list: \n\n{(items2_plain_text)}\n\nMerry Christmas!!!" 
        subject1 = "You've Been Matched!! - Sopko Family Pollyanna"
        send_email(email1, name1, subject1, body1, IMAGE_PATH)
        print(f"Email 1 sent to: {email1}")


        body2 = f"Dear {name2},\n\nThis Christmas season you have been matched up with {name1} for this years Pollyanna!\n\nHere is {name1}'s wish list: \n\n{str(items1_plain_text)}\n\nMerry Christmas!!!"
        subject2 = "You've Been Matched!! - Sopko Family Pollyanna"
        send_email(email2, name2, subject2, body2, IMAGE_PATH)
        print(f"Email 2 sent to: {email2}")

    return
    
def pair_emails_with_prohibition(email_and_list_data, prohibited_pairs): 

    entries = [(entry['email'], entry['name'], entry['items']) for entry in email_and_list_data]

    if len(entries) % 2 != 0:
        print("Needs to be an even number of emails for pairing!")
        return

    all_possible_pairs = list(itertools.combinations(entries, 2))

    # Remove prohibited pairs from the list
    if prohibited_pairs:
        all_possible_pairs = [(entry1, entry2) for entry1, entry2 in all_possible_pairs
                              if (entry1[1], entry2[1]) not in prohibited_pairs and (entry2[1], entry1[1]) not in prohibited_pairs]

    iteration_count = 0  # To limit the number of iterations for debugging
    while all_possible_pairs:
        iteration_count += 1
        print(f"Iteration {iteration_count}")

        random.shuffle(all_possible_pairs)

        entry1, entry2 = all_possible_pairs.pop()

        (email1, name1, items1) = entry1
        (email2, name2, items2) = entry2

        items1_plain_text = '\n'.join(items1)
        items2_plain_text = '\n'.join(items2)

        print(f"Processing pair: {name1} - {name2}")

        subject1 = "Subject for Email 1"
        body1 = f"Dear {name1}, \n\nhis Christmas season you have been matched up with {name2} for this years Pollyanna!\n\nHere is their corresponding wish list:\n{items2_plain_text}\n\nMerry Christmas!!!" 
        #send_email(email1, name1, subject1, body1, IMAGE_PATH)
        print(f"Email 1 sent to: {email1}")


        subject2 = "Subject for Email 2"
        body2 = f"Dear {name2},\n\nThis Christmas season you have been matched up with {name1} for this years Pollyanna!\n\nHere is their corresponding wish list:\n{items1_plain_text}\n\nMerry Christmas!!!"
        #send_email(email2, name2, subject2, body2, IMAGE_PATH)
        print(f"Email 2 sent to: {email2}")


        # Remove the sent pair and any pairs involving the participants from the list
        all_possible_pairs = [(e1, e2) for e1, e2 in all_possible_pairs
                              if e1[1] != name1 and e1[1] != name2 and e2[1] != name1 and e2[1] != name2]
        print(f"Remaining pairs: {all_possible_pairs}")

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Secret Pollyanna Script")
    parser.add_argument("--fields", required=True, help="Path to the fields YAML file")
    parser.add_argument("--sig_others", help="Path to the significant others YAML file")
    parser.add_argument("--prohibit", action="store_true", help="Prohibit significant others from being matched")
    args = parser.parse_args()

    with open(args.fields, "r") as file:
        email_and_list_data = yaml.safe_load(file)

    prohibited_pairs = None
    if args.prohibit and args.sig_others:
        with open(args.sig_others, "r") as file:
            significant_others_data = yaml.safe_load(file)
        prohibited_pairs = [(pair[0], pair[1]) for pair in significant_others_data]
        print(prohibited_pairs)
    if args.prohibit:
        pair_emails_with_prohibition(email_and_list_data,  prohibited_pairs)
    else:
        pair_emails_randomly(email_and_list_data)
