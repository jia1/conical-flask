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
