# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC4751b0bd2565d31ad6613f70157b6348'
auth_token = '482053b1804c74336f7e63f8163767d1'

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="ALERTA. Caudal bajo",
                     from_='+12564826982',
                     #to='+14252456016'
                     #to='+56982643292' # pampi, funciona
                     to='+56961702696'
                 )

print(message.sid)