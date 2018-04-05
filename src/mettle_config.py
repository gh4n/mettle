class MettleConfig:
    def __init__(self):
        self.db_email = "hgrace503@gmail.com"
        self.db_pwd = "hello30"
        self.ORG_EMAIL = "@gmail.com"
        self.FROM_EMAIL = "zrggyr"+self.ORG_EMAIL
        self.FROM_PWD = "mettle30"
        self.STMP_SERVER = "imap.gmail.com"
        self.STMP_PORT = 993

    def config_db(self):
        return {
            "apiKey": "AIzaSyCsWK-fZ8sQIg3ReJjderS58_b_hZSNjmg",
            "authDomain": "mlticket-6a2a8.firebaseapp.com",
            "databaseURL": "https://mlticket-6a2a8.firebaseio.com",
            "storageBucket": "",
        }

if __name__ == "__main__":
    mc = MettleConfig()
    count = mc.get_count()
    print(count)
    mc.set_count(5)
    print(mc.get_count())