from worker import handler
import json
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    print(req)
    return handler.handle(json.loads(req))
