# Dedalo

Dedalo explains why a set of URIs belongs together.

## Example

Have a look at the example below and get going in seconds!

We'll use the file `abba.txt` as input. Its contents are:

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

[Using URI prefixes](#using-uri-prefixes) makes the output look better. To learn more about what the input and output means, please read  the [background section](#background).

## Installation

Dedalov2 requires Python 3 and can be installed using Python's package manager, pip.

```bash
pip install dedalov2
```

Depending on your use case, you may want to pass the `-U` flag or run this in a virtual environment.

## Documentation

See the [documentation page](https://dedalov2.readthedocs.io/en/latest/index.html) for more examples.

## Background

