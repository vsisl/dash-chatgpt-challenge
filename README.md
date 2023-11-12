# PropagandaBot
A web app based on the plotly-dash framework developed to participate the [Dash-ChatGPT App Challenge](https://community.plotly.com/t/dash-chatgpt-app-challenge/75763).

The app uses ChatGPT API to discover propaganda techniques in a provided text. It can also generate propaganda articles for given topics.

The app is available online at [propagandabot.online](http://www.propagandabot.online/).

## Demo

![img.gif](demo.gif)

   
## Authors
- [Jan Bureš](https://www.linkedin.com/in/jan-bure%C5%A1-6b2283216/)
- [Christian Horvat](https://linkedin.com/in/christian-horvat-466048214)
- [Václav Šísl](https://linkedin.com/in/vaclav-sisl)

## How to run the app

### Step 1: Clone the repository

```bash
$ git clone https://github.com/vsisl/dash-chatgpt-challenge
$ cd dash-chatgpt-challenge
```

### Step 2: Add openAI API key
Go to [platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys), and crate an API key (`your_secrete_key`).

Create a file `.env` in the project root folder and add the secret key to it.

```bash
$ echo OPENAI_API_KEY=your_secrete_key > .env
```

### Step 3: Run the app

#### Option 1: Using Docker (recommended) 

##### Development environment

```bash
$ docker compose -f docker-compose.dev.yml up
```


##### Production environment

```bash
$ docker compose -f docker-compose.yml up
```

#### Option 2: Without Docker

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
