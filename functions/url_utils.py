import urllib.parse
import ipaddress
import random
import string

def is_ip_address(url):
    try:
        netloc = urllib.parse.urlsplit(url).netloc
        print(ipaddress.ip_address(netloc))
        ipaddress.ip_address(netloc)
        return True
    except ValueError:
        return False
    
def insert_domain_after_protocol(url, domain):
    scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)
    new_netloc = f"{domain}@{netloc}"
    return urllib.parse.urlunsplit((scheme, new_netloc, path, query, fragment))

def encode_random_chars(url, num_chars=5):
    try:
        url = url.replace("[", "%5B").replace("]", "%5D")  # Prevent errors with square brackets
        scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)
        netloc = netloc.replace("[", "%5B").replace("]", "%5D")  # Prevent errors with square brackets
        full_path = urllib.parse.urlunsplit(('', netloc, path, query, fragment))
        path_chars = list(full_path)
        
        positions = random.sample(range(len(path_chars)), min(num_chars, len(path_chars)))
        for pos in positions:
            char = path_chars[pos]
            if char in string.ascii_letters + string.digits:
                path_chars[pos] = '%{:02X}'.format(ord(char))
        
        new_full_path = ''.join(path_chars)
        _, new_netloc, new_path, new_query, new_fragment = urllib.parse.urlsplit(new_full_path)
        return urllib.parse.urlunsplit((scheme, new_netloc, new_path, new_query, new_fragment))
    except ValueError:
        print("Invalid URL provided: ", url)
        # Stop the program if an invalid URL is provided
        exit()