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
        listweights, listvalues = [], []
        for item in vault:
            listweights.append(item['weight'])
            listvalues.append(item['value'])
        count = 0
        listratios = []
        for i in listweights:
            listratios.append(listvalues[count]/i)
            count  = count + 1
            sortedindices = [i[0] for i in sorted(enumerate(listratios), key=lambda x:x[1])];
            listratios.sort();
            listweights = [ listweights[i] for i in sortedindices]
            weight = 0;
            totalweight = 0;
            count2= len(listratios)-1;
            dollarvalue = 0;
            while totalweight <= maxWeight:
                reqratio = listratios[count2]
                weight = listweights[count2]
                prevtotal = totalweight
                totalweight = totalweight + weight
                if maxWeight < totalweight:
                    dollarvalue = dollarvalue + (maxWeight - prevtotal)*reqratio;
                    break
                dollarvalue = dollarvalue + weight*reqratio;
                count2 = count2 - 1;
                return jsonify({"heist": dollarvalue});
