import axios from 'axios';

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
const postPhotos = (photoCollection) => {

    axios.post("http://localhost:5000/photos/", photoCollection)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                });

}

exports.postData = postData;