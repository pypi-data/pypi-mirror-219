# Wrangle EXIF Data in Python

A Python package for wrangling EXIF data extracted from images using Phil Harvey's EXIFTool.

## Set-up
### Install pyexifwrangle with pip

```bash
$ pip install pyexifwrangle
```

### Install Phil Harvey's EXIFTool
Install Phil Harvey's EXIFTool from https://exiftool.org/. This site has installation instructions if you need them.

## Usage
### Get EXIF data using EXIFTool
After installing EXIFTool, you can use the terminal to extract EXIF data from every image in a folder and save the 
results in a csv file. Open the terminal and change directories to the folder containing EXIFTool. On my computer, 
this step looks like

```bash
$ cd ~/Documents/Image-ExifTool-12.49
```
Extract the EXIF data and save it in a csv file.
```bash
$ exiftool -csv -r absolute_path/to/image_directory > path/to/output.csv
```
The image_directory can include subdirectories and the flag `-r` tells EXIFTool to include images in these 
subdirectories in the output.

### Wrangle the EXIF data in Python

Load the csv file into Python.
```python
import pyexifwrangle.wrangle as wr

df = wr.read_exif('path/to/output.csv', filename_col='SourceFile')
```
The function *wrangle.read_exif* uses the Pandas package to load the csv into a data frame. The parameter 
*filename_col* is the name of the column that contains the filenames of the images.  The absolute file paths are included with the filenames in the *filename_col*. After 
reading the EXIF data into a Pandas data frame, this function removes any images whose filename starts with '.'. 

I often organize my images into folders and sub-folders. For example one of my projects has the following folder tree:
```
├── Samsung_phones  # main directory
│   ├── s21  # model
│   │   ├── s21_1  # phone name
│   │   │ 	├── blank  # scene type
│   │   │	│	├── front  # camera
│   │   │	│	│	├──image1.jpg
│   │   │	│	│	├──image2.jpg
│   │   │	│	│	├──...
│   │   │	│	├── telephoto
│   │   │	│	│	├──image1.jpg
│   │   │	│	│	├──image2.jpg
│   │   │	│	│	├──...
│   │   │	│	├── ultra
│   │   │	│	│	├──image1.jpg
│   │   │	│	│	├──image2.jpg
│   │   │	│	│	├──...
│   │   │	│	├── wide
│   │   │	│	│	├──image1.jpg
│   │   │	│	│	├──image2.jpg
│   │   │	│	│	├──...
│   │   │ 	├── natural
│   │   │	│	├── front  
│   │   │	│	├── telephoto
│   │   │	│	├── ultra
│   │   │	│	├── wide
│   │   ├── s21_2 
│   │   │ 	├── blank
│   │   │	│	├── front
│   │   │	│	├── telephoto
│   │   │	│	├── ultra
│   │   │	│	├── wide
│   │   │ 	├── natural
│   │   │	│	├── front  
│   │   │	│	├── telephoto
│   │   │	│	├── ultra
│   │   │	│	├── wide
```
Extract the folder names from the images' absolute filepaths and make a new column for each folder.
```python
df = wr.filename2columns(df=df, filename_col='SourceFile', columns=['model', 'phone', 'scene_type', 'camera', 'image'])
```

Find images missing EXIF data. For example, search the data frame for images that don't have an Aperture.
```python
missing = wr.check_missing_exif(df=df, column='Aperture')
```

Group images by column(s) and count the number of images per group.
```python
counts = wr.count_images_by_columns(df=df, columns=['model', 'phone', 'scene_type', 'camera'])
```

Optionally, you can sort the output of *count_images_by_columns*
```python
counts_sorted = wr.count_images_by_columns(df=df, columns=['model', 'phone', 'scene_type', 'camera'], sorted=
['phone', 'camera', 'Aperture'])
```
