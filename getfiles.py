# Some complete stream of pages are cut and pasted to the bz2file.txt text file 
# to show the representation of the content inside a xml.bz2 file

# In that file we have some starting tags and ending tags between them we have 
# page tags which contains the information like 
# page { title, redirect title, id, revision { id, parent id, timestamp, contributor, comment, model, format, text { desciption containing [[child]] and subtitle} } } 

# <page>
#   <title>TITLE_NAME</title>
#   <redirect title="REDIRECT_TITLE_NAME" />
#   <text bytes="63690" xml:space="preserve">{ Description containing [[CHILD_NAME]] }
# </page>

# Parses the title and redirect title to alias file
# Parses the title and its children to edges file

import xml.etree.ElementTree as ET
import re
import bz2

# edges file to store the title, 
# alias file to store the same name of pages    

def parser(xmlInput):   # extracts pageid, title and text
    myroot = ET.fromstring(xmlInput)
    pageid, title, text = '', '', ''
    for x in myroot:
        if x.tag == 'revision':         # inside tag revision
            for y in x:
                if y.tag == 'text':     # inside tag text
                    text = y.text
                    break;
        elif x.tag == 'id':             # inside tag id
            pageid = x.text
        elif x.tag == 'title':          # inside tag title
            title = x.text
    return pageid, title.strip().lower(), text


def parserRedirect(xmlInput):   # extracts redirect title if it exists
    myroot = ET.fromstring(xmlInput)
    title, redtitle = '', '#####'
    for x in myroot:    # traversing xml tree
        if x.tag == 'redirect':         # in tag redirect
            for y, z in x.attrib.items():
                if y == 'title':        # in attribute title
                    redtitle = z
                    break
        elif x.tag == 'title':          # in tag title
            title = x.text
    return title.strip().lower(), redtitle.strip().lower()


def getLinksList(text):     # extracts wikilink references from text
    if text is None:
        return []
    ret = re.findall("\[\[[^\[\]\{\}:\\\/]+]]", text)    # matches [[pagename]], pagename does not contain ':', '\', '/'
    actret = []     # list to return
    for i in range(len(ret)):
        temp = ''
        for ch in ret[i]:
            if ch in ['|', ',', '#']:   # ignoring text after these because page title is complete
                break
            if ch != '[' and ch != ']':     # ignoring [[]]
                temp += ch
        temp = temp.lower().replace('\n', ' ')      # cleaning up the link
        temp = ' '.join(temp.split())
        if temp != '':
            actret.append(temp)
    return actret


alias = dict()      # stores redirect titles
# opening the file in writing mode to write the alias output
aliasfile = open('Project/Wiki/Wiki-Graph-main/data/alias.txt', 'w', encoding='utf-8')
# opening the file in reading mode to extract the pageid, title, text
fd = bz2.open('Project/Wiki/Wiki-Graph-main/data/enwiki-latest-pages-articles.xml.bz2', 'r')

startpoint = 0
while '<page>' not in fd.readline().decode():
    startpoint += 1
fd.close()

fd = bz2.open('Project/Wiki/Wiki-Graph-main/data/enwiki-latest-pages-articles.xml.bz2', 'r')
for i in range(startpoint):      # skips to where the dump starts
    fd.readline()
edgefile = open('Project/Wiki/Wiki-Graph-main/data/edges.txt', 'w', encoding='utf-8')
cnt = 0
aliascount = 0
lines = 0
pagenumber = dict()
while True:     # adds all edges to edges.txt
    xml = ''
    line = fd.readline().decode()
    if '<page>' not in line:    # end of file reached
        break
    while '</page>' not in line :       # closing tag of page
        xml += line.strip()+'\n'
        line = fd.readline().decode()
    xml += line.strip()+'\n'
    pageid, title, text = parser(xml)
    title, rdtitle = parserRedirect(xml)  # processing xml of the current page
    if re.fullmatch("[^\[\]\{\}:\\\/]+", title) is None:     # check if current page is valid
        continue

    links = getLinksList(text)  # get all links of the page
    # title = title.encode("utf-8")
    edgefile.write(title+'\n')  # write the current page once
    lines += 1
    for link in links:  # write all children
        edgefile.write(link+'\n')
        lines += 1
    edgefile.write('###\n')     # current node done
    lines += 1

    if title != '' and rdtitle != '' and rdtitle != '#####':  # page redirects to another page
        aliascount += 1
        alias[title] = rdtitle
        aliasfile.write(title + '\n' + rdtitle + '\n')      # write to alias.txt
    if cnt % 10000 == 0:    # progress update
        print(cnt, lines, aliascount)
    cnt += 1
fd.close()
edgefile.close()
print('execution complete')
