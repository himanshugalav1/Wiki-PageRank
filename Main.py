# data alias - 20,743,457
# data edges - 337,218,633

# now we will do a random walk of maxhops steps
# we will start with a randomly selected node from allnodes as cur
# if that node is not visited previously then make its visits[cur]=1
# else increase it by 1 as visits[cur]+=1
# now if that cur node doesn't have any children( len( adjlist[cur] ) == 0 ) then randomly select cur node again from allnodes
# but if it has children( len( adjlist[cur] ) != 0 ) then randomly select the cur node from its children( adjlist[cur] ) only 
# again increase the visits of children by 1 when visited
# when its steps becomes equal to maxhops steps our random walk completes

# Now to print the all the links present in a page named ab
# first check for its redirect title if present make ab = alias[ab]
# now we have the page name as ab
# so check for its children in adjlist using the uniqueID of that page by id = nodeid[ab]
# if children not present then print "Page not found" and then return
# if children are present then print all the links present in that page using print(nodename[c] for each c in adjlist[nodeid[ab]])

# Here comes the main() function of our python file
# 4 modes are present 
# mode 1 takes user input for number of random walks user want and then do all the walks
# mode 2 gives us the best/top k pages by printing the biggest k elements of visits list after sorting it in descending order
# mode 3 is to get all the links present in a page or to check whether it is present or not
# mode 4/Q is to exit the code

import random
import pickle
# adjlist = dict()    # adjacency list
# alias = dict()      # stores the redirect titles
# nodeid = dict()     # hash of page titles to unique integer
# nodename = dict()   # hash from unique integer to page title
# allnodes = dict()   # list of all nodes

# Load the dictionary from the pickle file
with open('alias.pkl', 'rb') as file:
    alias = pickle.load(file)
print("alias file loaded !!!")

with open('nodeid.pkl', 'rb') as file:
    nodeid = pickle.load(file)
print("nodeid file loaded !!!")

with open('nodename.pkl', 'rb') as file:
    nodename = pickle.load(file)
print("nodename file loaded !!!")

with open('adjlist.pkl', 'rb') as file:
    adjlist = pickle.load(file)
print("adjlist file loaded !!!")

with open('allnodes.pkl', 'rb') as file:
    allnodes = pickle.load(file)
print("allnodes file loaded !!!")

visits = dict()     # number of visits for pagerank

def randomwalk(maxhops):    # runs a random walk of 'maxhops' steps
    hops = 0

    cur = random.choice(allnodes)   # select a random starting node
    if visits.get(cur) is None:     # visit counter for page rank / if we havnt visited curr node before now make it visited by assigning its value as 1
        visits[cur] = 1
    else:   # here the visit stores the number of times a node is visited in a random walk for maxhops steps
        visits[cur] += 1    # if we have visited previously increase it by one again 

    while hops < maxhops:
        
        if random.random() < 0.9:   # goes to a neighbour
            if adjlist.get(cur) is None or len(adjlist[cur]) == 0:  # if the current node has no children present in adjlist of curr
                cur = random.choice(allnodes)                       # again randomly select the starting curr node from allnodes
            else:       # if children are present select curr node as any randomly selected child node
                cur = random.choice(adjlist[cur])
        else:   # if it is equal to 0.9 the last possible case or a 1 in a 10 case
            cur = random.choice(allnodes)   # again randomly select the curr node from allnodes
            
        if visits.get(cur) is None:     # increase its visit index by 1
            visits[cur] = 1
        else:
            visits[cur] += 1
        hops += 1
        
        if hops % 1000000 == 0:     # progress tracker that gives the percent of progress completed after every 10L rounds
            print(str(round((hops / maxhops * 100), 2)) + ' %')
    print('random walk completed')


def printlinks(ab):
    ab = ab.lower().strip()     # cleaning the input by removing all unneccesary starting and ending spaces and converting all character to lower case
    if alias.get(ab) is not None:   # if page redirects to another page 
        ab = alias[ab]              # make the page name equal to redirected page name
    if nodeid[ab] is None:
        print("page not found")
        return
    if adjlist.get(nodeid[ab]) is None:     # if there is no child of that page that page does not exist since child represents a link
        print('page not found')
        return
    for c in adjlist[nodeid[ab]]:       # if present - prints all the links
        print(nodename[c])


def main():
    
    while True:
        print('''Menu:
        1 : Run a random walk of X hops
        2 : Print the top K pages
        3 : See all links of a particular page
        P : Print the visits list
        Q : Quit'''
        )
        ip = input()
        
        if ip == '1':
            print('Enter number of hops: ')
            maxhops = int(input())
            randomwalk(maxhops)
        
        elif ip == '2':
            print('Enter number of top pages to be displayed')
            k = int(input())
            for a, b in sorted(visits.items(), key=lambda vk: (vk[1], vk[0]), reverse=True)[0:k]:
                print(nodename[a])
        
        elif ip == '3':
            print('Enter page name to look for: ')
            printlinks(input())
        
        elif ip == 'P':
            print(visits)

        elif ip == 'Q':
            print('Exiting')
            break

        else:
            print('Invalid input')

main()
