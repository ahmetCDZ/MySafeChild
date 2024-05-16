import imaplib
import email
from email.header import decode_header
from datetime import datetime
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton


def imapFunc():
    imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
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



class SafeChild(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MySafeChild")
        self.setGeometry(500,500,500,500)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.textEdit = QTextEdit()
        self.layout.addWidget(self.textEdit)

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Kelime Ara")
        self.layout.addWidget(self.searchBar)

        self.searchButton = QPushButton("Ara")
        self.searchButton.clicked.connect(self.search)
        self.layout.addWidget(self.searchButton)

        emailBodies = imapFunc()
        for emailBody in emailBodies:
            self.showEmail(emailBody)
    def showEmail(self, emailBody):
        self.textEdit.append(emailBody)
    def search(self):
        keyword = self.searchBar.text()
        document = self.textEdit.toPlainText()
        if keyword:
            highlightedText = document.replace(keyword, f"<span style='background-color: yellow;'>{keyword}</span>")
            self.textEdit.clear()
            self.textEdit.insertHtml(highlightedText)
        else:
            self.textEdit.setHtml(document)

def main():
    app = QApplication(sys.argv)
    window = SafeChild()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

