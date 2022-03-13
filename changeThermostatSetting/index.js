const axios = require("axios");

// Load the AWS SDK
const AWS = require('aws-sdk');

const region = "us-west-2";
const secretName = "CMPT_Pi_Secret";

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
    console.log(event['mode']);
    console.log(event['temperature']);
    const {base_url, project_id, device_id, access_token, refresh_token, client_id, client_secret } = await getSecrets(secretName);
    
    
    let url = `${base_url}/enterprises/${project_id}/devices/${device_id}:executeCommand`;
    
    
    
    try {
        // Change Mode
        await axios({
            method: "post",
            url: url,
            headers: {
              "Authorization": `Bearer ${access_token}`  
            },
            data: {
                command : "sdm.devices.commands.ThermostatMode.SetMode",
                params : {
                    "mode" : event['mode']
                }
            }
        });
        
        // Change the setting value for temperature
        if (event['mode'] == "HEAT") {
            console.log("Changing heat temperature...");
            await axios({
                method: "post",
                url: url,
                headers: {
                  "Authorization": `Bearer ${access_token}`  
                },
                data: {
                    command : "sdm.devices.commands.ThermostatTemperatureSetpoint.SetHeat",
                    params : {
                        "heatCelsius" : event['temperature']
                    }
                }
            });
        } else {
            await axios({
                method: "post",
                url: url,
                headers: {
                  "Authorization": `Bearer ${access_token}`  
                },
                data: {
                    command : "sdm.devices.commands.ThermostatTemperatureSetpoint.SetCool",
                    params : {
                        "coolCelsius" : event['temperature']
                    }
                }
            });
        }
        
        
        return {
            statusCode: 200,
            body: JSON.stringify('Succeed!'),
        };
    }catch (err) {
        console.log(err, err.stack);
        return {
            statusCode: 400,
            body: JSON.stringify('Failed!'),
        };
    }
    
};
