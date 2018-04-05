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

def incr_aggr(self, category):
    na = self.db.child("analytics").child("aggregate_all").get().val()
    print(na)
    na += 1
    self.db.child("analytics").update({"aggregate_all": na})

    na_category = self.db.child("analytics").child("category_all").child(category).get().val()
    na_category += 1
    self.db.child("analytics").child("category_all").update({category: na_category})
    return


def incr_corrected(self, category):
    nc = self.db.child("analytics").child("aggregate_corrected").get().val()
    nc += 1
    self.db.child("analytics").child("aggregate_corrected").update(nc)

    nc_category = self.db.child("analytics").child("category_corrected").child(category).get().val
    nc_category += 1
    self.db.child("analytics").child("category_corrected").child(category).update(nc_category)
    return
