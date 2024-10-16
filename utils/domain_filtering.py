import sys

import requests
from core.constants import (
    ANTIFILTER_DOMAINS_URL,
    KEYWORDS,
    MIN_DOMAIN_LEVEL,
    SECOND_LEVEL_DOMAIN_SEGMENTS,
)
from requests.exceptions import ConnectionError, Timeout


def get_antifilter_domains(timeout: int = 10) -> list:
    domains = []
    try:
        with requests.get(
            ANTIFILTER_DOMAINS_URL, timeout=timeout, stream=True
        ) as response:
            for line in response.iter_lines():
                domains.append(line.decode('utf-8').strip())
    except Timeout:
        print("Error! Didn't receive any response from antifilter!")
        sys.exit(1)
    except ConnectionError:
        print(
            "Error! Couldn't connect to antifilter! "
            'Check your internet connection.'
        )
        sys.exit(1)
    return domains


def extract_second_level_domains(domains: list) -> set:
    return {
        '.'.join(domain.split('.')[-SECOND_LEVEL_DOMAIN_SEGMENTS:])
        for domain in domains
        if len(domain.split('.')) > MIN_DOMAIN_LEVEL
    }


def filter_by_keywords(domains: set) -> set:
    for keyword in KEYWORDS:
        domains = {domain for domain in domains if keyword not in domain}
    return domains