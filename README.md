# **compose-update** a docker-compose-image-updater
![Test](https://github.com/frederikrogalski/compose-update/actions/workflows/test-workflow.yml/badge.svg)

This python script updates the images of one or many docker-compose stacks automatically.

If multiple docker-compose directories are supplied, the script updates them in parallel.

## Demo
*This DEMO is outdated. Use compose-update * to update all subdirectories*
![output](https://user-images.githubusercontent.com/31591562/133811801-16eb581f-f63c-454f-a5de-e872568f3477.gif)


## Usage
command: `compose-update *` for update all sub directory
```
Usage: compose-update [OPTIONS] [UPDATE_DIRS]...

  Update docker-compose images automatically.

  Takes one or more directories as input and searches for a
  compose file in one of the following forms:
  "compose.yaml", "compose.yml",
  "docker-compose.yaml", "docker-compose.yml"

Options:
  --prune, -p           Prune docker images after update
                        process if set
  --help                Show this message and exit.
```

By default the script gets run by the python interpreter located in `usr/bin/python3`.

If you want to run the script with a different python interpreter you can just call it as you would normaly with the interpreter.
```
python3 compose-update
```

## Installation
```
git clone https://github.com/FrederikRogalski/compose-update.git
cd compose-update
pip3 install -r requirements.txt
chmod +x compose-update
```

Then add the file 'update-compose' to your path.

## Known issues
At the moment the script has a problem with reading from stdin. Please supply your arguments after the command until this is fixed.
