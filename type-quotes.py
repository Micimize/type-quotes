import json, tempfile, subprocess, argparse, re, random

#Argument parsing
parser = argparse.ArgumentParser( formatter_class=argparse.RawTextHelpFormatter )
parser.add_argument('-c', '--count', type = int, help = 'number of quotes to type over', default=3)
parser.add_argument('-f', '--fortune', type = str, help = 'a fortune file to quote. -j takes priority over -f')
parser.add_argument('-j', '--json', type = str, help = """a json file with the structure:
    {
        "title": "The Dhammapada",
        "author": "Buddha",
        "chapters": [ {
            "title" : "The Pairs",
            "quotes": [ "speak or act with a peaceful mind" ]
        } ]
    }""")
parser.add_argument('LIBRARY', nargs='?', type = str, help = 'shortcut for "-j library/LIBRARY')
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


def get_random_member(lst):
    r = random.randint(1, len(lst))
    return r, lst[ r - 1 ]


#Logic
if (args.LIBRARY):
    args.json = "library/" + args.LIBRARY

if (args.json):
    source = json.load(open(args.json))

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
temp.write(lesson)
temp.file.flush()

#print lesson
subprocess.call(['gtypist', '-S', '-w', temp.name])
