# Compressio

Compressio is a python application that allows to edit images in bulk. Originally, it\'s purpose was to compress a
directory of pictures, but now it has the following functionality:

1. Compressio can compress (wow) multiple images depending on a chosen quality.
2. Compressio can resize all the images to a given width and height.
3. Compressio can change a format of all the pictures to a given one.

## Installation


```shell
# Cloning the repo
git clone https://github.com/knikolaeff/compressio.git && cd compressio

# Installing dependencies 
pip install -r requirements.txt

# Running the script
python compressio.py
```

If you are on Windows or don't want to use command line - there are two pre-built executables in the "[Releases](https://github.com/knikolaeff/compressio/releases)" tab.

Although it worth mentioning that I used PyInstaller to built these, what leads to pretty big size of the executables. 

Any contribution, especially reducing the executables size is welcome!
