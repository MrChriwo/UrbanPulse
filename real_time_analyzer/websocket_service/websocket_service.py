from websocket import WebSocketApp, enableTrace
import threading
import time
import json


class WebSocketClient:
    def __init__(self, url, token, process_classback = lambda x: print(x)):
        self.url = url
        self.token = token
        self.ws = None
        self.process_classback = process_classback

    def on_message(self, ws, message):
        self.process_classback(message)
    

    def on_error(self, ws, error):
        print("Error: " + str(error))

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed websocket connection ###")

    def on_open(self, ws):
        def run(*args):
            while True:
                time.sleep(1)
                ws.send("ping")
        thread = threading.Thread(target=run)
        thread.daemon = True 
        thread.start()

    def run_forever(self):
        # enableTrace(True)
        self.ws = WebSocketApp(self.url,
                               header={"Authorization": f"Basic {self.token}"},
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(ping_interval=1)  

if __name__ == "__main__":
    ws_client = WebSocketClient("wss://da-mobility.urbanpulse.de/OutboundInterfaces/outbound/SwarcoTMSEventTypeStatement", "c3dlaWZmZW5iYWNoOmwwc0tKOUxaZGV2Sk9vSkk0S3c2")
    ws_client.run_forever()