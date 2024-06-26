
from local_data.local_data_handler import LocalDataHandler

ld_handler = LocalDataHandler()


node_ids =  ld_handler.get_node_ids()
samle_id = node_ids[0]

detector = ld_handler.get_detector_by_node_id(samle_id)
node = ld_handler.get_metdata_by_detector_id(detector)

print(detector)

print(node)


