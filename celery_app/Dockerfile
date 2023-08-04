FROM continuumio/miniconda3:latest

MAINTAINER Vaclav Sisl <www.sisl.online>

# --- Create a non-root group and user
RUN groupadd --gid 999 docker
RUN useradd --system --uid 999 --gid docker docker
# change user
USER docker

# --- Create a new directory and set as working directory
WORKDIR /home/docker/dash-chatgpt-challenge

# --- Copy environment definition file
COPY environment.yml environment.yml

# --- Create conda environment
RUN conda env create -f environment.yml

# --- Activate conda environment
RUN echo "source activate dash_chatgpt" > ~/.bashrc
ENV PATH /home/docker/.conda/envs/dash_chatgpt/bin:$PATH

# --- Copy all content of the repo to the working directory
COPY . .

# --- Run celery worker process for async. tasks
CMD ["celery", "-A", "dash_app.app.celery_app", "worker", "--concurrency=2",  "--loglevel=INFO"]
