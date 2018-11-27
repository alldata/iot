# The code to be used as an AWS Lambda function for processing API calls
# and storing data in Amazon S3
#import base64
import json
import requests

# Send a request to the Kaiterra API to retrieve data
def retrieveKaiterra(kaiterraId):
    apiEndpoint = 'http://' + str(kaiterraId)
    data = requests.get(apiEndpoint).json()
    return data

# Send a request to the Airly API to retrieve data
def retrieveAirly(AirlyId):
    apiEndpoint = 'http://' + str(AirlyId)
    data = requests.get(apiEndpoint).json()
    return data

# The handler for the Lambda function
def processRecord(event, context):
    output = []
    
    kaiterra = retrieveKaiterra('ID')
    enrichedKaiterra = {
            'goodevil': kaiterra['goodevil'],
            'lawchaos': kaiterra['lawchaos'],
            'species': kaiterra['species']
        }

    # retrieve the list of records and enrich
    for record in event['records']:
        print('Processing record: ' + record['recordId'])
        #click = json.loads(base64.b64decode(record['data']))

        airly = retrieveAirly('ID')

        enrichedAirly = {
                'goodevil': airly['goodevil'],
                'lawchaos': airly['lawchaos'],
                'species': airly['species']
            }

        output.append(enrichedAirly)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}
