
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json

from collections import deque
#represent each city and the distance to their neighbours:
cities = {
    'harbin': [('shenyang', 4)],
    'shenyang': [('harbin',4), ('dalian',3), ('qinhuangdao',5), ('beijing',4)],
    'beijing': [('shenyang',4), ('tianjin',1), ('shijiazhuang',1)],
    'shijiazhuang': [('beijing',1), ('taiyuan',3), ('jinan',5),('zhengzhou',2)],
    'taiyuan': [('shijiazhuang',3)],
    'tianjin': [('beijing',1), ('jinan',2)],
    'qinhuangdao': [('shenyang',5)],
    'qingdao': [('jinan',4)],
    'dalian': [('shenyang',3)],
    'jinan': [('shijiazhuang',5), ('tianjin',2), ('qingdao',4), ('xuzhou',1)],
    'xuzhou': [('jinan',1), ('nanjing',1), ('zhengzhou',3)],
    'zhengzhou': [('xuzhou',3), ('shijiazhuang',2), ('xian',4), ('wuhan',2)],
    'xian': [('zhengzhou',4), ('baoji',2), ('jiangyou',6)],
    'baoji': [('xian',2), ('lanzhou',3)],
    'lanzhou': [('baoji',3), ('xining',3)],
    'xining': [('lanzhou',3)],
    'jiangyou': [('xian',6)],
    'wuhan': [('zhengzhou',2), ('chongqing',4), ('hefei',5), ('changsha',1)],
    'chongqing': [('wuhan',4), ('chengdu',3)],
    'chengdu': [('dazhou',6), ('chongqing',3)],
    'dazhou': [('chengdu',6)],
    'hefei': [('wuhan',5), ('nanjing',4)],
    'nanjing': [('xuzhou',1), ('hefei',4), ('shanghai',1)],
    'shanghai': [('nanjing',1), ('hangzhou',2), ('fuzhou',7)],
    'hangzhou': [('shanghai',2), ('changsha',5)],
    'changsha': [('hangzhou',5), ('wuhan',1), ('guiyang',5), ('guangzhou',2)],
    'guiyang': [('changsha',5), ('kunming',3)],
    'kunming': [('guiyang',3)],
    'guangzhou': [('changsha',2),('shenzhen',2)],
    'fuzhou': [('shanghai',7), ('shenzhen',5)],
    'shenzhen': [('fuzhou',5),('guangzhou',2)]
}


class Tree:
    # destTree=None

    '''
    return (whether has path, the path)
    '''
    def build_tree(self, start, dest):
        startingTree = {# build the root, who has no parent
            'parent': None,
            'root': start  # ,
            # 'leaves': []
        }
        pendingSearch = [
            startingTree
        ]
        searched = [start] # the searched nodes, put the starting node in it now

        #destTree = None
        searchlist = deque(pendingSearch)# the pending search list, start from the root
        while len(searchlist) > 0:
            searching = searchlist.popleft()# remove the first element of the searching list
            children = cities[searching['root']]# to find the leaves of the first element's  for looping
            for i in children:
                if dest == i[0]: # found the destination, then return the tree to this node
                    newTree = {'parent': searching, 'root': i[0]}
                    # searching['leaves'].append(destTree)
                    return True, self.getPath(newTree)
                elif i[0] not in searched: # if this leaf node has not been searched, add it as a leaf
                    newTree = {'parent': searching, 'root': i[0]}
                    # searching['leaves'].append(newTree)
                    searched.append(i[0])# do not search the same node
                    searchlist.append(newTree)

        return False, None # return None if cannot find out the path

    '''
    this function return the path of a tree

    '''
    def getPath(self,node):
        path=[]
        while node != None:
            path.insert(0,node['root'])
            node = node['parent']
        return path

class Dij:
    dist = {}# to store the shortest path's distance
    path = {}# to store the shortest path
    checked = {}# store checked nodes
    checklist = None#store nodes to be checked

    '''
    start the dijkstra algorithm
    return the (dist, path)
    '''
    def dij(self,start, dest):
        self.dist = {(start, start): 0}
        self.path = {(start, start): [start]}
        self.checked = {start: 1}
        self.checklist = deque(cities[start])

        while self.checklist:
            self.dd(self.checklist.popleft()[0], start)

        return self.dist[(start, dest)], self.path[(start, dest)]

    def dd(self,checkPoint,start):
        children = cities[checkPoint]  # get checkPoint's children
        tempdist = 999999
        tempTarget = None  # to store the leaf target that has the shortest path to checkPoint
        saved_dist = {} # the distance that searched before, but need to re-check here
        for i in children: # to loop leaves of checkPoint
            checking = i[0] # a city of leaves
            if checking in self.checked: # if the city already checked before, then try to see if any shorter path, else this city need to be check
                saved_dist[checking] = i[1] # the dist between checkPoint and the checking leaf
                if (self.dist[(start, checking)] + i[1]) < tempdist:
                    tempdist = self.dist[(start, checking)] + i[1]  # find the shorter dist
                    tempTarget = checking
            elif i not in self.checklist: # if this leaf not in checklist then add it to be checked later
                self.checklist.append(i)
        self.dist[(start, checkPoint)] = tempdist # update the dist between start and check point
        self.path[(start, checkPoint)] = self.path[(start, tempTarget)] + [checkPoint]
        self.checked[checkPoint] = 1 # marked checkpoint as checked, pls note that it's not marking its leaves!
        # recheck the checked points to see if any shorter path
        del saved_dist[tempTarget]  # remove the one that in the path to checkPoint
        for i in saved_dist: # to find if a shorter path to leaves that already checked before
            if self.dist[(start, checkPoint)] + saved_dist[i] < self.dist[(start, i)]:
                self.dist[(start, i)] = self.dist[(start, checkPoint)] + saved_dist[i]
                self.path[(start, i)] = self.path[(start, checkPoint)] + [i]

'''
Dij().dij()
t=Tree()
res=t.build_tree()
print(res[1])
'''


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):  # this is the server to handle all scratch client requests

    DEEP_FIRST = '/DeepFirst'
    DIJKSTRA = '/Dijkstra'
    FROM = 'from'
    TO = 'to'

    tree = Tree()
    dij = Dij()


    '''to check whether this input can complete the journey
    return (whether can complete, wrong city name if the path is wrong, number of hours) 
    '''
    def can_complete(self,input):
        time = 0
        res = True
        wrongCity = None
        for i in range(0,len(input)-1):
            inLeaf = False
            for j in cities[input[i]]:
                if input[i+1] == j[0]:
                    inLeaf = True
                    time += j[1]
                    break # found a child, then continue next checking

            if not inLeaf: # found a point that is not in the leaf, then return false
                res = False
                wrongCity = input[i]
                break
        return res,wrongCity,time

    def getPostContent(self):
        length = int(self.headers['Content-Length'])
        b = self.rfile.read(length)
        print(b.decode('UTF-8'))
        input = json.loads(b.decode('UTF-8'))
        return input




    def dijkstra(self):
        output = {'res': -1, 'wrongCity': '', 'correctpath': [], 'time': 0}
        input = self.getPostContent()

        start = input[0]
        dest = input[-1]
        alg_res = self.dij.dij(start, dest)

        res = self.can_complete(input)
        if res[0]:  # can go to destination
            if res[2] <= alg_res[0]:  # the answer is not worse than the algorithm
                output['res'] = 1
                output['time'] = alg_res[0]
            else:
                output['res'] = 0
                output['time'] = res[2]
        else:  # cannot go to dest
            output['res'] = -1
            output['wrongCity'] = res[1]

        output['correctpath'] = alg_res[1]

        print(json.dumps(output))
        return json.dumps(output)


    def deepFirst(self):
        output = {'res': -1, 'wrongCity': '', 'correctpath': [],'count':0}
        input = self.getPostContent()

        start = input[0]
        dest = input[-1]
        tree_res = self.tree.build_tree(start,dest)

        res = self.can_complete(input)
        if res[0]:  # can go to destination
            if len(input) <= len(tree_res[1]):# the answer is not worse than the algorithm
                output['res'] = 1
            else:
                output['res'] = 0
        else:  # cannot go to dest
            output['res'] = -1
            output['wrongCity'] = res[1]

        output['correctpath'] = tree_res[1]

        print(json.dumps(output))
        return json.dumps(output)

    def do_OPTIONS(self):
        self.send_response(200,'ok')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()




    def do_POST(self):
        print(self.path)

        if self.path == self.DEEP_FIRST:  # deep first
            self.reply(self.deepFirst())
        elif self.path == self.DIJKSTRA:  # dijkstra
            self.reply(self.dijkstra())


    def reset(self):
        print('empty reset')

    # httpd.charAssignment = {} # stores the character, and it's IP, pendingAction list; the key is the character name, e.g. 1/2/3...
    # httpd.allChars = ('a','b','c')#all available chars for selection
    # httpd.selectedChars =[] #a list to store selected chars
    # httpd.movingCharIndex = 0 # the index of the char that is moving at the moment, pls note it's index, not the char itself

    def reply(self, strOut):  # format and send out response
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        print('replying:', strOut)
        self.wfile.write(strOut.encode('UTF-8'))

    def log_message(self, format, *args):
        return


httpd = HTTPServer(('', 9999), SimpleHTTPRequestHandler)
httpd.serve_forever()


