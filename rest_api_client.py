import constants

import requests
import statistics
import time
from robot.api import logger


class RestApiClient(object):
    """ Class to interact with REST API
    """
    HOST = "finnhub.io"
    
    def __init__(self, token: str) -> None:
        self.__token = token
        self.__header = self.__get_header()
        self.api_url = self.get_api_url()
        
    
    def __get_header(self) -> dict:
        header = {'X-Finnhub-Token': self.__token}
        
        return header
        
    
    def get_api_url(self) -> str:
        api_url = "https://{host}/api/v1/forex".format(host=RestApiClient.HOST)
        
        return api_url
        
        
    def get_symbols_for_forex_exchange(self, forex_exchange: str) -> list:
        symbol_url = "{api_url}/symbol?exchange={forex_exchange}".format(api_url=self.api_url, forex_exchange=forex_exchange)
        symbols_data = requests.get(symbol_url, headers=self.__header)
        symbols = []
        for obj in symbols_data.json():
            symbols.append(obj["symbol"])
            
        return symbols
        
    
    def get_response_time(self, endpoint: str, params: dict, count: int = 30) -> list:
        url = "{api_url}/{endpoint}".format(api_url=self.api_url, endpoint=endpoint)
        response_time = []
        logger.info("Accessing {endpoint} endpoint for {count} times.".format(endpoint=endpoint.upper(), count=count))
        for _ in range(count):
            start_time = time.perf_counter()
            requests.get(url, params=params, headers=self.__header)
            elapsed_time = time.perf_counter() - start_time
            response_time.append(elapsed_time)
        
        return response_time
    
    
    @staticmethod
    def get_symbols_list(forex_exchange: str) -> list:
        return constants.SYMBOLS[forex_exchange]
        
    
    @staticmethod
    def get_statistics_for_endpoint(endpoint: str, response_time: list) -> None:
        average_time = statistics.mean(response_time)
        standard_deviation = statistics.stdev(response_time)
        
        logger.info("{endpoint} endpoint:".format(endpoint=endpoint.upper()))
        logger.info("- mean time = {time} s".format(time=round(average_time, 5)))
        logger.info("- standart deviation = {stdev} s".format(stdev=round(standard_deviation, 5)))  
