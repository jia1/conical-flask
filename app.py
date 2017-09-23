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
            data = data.strip()
            num_spaces = 0
            num_non_alphanum = 0
            prev = ''
            p = data[0]
            lzw_dict = {p: ord(p)}
            next_code = 256
            for i in range(1, len(data)):
                c = data[i]
                if c == ' ':
                    num_non_alphanum += 1
                    if prev != ' ':
                        num_spaces += 1
                elif not c.isalnum():
                    num_non_alphanum += 1
                else:
                    p_concat = p + c
                    if p_concat in lzw_dict:
                        p = p_concat
                    if len(p_concat) == 1 and 0 <= ord(p_concat) <= 255:
                        lzw_dict[p_concat] = ord(p_concat)
                        p = p_concat
                    else:
                        lzw_dict[p_concat] = next_code
                        next_code += 1
                    prev = c
            if len(data) == 0:
                answer = 0
            else:
                answer = (1 + num_spaces + num_non_alphanum) * 12 + len(lzw_dict)
                #answer = [num_spaces, num_non_alphanum, lzw_dict]
        else:
            pass
    res = Response(str(answer))
    res.headers['Content-Type'] = 'text/plain'
    return res

