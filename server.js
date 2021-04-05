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
const sensorProcess = spawn('python', ['./data-acquisition/sensor.py']); // this might need to be changed to trygps.py; Victor to confirm

sensorProcess.stdout.on('data', data => {
    
  if(data == "Mission End"){
    // Post data to server
    sensorAPI.postData(coordinates);
  }
  else{
    // Coerce Buffer object to Float
    coordinates.push(parseFloat(data));
  }

});


/*
 * Server
*/
const port = process.env.PORT || 3000;

app.get('/', function (req, res) {
  res.send('Welcome to FireDrone Raspberry Pi Server!');
});

app.listen(port, () => {
  console.log('Raspberry Pi server running!');
});
