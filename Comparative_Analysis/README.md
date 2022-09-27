# Comparative Analysis Practice Project

This project is intended to be a practice of NLP techniques looking forward to make contributions to the Human in the Loop research project elaborated by professor Sihong Xie.

## Directory Distribution

* **Imported Data:**: Raw Data on E-Commerce Product Reviews extracted from the Human in the Loop project repository and other internet sources.
* **Main:** Includes Python scripts for clean review data processing and analysis. More information in the section below.
* **Miscellaneous:** Files used as practice for implementations in the Main. Others.

## Main Directory

* **Data_Per_Product:** Folder including partially cleaned data files on product reviews.
* **dataSet.py:** Class that contains code for product review processing. Used as base for the object dataset which represents a the information from data file containing product reviews.
* **main.py:** Main class used to create the dataset object and execute the product review analysis based on the data file selected.
* **Results.txt and toImport.txt:** Contain the results from the review processing. Review.txt is for the user reading and toImport.txt ready to be imported as a CSV file.

## Current Status

To run our current processing and analysis of the product reviews data please go to the Main folder and type the following command:

```bash
python main.py
```