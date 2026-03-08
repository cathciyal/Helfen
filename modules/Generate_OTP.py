import msg91_sms as msgsms

msg = msgsms.Cspd_msg91(apikey='YOUR MSG91 API KEY')
sms_txt = "This is a text SMS from MSG91"
send_sms_resp = msg.send(4,'TXTIN','919999999999',sms_txt)
print(send_sms_resp)
