// import axios from 'axios';

const postData = (data) => {

    console.log("Data is: " + data);
    
    // axios.post("http://localhost:5000/sensor-data/add", data)
    //             .then((response) => {
    //                 console.log(response);
    //             })
    //             .catch((error) => {
    //                 console.log(error);
    //             });
}

exports.postData = postData;