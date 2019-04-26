<link rel="stylesheet" type="text/css" href="../www.css">
<TITLE>Julia Cheat Sheet</TITLE>
# [Julia](https://docs.julialang.org/en/stable/)
# (Julia)[https://docs.julialang.org/en/stable/]

looks like they don't use dot notation to call methods?

To start with 

    	zmq_socket.connect(zmq_tcp1) 

is not Julia syntax, correct syntax is 

    	connect(zmq_socket, zmq_tcp1) 

In other words, you don't invoke method of an object with 1 argument, but instead invoke a function with 2 arguments.