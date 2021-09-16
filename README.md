# docker-compose-image-updater
This python script updates the images of one or many docker-compose stacks automatically.

If multiple docker-compose directories are supplied, the script updates them in parallel.

## Usage
```
Usage: update-compose.py [OPTIONS] [UPDATE_DIRS]...

  Update docker-compose images automaticly.

  Takes one or more directorys as input and searches for a compose file in
  one of the following forms: "compose.yaml", "compose.yml", "docker-
  compose.yaml", "docker-compose.yml"

  After the images are updated you will be asked if you want to prune your
  images.

Options:
  --help  Show this message and exit.
```

## Installation
```
git clone https://github.com/FrederikRogalski/docker-compose-image-updater.git
cd docker-compose-image-updater
chmod +x update_compose.py
```

Then add the file 'update_compose.py' to the your path
