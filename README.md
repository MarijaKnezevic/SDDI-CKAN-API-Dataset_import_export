# CKAN-API-Dataset_import_export
The script accesses datasets from a [CKAN](https://ckan.org/) catalog using the [CKAN API](https://docs.ckan.org/en/2.9/api/). 
Python scripts for importing and exporting ckan datasets.

## Functionality

### CKAN API Export Scrypt Functionality
By running the python scrypts the CKAN datasets will be exported localy in `json` format. 

#### Description of the CKAN API Scrypt Export Functionality

In the file `ckan_API_export.py`, is required to address the CKAN Instance where dataset are hosted. This parameter is in [ckan_API_export.py](https://github.com/MarijaKnezevic/CKAN-API-export/blob/main/ckan_API_export.py) scrypt defined as `url` 

Example:
`url = 'http://localhost:5000/api/3/action/package_search'`

The results will be exported to a separate folder (name of the folder `export`) and the names of the individual data sets will be set as `Title` in the catalog.

When the code is executed, the user will be asked whether all datasets should be exported.
There are two options: 
- to export all datasets
- to specify the number of datasets which should be exported.

If all datasets needs to be exported, the tool will export all datasets in folder `export`
If not all data sets needs to be exported, the user needs to give the number of datasets that needs to be exported


Here is an example of the tool's dialog:

![image](https://github.com/MarijaKnezevic/CKAN-API-export/assets/93824048/b2d6d229-bab9-4f17-afbd-7acb2d8ab0fd)

In the following image is possible to see the folder `export` with few exported datasets:

![image](https://github.com/MarijaKnezevic/CKAN-API-export/assets/93824048/2ab39f31-2840-4f34-b499-95f67596c82a)


### CKAN API Import Scrypt Functionality
#### Description of the CKAN API Scrypt Import Functionality
