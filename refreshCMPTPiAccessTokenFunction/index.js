const axios = require("axios");
const AWS = require('aws-sdk');

const region = "us-west-2";
const secretName = "arn:aws:secretsmanager:us-west-2:536482454474:secret:CMPT_Pi_Secret-L3S9Di";

// Create a Secrets Manager client
const sm = new AWS.SecretsManager({
    region: region
});

const getSecrets = async (SecretId) => {
    return await new Promise((resolve, reject) => {
        sm.getSecretValue({SecretId}, (err, result) => {
            if (err) {
                reject(err);
            } else {
                // console.log(result.SecretString);  // For testing
                resolve(JSON.parse(result.SecretString)); // get the secret string that contains key-value pairs
            }
        })
    })
}

exports.handler = async (event) => {
    let {base_url, project_id, device_id, access_token, refresh_token, client_id, client_secret } = await getSecrets(secretName);
    
    let refresh_url = `https://www.googleapis.com/oauth2/v4/token?client_id=${client_id}&client_secret=${client_secret}&refresh_token=${refresh_token}&grant_type=refresh_token`;
    const result = await axios.post(refresh_url);
    let newAccessToken = result.data.access_token;
    let newSecretString = `{"base_url":"${base_url}","project_id":"${project_id}","device_id":"${device_id}","access_token":"${newAccessToken}","refresh_token":"${refresh_token}","client_id":"${client_id}","client_secret":"${client_secret}"}`;
    
    let params = {
        SecretId: secretName,
        SecretString: newSecretString
    };
    
    await sm.putSecretValue(params, function(err, data) {
        if (err) console.log(err, err.stack);
        else {
            console.log("Successfully refreshed the access_token!");
        }
    })
    
    const response = {
        statusCode: 200,
        body: JSON.stringify('Successfully refreshed the access_token!'),
    };
    return response;
};
