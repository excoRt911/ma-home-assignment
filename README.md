# MA-Home-Assignment #


## How To:

Use the command below to install the packages according to the configuration file <br>
    ```pip install -r requirements.txt```

Run the 1st script by using the command:
```python3 scraper.py -d <directory>```



# scraper.py parameters
| flag | Type | Description | default-value | example (Legacy Site)
| :--- | :--- | :--- | :--- | :--- | :--- |
| -d / --directory | string | downloaded .eml files | none | /users/alive/email_files/ |
| -els-id | string | elastic cloud-id | OS.env ['ELS_CLOUD_ID'] | 'elk-tenant:ZXUtY2VudHJhbC0xLmF3cy5jbG91Z' |
| -els-user | string | elastic user for basic auth | OS.env ['ELS_USER'] | 'elastic' |
| -els-user | string | elastic user password for basic auth | OS.env ['ES_PASSWORD'] | Ab123@321 |