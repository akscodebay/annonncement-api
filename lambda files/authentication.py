import json

def generatePolicyDocument(effect, methodArn):
    if effect == '' or methodArn == '':
        return null

    policyDocument = {
        'Version': '2012-10-17',
        'Statement': [{
            'Action': 'execute-api:Invoke',
            'Effect': effect,
            'Resource': methodArn
        }]
    }

    return policyDocument

def generateAuthResponse(principalId, effect, methodArn):
    policyDocument = generatePolicyDocument(effect, methodArn)

    return {
        'principalId': principalId,
        'policyDocument':policyDocument
    }

def lambda_handler(event, context):
    token = event['authorizationToken']
    methodArn = event['methodArn']
    
    if token == 'aayushkumarsrivastava':
        return generateAuthResponse('user', 'Allow', methodArn);
    else:
        return generateAuthResponse('user', 'Deny', methodArn);
    
