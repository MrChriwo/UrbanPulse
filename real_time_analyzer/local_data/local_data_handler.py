import pandas as pd 
import sys 
import os 


class LocalDataHandler():

    def __init__(self, file: str = "LSAs.xlsx"):
        self._file = file
        self.identifiers = []
        self.longitude = []
        self.latitude = []

        self.initilize_data()


    def initilize_data(self):
        try: 
            df = pd.read_excel(self._file)
            self.identifiers = df['lsa']
            self.longitude = df['laengengrad']
            self.latitude = df['breitengrad']

            print("Local data loaded successfully")
        
        except Exception as e:
            print(f"Error loading local data: {e}")

    def _is_source_available(self, target: list) -> bool:
        return len(target) > 0

    def get_data(self) -> tuple:
        if not self._is_source_available(self.longitude) or not self._is_source_available(self.latitude) or not self._is_source_available(self.identifiers):
            raise Exception("No data loaded")

        return self.identifiers, self.longitude, self.latitude
    
    def get_longitudes(self) -> list:
        if not self._is_source_available(self.longitude):
            raise Exception("Could not get longitudes. No data loaded")
        
        return self.longitude
    
    def get_latitudes(self) -> list:
        if not self._is_source_available(self.latitude):
            raise Exception("Could not get latitudes. No data loaded")
        
        return self.latitude
    
    def get_identifiers(self) -> list:
        if not self._is_source_available(self.identifiers):
            raise Exception("Could not get identifiers. No data loaded")
        
        return self.identifiers
        