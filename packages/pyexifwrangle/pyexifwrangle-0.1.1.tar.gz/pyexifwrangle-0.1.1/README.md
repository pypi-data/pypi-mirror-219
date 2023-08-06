# Wrangle EXIF Data in Python

## Extract EXIF Data with Phil Harvey's EXIFTool
Install Phil Harvey's EXIFTool from https://exiftool.org/. This site has installation instructions if you need them.

After installing EXIFTool, you can use the terminal to extract EXIF data from every image in a folder and save the 
results in a csv file. Open the terminal and change directories to the folder containing EXIFTool. On my computer, 
this step looks like

```
> cd ~/Documents/Image-ExifTool-12.49
```
Extract the EXIF data and save it in a csv file.
```
> exiftool -csv -r path/to/images > path/to/output.csv
```