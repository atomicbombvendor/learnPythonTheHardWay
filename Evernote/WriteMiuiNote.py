from evernote.api.client import EvernoteClient


dev_token = "S=s1:U=94ba3:E=16bc1d282e1:C=1646a215618:P=1cd:A=en-devtoken:V=2:H=5f04a9b0b09058797124cbda0aaec89b"
client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
user = userStore.getUser()
print user.username

noteStore = client.get_note_store()
noteBooks = noteStore.listNotebooks()
for n in noteBooks:
    print n.name