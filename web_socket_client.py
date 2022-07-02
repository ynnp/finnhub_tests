import json
import websocket
from robot.api import logger
    

class WebSocketClient(object):
    """ Class to interact with web socket
    """
    HOST = "ws.finnhub.io"
    
    def __init__(self, token: str) -> None:
        self.__token = token
        self.__url = self.__get_url()
        

    def __get_url(self) -> str:
        url = "wss://{host}?token={token}".format(host=WebSocketClient.HOST, token=self.__token)
        
        return url


    def open_web_socket_connection(self) -> websocket:
        web_socket = websocket.WebSocket()
        web_socket.connect(self.__url)
        logger.info("Opened web socket to {0} host.".format(WebSocketClient.HOST))
        
        return web_socket
        
        
    def subscribe_to_last_price_updates(self, web_socket: websocket, symbol: str) -> None:
        data = {"type": "subscribe", "symbol": symbol}
        web_socket.send(json.dumps(data))
        logger.info("Successfully subscribed to {0}.".format(symbol))
            
            
    def get_price_updates(self, web_socket: websocket) -> list:
        updates = web_socket.recv()
        updates = json.loads(updates)
        logger.info("Received updates: {0}".format(updates))
        
        return updates["data"]


    def close_web_socket_connection(self, web_socket: websocket) -> None:
        web_socket.close()
        logger.info("Web socket was closed.")
