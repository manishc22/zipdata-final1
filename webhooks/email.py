# import smtplib
# import ssl
import resend

resend.api_key = "re_72fX7G37_3SsPd4XpzthsRrBZhs1Dbfev"


def send_email():

    r = resend.Emails.send({
        "from": "manish@zipdata.ai",
        "to": "manish.chaturvedi@gmail.com",
        "subject": "Hello World",
        "html": "<p>Congrats on sending your <strong>second email</strong>!</p>"
    })
    return r
