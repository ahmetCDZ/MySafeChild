import imaplib
import email
from email.header import decode_header
from datetime import datetime

# E-posta hesabı bilgileri
email_address = "ahmetzincir27@gmail.com"
password = "nxsy grjm qjur hxiw"

imap_server = "imap.gmail.com"
imap_port = 993
imap = imaplib.IMAP4_SSL(imap_server, imap_port)

imap.login(email_address, password)

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
        date_str = local_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        date_str = "No Date"

    # E-postanın başlığını ve kimden geldiğini almak
    if msg["Subject"] is not None:
        subject = decode_header(msg["Subject"])[0][0]
    else:
        subject = "No subject"
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

    # Tarih, başlık, gönderen ve içeriğin yazdırılması
    print("Date:", date_str)
    print("Subject:", subject)
    print("From:", sender)
    print("Content:", email_body)
    print()

    # İhtiyacınıza göre e-posta içeriğini ve diğer detayları işleyebilirsiniz

# IMAP oturumunu sonlandırma
imap.close()
imap.logout()
