import imaplib
import email
from datetime import datetime
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

def imapFunc(fromAdress):
    imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    imap.login("ahmetzincir27@gmail.com", "nxsy grjm qjur hxiw")
    mailbox = "INBOX"
    imap.select(mailbox)


    emailBodies = []
    dateStrings = []

    status, data = imap.search(None, f'FROM "{fromAdress}"')
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
            dateStrings.append(date_str)  # Tarih dizisine ekle
        else:
            date_str = "No Date"

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    emailBody = body
                    emailBodies.append(emailBody)  # Gövdeleri listeye ekle
        else:
            emailBody = msg.get_payload(decode=True).decode()
            emailBodies.append(emailBody)  # Gövdeleri listeye ekle

        print("Date:", date_str)
        print("Content:", emailBody)
        print()

    imap.close()
    imap.logout()

    return emailBodies, dateStrings  # emailBodies ve dateStrings listelerini döndür


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

        self.fromEmail = QLineEdit()
        self.fromEmail.setPlaceholderText("Email adresi gir")
        self.layout.addWidget(self.fromEmail)


        self.searchButton = QPushButton("Ara")
        self.searchButton.clicked.connect(self.search)
        self.layout.addWidget(self.searchButton)


    def showEmail(self, date_str, emailBody):
        self.textEdit.append(f"Date: {date_str}\nContent: {emailBody}\n")

    def search(self):
        whichEmmail = self.fromEmail.text()
        emailBodies, dateStrings = imapFunc(whichEmmail)
        for emailBody, date_str in zip(emailBodies, dateStrings):  # emailBodies ve dateStrings listelerini eşleştir
            self.showEmail(date_str, emailBody)
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
