# to build the docker image, execute the following from the project root
#  $ docker build --no-cache -t vsisl/dash_chatgpt_challenge:tag -f dash_app/Dockerfile .

# to run a container based on that image, execute the following:
#  $ docker run -p 5000:80 vsisl/dash_chatgpt_challenge:tag

# --- Use miniconda linux installation as a starting point
#  see https://hub.docker.com/r/continuumio/miniconda3
FROM continuumio/miniconda3:latest

MAINTAINER Vaclav Sisl <www.sisl.online>

# --- Create a non-root group and user
RUN groupadd --gid 999 docker
RUN useradd --system --uid 999 --gid docker docker
# change user
USER docker

# --- Create a new directory and set as working directory
WORKDIR /home/docker/dash-chatgpt-challenge

# --- Copy all content of the repo to the working directory
COPY . .

# --- Create conda environment
RUN conda env create -f environment.yml

# --- Activate conda environment
RUN echo "source activate dash_chatgpt" > ~/.bashrc
ENV PATH /home/docker/.conda/envs/dash_chatgpt/bin:$PATH

# --- Run production server (Gunicorn)
#  --log-level options: debug, info (default), warning, error, critical
#  --timeout [seconds]
CMD ["gunicorn", "dash_app.wsgi:application", "--bind=0.0.0.0:80", "--workers=3", "--timeout=300",  "--log-level=info"]
