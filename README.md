# CKAN-API-Dataset_import_export
The script accesses datasets from a [CKAN](https://ckan.org/) catalog using the [CKAN API](https://docs.ckan.org/en/2.9/api/). 
Python scripts for importing and exporting ckan datasets.

## Functionality

### CKAN API Export Scrypt Functionality
By running the python scrypt `ckan_API_export.py` the CKAN datasets will be exported localy in `json` format in a folder called `export`. 

#### Description of the CKAN API Scrypt Export Functionality

By running scrypt, the user is asked to enter the URL page of the catalog from which he wants to export the data.

When the code is executed, the user will be asked whether all datasets should be exported.
There are two options: 
- to export all datasets
- to specify the number of datasets which should be exported.

The selected number of datasets will can be exported as a single json file or separately for each dataset. The results will be exported to a separate folder (name of the folder `export`).

### How to export all datasets
The following image shows a prompt example for exporting all data records to a single file:
![image](https://github.com/MarijaKnezevic/CKAN-API-Dataset_import_export/assets/93824048/d65548db-96ee-4ba3-8def-f0154f0a4c3c)

The following figure shows an example of a json file and the location where the export file is saved:
![image](https://github.com/MarijaKnezevic/CKAN-API-Dataset_import_export/assets/93824048/2a2fdd1d-53f9-4ee2-b6ec-20a3d60b17b1)

The exported json file has the name of the catalog, indicates that all data is exported in the json file and the date and time of export (the following image is as example):

![image](https://github.com/MarijaKnezevic/CKAN-API-Dataset_import_export/assets/93824048/d6f21680-1506-4b30-b60f-38af21847ff0)
In the prompt, it is possible to select the export of the data set as separate json files.


### How to export specific number of datasets
If not all data sets needs to be exported, the user needs to give the number of datasets that needs to be exported


Here is an example of the tool's dialog:

![image](https://github.com/MarijaKnezevic/CKAN-API-Dataset_import_export/assets/93824048/ee875a40-0335-46cf-b72c-357aff85c694)


In the following image is possible to see the folder `export` with few exported datasets:

![image](https://github.com/MarijaKnezevic/CKAN-API-Dataset_import_export/assets/93824048/e330adff-9943-4b1b-9540-b02219aa4d11)

The name of the dataset will be the titel defined in the catalog and the date and time of export.
In the prompt is possible to export defined number of the dataset as one json file.



### CKAN API Import Scrypt Functionality
#### Description of the CKAN API Scrypt Import Functionality
