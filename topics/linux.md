<link rel="stylesheet" type="text/css" href="../www.css">
<a name="LINUX">LINUX:</a>

- <a href="#tmux">Tmux</a>

## remote view of apps?

need to view GUI from remote linux box on windows or other linux machine?  
if xserver is running on the 'viewer', the app should pop up. 

- do method 1 or 2 from below
  - method 1 (simplest method) 
    - use '-X' via ssh, e.g. '`ssh -X IP`' , 
  - method 2: 
    - `ssh` to the remote linux box
    - `export DISPLAY:$IP_OF_MACHINE_TO_VIEW:0.0`
- then run the program.
- it should appear locally. 

MobaXterm is something you would want to install and have running on windows if the viewing machine is a windows box.

## linux permissions

    Permissions (they are additive)
      1 x
      2 w
      3 wx 
      4 r
      5 rx
      6 rw
      7 rwx

## some linux commands

    sudo /etc/init.d/httpd restart
    find ../ -name *wsgi

on windows , to grep for more than one word, use '\' before '|'

    grep "id\|li_" templates\treatments.html

to use '`less`' like 'tail -f', 
  `"Shift-F"`



## <a name="tmux">Tmux</a>

to split into left/right sides, CTRL-B (which is always the prefix), followed by SHIFT 5 (to get %).   
NOTE: use SHIFT to get the symbols like `%{}` working. 


