import constants

import statistics
from robot.api import logger


def get_symbols_list(forex_exchange: str) -> list:
        return constants.SYMBOLS[forex_exchange]
        
 
def get_statistics_for_endpoint(endpoint: str, response_time: list) -> None:
    average_time = statistics.mean(response_time)
    standard_deviation = statistics.stdev(response_time)
     
    logger.info("{endpoint} endpoint:".format(endpoint=endpoint.upper()))
    logger.info("- mean time = {time} s".format(time=round(average_time, 5)))
    logger.info("- standart deviation = {stdev} s".format(stdev=round(standard_deviation, 5)))