#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, tempfile, subprocess, argparse, re, random, os

#Argument parsing
parser = argparse.ArgumentParser( formatter_class=argparse.RawTextHelpFormatter )
parser.add_argument('-c', '--count', type = int, help = 'number of quotes to type over', default=3)
parser.add_argument('-f', '--fortune', type = str, help = 'a fortune file to quote. -j takes priority over -f')
parser.add_argument('-t', '--track', type = int, help = 'if the input is an album, type over the given track by number')
parser.add_argument('-j', '--json', type = str, help = """a json file with the structure:
    {
        "type": "book"
        "title": "The Dhammapada",
        "author": "Buddha",
        "chapters": [ {
            "title" : "The Pairs",
            "quotes": [ "speak or act with a peaceful mind" ]
        } ]
    }
    or {
        "type": "album",
        "language": "bulgarian",
        "title": ["След любов по време на война", "After love in war" ],
        "artist": "Остава",
        "tracks": [ {
            "title": [ "Огледало", "Mirror" ],
            "verses": [ [ "Оглеждам се случайно,",      "looking over ourselves idly," ],
                       [ "усмихвам се навярно.",       "probably smiling."            ],
                       ...  ]
        } ]
    }""")
parser.add_argument('LIBRARY', nargs='?', type = str, help = 'shortcut for "-j library/LIBRARY"')
args = parser.parse_args()


#Functions
def build_exercise(chapter, quote):
    return (
        (('I: - - ' + chapter + ' - -') if chapter else '') +
        '\ns:' + re.sub(r'^[ \t]*\n', '', re.sub('[ \t]+', ' ', quote)).replace('\n', '\n :') +
        '\n'
    )


def build_lesson(title, author, source_function, count):
    lesson = 'B:' + title + ' by ' + author + '\n'

    while (count > 0):
        lesson += build_exercise( *source_function() )
        count -= 1

    return lesson

def build_ordered_lesson(title, author, source_function, text_list):
    lesson = 'B:' + title + ' by ' + author + '\n'

    for text in text_list:
        lesson += build_exercise( *source_function(text) )

    return lesson


def get_random_member(lst):
    r = random.randint(1, len(lst))
    return r, lst[ r - 1 ]


#Logic
if (args.LIBRARY):
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    args.json = "library/" + args.LIBRARY

if (args.json):
    source = json.load(open(args.json))
    if source.has_key("type") and source["type"] == "album":
        if args.track is not None:
            track_number, song = args.track, source['tracks'][args.track - 1]
        else:
            track_number, song = get_random_member(source['tracks'])

        full_title = song['title'][0] #+ ", " + song['title'][1]
        #verses = ["\n".join(["\n".join([b, e]) for b, e in verse]) for verse in song["verses"]]
        verses = ["\n".join([b for b, e in verse]) for verse in song["verses"]]
        def quote_generator(text):
            return "Track " + str(track_number) + ", " + full_title, text
        lesson = build_ordered_lesson(source['title'], source['artist'], quote_generator, verses) 

        
    elif not source.has_key("type") or source["type"] == "book":
        def quote_generator():
            chapter_number, chapter = get_random_member(source['chapters'])
            verse = get_random_member(chapter['quotes'])[1]
            return "Chapter " + str(chapter_number) + ", " + chapter['title'], verse
        lesson = build_lesson(source['title'], source['author'], quote_generator, args.count)

elif (args.fortune):

    def fortune_generator():
        p = subprocess.Popen(['fortune',args.fortune], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        fortune, err = p.communicate()
        return None, fortune

    lesson = build_lesson(args.fortune, 'fortune', fortune_generator, args.count)
    
temp = tempfile.NamedTemporaryFile()
temp.write(lesson.encode("utf-8"))
temp.file.flush()

#print lesson
subprocess.call(['gtypist', '-S', '-w', temp.name])
