# dash-chatgpt-challenge
A web app based on the plotly-dash framework developed to participate the [Dash-ChatGPT App Challenge](https://community.plotly.com/t/dash-chatgpt-app-challenge/75763)

## How to run the app

### With Docker 

#### Development environment
```bash
$ docker compose -f docker-compose.dev.yml up
```


#### Production environment
```bash
$ docker compose -f docker-compose.yml up
```

### Without Docker

1) Create conda virtual environment:

    ```bash
    $ conda env create -f environment.yml
    ```
   
2) Activate conda environment:

    ```bash
    $ conda activate dash_chatgpt
    ```
   
3) Run the app (for development purposes only):

    ```bash
    $ python dash_app/app.py
    ```