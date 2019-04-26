#!/usr/bin/env python
#print "hello Again from fn.py"


import cgi
from google.appengine.api import mail

def process_cgi_form():
    form = cgi.FieldStorage()
    global email_address
    global character_limit
    (character_limit,email_address,msg_string)=(0,'','')
    if  form.has_key("character_limit"):
        character_limit = form['character_limit'].value
        character_limit = int(character_limit)
        #print "Character Limit:\t" + character_limit + "<BR>"
    if  form.has_key("email_address"):
        email_address = form['email_address'].value
        #print "Email Address:\t" + email_address + "<BR>"
    if  form.has_key("msg"):
        msg = form['msg'].value
        msg_string = msg
    if  form.has_key("Test_Character_Limit"):
        Test_Character_Limit = form['Test_Character_Limit'].value
        print "<BR>Test_Character_Limit:\t" + Test_Character_Limit
        send_test()
    if  form.has_key("Verify_Email_Character_Length"):
        Test_Character_Limit = form['Test_Character_Limit'].value
        print "<BR>Verify_Email_Character_Length:\t" + Verify_Email_Character_Length
        verify_character()
        # create custom form to take the last 3 digits and return what limit is
        #print "msg\t" + msg + "<BR>"
    return (character_limit,email_address,msg_string)

def verify_character():
    print "verify_character function"

def splitmessage_by_words (msg_string, number_each_msg,email_address,from_email):
    print "<BR>email_address:\t" + email_address
    if number_each_msg == 0:
        number_each_msg = 1
    print "<BR>number_each_msg:\t" + str(number_each_msg)
    msg_string = msg_string.replace("  ",' ')
    msg_string = msg_string .replace('\n','')
    msg_string = msg_string.strip()
    str_increment = number_each_msg
    number_of_messages = (len(msg_string)/number_each_msg)+1
    print "<BR>number_of_messages:\t" + str(number_of_messages)
    email_body = ''
    msg_list = msg_string.split()
    subject = (' ').join(msg_list[0:5])
    i=0
    word_number=0
    for word in msg_list:
        word_number +=1
        if len (email_body + " " + word) <= character_limit:
            email_body += " " + word
            if word_number==len(msg_list):
                i+=1
                email_body = email_body.strip()
                increment_subject = str(i) + ": " + subject
                print "<BR>" + increment_subject
                print "<BR>"  + email_body
                send_msg (increment_subject,email_body,email_address,from_email)
        else:
            i+=1
            email_body = email_body.strip()
            increment_subject = str(i) + ": " + subject
            print "<BR>" + increment_subject
            print "<BR>"  + email_body
            send_msg (increment_subject,email_body,email_address,from_email)
            email_body = ''
def send_test():
    t= open('t').read()
    send_msg ("test character limit",t, email_address,from_email)
            
def send_msg(subject,email_body,email_address,from_email):
    #print "subject:\n" + subject + '\n'
    #print "<BR><B>email_body</B>" + email_body + '\n'
    #return "True"
    #print "<BR>DMJ mail function email:" + email_address
    mail.send_mail(sender=from_email,to="cell <" + email_address + ">", subject=subject, body=email_body)
#              to="Albert Johnson <Albert.Johnson@example.com>",

def get_user():
    from google.appengine.api import users
    user = users.get_current_user()
    if user:
        #self.response.headers['Content-Type'] = 'text/plain'
        print "welcome ", user.nickname()
        #self.response.out.write('Hello, ' + user.nickname())
        from_email = user.email()
        print "this is your email " + from_email
        print '<BR>If you want to logout, click <a href="' + users.create_logout_url("/") + '">Log off my account.</a>'
        return from_email
    else:
        greeting = ("<a href=\"%s\">Sign in or register</a> to use the extended features that do not exist yet." %users.create_login_url("/"))
        #print "greeting is next.<BR>"
        print greeting
        #users.create_login_url(self.request.uri))
        #if "None" in user:
        print "<BR>You are not yet logged in. in the future, you should login b/c we will save your character limit and phone's email address for future visits."
        from_email= "not possible"
        return from_email

html_form_verify_character_length="""<FORM>
<input type="text" name="email_address" value="8133009639@tmomail.net"/>"""

#GOOGLE TABLE should contain username, destination address, and limit for that address
import datetime 
from google.appengine.ext import db 
from google.appengine.api import users
class messages(db.Model): 
    name = db.StringProperty(required=True) 
    possible_email=db.StringProperty()
    char_limit=db.StringProperty()
e = messages(name="David",possible_email="8133009639@tmomail.net", char_limit="1500" ) 
e.put()