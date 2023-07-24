# PropagandaBot
A web app based on the plotly-dash framework developed to participate the [Dash-ChatGPT App Challenge](https://community.plotly.com/t/dash-chatgpt-app-challenge/75763)

The app uses ChatGPT API to discover propaganda techniques in a provided text. It can also generate propaganda articles for given topics.

## Demo

![img.gif](demo.gif)

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
   
3) Run redis database (using docker): 

   ```bash
    $ docker run -p 6379:6379 --rm redis
    ```
    
4) In another terminal window, run celery worker:

   ```bash
    $ celery -A dash_app.app.celery_app worker --concurrency=2 --loglevel=INFO
    ```
       
5) In another terminal window, run the dash app:

    ```bash
    $ python -m dash_app.app
    ```