const axios = require('axios');
const FormData = require('form-data');
var fs = require('fs');
var path = require('path');

/**
 * POST method to send a collection of photos to the backend
 * @param {number} incidentNum - Number to keep track of alert/ IFR
 * @param {object[]} photos - Array of photos
 * @param {buffer} photos.data
 * @param {string} photos.dataType
 * @param {string} photos.time
 * @param {object} photos.coordinate
 * @param {number} photos.coordinate.longitutde
 * @param {number} photos.coordinate.latitude
 */
const postPhotos = (incidentNum, fileName) => {
    let imgPath = path.join(__dirname, '../photos/' + fileName);
    let data = new FormData();
    data.append('incidentNum', incidentNum)
    data.append('photo', fs.createReadStream(imgPath));

    axios.post("http://localhost:5000/photos/", data, {
        headers: {
            'accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.8',
            'Content-Type': `multipart/form-data; boundary=${data._boundary}`
        }})
        .then((response) => {
            console.log(response);
        })
        .catch((error) => {
            console.log(error);
        });

}

exports.postPhotos = postPhotos;