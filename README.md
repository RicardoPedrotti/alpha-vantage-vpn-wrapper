# Fenix Alpha Vantage Wrapper

The intention of this wrapper is to bypass some Alpha Vantage API limitations and make it easier to manipulate 
data from the endpoints.
  
### - The config.yml file
- You will need to have a file named ```config.yml``` with the 
  characteristics below:
```
alpha_vantage_api_key_list:
  [
          yourkey1,
          yourkey2,
          yourkey3,
  ]
vpn_proxies:
    "http": "your_http_proxy_url"
    "https": "your_https_proxy_url"

```
