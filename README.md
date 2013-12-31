type-quotes
===========

Unix utility for feeding quotes to gtypist to type over.
Currently comes prepackaged with The Art of War (taow) and The Dhammapada (dhammapada)

Examples:
python type-quotes -f art
 => gives you 3 random art quotes to type through

python type-quotes -c 5 taow => type 5 quotes from Sun Tzu's Art of War


USAGE
usage: type-quotes.py [-h] [-c COUNT] [-f FORTUNE] [-j JSON] [LIBRARY]

positional arguments:
  LIBRARY               shortcut for "-j library/LIBRARY

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        number of quotes to type over. Default: 3
  -f FORTUNE, --fortune FORTUNE
                        a fortune file to quote. -j takes priority over -f
  -j JSON, --json JSON  a json file with the structure:
                            {
                                "title": "The Dhammapada",
                                "author": "Buddha",
                                "chapters": [ {
                                    "title" : "The Pairs",
                                    "quotes": [ "speak or act with a peaceful mind" ]
                                } ]
                            }

TODOS:
    create build distribution for easy installation
    add tab completion for library texts
    create more library texts and make the "chapters" section recursive and optional.
    add options for:
        * specific chapter and quote
        * reading the text without typing
    stretch functionalities:
        * saving favorite quotes
        * logging scores (haven't gotten gtypist logs to work on my machine, personally)
        * logging a count of the times a user has typed over a quote
