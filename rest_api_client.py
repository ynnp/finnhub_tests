import requests
import time
from robot.api import logger


class RestApiClient(object):
    """ Class to interact with REST API
    """
    HOST = "finnhub.io"
    
    def __init__(self, token: str) -> None:
        self.api_url = self.get_api_url()
        self.__token = token
        self.__auth_header = self.__get_auth_header()
        self.__session = requests.session()
        self.__session.headers.update(self.__auth_header)
        
    
    def __get_auth_header(self) -> dict:
        header = {'X-Finnhub-Token': self.__token}
        
        return header
        
    
    def get_api_url(self) -> str:
        api_url = "https://{host}/api/v1/forex".format(host=RestApiClient.HOST)
        
        return api_url
        
        
    def get_symbols_for_forex_exchange(self, forex_exchange: str) -> list:
        symbol_url = "{api_url}/symbol?exchange={forex_exchange}".format(api_url=self.api_url, forex_exchange=forex_exchange)
        symbols_data = self.__session.get(symbol_url)
        symbols = []
        for obj in symbols_data.json():
            symbols.append(obj["symbol"])
            
        return symbols
        
    
    def execute_get_request(self, endpoint: str, params: dict) -> None:
        url = "{api_url}/{endpoint}".format(api_url=self.api_url, endpoint=endpoint)
        requests.get(url, params=params, headers=self.__auth_header)
