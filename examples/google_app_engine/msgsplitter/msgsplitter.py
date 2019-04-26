#!/usr/bin/env python
print "Content-Type: text/html\r\n"
msg_string = ''
#number_each_msg = 700
execfile('fn.py')
header = """\n<html>
\n<HEAD>
\n<TITLE>Split the message to your phone's email!</TITLE>
\n</HEAD>
\n<body>
<h1>It is very simple to use.</h1>
<h4>
<UL>we just need <LI>your phone's email address, this is the destination</LI>
<LI>the length each message should be (# of characters you want per message), and , of course,</LI>
<LI>the message you want to split into pieces (this is the actual data being sent).</LI>
</UL>
</h4>
<BR>Now you can send you phone long messages and know that the entire message will reach the phone.
<BR>this webapp was created b/c messages often get truncated when emailed to our phones.
<BR>this application will divide the message up into parts that can fit on your phone (just be sure to give the right 'character limit' below).
the message will show up in your sent items of your GMAIL account. however, this app is safe in that it does not have any access to read the emails.
<HR>"""

form_input  = """<p>Enter 3 things:
<BR>1) the character limit of your phone
<BR>2) your phone's email
<BR>3) the message
</p>
\n<form name="input" action="/msgsplitter.py" method="POST">
\n<input type="SUBMIT" name="Submit">   
\nCharacter Limit: <input type="text" name="character_limit" value="1500" />
\n
\n<BR>Email address of phone:
\n<input type="text" name="email_address" size="25"/>
\n<BR>Full message (this will be split up into increments equal to the limit you typed above.)

\n<BR><textarea name="msg" rows="20" cols="120">"""

form_input += msg_string
form_input += """
\n</textarea>
\n<BR>
\n<input type="SUBMIT" name="Submit">
\n<input type="SUBMIT" name="Test_Character_Limit" value="Test Character Limit - not yet working!">
\n<input type="RESET" name="RESET">
</form>"""

footer = """\n</body></html> """

print header
from_email = get_user()
(character_limit,email_address,msg_string)=process_cgi_form()
#if email_address !='':
#splitmessage(msg_string, character_limit)
if email_address !='' and from_email !="not possible":
    splitmessage_by_words (msg_string, character_limit,email_address,from_email)
if email_address !='' and from_email =="not possible":
    print "<P><B><FONT COLOR=RED> sorry, but to send the message, we need you to login. <BR>the message gets sent from your gmail account.</FONT></B>"
#send_test()
print form_input 
print footer