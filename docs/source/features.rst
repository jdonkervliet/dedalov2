
.. toctree::
   :maxdepth: 1
   :caption: Contents:

Features
========

Below are descriptions of the important dedalov2 features.
All of them are controlled by passing parameters to dedalov2's *explain* method.
All of them, except prefixes_, change the search behavior of the system.

Changing the Search Heuristic
-----------------------------

You can change the search behavior of dedalov2 by choosing a search heuristic.
Currently, dedalov2 offers three search heuristics: *entropy*, *longest path first*, and *shortest path first*.
Each of these heuristics is explained below.
If you haven't done so already, it is recommended to read about Paths_ first.

.. _Paths: background.rst

Entropy
~~~~~~~

In information theory, entropy is defined as

.. math::

   S = - \sum_{i}P_{i}\log {P_{i}}

Dedalov2 adapts this function to calculate the entropy of a path, :math:`p`.
It does this by considering as its outcomes all explanations that use the path [e.g., :math:`\{e : e = (p,o_i) \}`].
For each of these outcomes, it calculates its probability as the the number of roots it has divided by the total number of examples [e.g., :math:`\frac{|R(p,o)|}{|E|}`].
Entropy can be calculated using different bases for its logaritm.
To stay consistent with previous work, dedalov2 uses the base 10 logarithm.
This results in the path evaluation function below.

.. math::

   S(p) = - \sum_o \frac{|R(p,o)|}{|E|} \log_{10} \frac{|R(p,o)|}{|E|}

In code, the result looks like:

.. code:: python

   def entropy(p: Path, examples: Examples) -> float:
      res: float = 0
      for obj in p.get_end_points():
         num_roots = len(p.get_starting_points_connected_to_endpoint(obj))
         frac = num_roots/len(examples)
         res -= frac * math.log10(frac)
      return res

Longest Path First
~~~~~~~~~~~~~~~~~~

This search heuristic assigns higher scores to longer paths.
This causes a depth-first-search-like behavior,
extending a single path as long as possible before backtracking to previous ones.

Shortest Path First
~~~~~~~~~~~~~~~~~~~

This search heuristic assigns higher scores to shorter paths.
This causes a breadth-first-search-like behavior,
first extending all paths of the shortest length before selecting a longer path.
This approach causes the search frontier to quickly increase in size.
When using a large HDT file, consider using
explicit memory usage limits to prevent MemoryErrors.

Pruning Search Paths
--------------------

By default, Dedalov2 applies branch pruning to reduce the amount of work
it needs to do. You can turn this off, or reduce its effect, by
selecting a different branch pruning method. There are currently five
such methods available.

+-----------------------+-----------------------+-----------------------+
| Policy                | Short Name            | Description           |
+=======================+=======================+=======================+
| global-less-equal     | gle                   | Prune path if it can  |
| **(default)**         |                       | only yield            |
|                       |                       | explanations with     |
|                       |                       | scores less *or       |
|                       |                       | equal* than the       |
|                       |                       | current global        |
|                       |                       | maximum.              |
+-----------------------+-----------------------+-----------------------+
| global-less           | gl                    | Prune path if it can  |
|                       |                       | only yield            |
|                       |                       | explanations with     |
|                       |                       | scores less than the  |
|                       |                       | current global        |
|                       |                       | maximum.              |
+-----------------------+-----------------------+-----------------------+
| path-less-equal       | ple                   | Prune path if it can  |
|                       |                       | only yield            |
|                       |                       | explanations with     |
|                       |                       | scores less or equal  |
|                       |                       | than the current      |
|                       |                       | *path* maximum.       |
+-----------------------+-----------------------+-----------------------+
| path-less             | pl                    | Prune path if it can  |
|                       |                       | only yield            |
|                       |                       | explanations with     |
|                       |                       | scores less than the  |
|                       |                       | current *path*        |
|                       |                       | maximum.              |
+-----------------------+-----------------------+-----------------------+
| off                   | off                   | Don’t prune branches. |
|                       |                       | *Warning:* this can   |
|                       |                       | result in large       |
|                       |                       | numbers of results    |
|                       |                       | and long computation  |
|                       |                       | times.                |
+-----------------------+-----------------------+-----------------------+

You can change the path pruning policy by passing it as a parameter.

.. code:: python

   ddl.explain("the-internet.hdt", "abba.txt", prune="ple")

Blacklisting URIs
-----------------

Some predicates are too common or too unreliable to yield good explanations.
In such cases, you can blacklist these predicates by passing to dedalov2 a file with blacklisted URIs.

blacklist.txt:

::

   http://www.w3.org/2000/01/rdf-schema#label
   http://www.w3.org/2002/07/owl#sameAs
   http://www.w3.org/2004/02/skos/core#altLabel

Pass blacklist via parameter of the same name:

.. code:: python

   ddl.explain("the-internet.hdt", "abba.txt", blacklist="blacklist.txt")

.. _prefixes:

Using URI Prefixes
------------------

The long URIs in the results make them hard to read. Dedalov2 supports
URI prefixes. Simply pass your file with prefixes as a parameter.

.. code:: python

   import dedalov2 as ddl

   for explanation in ddl.explain("the-internet.hdt",
                                  "abba.txt",
                                  minimum_score=1,
                                  groupid=1,
                                  prefix="prefix.txt"):
       print(explanation)

Results in

::

   dbpedia2:label -| dbpedia:Polar_Music
   dbpedia2:associatedActs -| dbpedia:ABBA
   dbpedia2:wikilink -| dbpedia:Anni-Frid_Lyngstad
   skos:subject -| dbpedia:Category:ABBA_members
   dbpedia2:wikilink -| dbpedia:Cher
   dbpedia2:wikilink -| dbpedia:Polar_Music
   dbpo:associatedBand -| dbpedia:ABBA
   dbpo:associatedMusicalArtist -| dbpedia:ABBA
   dbpedia2:wikilink -| dbpedia:Svensktoppen
   dbpedia2:wikilink -| dbpedia:Eurovision_Song_Contest
   dbpedia2:wikilink -| dbpedia:ABBA
   dbpedia2:wikiPageUsesTemplate -| dbpedia:Template:infobox_musical_artist
   dbpedia2:wikilink -| dbpedia:Rik_Mayall
   dbpo:label -| dbpedia:Polar_Music

Where ``prefix.txt`` is a tab-separated file that looks like:

::

   madsrdf http://www.loc.gov/mads/rdf/v1#
   bflc    http://id.loc.gov/ontologies/bflc/
   rdf http://www.w3.org/1999/02/22-rdf-syntax-ns#
   foaf    http://xmlns.com/foaf/0.1/
   yago    http://yago-knowledge.org/resource/
   rdfs    http://www.w3.org/2000/01/rdf-schema#
   dbo http://dbpedia.org/ontology/
   dbp http://dbpedia.org/property/
   dc  http://purl.org/dc/elements/1.1/
   gr  http://purl.org/goodrelations/v1#
   ...

Don’t write this file yourself. Download one from
http://prefix.cc/popular.

Handling Large Input Files
----------------------------------

Using a large example files as input has two significant drawbacks.
Below are descriptions of these drawbacks,
and how you can deal with them.

Firstly, the time required to find good explanations will go up.
For every explanation, dedalov2 has to check to which examples it connects.
Having more examples means more checks.
Dedalov2 allows you to truncate the input file to reduce the number of input examples without having to modify the input file.
This makes finding the right number of examples to include by trial-and-error much easier.

.. code:: python

   ddl.explain("the-internet.hdt", "abba.txt", truncate=10)

Using truncate with a value of 10 means that the algorithm will use 10 positive examples and 10 negative examples.
If the number of positive or negative examples in the input file is lower than 10, it will use all of them.

Secondly,
the ratio of positive/negative examples may affect the search heuristic.
For example, the entropy path heuristic prioritizes paths that are, more or less,
equally connected to positive and negative examples.
If the number of positive, or negative, examples in the input file is much larger than the others,
the entropy search heuristic may select different paths.

To prevent this, dedalov2 by default limits the number of positive and negative examples to the size of the smallest group.
You can disable this by using the balance parameter.

.. code:: python

   ddl.explain("the-internet.hdt", "abba.txt", balance=False)

This allows the number of positive examples to differ from the number of negative examples.
