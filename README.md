# MA-Home-Assignment #


## How To:

Clone this repository to your local machine: <br>
    ```git clone <repository_url>```

Use the command below to install the packages according to the configuration file <br>
    ```pip install -r requirements.txt```

Run the 1st script by using the command:**<br>
```python3 scraper.py -d <directory>```


Activate packet shipper and configure it to ship data to ELK.<br>
(For example using packetbeat)<br>
```sudo ./packetbeat -e -c packetbeat.yml```<br>

Run the 2nd script by using the command:**<br>
```python3 alerter.py -d <directory>```<br>

The script output will alert you if domain browsing correlation was found.<br>

```bash
[ALERT] user domain browsing detected! [storage.googleapis.com] - Number of hits: 3
[ALERT] user domain browsing detected! [fonts.googleapis.com] - Number of hits: 22
[ALERT] user domain browsing detected! [ynet.co.il] - Number of hits: 51
[ALERT] user domain browsing detected! [discord.com] - Number of hits: 17
[ALERT] user domain browsing detected! [facebook.com] - Number of hits: 18
[ALERT] user domain browsing detected! [www.youtube.com] - Number of hits: 2
[ALERT] user domain browsing detected! [twitter.com] - Number of hits: 11
[ALERT] user domain browsing detected! [cnn.com] - Number of hits: 28
```
example outout:


# scraper.py parameters
| flag | Type | Description | default-value | example (Legacy Site) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| -d / --directory | string | downloaded .eml files | none | /users/alive/email_files/ |
| -els-id | string | elastic cloud-id | OS.env ['ELS_CLOUD_ID'] | 'elk-tenant:ZXUtY2VudHJhbC0xLmF3cy5jbG91Z' |
| -els-user | string | elastic user for basic auth | OS.env ['ELS_USER'] | 'elastic' |
| -els-user | string | elastic user password for basic auth | OS.env ['ES_PASSWORD'] | Ab123@321 |