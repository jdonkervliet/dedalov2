
## Features

### Changing the Search Heuristic

### Pruning Search Paths

By default, Dedalov2 applies branch pruning to reduce the amount of work it needs to do. You can turn this off, or reduce its effect, by selecting a different branch pruning method. There are currently five such methods available.

| Policy | Description |
|:--|:--|
| **global-less-equal** | Prune path if it can only yield explanations with scores less _or equal_ than the current global maximum.  |
| global-less | Prune path if it can only yield explanations with scores less than the current global maximum. |
| path-less-equal | Prune path if it can only yield explanations with scores less or equal than the current _path_ maximum. |
| path-less | Prune path if it can only yield explanations with scores less than the current _path_ maximum. |
| off | Don't prune branches. _Warning:_ this can result in large numbers of results and long computation times. |

You can change the path pruning policy by passing it as a parameter.

```python
ddl.explain("the-internet.hdt", "abba.txt", prune="path-less-equal")
```

### Using URI Prefixes

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

Where `prefix.txt` is a tab-separated file that looks like:

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

### Blacklisting URIs

### Handling Large Input Files