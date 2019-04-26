`tp` is short for Thought Pad. 
it writes ideas to a quick thoughts file . 
it will also help you find them.

https://pypi.org/project/thought-pad/

    pip install thought-pad

it deliberately does not use argparse, b/c it's supposed to be easy to use, 
not bog you down with --flags.  
Who wants to type flags when it's already so simple?

how does it work?

### put the tp.py file in your path 

you might have to dig around your site-packages folder to find it (sorry)
future versions in pypi will install to your path. 

#### create an alias 

    alias tp='python <path to tp.py>'

or if the file tp.py is in your path, you can make it simpler

    alias tp='python tp.py'

from command line, simply type:
one of these accepted commands:

    ('x', 'v', 'f', 'h', 'e')

each letter stands for an action to take on the file.

- v = View the file (think 'cat' on a file to see the whole thing)
- f = Find 
- x = similar to find, but more eXact (e.g. case sensitive)
- e = Edit the file (this script uses vim but notepad also works.)

if no command is specified, it defaults to "append" mode, which will add to the file.  
this is the most common use case for me anyway.


you can try to read through the script to see how it works or just follow these examples:

#### want to add a line to the file?
just type the alias or the full path as shown below and then your message.
i like to prefix my messages with a topic to make it easier to find later.
below 

    python tp.py  python:how can i learn python? google PEP8

if your "thought" contains a single quote, wrap the entire thought in double quotes:

    tp "python: Guido didn't say he would never return though. or did he?"    

#### search capability
later i can search the file for all python related "thoughts"

    tp  f python

#### results in:

    0 2019-04-25 python:how can i learn python? google PEP8
    1 2019-04-25 python:who is the BDFL? it was Guido, but no more!
    2 2019-04-25 python: he didn't say he quit though


## use cases
- want to track when you start or stop something or anything arbitrary that 
you think you might want to search for again later?
- want to be able to find a project billing number quickly?
- want to recall the syntax for a particular command that you figured out, 
but don't use enough to keep in the forefront of you mind?
- the list can go on and on...

## why does this exist?
i was curious about the process to publish python package to pypi.org.

the original name was quickthought, qt.py, but i decided to use tp.py for this.
this script is ugly and should be refactored, but works flawlessly. 
it was written by me years ago, but only recently published to pypi.

