import axios from 'axios';

/**
 * POST method to send data struct to backend
 * @param {object} alert 
 * @param {int} alert.incidentNum
 * @param {object} alert.coordinates
 * @param {double} alert.coordinates.longitude
 * @param {double} alert.coordinates.lattitude
 */
const postData = (alert) => {

    axios.post("http://localhost:5000/sensor-data/", alert)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                });

}

exports.postData = postData;