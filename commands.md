# Useful Commands

## Table of Contents

* [System Resources](#system-resources)
* [Python](#python)
* [Conda](#conda)
* [Git](#git)
* [Docker](#docker)

## System Resources

### Show running processes

```bash
top
```

### Show info about CPU

```bash
lscpu
```

### Show info about memory

```bash
free -h
```

### Monitor CPU & memory

```bash
htop
```

### Monitor NVIDIA GPU

```bash
watch -n 1 nvidia-smi
```

### Show disk usage

```bash
df -h
```

### Show directory size

```bash
du -h <path/to/dir>
```

Example:

```bash
du -h datasets/
```

## Python

### Create `requirements.py`

```bash
pip freeze > requirements.py
```

### Clear cache (`pip`)

```bash
pip cache purge
```

## Conda

### Create virtual environment

```bash
conda create -n <env_name> [<packages>] [-y]
```

_Note_: `<packages>` is a list of packages to install in the environment. Use `-y` to automatically answer "yes" to any confirmations.

Example:

```bash
conda create -n ml python=3.9 numpy -y
```

### Enter virtual environment

```bash
conda activate <env_name>
```

Example:

```bash
conda activate ml
```

### Exit virtual environment

```bash
conda deactivate <env_name>
```

Example:

```bash
conda deactivate ml
```

### Clear cache (`conda`)

```bash
conda clean -a
```

## Git

### Clone repo

```bash
git clone {<repo_url>, <username>/<repo_name>}
```

### Show uncommitted changes

```bash
git status
```

### Show differences

```bash
git diff
```

### Add changes to staging area

```bash
git add <file>...
```

Example:

```bash
git add .
```

### Restore files in working directory

```bash
git restore <file>...
```

### Commit changes to local repo

```bash
git commit -m "<message>"
```

### Push local changes to remote repo

```bash
git push
```

### Pull remote changes to local repo

```bash
git pull
```

## Docker

### Show all images

```bash
docker images
```

### Show all containers

```bash
docker ps -a [--size]
```

_Note_: `--size`: Show size of each container.

### Pull image

```bash
docker pull <image_name>:<tag>
```

Example:

```bash
docker pull nvidia/cuda:11.8.0-devel-ubuntu22.04
```

### Create container

```bash
docker run [--gpus all] [-p <host_port>:<container_port>] [-v <host_dir>:<container_dir>] -it --name <container_name> <image_name>:<tag>
```

_Note_: `--gpus all`: Access all available GPUs. `-p <host_port>:<container_port>`: Map a port on the container to that on the host. `-v <host_dir>:<container_dir>`: Mount a directory on the host inside the container.

Example:

```bash
docker run -it --name deeplearning nvidia/cuda:11.8.0-devel-ubuntu22.04
```

### Attach to running container

```bash
docker attach <container_name_or_id>
```

Example:

```bash
docker attach deeplearning
```

### Exit container

```bash
docker {stop, kill} <container_name_or_id>
```

_Note_: `stop`: Exit gracefully; `kill`: Exit immediately.

Example:

```bash
docker stop deeplearning
```

### Restart exited container

```bash
docker start <container_name_or_id>
```

Example:

```bash
docker start deeplearning
```

### Copy files to container

```bash
docker cp <local_source> <container_name_or_id>:<container_destination>
```

Example:

```bash
docker cp ./training_scripts/ deeplearning:/
```

### Copy files from container

```bash
docker cp <container_name_or_id>:<container_source> <local_destination>
```

Example:

```bash
docker cp deeplearning:/models/model_final.pth ./models/
```

### Start new process inside container

```bash
docker exec -it <container_name_or_id> <command>
```

Example:

```bash
docker exec -it deeplearning /bin/bash
```

### Remove container

```bash
docker rm <container_name_or_id>
```

Example:

```bash
docker rm deeplearning
```

### Build image from `Dockerfile`

```bash
docker build -t <tag> <path/to/Dockerfile>
```

Example:

```bash
docker build -t my-image .
```

### Save container as image

```bash
docker commit <container_name_or_id> <image_name>
```

### Export image as `.tar`

```bash
docker save -o <output_file.tar> <image_name>
```

### Load image from `.tar`

```bash
docker load -i <input_file.tar>
```
