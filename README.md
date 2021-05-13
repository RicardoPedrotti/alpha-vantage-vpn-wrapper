# Fenix Alpha Vantage Wrapper

The intention of this wrapper is to bypass some Alpha vantage API limitations and make it easier to manipulate 
data from the endpoints.

## Setup:
### - Pipenv
- To setup the dependencies for the project we use [Pipenv](https://pipenv.pypa.io/en/latest/).
- **Install it** then **open a terminal window on this project folder** and finally open the virtual pipenv environment simply by
writing ```pipenv shell```
  

### - config.yml
- To finish setting up your environment, you will need to have a file named ```config.yml``` with
  the characteristics below:  
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