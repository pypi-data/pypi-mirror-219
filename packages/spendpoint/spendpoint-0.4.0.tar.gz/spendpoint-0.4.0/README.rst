##########
SpEndPoint
##########

Creates a SPARQL endpoint supporting custom services.
The default access point is at `http://127.0.0.1:8000`.
This endpoint can be configured in the `configuration.toml <data/configuration.toml>`_ file.
The docker image created uses uvicorn the host the application at `0.0.0.0:80`. Feel free to map this to any port of your liking.

We currently support 3 services out of the box:

.. code-block::

   dtf:outlier
   dtf:example
   dtf:conversion

The outlier service relies on `another endpoint <https://msdl.uantwerpen.be/git/lucasalbertins/DTDesign/src/main/tools/typeOperations>`_ which needs to be set up and accessible.

Installation
------------

..
   .. code-block:: shell

      pip install spendpoint

   or

.. code-block:: shell

   pip install --index-url https://pip:glpat-m8mNfhxZAUnWvy7rLS1x@git.rys.one/api/v4/projects/262/packages/pypi/simple --no-deps spendpoint

Configuration
-------------

A configuration file at `configuration.toml <data/configuration.toml>`_ holds all user configurable data.
You can set the `host` and `port` the server will listen on.
A more advanced use is to import extra services.
These services need to be defined in the `service.py` file as well.
