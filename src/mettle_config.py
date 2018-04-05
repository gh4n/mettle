class MettleConfig:
    def __init__(self):
        self.db_email = "hgrace503@gmail.com"
        self.db_pwd = "hello30"
        self.ORG_EMAIL = "@gmail.com"
        self.FROM_EMAIL = "zrggyr"+self.ORG_EMAIL
        self.FROM_PWD = "mettle30"
        self.STMP_SERVER = "imap.gmail.com"
        self.STMP_PORT = 993
        self.count_file = 'count.txt'

    def get_count(self):
        f = open(self.count_file, 'r')
        count = int(f.read())
        f.close()
        return count

    def set_count(self, new):
        count = self.get_count()
        print(count)
        f = open(self.count_file, 'w')
        print(count)
        f.write(new)
        f.close()
        return

if __name__ == "__main__":
    mc = MettleConfig()
    count = mc.get_count()
    print(count)
    mc.set_count(5)
    print(mc.get_count())