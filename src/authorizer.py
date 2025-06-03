def generate_policy(principal_id, effect, resource):
    auth_response = {}
    auth_response["principalId"] = principal_id
    if effect and resource:
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {"Action": "execute-api:Invoke", 
                 "Effect": effect, 
                 "Resource": resource}
            ],
        }
        auth_response["policyDocument"] = policy_document
    return auth_response


def lambda_handler(event, context):

    token = event["authorizationToken"]

    valid_token = "abc123"

    if token == valid_token:
        return generate_policy("user", "Allow", event["methodArn"])
    else:
        return generate_policy("user", "Deny", event["methodArn"])
