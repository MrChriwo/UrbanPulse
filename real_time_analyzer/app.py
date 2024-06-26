
from local_data.local_data_handler import LocalDataHandler

ld_handler = LocalDataHandler()

print("longitudes: ", ld_handler.get_longitudes())
print("latitudes: ", ld_handler.get_latitudes())
print("identifiers: ", ld_handler.get_identifiers())

print("data", ld_handler.get_data())

