# Fenix Alpha Vantage Wrapper

The intention of this wrapper is to bypass some Alpha Vantage API limitations and make it easier to manipulate 
data from the endpoints.

## Setup:
### - Pipenv
- To setup the dependencies for the project we use [Pipenv](https://pipenv.pypa.io/en/latest/).
- **Install it** then **open a terminal window on this project folder** ```cd your/path/to/here/fenix-alpha-vantage``` 
  and finally open the virtual pipenv environment simply by writing ```pipenv shell``` in your terminal window and
  pressing **enter**
  
- You are inside the pipenv shell if your terminal command line is similar to ```(fenix-alpha-vantage) YourPcUsername@MachineName```
  
### - The config.yml file
- You will need to have a file named ```config.yml``` inside the folder ```fenix_alpha_vantage_interface``` with the 
  characteristics below:
  
ps.: Lucas, se você está lendo isso, é só me pedir que te passo esse arquivo. :)
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
  
### - Installing fenix_alpha_vantage_interface as a library
- With the file in place and our terminal in the pipenv shell of our project, simply type 
  ```pipenv run pip install -e .``` to install our alpha vantage interface as a library 
  
### - Jupyter Notebook 

Jupiter offers us an easy-to-use interface for coding and specially testing. Let's set up our environment.

- Right now we want to create a new execution context on Jupyter. We call it a Kernel. 
  
- While on our pipenv shell from the previous steps, run 
  ```python -m ipykernel install --user --name=alpha-fenix-kernel``` to create a new kernel (when creating a new
  notebook on jupiter interface, you will be displayed with the option we just created).
  
- For the sake of easier coding on Jupiter, it would be good to install some auto complete extensions. Commands are:
```jupyter contrib nbextension install --user```
  ``` jupyter nbextensions_configurator enable --user```
  
- And then finally ```jupyter notebook``` to launch our environment.

- The environment will keep the terminal window open. To finish Jupiter type ```Ctrl-C or Cmd-C``` on this window.
