# MA-Home-Assignment #

General Guidelines:

scraper.py

This script does the following:
 -Connect to elastic instance via given arguments
 -Scrapes .eml fiels from ```--directory``` location and create map list for each .eml file
 -Send each json record data to ```email_scraper``` indice name

 alerts.py

 This script does the following:
 -Connect to elastic instance via given arguments
 -Retreive domain list from previous script indice name: ```email_scraper```
 -Search given indice name from traffic shipper the extracted domains
 -Alerts if domain found in each domain search

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
example outout:

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


scraper.py script exceution example 

```bash
python3 scraper.py --directory /users/projects/script/ma-home-assignment/pre-scanned-emails
```
### scraper.py parameters ###
| flag | Type | Description | default-value | example (Legacy Site) 
| :--- | :--- | :--- | :--- | :--- |
| -d / --directory | string | the folder location of the downloaded .eml files | none | /users/alive/email_files/ |
| -els-id | string | elastic cloud-id | OS.env ['ELS_CLOUD_ID'] | 'elk-tenant:ZXUtY2VudHJhbC0xLmF3cy5jbG91Z' |
| -els-user | string | elastic user for basic auth | OS.env ['ELS_USER'] | 'elastic' |
| -els-user | string | elastic user password for basic auth | OS.env ['ES_PASSWORD'] | Ab123@321 |

