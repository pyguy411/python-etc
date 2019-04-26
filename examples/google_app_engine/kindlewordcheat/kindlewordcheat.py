import itertools, sys, os, cgi, time
import cgitb; cgitb.enable()
def process_cgi_form(form):
    dict_data = {}
    if form.has_key('word'):
        word = form.getlist("word")
        dict_data['word']=word
    if form.has_key('word_len'):
        word_len = form.getlist("word_len")
        word_len = int(word_len[0])
        dict_data['word_len']=word_len
    return dict_data    
def fun_createcombination(word,word_len):
    #print (word,word_len)
    y=itertools.permutations (word,word_len) 
    n=[] # list for the potential words
    for i in y:
        #print 'i' + str(i)
        word = ('').join(i)
        n.append(word)
    #print "completed:\tfun_createcombination"
    #print str(n)
    n.sort()
    return n
def validateword(word):
    #lookup the word on google if does not already exist
    uri = "/dictionary/wordlistop?q=" + word + "&sl=en&tl=en&action=lookupword"
    word_valid = False
    #print uri
    known_valid_words = ["fucare",'fuc','eafcur','careful','ahppy','happy','cfrleua']
    if word in known_valid_words:
        word_valid = True
    else:
        return True     
HTMLform="""Content-Type: text/plain\n\n<HTML>\n<TITLE>get hints for Kindle word</TITLE>\n<BODY>\n
<form action="kindlewordcheat.py" method="GET" enctype="multipart/form-data">\n
WORD:<INPUT type="text" name="word" size="30" value="careful">\n
<INPUT type="text" name="word_len" size="3" value="6">\n
<input name="Submit" type="submit" value="Show Possible Words">\n
</form>""" 
print HTMLform

form = cgi.FieldtSorage()
cgi_dict_data = process_cgi_form(form)
#print str(cgi_dict_data)
if cgi_dict_data.has_key('word') and cgi_dict_data.has_key('word_len'): # this relates to the refresh mechanism
    word = cgi_dict_data['word'] 
    #print "<br>word was " + str(word[0])
    word_len = cgi_dict_data['word_len']
    #word_len = len(word[0]) #6  # sys.argv[2]
    #print (word,word_len)
    n = fun_createcombination (word[0],word_len)
    #print type(n)
    li_valid_words=[]
    print str(len(n)) + " potential words found!<BR>"
    for i in n:
        word = i 
        #print "<li>" + word
        print word
        response = validateword(word)
        if response == True:
            li_valid_words.append((word))
else:
    pass
    
print "</BODY></HTML>"

    
