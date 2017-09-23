from copy import deepcopy
from dateutil.parser import parse
from flask import Flask, jsonify, request, Response
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/sort', methods = ['POST'])
def sorting():
    if request.headers['Content-Type'] == 'application/json':
        data = eval(request.data)
        data.sort()
        return str(data)
    return 'NAK'

@app.route('/heist', methods = ['POST'])
def heist():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        maxWeight = data['maxWeight']
        vault = data['vault']
        listWeights, listValues = [], []
        for item in vault:
            listWeights.append(item['weight'])
            listValues.append(item['value'])
        #return jsonify({'m': maxWeight, 'w': listWeights, 'v': listValues})
        count = 0
        listRatios = []
        for i in listWeights:
            listRatios.append(listValues[count]/i)
            count  = count + 1
            sortedIndices = [i[0] for i in sorted(enumerate(listRatios), key=lambda x:x[1])]
            listRatios.sort()
            listWeights = [ listWeights[i] for i in sortedIndices]
            weight = 0
            totalWeight = 0
            count2= len(listRatios)-1
            dollarValue = 0
            while totalWeight <= maxWeight:
                reqRatio = listRatios[count2]
                weight = listWeights[count2]
                prevTotal = totalWeight
                totalWeight = totalWeight + weight
                if maxWeight < totalWeight:
                    dollarValue = dollarValue + (maxWeight - prevTotal)*reqRatio
                    break
                dollarValue = dollarValue + weight*reqRatio
                count2 = count2 - 1
                return jsonify({"heist": dollarValue})

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

        curr_max = 0
        curr_max_via = ''
        list_max = {}
        for stn_name in nodes:
            curr_count = 0
            prev_stn = None
            curr_stn = nodes[stn_name]
            while curr_stn.get_name() != dest:
                curr_count += curr_stn.get_passengers()
                prev_stn = curr_stn
                curr_stn = curr_stn.get_pointer()
            if prev_stn != None:
                prev_stn_name = prev_stn.get_name()
                if prev_stn_name in list_max:
                    #curr_count += list_max[prev_stn_name]
                    pass
                if curr_count > curr_max:
                    curr_max = curr_count
                    curr_max_via = prev_stn_name
                    list_max[curr_max_via] = curr_max
                list_max[prev_stn_name] = curr_count

        return jsonify({"line":nodes[curr_max_via].get_line(),"totalNumOfPassengers":curr_max,"reachingVia":curr_max_via})
