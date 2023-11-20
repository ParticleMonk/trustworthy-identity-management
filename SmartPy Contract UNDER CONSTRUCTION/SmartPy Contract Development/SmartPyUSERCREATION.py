import smartpy as sp

class UserContract(sp.Contract):
    def __init__(self):
        self.init(
            users = sp.big_map(tkey = sp.TString, tvalue = sp.TRecord(name = sp.TString, email = sp.TString, password = sp.TString))
        )

    @sp.entry_point
    def addUser(self, params):
        sp.verify(~ self.data.users.contains(params.email), message = "Email already exists")
        self.data.users[params.email] = sp.record(name = params.name, email = params.email, password = params.password)

    @sp.entry_point
    def removeUser(self, params):
        sp.verify(self.data.users.contains(params.email), message = "Email does not exist")
        del self.data.users[params.email]

