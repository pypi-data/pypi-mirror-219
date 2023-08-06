####
Owly
####

Set of utilities related to ontologies and their management.

.. code-block:: python

    endpoint = Endpoint("https://example.com/dataset/")
    result = endpoint.perform_query("""SELECT ?subject ?predicate ?object WHERE { ?subject ?predicate ?object } LIMIT 5""")
    print(result.as_text())


Installation
------------

.. code-block:: shell

   pip install owly
