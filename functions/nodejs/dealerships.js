const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

const DATABASE_DEALERSHIPS = 'dealerships'

function main(params) {

    const authenticator = new IamAuthenticator({apikey: params.IAM_API_KEY});

    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });

    cloudant.setServiceUrl(params.COUCH_URL);

    //GET
    if (params.__ow_method === 'get') {

        if (params.state && params.state !== '') {

            //return {body: params}
            return getDataByState(cloudant, params.state);

        } else {

            return getData(cloudant);
        }
    }

    return {
        statusCode: 400,
        headers: {'Content-Type': 'application/json'},
        body: {error: 'Bad Request', code: 400}
    };
}

function getData(cloudant) {
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({db: DATABASE_DEALERSHIPS, includeDocs: true, limit: 1000})
            .then(response => {

                if (response.result.rows.length) {
                    //parse data
                    let result = response.result.rows.map(
                        ({doc: {id, city, state, st, address, zip, lat, long, short_name, full_name}}) => {
                            return {
                                id,
                                city,
                                state,
                                st,
                                address,
                                zip,
                                lat,
                                long,
                                short_name,
                                full_name
                            }
                        })

                    resolve({
                        statusCode: 200,
                        headers: {'Content-Type': 'application/json'},
                        body: result
                    });

                } else {

                    resolve({
                        statusCode: 404,
                        headers: {'Content-Type': 'application/json'},
                        body: {message: 'Not Found', code: 404}
                    });
                }
            })
            .catch(err => {

                switch (err.code) {
                    case 404:

                        resolve({
                            statusCode: 404,
                            headers: {'Content-Type': 'application/json'},
                            body: {message: 'Not Found', code: 404}
                        });
                        break;

                    default:

                        reject({
                            statusCode: 500,
                            headers: {'Content-Type': 'application/json'},
                            body: {message: 'Internal Server Error', code: 500}
                        });
                }
            });
    });
}

function getDataByState(cloudant, state) {
    return new Promise((resolve, reject) => {

        const selector = CloudantV1.Selector = {
            state: state,
            _id: {"$gte": 0}
        };

        cloudant.postFind({
            db: DATABASE_DEALERSHIPS,
            selector: selector,
            fields: ['id', 'city', 'state', 'st', 'address', 'zip', 'lat', 'long', 'short_name,', 'full_name'],
            sort: [{'_id': 'asc'}]
        }).then(response => {

            if (response.result.docs.length) {

                resolve({
                    statusCode: 200,
                    headers: {'Content-Type': 'application/json'},
                    body: response.result.docs
                });

            } else {

                resolve({
                    statusCode: 404,
                    headers: {'Content-Type': 'application/json'},
                    body: {message: 'Not Found', code: 404}
                });
            }
        })
            .catch(err => {

                switch (err.code) {
                    case 404:

                        resolve({
                            statusCode: 404,
                            headers: {'Content-Type': 'application/json'},
                            body: {message: 'Not Found', code: 404}
                        });
                        break;

                    default:

                        reject({
                            statusCode: 500,
                            headers: {'Content-Type': 'application/json'},
                            body: {message: 'Internal Server Error', code: 500}
                        });
                }
            });
    });
}
