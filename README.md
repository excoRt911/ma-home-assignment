# MA-Home-Assignment #

General Guidelines:

**scraper.py**

This script does the following:<br>
 -Connect to elastic deployment via given arguments<br>
 -Scrapes .eml files from ```--directory``` location and create map list that contains each .eml file IOC's<br>
 -Send each json record data to ```email_scraper``` indice name in elastic deployment<br>

 **alerts.py**

 This script does the following:<br>
 -Connect to elastic deployment via given arguments<br>
 -Retreive domain list from previous script indice name: ```email_scraper```<br>
 -Search given indice name from traffic shipper against the domains extracted from the scraper<br>
 -Alerts if domain found in each search itterations<br>

## How To:

Clone this repository to your local machine: <br>
    ```git clone <repository_url>```

Use the command below to install the packages according to the configuration file <br>
    ```pip install -r requirements.txt```

Run the 1st script by using the command: (Please pay attention to the argument list in the end of this file)<br>
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


**scraper.py script exceution example**

```bash
python3 scraper.py --directory /users/projects/script/ma-home-assignment/pre-scanned-emails
```
### scraper.py parameters ###
| flag | Type | Description | default-value | example 
| :--- | :--- | :--- | :--- | :--- |
| -d / --directory | string | the folder location of the downloaded .eml files | none | /users/alive/email_files/ |
| -els-id | string | elastic cloud-id | OS.env ['ELS_CLOUD_ID'] | 'elk-tenant:ZXUtY2VudHJhbC0xLmF3cy5jbG91Z' |
| -els-user | string | elastic user for basic auth | OS.env ['ELS_USER'] | 'elastic' |
| -els-password | string | elastic user password for basic auth | OS.env ['ES_PASSWORD'] | Ab123@321 |

**__alerter.py script exceution example__**

```bash
python3 alerter.py -els-sniffer-index .ds-packetbeat-8.8.1-2023.06.10-000001
```
### alerter.py parameters ###
| flag | Type | Description | default-value | example 
| :--- | :--- | :--- | :--- | :--- |
| -els-id | string | elastic cloud-id | OS.env ['ELS_CLOUD_ID'] | 'elk-tenant:ZXUtY2VudHJhbC0xLmF3cy5jbG91Z' |
| -els-user | string | elastic user for basic auth | OS.env ['ELS_USER'] | 'elastic' |
| -els-password | string | elastic user password for basic auth | OS.env ['ES_PASSWORD'] | Ab123@321 |
| -els-sniffer-index | string | the sniffer index that contains users network activity | none | .ds-packetbeat-8.8.1-2023.06.10-000001


