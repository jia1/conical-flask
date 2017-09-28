# https://cis2017-coordinator-demo.herokuapp.com/
# https://cis2017-coordinator-sg.herokuapp.com/leaderboard/index.html

# Add team
curl -X POST http://cis2017-coordinator-sg.herokuapp.com/api/teams -H 'Content-Type:application/json' -d '{"name":"codeit-team-septers","url":"https://codeit-team-septers.herokuapp.com","members":["Jia Yee","Alan","Shuwei"]}'

# Response
{"id":13,"name":"codeit-team-septers","url":"http://codeit-team-septers.herokuapp.com","members":["Jia Yee","Alan","Shuwei"]}

# Evaluate sorting
curl -X POST http://cis2017-coordinator-sg.herokuapp.com/api/evaluate -H 'Content-Type:application/json' -d '{"team":"codeit-team-septers","challenge":"Sorting"}'

curl -X POST http://cis2017-coordinator-sg.herokuapp.com/api/evaluate -H 'Content-Type:application/json' -d '{"team":"codeit-team-septers","challenge":"Jewellery Heist"}'

curl -X POST http://cis2017-coordinator-sg.herokuapp.com/api/evaluate -H 'Content-Type:application/json' -d '{"team":"codeit-team-septers","challenge":"Release Schedule"}'

curl -X POST http://cis2017-coordinator-sg.herokuapp.com/api/evaluate -H 'Content-Type:application/json' -d '{"team":"codeit-team-septers","challenge":"String Compression"}'

curl -X POST http://cis2017-coordinator-sg.herokuapp.com/api/evaluate -H 'Content-Type:application/json' -d '{"team":"codeit-team-septers","challenge":"Horse Racing"}'

curl -X POST http://cis2017-coordinator-sg.herokuapp.com/api/evaluate -H 'Content-Type:application/json' -d '{"team":"codeit-team-septers","challenge":"Train Planner"}'

curl -X POST http://cis2017-coordinator-sg.herokuapp.com/api/evaluate -H 'Content-Type:application/json' -d '{"team":"codeit-team-septers","challenge":"Calculate Empty Area"}'

# Get evaluation
https://cis2017-coordinator-sg.herokuapp.com/leaderboard/index.htmlcurl -X GET http://cis2017-coordinator-sg.herokuapp.com/api/evaluation-run/

# Self-test sort
curl -X POST http://codeit-team-septers.herokuapp.com/sort -H 'Content-Type:application/json' -d '[4,3,2,1]'

# Local self-test
curl -X POST http://localhost:5000/sort -H 'Content-Type:application/json' -d '[4,3,2,1]'

curl -X POST http://cis2017-coordinator-sg.herokuapp.com/releaseSchedule -H 'Content-Type:application/json' -d '["3;28-05-2017 13:00:00.000+0800;28-05-2017 16:00:00.000+0800",
"London morning trading check;28-05-2017 05:15:00.000Z;28-05-2017 06:15:00.000Z",
"Tokyo risk testing;28-05-2017 16:15:00.000+0900;28-05-2017 16:45:00.000+0900",
"New York midnight database check;28-05-2017 03:50:00.000-0400;28-05-2017 03:59:00.000-0400"]'

curl -X POST http://localhost:5000/heist -H 'Content-Type:application/json' -d '{
  "maxWeight": 4,
  "vault": [
  {"weight": 1, "value": 200},
  {"weight": 3, "value": 240},
  {"weight": 5, "value": 150},
  {"weight": 2, "value": 140}
  ]
}'

curl -X POST http://localhost:5000/releaseSchedule -H 'Content-Type:application/json' -d '["3;28-05-2017 13:00:00.000+0800;28-05-2017 16:00:00.000+0800",
"London morning trading check;28-05-2017 05:15:00.000Z;28-05-2017 06:15:00.000Z",
"Tokyo risk testing;28-05-2017 16:15:00.000+0900;28-05-2017 16:45:00.000+0900",
"New York midnight database check;28-05-2017 03:50:00.000-0400;28-05-2017 03:59:00.000-0400"]'

curl -X POST http://localhost:5000/stringcompression/RLE -H 'Content-Type:application/json' -d '{"data": "RRRRRRTTTTYYYULLL"}'

curl -X POST http://localhost:5000/stringcompression/LZW -H 'Content-Type:application/json' -d '{"data": "BABAABAAA"}'

curl -X POST http://localhost:5000/stringcompression/WDE -H 'Content-Type:application/json' -d '{"data": "HOW MUCH WOOD COULD A WOOD CHUCK CHUCK IF A WOOD CHUCK COULD CHUCK WOOD"}'

curl -X POST http://localhost:5000/trainPlanner -H 'Content-Type:application/json' -d '{"destination":"DhobyGhaut","stations":[{"name":"Punggol","passengers":80,"connections":[{"station":"Sengkang","line":"purple"}]},{"name":"Sengkang","passengers":40,"connections":[{"station":"Punggol","line":"purple"},{"station":"Serangoon","line":"purple"}]},{"name":"Serangoon","passengers":40,"connections":[{"station":"LittleIndia","line":"purple"},{"station":"Sengkang","line":"purple"},{"station":"PayaLebar","line":"orange"},{"station":"Bishan","line":"orange"}]},{"name":"LittleIndia","passengers":40,"connections":[{"station":"Serangoon","line":"purple"},{"station":"DhobyGhaut","line":"purple"}]},{"name":"DhobyGhaut","passengers":20,"connections":[{"station":"LittleIndia","line":"purple"},{"station":"HarbourFront","line":"purple"},{"station":"Somerset","line":"red"},{"station":"MarinaBay","line":"red"},{"station":"Esplanade","line":"orange"}]},{"name":"HarbourFront","passengers":90,"connections":[{"station":"DhobyGhaut","line":"purple"}]},{"name":"Somerset","passengers":0,"connections":[{"station":"DhobyGhaut","line":"red"},{"station":"Orchard","line":"red"}]},{"name":"Orchard","passengers":30,"connections":[{"station":"Somerset","line":"red"},{"station":"Novena","line":"red"}]},{"name":"Novena","passengers":10,"connections":[{"station":"Orchard","line":"red"},{"station":"Bishan","line":"red"}]},{"name":"Bishan","passengers":20,"connections":[{"station":"Novena","line":"red"},{"station":"Woodlands","line":"red"},{"station":"Serangoon","line":"orange"}]},{"name":"Woodlands","passengers":40,"connections":[{"station":"Bishan","line":"red"}]},{"name":"MarinaBay","passengers":100,"connections":[{"station":"DhobyGhaut","line":"red"}]},{"name":"Esplanade","passengers":0,"connections":[{"station":"DhobyGhaut","line":"orange"},{"station":"PayaLebar","line":"orange"}]},{"name":"PayaLebar","passengers":75,"connections":[{"station":"Esplanade","line":"orange"},{"station":"Serangoon","line":"orange"}]}]}'
