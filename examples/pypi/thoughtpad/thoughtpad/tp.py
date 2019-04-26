#!python
"""
    tp is short for __Thought __Pad. 
    it writes ideas to a quick thoughts file . 
    it will also help you find them.
"""

import sys
import os
import datetime
import codecs
from subprocess import Popen, PIPE
import logging
if __name__ == "__main__":
#     import argparse
    logging.basicConfig(level=logging.DEBUG)
    qt_file_basename = 'chronicles.{}.txt'.format(os.environ['USER'])
    logger = logging.getLogger()
    logger.debug("args: %s" % sys.argv)
    DEBUG = 1
    try:
        folder = os.environ['USERPROFILE']  # would make it "Windows"
    except KeyError:
        # if 'linux' in sys.platform or 'darwin' in sys.platform:
        folder = os.environ['HOME']
    editor = 'vim'
    my_file = os.path.join(folder, qt_file_basename)
    if DEBUG:
        logger.debug(my_file)
        # sys.exit()
    logger.debug("len(sys.argv):%s" % len(sys.argv))
    if DEBUG:
        for i in sys.argv:
            print('arg:%s' % i)
    directive = ''
    long_string = ' '.join(sys.argv[1:])

    if '"' in long_string:
        logger.debug('quotes inside: %s', ' '.join(sys.argv))  # they get stripped, need to add them back by checking
        # if an arg can be split by spaces. if so, then it needs quotes added to front and back.

    accepted_commands = ('x', 'v', 'f', 'h', 'e')
    if len(sys.argv) == 1:
        directive = 'v'

    words = ''
    if len(sys.argv) > 1:
        if sys.argv[1] in accepted_commands:
            directive = sys.argv[1]
            if len(sys.argv) > 2:
                words = ' '.join(sys.argv[2:])  # words will either be searched for or added
        else:
            directive = 'a'
            words = ' '.join(sys.argv[1:])
    if ':' in words:
        (subject, rest) = words.split(':', 1)
    else:
        subject = "quick generic thought"
        rest = words
    logger.debug("directive:%s" % directive)
    if directive in ('v', 'x', 'f'):
        with codecs.open(my_file, encoding='utf-8', errors='ignore') as fh:
            for x, line in enumerate(fh):
                try:
                    #logger.debug(type(line))
                    line = line.strip()
                    # logger.debug(line)
                    if directive == 'v':
                        # print("%s - %s" % (x, line))
                        print(line)
                    elif directive == 'f':  # find any match
                        if len(sys.argv) == 3:
                            if words.lower() in line.lower():
                                print(str(x) + ' ' + line)
                        else:
                            for i in line.split():
                                if i.lower() in words.lower():
                                    print("found:%s" % i)
                                    print(str(x) + ' ' + line)
                                    break
                    elif directive == 'x':
                        if words.lower() in line.lower():
                            logger.debug(str(x) + ' ' + line)
                    # x += 1
                except:
                    logger.error("\n\nline # %s", x, exc_info=True)
                    input('waiting...')
    elif directive == 'h':
        logger.debug("options are %0 [v or e or f or x or a (implied if not specified)]")
        logger.debug("which amounts to View, Edit, Filter (look for word(s)), and eXact (just find it )")
    elif directive == 'a':  # this should not be default, default should be view all lines.
        dt = datetime.date.today().strftime('%Y-%m-%d')
        open(my_file, 'a').write(dt + ' ' + words + '\n')
        # blog_it = raw_input('blog this?').lower()
        # if 'y' == blog_it.lower():
        #     from subprocess import Popen, PIPE
        #
        #     try:
        #         args = ['google', 'blogger', 'post', '--title', subject, rest]
        #         logger.debug("what we sent:" + ' '.join(args))
        #         out, err = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
        #         logger.debug("out:%s" % out)
        #         if err:
        #             logger.debug("err:%s" % err)
        #     except:
        #         logger.debug(sys.exc_info())
    elif directive == 'e':  # edit the file
        args = [editor, my_file]
        logger.debug(args)
        out, err = Popen(args).communicate()
        logger.debug("out:%s" % out)
        if err:
            logger.debug("err:%s" % err)