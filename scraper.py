from typing import Optional, List
import os
from email.header import decode_header
import re
import mailparser
from elasticsearch import Elasticsearch
from urllib.parse import urlparse
import argparse


URL_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
IP_REGEX = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
ELS_SCRAPER_INDEX = "email_scraper"

def extract_sender_ip(mail) -> Optional[str]:
    headers = mail.headers

    ips = []
    for key, value in headers.items():
        if key.lower().startswith('received'):
            ips.extend(re.findall(IP_REGEX, value))
    if ips:
        return ips[-1]  # The last IP is typically the sender's IP
    return None


def extract_urls(mail_body: str) -> Optional[List[str]]:
    url_pattern = re.compile(URL_REGEX)
    found_urls = re.findall(url_pattern, mail_body)
    return found_urls


def extract_domain(url: str) -> str:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


def extract_email_files(directory: str) -> List[str]:
    file_names = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.eml'):
                file_path = os.path.join(root, file)
                file_names.append(file_path)

    return file_names

 
def extract_ioc_from_mails(emails_file_list: List[str]) -> List[dict]:
    els_json_records = []
    for file in emails_file_list:
        iocs = {}
        mail = mailparser.parse_from_file(file)
        sender_ip = extract_sender_ip(mail)
        iocs['SenderIP'] = sender_ip
        iocs['Subject'] = mail.subject
        iocs['Date'] = mail.date
        iocs['From'] = mail.from_[0][1]

        try:
            iocs['To'] = mail.to[0][1]
        except:
            iocs['To'] = "Unknown"
        

        links = extract_urls(mail.body)
        domains = set()
        for url in links or []:
            domain = extract_domain(url)
            domains.add(domain)
        iocs['Links'] = links
        iocs['Domains'] = list(domains)

        els_json_records.append(iocs)
    return els_json_records



def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-d", "--directory", default=None, required=True, help="Path for directory that contains emails")
    p.add_argument("-els-id", default=os.environ.get('ELS_CLOUD_ID'), help="Elasticsearch cloud id")
    p.add_argument("-els-user", default=os.environ.get('ELS_USER'), help="Elasticsearch username")
    p.add_argument("-els-password", default=os.environ.get('ELS_PASSWORD'), help="Elasticsearch password")
    return p.parse_args()



def main():
    args = parse_args()

    # Create Elasticsearch connection
    es = Elasticsearch(
        cloud_id=args.els_id,
        basic_auth=(args.els_user, args.els_password)
    )

    # extract all email files
    email_files_list = extract_email_files(args.directory)

    # extract required IOC's
    extracted_iocs = extract_ioc_from_mails(email_files_list)
    
    # Send each record to Elasticsearch
    for record in extracted_iocs:
        response = es.index(index=ELS_SCRAPER_INDEX, document=record)


if __name__ == "__main__":
    main()
