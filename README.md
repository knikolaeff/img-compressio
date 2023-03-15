# Compressio

My final project in college

Compressio is a python application that allows to edit images in bulk. Originally, it\'s purpose was to compress a
directory of pictures, but now it has the following functionality:

1. Compressio can compress (wow) multiple images depending on a chosen quality.
2. Compressio can resize all the images to a given width and height.
3. Compressio can change a format of all the pictures to a given one.

## Installation

#### Using Poetry (Linux, macOS, Windows **(WSL)**)

```shell
# Installing Poetry 
curl -sSL https://install.python-poetry.org | python3 -

# Cloning the repo
git clone https://github.com/knikolaeff/img-compressio.git

cd img-compressio

# Installing dependencies
poetry install

# Running the script
python3 compressio.py
```

#### Using Poetry (Windows **(Powershell)**)

```shell
# Installing Poetry 
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Cloning the repo
git clone https://github.com/knikolaeff/img-compressio.git

cd img-compressio

# Installing dependencies
poetry install

# Running the script
python compressio.py
```
