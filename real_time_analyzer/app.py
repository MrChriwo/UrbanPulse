
from local_data.local_data_handler import LocalDataHandler
from websocket_service.websocket_service import WebSocketClient
import dotenv
import os
import json
from plotter.plotter import RealTimeGeoPlotter
import threading

import pandas as pd 



dotenv.load_dotenv()
access_token = os.getenv("ACCESS_TOKEN")
ws_url = os.getenv("WS_URL")

local_data = LocalDataHandler()


metadata = local_data.get_metadata()
location_data = local_data.get_location_data()
node_ids = location_data[0]

longitudes = location_data[1]
latituteds = location_data[2]

plotter = RealTimeGeoPlotter(longitudes, latituteds, [0] * len(node_ids))


detectors = metadata.keys()
detector_fails = 0

# dict to ount available nodes
node_count = {key: 0 for key in node_ids}
node_fail_count = []
available_nodes = []


def process_ws_data(data):
    try: 
        global detector_fails
        global node_fail_count
        global node_count

        data = json.loads(data)

        node_id = data["Bezeichnung"]
        node_id = node_id.replace(" ", "")
        
        if not node_id[0].isalpha() or len(node_id) < 4:
            if len(node_id) < 3:
                # add two zeros from the 2nd index
                node_id = node_id[:1] + "00" + node_id[1:]
            else:
                node_id = node_id[:1] + "0" + node_id[1:]
            

        if node_id not in node_ids and node_id not in node_fail_count:
            node_fail_count.append(node_id)
            return
    
        if node_id not in available_nodes:
            available_nodes.append(node_id)
        
        node_count[node_id] += 1

        node_meta_index = node_ids.index(node_id)
        node_lat = latituteds[node_meta_index]
        node_lon = longitudes[node_meta_index]

        availality = node_count[node_id]

        plotter.add_data(node_lon, node_lat, availality)

        # calc the percetage of available nodes
        total_nodes = len(node_ids)
        availbe_nodes = len(available_nodes)
        percentage = (availbe_nodes / total_nodes) * 100

        print(f"Percentage of available nodes: {percentage}%\r")


    except Exception as e:
        print(f"Error processing data: {e}")



def run_websocket():
    ws_client = WebSocketClient(ws_url, access_token, process_ws_data)
    ws_client.run_forever()


if __name__ == "__main__":    
    ws_thread = threading.Thread(target=run_websocket)

    ws_thread.start()

    plotter.show_plot()

    # if script exits, create a dataframe of node_count and sacve it to a csv file

    data = {
        "Node": list(node_count.keys()),
        "Count": list(node_count.values()), 
    }

    df = pd.DataFrame(data)
    df.to_csv("node_count.csv", index=False)



