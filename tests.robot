*** Settings ***
Library  web_socket_client.WebSocketClient  *TOKEN*  WITH NAME  ws_client
Library  rest_api_client.RestApiClient  *TOKEN*  WITH NAME  rest_client
Library  helpers
Library  DateTime
Library  Collections


*** Variables ***
${symbol}  BINANCE:BTCUSDT
${forex_exchange}  fxcm
${count}  30
${endpoint}  symbol
&{params}=  exchange=oanda


*** Test Cases ***
Check price update
  ${ws}  ws_client.open_connection
  ws_client.subscribe_to_last_price_updates  ${ws}  ${symbol}
  @{price_updates}  ws_client.get_price_updates  ${ws}
  FOR  ${update}  IN  @{price_updates}
    Should Be Equal  ${symbol}  ${update}[s]
    Should Be True  ${update}[p] > 0
    Should Be True  ${update}[v] > 0
  END
  [Teardown]  ws_client.close_connection  ${ws}
  
  
Check symbols for forex exchange
  @{symbols}  rest_client.get_symbols_for_forex_exchange  ${forex_exchange}
  @{static_list}  get_symbols_list  ${forex_exchange}
  FOR  ${symbol}  IN  @{static_list}
    Should contain  ${symbols}  ${symbol}
  END
  
  
Get performance statistics
  @{responses_list}  Create List
  FOR  ${i}  IN RANGE  ${count}
    ${start_time}  Get Current Date
    rest_client.execute_get_request  ${endpoint}  ${params}
    ${end_time}  Get Current Date
    ${response_time}  Subtract Date From Date  ${end_time}  ${start_time}
    Append To List  ${responses_list}  ${response_time}
  END
  get_statistics_for_endpoint  ${endpoint}  ${responses_list}
  