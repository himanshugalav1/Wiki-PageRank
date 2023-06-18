# data alias - 20,743,457
# data edges - 337,218,633

# Open the alias text file as aliasfile 
# aliasfile's first line contains title of a page and second line contains redirected title
# read its first line as title and second line as rdtitle
# store them in a dictionary named alias as  -   alias [ title ] = rdtitle

# When line goes emmpty aliasfile ends 

# Now open the edges text file as edgefile
# read the first line as title 
# check alias dictionary if its redirect title is available or not None
# make the title equal to its redirect title as that title has no existance as a page it redirects to redirect title only
# Now we have the final title
# If we havnt assigned any unique id to that title assign it both way as nodeid[title] = uniqueID  &  nodename[uniqueID] = title 
# Now for it will have children till ### comes in a line 
# so iterate till ### comes and do the same for its children
# like check for presence of its redirect title and then assign uniqueID if not assigned before and so on.....
# and also append the id of all the children nodes to adjlist dictionary for a title
# and append all the present tile and their children node to allnodes

# Now we have dictionaries as - alias, nodeid, nodename, adjlist, allnodes
# as alias[title] = rdtitle
# nodeid[title] = uniqueID
# nodename[uniqueID] = title
# adjlist.append(childID)
# allnodes = {c for c, c1 in adjlist.items()}


import pickle
adjlist = dict()    # adjacency list
alias = dict()      # stores the redirect titles
nodeid = dict()     # hash of page titles to unique integer
nodename = dict()   # hash from unique integer to page title
allnodes = dict()   # list of all nodes

aliasfile = open('textfiles/alias.txt', 'r', encoding='utf-8')
edgefile = open('textfiles/edges.txt', 'r', encoding='utf-8')


def init():     # loads the graph into memory
    print('loading graph into memory')
    aliascount = 0
    while True:     # links pages that redirect to another page
        title = aliasfile.readline().strip()  # reading first line as title after removing all the beginning and ending spaces
        if title == '':
            break
        rdtitle = aliasfile.readline().strip()  # read the second line as rdtitle
        alias[title] = rdtitle      # hashing the redirect title or defining rdtitle as title
        aliascount += 1
        if aliascount % 10000 == 0:     # progress update
            print('alias count: ' + str(aliascount))
    print("alias file completed !!!")

    # Save the alias dictionary to alias.pkl file
    with open('alias.pkl', 'wb') as file:
        pickle.dump(alias, file)
    print("alias stored successfully !!!")

    print('loading edges...')
    cnt = 0     # counts the total line done reading
    uniqueID = 0    # serves as a unique id provider
    while True:     # loads edges into memory
        title_edge = edgefile.readline().strip()    # first line of edge named as title_edge
        if title_edge == '':
            break
        if alias.get(title_edge) is not None:    # if page redirects to another page
            title_edge = alias[title_edge]
        if nodeid.get(title_edge) is None:   # assigning unique id to page for performance
            nodeid[title_edge] = uniqueID        # assign some unique id to page title - nodeid[title] = uniqueID
            nodename[uniqueID] = title_edge      # store the same in reverse way  - nodename[uniqueID] = title
            uniqueID += 1
        cnt += 1
        
        id = nodeid[title_edge]   # unqieID of title_edge
        if adjlist.get(id) is None:      # if no list is present for the id
            adjlist[id] = []            # make a empty list
        
        rdtitle_edge = edgefile.readline().strip()     # next line of edge named as rdtitle_edge
        cnt += 1
        while '###' not in rdtitle_edge:   # no more edges for current node or loop till other rdtitle_edge are present for title_edge
            if cnt % 100000 == 0:   # progress update after every 10K lines
                print('Edges added: ' + str(cnt))
            if rdtitle_edge == '':     # ignoring blank lines
                cnt += 1
                rdtitle_edge = edgefile.readline().strip() # if line is blank read other line
                continue
            if alias.get(rdtitle_edge) is not None:    # if page redirects to another page
                rdtitle_edge = alias[rdtitle_edge]
            if nodeid.get(rdtitle_edge) is None:    # assigning unique id to page for performance
                nodeid[rdtitle_edge] = uniqueID
                nodename[uniqueID] = rdtitle_edge
                uniqueID += 1
            
            rdid = nodeid[rdtitle_edge]
            adjlist[id].append(rdid)    # adding edge to adjacency list
            rdtitle_edge = edgefile.readline().strip()
            cnt += 1

    aliasfile.close()
    edgefile.close()
    global allnodes
    allnodes = [c for c, c1 in adjlist.items()]     # list of all nodes
    print("Edges file completed !!!")

    with open('nodeid.pkl', 'wb') as file:
        pickle.dump(nodeid, file)
    print("nodeid stored successfully !!!")
    with open('nodename.pkl', 'wb') as file:
        pickle.dump(nodename, file)
    print("nodename stored successfully !!!")
    with open('adjlist.pkl', 'wb') as file:
        pickle.dump(adjlist, file)
    print("adjlist stored successfully !!!")
    with open('allnodes.pkl', 'wb') as file:
        pickle.dump(allnodes, file)
    print("allnodes stored successfully !!!")


def main():
    init()
    
main()
