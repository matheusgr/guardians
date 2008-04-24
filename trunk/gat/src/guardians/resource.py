import os

def find_resource(resource):
    path = os.path.dirname(__file__)
    return os.path.join(path, "resource", resource)