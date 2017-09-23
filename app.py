from flask import Flask, jsonify, request
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

@app.route('/stringcompression/<mode>', methods = ['POST'])
def compress(mode):
    answer = 0
    if request.headers['Content-Type'] == 'application/json':
        data = request.json['data']
        if mode == 'RLE':
            compressed = []
            sequence = ['']
            counter = {}
            for c in data:
                if c != sequence[-1]:
                    counter[c] = 1
                else:
                    sequence.append(c)
                    counter[c] += 1
            for c in sequence:
                compressed.append(counter[c])
                compressed.append(c)
            compressed = ''.join(compressed)
            answer = len(answer) * 8
        elif mode == 'LZW':
            codes = []
            lzw_dict = {}
            next_code = 256
            p = data[0]
            for i in range(1, len(data)):
                p_concat = p + data[i]
                if (len(p_concat) == 1 and 0 <= ord(p_concat) <= 255) or p_concat in lzw_dict:
                    p = p_concat
                else:
                    lzw_dict[p_concat] = next_code
                    next_code += 1
                    codes.append(p)
                    p = data[i]
            answer = len(codes) * 12
        elif mode == 'WDE':
            data = data.strip()
            num_spaces = 0
            num_non_alphanum = 0
            prev = ''
            lzw_dict = {}
            next_code = 256
            p = data[0]
            for i in range(1, len(data)):
                c = data[i]
                if c == ' ':
                    if prev != ' ':
                        num_spaces += 1
                elif not c.isalnum():
                    num_non_alphanum += 1
                else:
                    p_concat = p + c
                    if (len(p_concat) == 1 and 0 <= ord(p_concat) <= 255) or p_concat in lzw_dict:
                        p = p_concat
                    else:
                        lzw_dict[p_concat] = next_code
                        next_code += 1
                    prev = c
            if len(data) == 0:
                answer = 0
            else:
                answer = (num_spaces + 1) * 12 + num_non_alphanum * 12 + len(lzw_dict)
        else:
            pass
    res = flask.Response(str(answer))
    res.headers['Content-Type'] = 'text/plain'
    return res

