import json
def pprint(someObject):
    if (type(someObject) is dict):
        print(json.dumps(someObject, indent=4, default=str))
    elif (type(someObject) is list):
        for item in someObject:
            print(json.dumps(item, indent=4, default=str))
    else:
        print(someObject)