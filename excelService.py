from mongoService import MongoDBConnection
import pandas as pd


if(__name__ == '__main__'):
    
    connection = MongoDBConnection()
    data = connection.get_all_documents('datacollection')
    df = pd.DataFrame(data)

    df.to_excel('gyalcinkaya_connections.xlsx', index=False)

    print(f"Data exported successfully.")