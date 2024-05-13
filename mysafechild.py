import imaplib
import email
from email.header import decode_header
from datetime import datetime

imap = imaplib.IMAP4_SSL( "imap.gmail.com", 993)
imap.login("ahmetzincir27@gmail.com", "nxsy grjm qjur hxiw")
mailbox = "INBOX"
imap.select(mailbox)

status, data = imap.search(None, 'FROM "ahmetzincir27@gmail.com"')
# Alınan tüm e-postaları işleme
for num in reversed(data[0].split()):
    # E-postanın alınması
    status, raw_email = imap.fetch(num, "(RFC822)")
    raw_email = raw_email[0][1]

    # E-posta mesajını parse etme
    msg = email.message_from_bytes(raw_email)

    # Tarih bilgisini almak
    date_tuple = email.utils.parsedate_tz(msg["Date"])
    if date_tuple:
        local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        date_str = local_date.strftime("%Y-%m-%d %H:%M")
    else:
        date_str = "No Date"
    sender = decode_header(msg["From"])[0][0]

    # E-posta içeriğini almak
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass
            if content_type == "text/plain" and "attachment" not in content_disposition:
                email_body = body
    else:
        email_body = msg.get_payload(decode=True).decode()

    print("Date:", date_str)
    print("Content:", email_body)
    print()
imap.close()
imap.logout()
