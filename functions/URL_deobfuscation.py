import re
import ipaddress
import urllib.parse

# Normal IP address format in regular expression
IP_REGEX = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# Function to convert a number in any format (hex, oct, or decimal) to integer
def convert_to_decimal(num_str):
    if num_str.startswith('0x') or num_str.startswith('0X'):
        # Hexadecimal
        return int(num_str, 16)
    elif num_str.startswith('0'):
        # Octal
        return int(num_str, 8)
    else:
        # Decimal
        return int(num_str)

# Function to normalize IP address format
def normalize_ip(ip_str):
    # Remove 'http://' and trailing '/'
    ip_str = ip_str.replace('http://', '').rstrip('/')

    # Single decimal or hexadecimal (e.g., 0XD85CA1AB or 3629949355)
    if re.fullmatch(r'0[xX][0-9A-Fa-f]+|\d+', ip_str):
        ip_int = convert_to_decimal(ip_str)
        return '.'.join(map(str, ip_int.to_bytes(4, 'big')))  # Convert to dotted-decimal format
    
    # Split into parts based on the dots
    ip_parts = ip_str.split('.')

    # Convert each part to decimal
    try:
        decimal_parts = [convert_to_decimal(part) for part in ip_parts]
        # Join as standard dotted-decimal format
        deobfuscate_ip = '.'.join(map(str, decimal_parts))
        if re.fullmatch(IP_REGEX, deobfuscate_ip):
            return deobfuscate_ip
        else:
            # return how many dots are in the IP
            if deobfuscate_ip.count('.') == 2:
                # Get the last part seperated by dot in the IP, and turn it inti binary
                binary = bin(int(deobfuscate_ip.split('.')[2]))[2:]
                # Check if the binary is 8*3 bits long, if not, add 0s to the front
                if len(binary) < 16:
                    binary = '0'*(16-len(binary)) + binary
                # Split the binary into 2 parts of 8 bits each
                # Convert the 2 parts to decimal
                ip_part1 = int(binary[:8], 2)
                ip_part2 = int(binary[8:], 2)
                # Combine the results to form an IP address
                ip_address = f"{deobfuscate_ip.split('.')[0]}.{deobfuscate_ip.split('.')[1]}.{ip_part1}.{ip_part2}"
                return ip_address
            elif deobfuscate_ip.count('.') == 1:
                # Get the last part seperated by dot in the IP, and turn it inti binary
                binary = bin(int(deobfuscate_ip.split('.')[1]))[2:]
                # Check if the binary is 8 bits long, if not, add 0s to the front
                if len(binary) < 24:
                    binary = '0'*(24-len(binary)) + binary
                # Split the binary into 3 parts of 8 bits each
                # Convert the 3 parts to decimal
                ip_part1 = int(binary[:8], 2)  
                ip_part2 = int(binary[8:16], 2)
                ip_part3 = int(binary[16:], 2)
                # Combine the results to form an IP address
                ip_address = f"{deobfuscate_ip.split('.')[0]}.{ip_part1}.{ip_part2}.{ip_part3}"
                return ip_address
            else:
                return f"Invalid IP: {deobfuscate_ip}"
    except ValueError:
        return "Invalid IP"

def deobfuscate_ip(ip_str):
    """Deobfuscates an IP address string."""
    try:
        return normalize_ip(ip_str)
    except Exception as e:
        return f"Deobfuscation error: {e}"

def deobfuscate_url(url):
    """Deobfuscates a URL by decoding and removing HTTP basic auth."""
    url = urllib.parse.unquote(url)  # Decode percent-encoded characters
    return urllib.parse.urlsplit(url).netloc.split('@')[-1]  # Remove basic auth