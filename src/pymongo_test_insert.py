import json
import requests

def get_data(uri, data_format="json"):
    """
        Method description:
        Deletes/Unregisters an application entity(AE) from the OneM2M framework/tree
        under the specified CSE

        Parameters:
        uri_cse : [str] URI of parent CSE
        ae_name : [str] name of the AE
        fmt_ex : [str] payload format
    """
    headers = {
        'X-M2M-Origin': '2vCsok51z6:xB2p5Mj@N2',
        'Content-type': 'application/{}'.format(data_format)}

    response = requests.get(uri, headers=headers)
    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))
    _resp = json.loads(response.text)
    return response.status_code, _resp["m2m:cin"]["con"] ## To get latest or oldest content instance
    #return response.status_code, _resp["m2m:cnt"]#["con"] ## to get whole data of container (all content instances)

def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://poojadesur:123@obstacleavoidingrobot.obaea.mongodb.net/Team11?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    print("client created")
    # Create the database for our example (we will use the same database throughout the tutorial
    return client['Team11']

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()
    collection_name = dbname["directions"]

    print("collection created")

    uri_cnt = "https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-11/Node-1/Data"

    
    print(get_data(uri_cnt + "/Directions"))



    # collection_name.insert_many([item_1,item_2])


    print("data inserted")



