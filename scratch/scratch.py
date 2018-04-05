# def config_email(self):
#     """
#     configures email IMAP authentication
#     """
#     mail = imaplib.IMAP4_SSL(self.config.STMP_SERVER)
#     mail.login(self.config.FROM_EMAIL, self.config.FROM_PWD)
#     mail.select('inbox')
#     type, data = mail.search(None, 'ALL')
#     mail_ids = data[0]
#     id_list = mail_ids.split()
#     latest_email_id = int(id_list[-1])
#     type, data = mail.fetch(str.encode(str(latest_email_id)), '(RFC822)')
#     for response in data:
#         if isinstance(response, tuple):
#             msg = email.message_from_string(response[1].decode())
#             email_subject = msg['subject']
#             email_from = msg['from']
#             for message_data in msg.get_payload():
#                 print(message_data)
#     return
