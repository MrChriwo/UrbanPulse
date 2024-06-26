import pandas as pd 
import sys 
import os 


class LocalDataHandler():

    def __init__(self, locations_file: str = "LSAs.xlsx", meta_file: str = "metadata.xlsx"):
        self._locations_file = locations_file
        self._meta_file = meta_file
        self.node_ids = []
        self.longitude = []
        self.latitude = []
        self.metadata = dict()
        self.id_losses = 0

        self._initilize_data()


    def _init_location_data(self) -> tuple:

        df = pd.read_excel(self._locations_file)
        self.node_ids = df['lsa'].to_list()
        self.longitude = df['laengengrad'].to_list()
        self.latitude = df['breitengrad'].to_list()

        print("Local data loaded successfully")

        
    def _init_metadata(self) -> tuple:
        try:
            df = pd.read_excel(self._meta_file)
            filtered_by_detector = df[df['Typ'] == 'Detektor']

            for index, row in filtered_by_detector.iterrows():
                key = row['Bezeichnung im WebSocket']

                if key not in self.metadata:
                    self.metadata[key] = {
                        "node_id": [],
                        "real_name": []
                    }

                id = (row['Knotenpunkt'])

                if id not in self.node_ids:
                    self.id_losses += 1
                    continue

                self.metadata[key]["node_id"].append(id)
                self.metadata[key]["real_name"].append(row['Reale Bezeichnung'])

        except Exception as e:
            print(f"Error loading metadata: {e}")


    def _initilize_data(self):
        self._init_location_data()
        self._init_metadata()


    def _is_source_available(self, target: list) -> bool:
        return len(target) > 0
    

    def get_location_data(self) -> tuple:
        """
        Returns a tuple containing the node_ids, longitudes and latitudes
        """
        if not self._is_source_available(self.longitude) or not self._is_source_available(self.latitude) or not self._is_source_available(self.identifiers):
            raise Exception("No data loaded")

        return self.node_ids, self.longitude, self.latitude
    
    
    def get_longitudes(self) -> list:
        """
        Returns a list of all the longitudes
        """
        if not self._is_source_available(self.longitude):
            raise Exception("Could not get longitudes. No data loaded")
        
        return self.longitude
    

    def get_latitudes(self) -> list:
        """
        Returns a list of all the latitudes
        """
        if not self._is_source_available(self.latitude):
            raise Exception("Could not get latitudes. No data loaded")
        
        return self.latitude
    

    def get_node_ids(self) -> list:
        """
        Returns a list of all the node ids - Example: A001
        """
        if not self._is_source_available(self.node_ids):
            raise Exception("Could not get identifiers. No data loaded")
        
        return self.node_ids
        

    def get_metadata(self) -> dict:
        """
        Returns a dictionary containing all the metadata for each detector
        """
        if not self._is_source_available(self.metadata.keys()):
            raise Exception("Could not get metadata. No data loaded")
        
        return self.metadata
    

    def get_metdata_by_detector_id(self, detector_id: str) -> dict:
        """
        Returns the metadata for a specific detector_id
        """
        if not self._is_source_available(self.metadata.keys()):
            raise Exception("Could not get metadata. No data loaded")
        try:
            return self.metadata[detector_id]
        except KeyError:
            raise Exception(f"Could not find metadata for detector_id: {detector_id}")
       
        
    def get_detector_by_node_id(self, node_id: str) -> dict:
        """
        Returns the detector_id for a specific node_id - Example: D01-16
        """
        if not self._is_source_available(self.metadata.keys()):
            raise Exception("Could not get metadata. No data loaded")
        
        try: 
            for key, value in self.metadata.items():
                if node_id in value["node_id"]:
                    return key
        except KeyError:
            raise Exception(f"Could not find metadata for node_id: {node_id}")


if __name__ == "__main__":
    ld_handler = LocalDataHandler()
    print("metadata: ", ld_handler.get_metadata().keys())
    print("losed ids: ", ld_handler.id_losses)
    print("length of ids", len(ld_handler.identifiers))

