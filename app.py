from collections import Counter
from copy import deepcopy
from dateutil.parser import parse
from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/sort', methods = ['POST'])
def sorting():
    if request.headers['Content-Type'] == 'application/json':
        data = eval(request.data)
        #data.sort()
        def qsort(inlist):
            if inlist == []:
                return []
            else:
                pivot = inlist[0]
                lesser = qsort([x for x in inlist[1:] if x < pivot])
                greater = qsort([x for x in inlist[1:] if x >= pivot])
                return lesser + [pivot] + greater
        return qsort(data)
    return 'NAK'

@app.route('/heist', methods = ['POST'])
def heist():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        maxWeight = data['maxWeight']
        vault = data['vault']
        dictionary = {} #value: weight
        total_value = 0
        for x in vault:
            weight = int(x['weight'])
            value = int(x['value'])
            ratio = value / weight
            dictionary[ratio] = weight
        sorted_key = sorted(list(dictionary.keys()), reverse=True)
        for r in sorted_key:
            w = dictionary[r]
            if w >= maxWeight:
                total_value = total_value + int(r * maxWeight)
                return jsonify({"heist": total_value})
            else:
                total_value = total_value + int(r * w)
                maxWeight = maxWeight - w
        return jsonify({"heist": total_value})

@app.route('/releaseSchedule', methods = ['POST'])
def release():
    if request.headers['Content-Type'] == 'application/json':
        data = eval(request.data)
        tasks = data[0].split(';')
        task_num = int(tasks[0])
        start_time = parse(tasks[1])
        end_time = parse(tasks[2])
        for x in range(1,task_num+1):
            task = data[x].split(';')
            task_start = parse(task[1])
            task_end = parse(task[2])
            if task_start < start_time:
                if task_end > start_time & task_end < end_time:
                    start_time = task_end
                elif task_end > end_time:
                    return 0
            elif (task_start > start_time) & (task_start < end_time):
                if task_end < end_time:
                    gap1 = task_start - start_time
                    gap2 = end_time - task_end
                    if gap1 > gap2:
                        end_time = task_start
                    else:
                        start_time = task_end
                elif task_end > end_time:
                    end_time = task_start
        res = Response(str((end_time - start_time).seconds))
        res.headers['Content-Type'] = 'text/plain'
        return res

@app.route('/stringcompression/<mode>', methods = ['POST'])
def compress(mode):
    answer = 'NAK'
    if request.headers['Content-Type'] == 'application/json':
        data = request.json['data']
        if mode == 'RLE':
            compressed = []
            sequence = ['']
            counter = {}
            for c in data:
                if c != sequence[-1]:
                    sequence.append(c)
                    counter[c] = 1
                else:
                    counter[c] += 1
            for c in sequence[1:]:
                if counter[c] > 1:
                    compressed.append(str(counter[c]))
                compressed.append(c)
            compressed = ''.join(compressed)
            answer = len(compressed) * 8
        elif mode == 'LZW':
            p = data[0]
            lzw_dict = {p: ord(p)}
            next_code = 256
            for i in range(1, len(data)):
                c = data[i]
                p_concat = p + c
                if (p_concat in lzw_dict):
                    p = p_concat
                elif len(p_concat) == 1 and 0 <= ord(p_concat) <= 255:
                    lzw_dict[p_concat] = ord(p_concat)
                    p = p_concat
                else:
                    lzw_dict[p_concat] = next_code
                    next_code += 1
                    p = c
            answer = len(lzw_dict) * 12
        elif mode == 'WDE':
            data = data.strip().split(' ')
            p = data[0]
            lzw_dict = {p: 0}
            next_code = 1
            for i in range(1, len(data)):
                c = data[i]
                if c in lzw_dict:
                    pass
                else:
                    lzw_dict[c] = next_code
                    next_code += 1
            if len(data) == 0:
                answer = 0
            else:
                total_char = 0
                for w in lzw_dict:
                    total_char += len(w)
                answer = (len(data) * 2 - 1) * 12 + total_char * 8
        else:
            pass
    res = Response(str(answer))
    res.headers['Content-Type'] = 'text/plain'
    return res

@app.route('/horse-racing', methods = ['POST'])
def race():
    if request.headers['Content-Type'] == 'application/json':
        print('/horse-racing')
        data = request.data
        c_horse = Counter([])
        c_jockey = Counter([])
        c_trainer = Counter([])
        combination = Counter([])
        for x in data:
            placing = int(x['Placing'])
            if placing < 4:
                #q1
                if placing == 1:
                    horse = x['Horse']
                    jockey = x['jockeycode']
                    trainer= x['Trainer']
                    c_horse.update([horse])
                    c_jockey.update([jockey])
                    c_trainer.update([trainer])
                #q2
                score = 0
                c_name = x['Horse'] + '-' + x['jockeycode'] + '-' + x['Trainer']
                if placing == 1:
                    score = 7
                elif placing == 2:
                    score = 3
                else:
                    score = 1
                combination.update({c_name:score})
            #q3

        q1 = {"horse":max(c_horse),"jockey":max(c_jockey),"trainer":max(c_trainer)}
        best_combi = max(combination).split('-')
        q2 = {"horse":best_combi[0],"jockey":best_combi[1],"trainer":best_combi[2]}
        return jsonify({"q1":q1,"q2":q2,"q3":""})

@app.route('/trainPlanner', methods = ['POST'])
def plan():
    if request.headers['Content-Type'] == 'application/json':
        class Node:
            name = ''
            line = ''
            passengers = 0
            connections = []
            pointer = None

            def __init__(self, name = '', line = '', passengers = 0, connections = [], pointer = None):
                self.name = name
                self.line = line
                self.passengers = passengers
                self.connections = connections
                self.pointer = pointer

            def get_name(self): return self.name

            def get_line(self): return self.line
            def set_line(self, line): self.line = line

            def get_passengers(self): return self.passengers
            def add_passengers(self, passengers): self.passengers += passengers

            def get_connections(self): return self.connections
            def add_connections(self, connections): self.connections.extend(connections)

            def get_pointer(self): return self.pointer
            def set_pointer(self, node): self.pointer = node

        data = request.json
        dest = data['destination']
        stns = data['stations']

        nodes = {}
        for stn in stns:
            stn_name = stn['name']
            nodes[stn_name] = Node(name = stn_name, passengers = stn['passengers'], connections = stn['connections'])
        nodes[dest].set_pointer(nodes[dest])

        to_explore = [dest]
        explored = set()
        while to_explore:
            # Should use queue
            src = to_explore.pop(0)
            if src not in explored:
                for neighbour in nodes[src].get_connections():
                    neighbour_name = neighbour['station']
                    nodes[neighbour_name].set_line(neighbour['line'])
                    if nodes[neighbour_name].get_pointer() == None:
                        nodes[neighbour_name].set_pointer(nodes[src])
                        to_explore.append(neighbour_name)
                explored.add(src)

        counted = {}
        curr_max = 0
        curr_max_via = ''
        list_max = {}
        for stn_name in nodes:
            curr_count = 0
            prev_stn = None
            curr_stn = nodes[stn_name]
            while curr_stn.get_name() != dest:
                if curr_stn.get_name() not in counted:
                    curr_count += curr_stn.get_passengers()
                    counted[curr_stn.get_name()] = True
                prev_stn = curr_stn
                curr_stn = curr_stn.get_pointer()

            if prev_stn != None:
                prev_stn_name = prev_stn.get_name()
                if prev_stn_name in list_max:
                    curr_count += list_max[prev_stn_name]
                if curr_count > curr_max:
                    curr_max = curr_count
                    curr_max_via = prev_stn_name
                    list_max[curr_max_via] = curr_max
                list_max[prev_stn_name] = curr_count

        return jsonify({"line":nodes[curr_max_via].get_line(),"totalNumOfPassengers":curr_max,"reachingVia":curr_max_via})

@app.route('/calculateemptyarea', methods = ['POST'])
def empty():
    if request.headers['Content-Type'] == 'application/json':
        def rectOverlap(l1, r1 , l2, r2):
            #If one rectangle is on left side of other
            if (l1[0] > r2[0]) or (l2[0] > r1[0]):
                return 0
            #If one rectangle is above other
            if (l1[1] < r2[1]) or (l2[1] < r1[1]):
                return 0
                #return 1;
            if l1[0] < l2[0]:
                if l1[1] >= l2[1]:
                    return 1
                else:
                    return 2
            else:
                if r1[1] >= r2[1]:
                    if r1[0]<= r2[0]:
                        return 3
                    else:
                        return 4
                else:
                    return 5

        data = request.data
        container, child = {}, {}
        for key in container:
            if key == 'container':
                container = data[key]
            else:
                child = data[key]

        #container should be a list with first item coordinate, second item width
        #and third item height
        #child shape should be a list with first item shape, second item coordinate
        #third item width/radius and fourth item height
        childShape = child[0]
        childCoord = child[1]
        # childXCoord = childCoord[0];
        #childYCoord = childCoord[1];
        childWidth =child[2]
        #outerchildWidth = childWidth + childXCoord;
        #childHeight = child[3];
        containerCoord = container[0]
        #containerXCoord = containerCoord[0];
        #containerycoord = containerCoord[1];
        containerWidth = container[1]
        containerHeight = container[2]
        #outerContainerWidth = containerWidth + containerXCoord
        #test cases:
        containerCoord = [0,0]
        childCoord = [5,2]
        childWidth = 4
        childHeight = 4
        containerWidth = 10
        containerHeight = 8
        if (childShape == "rectangle") or (childShape=="square"):
            childWidth = child[2]
        if childShape=="rectangle":
            childHeight = child[3]
        else:
            childHeight = childWidth;

        l1 = [sum(x) for x in zip(childCoord, [0,childHeight])]
        l2 = [sum(x) for x in zip(containerCoord, [0,containerHeight])]
        r1 = [sum(x) for x in zip(childCoord, [childWidth,0])]
        r2 = [sum(x) for x in zip(containerCoord, [containerWidth,0])]
        containerArea = containerWidth*containerHeight

        if rectOverlap(l1,r1,l2,r2) == 0:
            emptyArea = containerArea
        elif rectOverlap(l1,r1,l2,r2) == 1:
            emptyArea = containerArea - (r1[0] - l2[0])*(l2[1] - r1[1])
        elif rectOverlap(l1,r1,l2,r2) == 2:
            if r2[1]<=r1[1]:
                emptyArea = containerArea - (r1[1]-l1[1])*(r1[0]-l2[0])
            else:
                upperChildCor = [sum(x) for x in zip(childCoord, [childWidth,childHeight])]
                emptyArea = containerArea - (upperChildCor[0]-containerCoord[0])*(upperChildCor[1]-containerCoord[1])
        elif rectOverlap(l1,r1,l2,r2) == 3 :
            if l1[1] <= l2[1]:
                emptyArea = containerArea - (childWidth)*(childHeight)
                #emptyArea = containerArea - (childWidth)*(l2[1]-r1[1]);
            else:
                #emptyArea = containerArea - (childWidth)*(childHeight);
                emptyArea = containerArea - (childWidth)*(l2[1]-r1[1])
        elif rectOverlap(l1,r1,l2,r2) == 4:
            if l1[1] > l2[1]:
                emptyArea = containerArea - (l2[1]-childCoord[1])*(r2[0]-childCoord[0])
            else:
                emptyArea = containerArea - (r2[0] - l1[0])*(childHeight)
        else:
            if r1[0]>r2[0]:
                emptyArea = containerArea - (r2[0]-l1[0])*(r2[1]-l1[1])
            else:
                emptyArea = containerArea - childWidth*(l1[1]-r2[1])

        return emptyArea
