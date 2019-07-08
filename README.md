# Dedalo

Dedalo explains why a set of URIs belongs together.

## Installation

Dedalov2 requires Python 3 and can be installed using Python's package manager, pip.

```bash
pip install dedalov2
```

Depending on your use case, you may want to pass the `-U` flag or run this in a virtual environment.

## Examples

Have a look at the examples below and get going in seconds! The first example shows the main feature of this library and contains input and output details. The remaining examples show off more advanced features.

### Full Example

For the examples below, we'll use the file `abba.txt` as input. Its contents are:

```
1,http://dbpedia.org/resource/Benny_Andersson
1,http://dbpedia.org/resource/Björn_Ulvaeus
1,http://dbpedia.org/resource/Agnetha_Fältskog
1,http://dbpedia.org/resource/Anni-Frid_Lyngstad
2,http://dbpedia.org/resource/Linus_Torvalds
2,http://dbpedia.org/resource/Avicii
2,http://dbpedia.org/resource/Stellan_Skarsgård
2,http://dbpedia.org/resource/Markus_Persson
```

The number at the start of each line indicates the _group_ the URI belongs to. You can use any number you like, as long as it's an integer.

You can use the following code to explain group 1.

```python
import dedalov2 as ddl

for explanation in ddl.explain("the-internet.hdt",
                               "abba.txt",
                               minimum_score=1,
                               groupid=1):
    print(explanation)
```

The results depend on the `hdt` file you're using. If it includes URIs from DBPedia, the results look something like this:

```
http://dbpedia.org/property/label -| http://dbpedia.org/resource/Polar_Music
http://dbpedia.org/property/associatedActs -| http://dbpedia.org/resource/ABBA
http://dbpedia.org/property/wikilink -| http://dbpedia.org/resource/Anni-Frid_Lyngstad
http://www.w3.org/2004/02/skos/core#subject -| http://dbpedia.org/resource/Category:ABBA_members
http://dbpedia.org/property/wikilink -| http://dbpedia.org/resource/Cher
http://dbpedia.org/property/wikilink -| http://dbpedia.org/resource/Polar_Music
http://dbpedia.org/ontology/associatedBand -| http://dbpedia.org/resource/ABBA
http://dbpedia.org/ontology/associatedMusicalArtist -| http://dbpedia.org/resource/ABBA
http://dbpedia.org/property/wikilink -| http://dbpedia.org/resource/Svensktoppen
http://dbpedia.org/property/wikilink -| http://dbpedia.org/resource/Eurovision_Song_Contest
http://dbpedia.org/property/wikilink -| http://dbpedia.org/resource/ABBA
http://dbpedia.org/property/wikiPageUsesTemplate -| http://dbpedia.org/resource/Template:infobox_musical_artist
http://dbpedia.org/property/wikilink -| http://dbpedia.org/resource/Rik_Mayall
http://dbpedia.org/ontology/label -| http://dbpedia.org/resource/Polar_Music
```

To learn more about what the input and output means, please read  the [background section](#background).

### Advanced Features

#### Changing the Search Heuristic

#### Pruning Search Paths

By default, Dedalov2 applies branch pruning to reduce the amount of work it needs to do. You can turn this off, or reduce its effects, by selecting a different branch pruning method. There are currently four such methods available.

1. maxge: Only follow a path if it can lead to an explana
2. maxg": prune_max_score_greater,
3. pathge": prune_max_path_score_greater_equal,
4. pathg": prune_max_path_score_greater,

#### Using URI Prefixes

The long URIs in the results make them hard to read. Dedalov2 supports URI prefixes. Simply pass your file with prefixes as a parameter.

```python
import dedalov2 as ddl

for explanation in ddl.explain("the-internet.hdt",
                               "abba.txt",
                               minimum_score=1,
                               groupid=1,
                               prefix="prefix.txt"):
    print(explanation)
```

Results in

```
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
```

Where `prefix.txt` looks like:

```
madsrdf	http://www.loc.gov/mads/rdf/v1#
bflc	http://id.loc.gov/ontologies/bflc/
rdf	http://www.w3.org/1999/02/22-rdf-syntax-ns#
foaf	http://xmlns.com/foaf/0.1/
yago	http://yago-knowledge.org/resource/
rdfs	http://www.w3.org/2000/01/rdf-schema#
dbo	http://dbpedia.org/ontology/
dbp	http://dbpedia.org/property/
dc	http://purl.org/dc/elements/1.1/
gr	http://purl.org/goodrelations/v1#
...
```

Don't write this file yourself. Download one from [http://prefix.cc/popular](http://prefix.cc/popular).

#### Blacklisting URIs

#### Handling Large Input Files

## Documentation

## Background

