import smtplib
import obvescanje_settings

from_name = "K4"
 
def sendemail(from_addr, to_addr_list,
              subject, message,
              login, password,
              smtpserver='%s:%s' % (obvescanje_settings.MAIL_SENDER['server'], obvescanje_settings.MAIL_SENDER['port'])):
    header  = 'From: %s\n' % from_name
    header += 'To: %s\n' % ','.join(to_addr_list)
    #header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems
