*** Settings ***
Library  web_socket_client.WebSocketClient  *TOKEN*  WITH NAME  ws_client
Library  rest_api_client.RestApiClient  *TOKEN*  WITH NAME  rest_client
Library  helpers


*** Variables ***
${symbol}  BINANCE:BTCUSDT
${forex_exchange}  fxcm
${endpoint}  symbol
&{params}=  exchange=oanda


*** Test Cases ***
Check price update
  ${ws}  ws_client.open_web_socket_connection
  ws_client.subscribe_to_last_price_updates  ${ws}  ${symbol}
  @{price_updates}  ws_client.get_price_updates  ${ws}
  FOR  ${update}  IN  @{price_updates}
    Should Be Equal  ${symbol}  ${update}[s]
	Should Be True  ${update}[p] > 0
	Should Be True  ${update}[v] > 0
  END
  [Teardown]  ws_client.close_web_socket_connection  ${ws}
  
  
Check symbols for forex exchange
  @{symbols}  rest_client.get_symbols_for_forex_exchange  ${forex_exchange}
  @{static_list}  get_symbols_list  ${forex_exchange}
  FOR  ${symbol}  IN  @{static_list}
    Should contain  ${symbols}  ${symbol}
  END
  
  
Get performance statistics
  @{response_time}  rest_client.get_response_time  ${endpoint}  ${params}
  get_statistics_for_endpoint  ${endpoint}  ${response_time}