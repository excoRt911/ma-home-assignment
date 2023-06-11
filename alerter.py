from typing import Optional, List,Dict,Any
from elasticsearch import Elasticsearch
import os
import argparse



def check_hit_on_network_traffic(els_connection: Elasticsearch,domains: List[str]) -> Dict[str,Any]:
    hits = {}
    for domain in domains:
        query = {
                "wildcard": {
                    "server.domain": {
                        "value": f"*{domain}*"
                    }
                }
        }
        response = els_connection.count(index="packetbeat-8.8.1", query=query)
        hit_count = response.body.get("count", 0)
        if hit_count > 0:
            hits[domain] = hit_count
    
    return hits
            
        

def retrieve_main_domains(els_connection: Elasticsearch) -> List[str]:
    main_domain_list     = []
    index_name = "email_scraper"
    query = {
            "wildcard": {
                "Domains": {
                    "value": "*"
                }
            }
    }
    response = els_connection.search(index=index_name, query=query)
    

    hits = response.get("hits",{}).get("hits",[])

    # Process the retrieved hits from the elk query
    for hit in hits:
        source = hit.get("_source",{}).get('Domains',[])
        for domain in source:
            if domain in main_domain_list:
                continue
            else:
                main_domain_list.append(domain)
        
    return main_domain_list


def parse_args():
    p = argparse.ArgumentParser()
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

    # extract all domains from parsed .emls
    domains_list = retrieve_main_domains(es)

    # detects hits from retrieved domains list
    detect_hits = check_hit_on_network_traffic(es,domains_list)

    # Alerts from each HIT
    for domain,count in detect_hits.items():
        print((f"[ALERT] user domain browsing detected! [{domain}] - Number of hits: {count}"))
        

if __name__ == "__main__":
    main()
