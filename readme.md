SimpleStats
===========

SimpleStats is a simple twisted web/tcp server that receives data,
sent as JSON tuples

    ["var_name", timestamp, value]

(where timestamp is specified as seconds since the epoch, UTC time); the data is stored in memory and displayed via web, where you can also filter values and
import/export data.

SimpleStats is a simple example of a twisted server. It also uses:

 * Bootstrap (http://twitter.github.com/bootstrap/)
 * jQuery (http://jquery.com/)
 * Flot (http://code.google.com/p/flot/)

Get SimpleStats
---------------

    $ git clone git://github.com/matiasb/simplestats.git


How to set up SimpleStats?
--------------------------

The only requirement is to have Twisted >= 11.0 installed.

You can also create a virtualenv[1], activate it and install dependencies:

    $ cd simplestats
    $ wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    $ python virtualenv.py env
    $ . env/bin/activate
    $ pip install -r requirements.txt


Running SimpleStats
-------------------

    $ python server/main.py

After this, you should be able to point your browser to:

    http://localhost:8080/

and also connect via telnet:

    $ telnet 127.0.0.1 8007

You can change server ports settings in server/settings.py.

Telnet Example Session
----------------------

    $ telnet 127.0.0.1 8007
    Trying 127.0.0.1...
    Connected to 127.0.0.1.
    Escape character is '^]'.
    --Hint: send data of the form [name:str, timestamp:float, data:float]
    ["var1", 1322721979, 8]
    --OK

Notice the expected row value format.

Running the Tests
-----------------

To run the server test suite:

    $ trial server

Samples Generator
-----------------

You will find a simple script to generate random samples that could be used
as input for simplestats:

    $ python misc/sample_generator.py 10 

You can specify the number of samples to return (10 in the example above,
20 by default). Each row will get a random timestamp in the last 7 days.

[1] http://www.virtualenv.org/
