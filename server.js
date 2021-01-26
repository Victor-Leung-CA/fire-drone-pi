const sensorAPI = require('./API/sensorAPI')
var express = require('express');

var app = express();
app.use(express.json());

//For running python script as child process
const { spawn } = require('child_process');


/*
 * Launch external scripts
*/

// Store GPS readings
const coordinates = [];
const sensorProcess = spawn('python', ['./data-acquisition/sensor.py']);

sensorProcess.stdout.on('data', data => {
    
    // Coerce Buffer object to Float
    coordinates.push(parseFloat(data));

    // Log to debug
    sensorAPI.postData(coordinates[coordinates.length-1]);
});


/*
 * Server
*/
const port = process.env.PORT || 5000;

app.get('/', function (req, res) {
  res.send('Welcome to FireDrone Raspberry Pi Server!');
});

app.listen(port, () => {
  console.log('Raspberry Pi server running!');
});