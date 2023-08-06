# DeviceServer.DevicesApi

All URIs are relative to *http://localhost/DeviceServer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_device_device_id_ports**](DevicesApi.md#get_device_device_id_ports) | **GET** /Devices/{device_id}/Ports | GET all ports for device
[**get_device_id_port_index**](DevicesApi.md#get_device_id_port_index) | **GET** /Devices/{device_id}/Ports/{port_index} | GET status of port
[**get_devices**](DevicesApi.md#get_devices) | **GET** /Devices | GET list of devices
[**get_devices_button**](DevicesApi.md#get_devices_button) | **GET** /Devices/{device_id}/Button | GET state of button
[**get_devices_index**](DevicesApi.md#get_devices_index) | **GET** /Devices/{device_id} | GET single device
[**get_devices_led**](DevicesApi.md#get_devices_led) | **GET** /Devices/{device_id}/Leds/{led_index} | GET state of LED
[**get_devices_temperature**](DevicesApi.md#get_devices_temperature) | **GET** /Devices/{device_id}/Temperature | Your GET endpoint
[**get_host_config**](DevicesApi.md#get_host_config) | **GET** /Host/Config | Your GET endpoint
[**get_port**](DevicesApi.md#get_port) | **GET** /Port/{port_id} | GET status of port by id
[**get_port_states**](DevicesApi.md#get_port_states) | **GET** /PortStates/{port_id} | Your GET endpoint
[**get_ports**](DevicesApi.md#get_ports) | **GET** /Ports | GET status of all ports
[**get_relay_state**](DevicesApi.md#get_relay_state) | **GET** /Devices/{device_id}/Relay | Your GET endpoint
[**get_temperature_range**](DevicesApi.md#get_temperature_range) | **GET** /Devices/{device_id}/Temperature/Range | Your GET endpoint
[**get_temperature_thresholds**](DevicesApi.md#get_temperature_thresholds) | **GET** /Devices/{device_id}/Temperature/Thresholds | Your GET endpoint
[**put_device_device_id_description**](DevicesApi.md#put_device_device_id_description) | **PUT** /Device/{device_id}/Description | 
[**put_device_device_id_name**](DevicesApi.md#put_device_device_id_name) | **PUT** /Device/{device_id}/Name | 
[**put_device_id_label**](DevicesApi.md#put_device_id_label) | **PUT** /Device/{device_id}/Port/{port_index}/Label | 
[**put_devices_led_index**](DevicesApi.md#put_devices_led_index) | **PUT** /Devices/{device_id}/Leds/{led_index} | PUT state of LED
[**put_devices_ports**](DevicesApi.md#put_devices_ports) | **PUT** /Devices/{device_id}/Ports/{port_index} | PUT state of port
[**put_devices_ports_pulse**](DevicesApi.md#put_devices_ports_pulse) | **PUT** /Devices/{device_id}/Ports/{port_index}/Pulse | PUT port into state for period of time
[**put_host_config**](DevicesApi.md#put_host_config) | **PUT** /Host/Config | 
[**put_port_port_id_label**](DevicesApi.md#put_port_port_id_label) | **PUT** /Port/{port_id}/Label | 
[**put_port_states_port_id**](DevicesApi.md#put_port_states_port_id) | **PUT** /PortStates/{port_id} | 
[**put_ports_pulse**](DevicesApi.md#put_ports_pulse) | **PUT** /Ports/{port_index}/Pulse | PUT port into state for period of time
[**put_relay_state**](DevicesApi.md#put_relay_state) | **PUT** /Devices/{device_id}/Relay | 
[**put_socket_refresh**](DevicesApi.md#put_socket_refresh) | **PUT** /Devices/{device_id}/Socket/Refresh | 
[**put_state_by_port_id**](DevicesApi.md#put_state_by_port_id) | **PUT** /Port/{port_id} | PUT state of port


# **get_device_device_id_ports**
> list[DevicePort] get_device_device_id_ports(device_id)

GET all ports for device

returns a list of all ports attached to a device

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device

    try:
        # GET all ports for device
        api_response = api_instance.get_device_device_id_ports(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_device_id_ports: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 

### Return type

[**list[DevicePort]**](DevicePort.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_device_id_port_index**
> DevicePort get_device_id_port_index(device_id, port_index)

GET status of port

returns status of ports

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of port

    try:
        # GET status of port
        api_response = api_instance.get_device_id_port_index(device_id, port_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_id_port_index: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of port | 

### Return type

[**DevicePort**](DevicePort.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_devices**
> list[Device] get_devices()

GET list of devices

Returns list of devices

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    
    try:
        # GET list of devices
        api_response = api_instance.get_devices()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_devices: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Device]**](Device.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_devices_button**
> GetDevicesLed200Response get_devices_button(device_id, button_index)

GET state of button

Returns state of the selected devices button

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
button_index = 56 # int | index of the button on tha device (1-100)

    try:
        # GET state of button
        api_response = api_instance.get_devices_button(device_id, button_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_devices_button: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **button_index** | **int**| index of the button on tha device (1-100) | 

### Return type

[**GetDevicesLed200Response**](GetDevicesLed200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_devices_index**
> Device get_devices_index(device_id)

GET single device

Gets information for a single device

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device

    try:
        # GET single device
        api_response = api_instance.get_devices_index(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_devices_index: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 

### Return type

[**Device**](Device.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_devices_led**
> GetDevicesLed200Response get_devices_led(device_id, led_index)

GET state of LED

Returns state of selected led on selected device

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
led_index = 56 # int | Index of LED

    try:
        # GET state of LED
        api_response = api_instance.get_devices_led(device_id, led_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_devices_led: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **led_index** | **int**| Index of LED | 

### Return type

[**GetDevicesLed200Response**](GetDevicesLed200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_devices_temperature**
> float get_devices_temperature(device_id, thermometer_index)

Your GET endpoint

Get temperature reading from specified device

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
thermometer_index = 56 # int | Index of the thermometer (1-7)

    try:
        # Your GET endpoint
        api_response = api_instance.get_devices_temperature(device_id, thermometer_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_devices_temperature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **thermometer_index** | **int**| Index of the thermometer (1-7) | 

### Return type

**float**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_host_config**
> HostConfig get_host_config()

Your GET endpoint

Get config of host, includes ip namme etc

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    
    try:
        # Your GET endpoint
        api_response = api_instance.get_host_config()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_host_config: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**HostConfig**](HostConfig.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_port**
> DevicePort get_port(port_id)

GET status of port by id

returns status of port

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | id of port to set

    try:
        # GET status of port by id
        api_response = api_instance.get_port(port_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_port: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**| id of port to set | 

### Return type

[**DevicePort**](DevicePort.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_port_states**
> list[PortState] get_port_states(port_id)

Your GET endpoint

Gets a list of available port states for a port

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | 

    try:
        # Your GET endpoint
        api_response = api_instance.get_port_states(port_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_port_states: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**|  | 

### Return type

[**list[PortState]**](PortState.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ports**
> DevicePort get_ports()

GET status of all ports

status of port

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    
    try:
        # GET status of all ports
        api_response = api_instance.get_ports()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_ports: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**DevicePort**](DevicePort.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_relay_state**
> GetDevicesLed200Response get_relay_state(device_id, index)

Your GET endpoint

Get state of relay at index

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
index = 56 # int | index of relay to get state of

    try:
        # Your GET endpoint
        api_response = api_instance.get_relay_state(device_id, index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_relay_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **index** | **int**| index of relay to get state of | 

### Return type

[**GetDevicesLed200Response**](GetDevicesLed200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_temperature_range**
> TempRange get_temperature_range(device_id)

Your GET endpoint

Get the minimum and maximum temperatures for a given hex thermometer

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 

    try:
        # Your GET endpoint
        api_response = api_instance.get_temperature_range(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_temperature_range: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 

### Return type

[**TempRange**](TempRange.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_temperature_thresholds**
> list[float] get_temperature_thresholds(device_id)

Your GET endpoint

get the points at which the temperature enters danger zones

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | the device id

    try:
        # Your GET endpoint
        api_response = api_instance.get_temperature_thresholds(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_temperature_thresholds: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| the device id | 

### Return type

**list[float]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_device_device_id_description**
> put_device_device_id_description(device_id, description)



Set Description of the Device hosting ports 

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
description = 'description_example' # str | 

    try:
        # 
        api_instance.put_device_device_id_description(device_id, description)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_device_id_description: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **description** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_device_device_id_name**
> put_device_device_id_name(device_id, name)



set name of device

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | id of device 
name = 'name_example' # str | name to apply to device

    try:
        # 
        api_instance.put_device_device_id_name(device_id, name)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_device_id_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| id of device  | 
 **name** | **str**| name to apply to device | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_device_id_label**
> put_device_id_label(device_id, port_index, label)



Sets the label used for a port

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
port_index = 56 # int | 
label = 'label_example' # str | new label for port

    try:
        # 
        api_instance.put_device_id_label(device_id, port_index, label)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_id_label: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **port_index** | **int**|  | 
 **label** | **str**| new label for port | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_devices_led_index**
> put_devices_led_index(device_id, led_index, state)

PUT state of LED

Set led at index on selected device

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
led_index = 56 # int | Index of LED
state = True # bool | True = LED on, False = LED off

    try:
        # PUT state of LED
        api_instance.put_devices_led_index(device_id, led_index, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_devices_led_index: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **led_index** | **int**| Index of LED | 
 **state** | **bool**| True &#x3D; LED on, False &#x3D; LED off | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_devices_ports**
> put_devices_ports(device_id, port_index, state)

PUT state of port

Set State of Port 

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of port
state = 56 # int | state id to switch to, 1 or more

    try:
        # PUT state of port
        api_instance.put_devices_ports(device_id, port_index, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_devices_ports: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of port | 
 **state** | **int**| state id to switch to, 1 or more | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_devices_ports_pulse**
> put_devices_ports_pulse(device_id, port_index, time, state)

PUT port into state for period of time

Pulse port from one state to another for a period of time in seconds

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of port
time = 3.4 # float | time in seconds to press for 0.1 = 100ms
state = 56 # int | state to switch to

    try:
        # PUT port into state for period of time
        api_instance.put_devices_ports_pulse(device_id, port_index, time, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_devices_ports_pulse: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of port | 
 **time** | **float**| time in seconds to press for 0.1 &#x3D; 100ms | 
 **state** | **int**| state to switch to | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_host_config**
> put_host_config(host_config=host_config)



Set new config of host, includes ip namme etc

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    host_config = DeviceServer.HostConfig() # HostConfig |  (optional)

    try:
        # 
        api_instance.put_host_config(host_config=host_config)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_host_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_config** | [**HostConfig**](HostConfig.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_port_port_id_label**
> put_port_port_id_label(port_id, label=label)



set the label for the port identified by the given id

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | id of port for which label applies
label = 'label_example' # str | new label for the given port (optional)

    try:
        # 
        api_instance.put_port_port_id_label(port_id, label=label)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_port_port_id_label: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**| id of port for which label applies | 
 **label** | **str**| new label for the given port | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_port_states_port_id**
> put_port_states_port_id(port_id, port_state=port_state)



Updates the list of port states for given port 

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | 
port_state = [DeviceServer.PortState()] # list[PortState] | Array of ports states to be used for the port given (optional)

    try:
        # 
        api_instance.put_port_states_port_id(port_id, port_state=port_state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_port_states_port_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**|  | 
 **port_state** | [**list[PortState]**](PortState.md)| Array of ports states to be used for the port given | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_ports_pulse**
> put_ports_pulse(port_index, device_id, time, state)

PUT port into state for period of time

Pulse port from one state to another for a period of time in seconds

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    port_index = 56 # int | Index of port
device_id = 'device_id_example' # str | the unique id of a device
time = 3.4 # float | time in seconds to press for 0.1 = 100ms
state = 56 # int | state to switch to

    try:
        # PUT port into state for period of time
        api_instance.put_ports_pulse(port_index, device_id, time, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_ports_pulse: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_index** | **int**| Index of port | 
 **device_id** | **str**| the unique id of a device | 
 **time** | **float**| time in seconds to press for 0.1 &#x3D; 100ms | 
 **state** | **int**| state to switch to | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_relay_state**
> put_relay_state(device_id, index, state)



Put state of relay at index

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
index = 56 # int | index of relay to set state
state = True # bool | state to put

    try:
        # 
        api_instance.put_relay_state(device_id, index, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_relay_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **index** | **int**| index of relay to set state | 
 **state** | **bool**| state to put | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_socket_refresh**
> put_socket_refresh(device_id, refresh_rate)



Tell the device how often to send data to the socket server.

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
refresh_rate = 3.4 # float | how long between messages

    try:
        # 
        api_instance.put_socket_refresh(device_id, refresh_rate)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_socket_refresh: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **refresh_rate** | **float**| how long between messages | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_state_by_port_id**
> put_state_by_port_id(port_id, state)

PUT state of port

Set State of Port by id 

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | id of port to set
state = 56 # int | state id to switch to, 1 or more

    try:
        # PUT state of port
        api_instance.put_state_by_port_id(port_id, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_state_by_port_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**| id of port to set | 
 **state** | **int**| state id to switch to, 1 or more | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

