var express = require('express');
//For running python script as child process
const { spawn } = require('child_process');
const postPhotos = require('./API/postPhotos').postPhotos

var app = express();
app.use(express.json());

/*
 * Launch external scripts
*/

// Store GPS readings
const coordinates = [];
const sensorProcess = spawn('python', ['./data-acquisition/sensor.py']); // this might need to be changed to trygps.py; Victor to confirm

sensorProcess.stdout.on('data', data => {
  if(data.toString().includes("test-photo")){
    // Post data to server
    postPhotos(0, "fire_drone.png")
    console.log("Sending photo to server")

  }
  else{
    console.log("something is wrong...")
  }

});

sensorProcess.on('exit', (code) => {
  console.log(`Child process exited with code ${code}`);
});

/*
 * Server
*/
const port = process.env.PORT || 5001;

app.get('/', function (req, res) {
  res.send('Welcome to FireDrone Raspberry Pi Server!');
});

app.listen(port, () => {
  console.log('Raspberry Pi server running!');
});
