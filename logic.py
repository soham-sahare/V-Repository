import email.message as em
import smtplib

def send_mail(TO, EMAIL_ADDRESS, EMAIL_PASSWORD, username, password):

    msgstr = '''<h1 style="text-align: center;"><font face="Tahoma">Faculty Repository System&nbsp;</font></h1><div><font size="4" face="Tahoma">We've got a request to change your account password.</font></div><div><font size="4" face="Tahoma">If this wasn't done by you, please contact us immediately so we can sort this out.</font></div><div><font size="4" face="Tahoma">Your temporary password is -</font></div><div><font size="4" face="Tahoma"><br></font></div><div><font face="Tahoma" size="4">Username: {}</font></div><div><font face="Tahoma" size="4">Password: {}</font></div><div><font face="Tahoma" size="4"><br></font></div><div><font face="Tahoma" size="4">You can't login with your old password.</font></div><div><font face="Tahoma" size="4">You can later change this password after you have logged in by clicking on hamburger menu in right-bottom corner.</font></div><div><font size="4" face="Tahoma"><br></font></div><div><font size="4" face="Tahoma">Regards,&nbsp;</font></div><div><a href="#"><font size="4" face="Tahoma">@faculty_repository_system</font></a></div>'''.format(username, password)

    msg = em.Message()
    msg['Subject'] = 'Password change request'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(msgstr)

    s = smtplib.SMTP("smtp.outlook.com", 587)
    s.starttls()

    s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    s.sendmail(EMAIL_ADDRESS, TO, msg.as_string())
    s.quit()

def send_mail_danger(TO, EMAIL_ADDRESS, EMAIL_PASSWORD):

    msgstr = '''<h1 style="text-align: center;"><font face="Tahoma">Faculty Repository System&nbsp;</font></h1><div><font size="4" face="Tahoma">We've changed your account password.</font></div><div><font size="4" face="Tahoma">If this was you, then you can safely ignore this mail.</font></div><div><font face="Tahoma" size="4"><br></font></div><div><font face="Tahoma" size="4">If this wasn't you, your account can be compromised, please reset your password <a href="#">RESET</a></font></div><div><font size="4" face="Tahoma"><br></font></div><div><font size="4" face="Tahoma">Regards,&nbsp;</font></div><div><a href="#"><font size="4" face="Tahoma">@faculty_repository_system</font></a></div>'''

    msg = em.Message()
    msg['Subject'] = 'Password Changed'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(msgstr)

    s = smtplib.SMTP("smtp.outlook.com", 587)
    s.starttls()

    s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    s.sendmail(EMAIL_ADDRESS, TO, msg.as_string())
    s.quit()

def send_mail_certificate(TO, EMAIL_ADDRESS, EMAIL_PASSWORD, name, title, source, duration, year):

    msgstr = '''<h1 style="text-align: center;"><font face="Tahoma">Faculty Repository System&nbsp;</font></h1><div><font size="4" face="Tahoma">We've seen an activity, you have uploaded a certificate as follows -&nbsp;&nbsp;</font></div><div><font size="4" face="Tahoma"><br></font></div><div><font size="4" face="Tahoma">Name : {}</font></div><div><font size="4" face="Tahoma">Title : {}</font></div><div><font size="4" face="Tahoma">Source : {}</font></div><div><font size="4" face="Tahoma">Duration : {}</font></div><div><font size="4" face="Tahoma">Year : {}</font></div><div><font size="4" face="Tahoma"><br></font></div><div><font size="4" face="Tahoma">If this was you, then you can safely ignore this mail.</font></div><div><font face="Tahoma" size="4"><br></font></div><div><font face="Tahoma" size="4">If this wasn't you, your account can be compromised, please reset your password <a href="#">RESET</a></font></div><div><font size="4" face="Tahoma"><br></font></div><div><font size="4" face="Tahoma">Regards,&nbsp;</font></div><div><a href="#"><font size="4" face="Tahoma">@faculty_repository_system</font></a></div>'''''.format(name, title, source, duration, year)

    msg = em.Message()
    msg['Subject'] = 'Certificate Uploaded'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(msgstr)

    s = smtplib.SMTP("smtp.outlook.com", 587)
    s.starttls()

    s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    s.sendmail(EMAIL_ADDRESS, TO, msg.as_string())
    s.quit()