from payloads import *

def handle_request(client_request):
    """
    This function will be called when a request is received from the client.
    It must return the request to be forwarded to the server (or proxy if specified).
    """


    """ Group parent(finalproject-mclean-parent)
    python mitm.py -r udp:8084:localhost:8080 -s mitm-script.py --replay True
    python chatClient.py -u bob -sip 127.0.0.1 -w ILoveTheCats -sp 8084 -pub ./rsa_keys/bob_public_key.der  -priv ./rsa_keys/bob_private_key.pem -servpub ./rsa_keys/alice_public_key.der
    payload = PARENT_FAIL_REPLAY
    """
    return PARENT_FAIL_REPLAY


def handle_response(server_response):
    """
    This function will be called when a response is received from the server.
    It must return the response to be fowarded to the client (or proxy if specified).
    """

    modified_response = server_response.replace('example', 'testing')
    print 'resp'

    return modified_response
