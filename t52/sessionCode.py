import pickle
import base64

print base64.b64decode(open("sessions/edd3378b9db950d914d2cceb6d668b26f355c2eb").read())

x = base64.b64decode(open("sessions/edd3378b9db950d914d2cceb6d668b26f355c2eb").read())

print pickle.loads(x)

