from functions.url_utils import insert_domain_after_protocol, encode_random_chars

# IP obfuscation functions
def hex_n(ip_parts, n):
    return '.'.join([f"0x{int(part):X}" if i == n - 1 else part for i, part in enumerate(ip_parts)])

def hex_dec_n(ip_parts, n):
    return '.'.join([f"0x{int(part):X}" for part in ip_parts[:n]] + ip_parts[n:])

def hex_padded_n(ip_parts, n):
    return '.'.join([f"0x{int(part):08X}" for part in ip_parts[:n]] + ip_parts[n:])

def hex_dec_merge_n(ip_parts, n):
    first = [f"0x{int(part):X}" for part in ip_parts[:n - 1]]
    decimal = sum(int(ip_parts[i]) * (256 ** (3 - i)) for i in range(n - 1, 4))
    return '.'.join(first) + '.' + str(decimal)

def hex_hex_merge_n(ip_parts, n):
    first = [f"0x{int(part):X}" for part in ip_parts[:n - 1]]
    decimal = sum(int(ip_parts[i]) * (256 ** (3 - i)) for i in range(n - 1, 4))
    if first:
        return '.'.join(first) + '.' + f"0X{decimal:X}"
    else:
        return f"0X{decimal:X}"

def hex_oct_n(ip_parts, n):
    return '.'.join([f"0x{int(part):X}" for part in ip_parts[:n]] + [f"{int(part):04o}" for part in ip_parts[n:]])

def hex_oct_merge_n(ip_parts, n):
    first = [f"0x{int(part):X}" for part in ip_parts[:n - 1]]
    octal = sum(int(ip_parts[i]) * (256 ** (3 - i)) for i in range(n - 1, 4))
    return '.'.join(first) + '.' + f"{octal:04o}"

def hex_oct_dec(ip_parts, n):
    if n == 1:
        return f"0x{int(ip_parts[0]):X}.{int(ip_parts[1]):04o}.{int(ip_parts[2]) * 256 + int(ip_parts[3])}"
    elif n == 2:
        return f"0x{int(ip_parts[0]):X}.{int(ip_parts[1]):04o}.{int(ip_parts[2]):04o}.{int(ip_parts[3])}"

def hex_dec_oct(ip_parts, n):
    if n == 1:
        last = int(ip_parts[2]) * 256 + int(ip_parts[3])
        return f"0x{int(ip_parts[0]):X}.{int(ip_parts[1])}.{last:04o}"
    elif n == 2:
        return f"0x{int(ip_parts[0]):X}.{int(ip_parts[1])}.{int(ip_parts[2])}.{int(ip_parts[3]):04o}"

def hex_dec_hex(ip_parts, n):
    if n == 1:
        last = int(ip_parts[2]) * 256 + int(ip_parts[3])
        return f"0x{int(ip_parts[0]):X}.{int(ip_parts[1])}.0x{last:X}"
    elif n == 2:
        return f"0x{int(ip_parts[0]):X}.{int(ip_parts[1])}.{int(ip_parts[2])}.0x{int(ip_parts[3]):X}"

def hex_oct_hex(ip_parts, n):
    if n == 1:
        last = int(ip_parts[2]) * 256 + int(ip_parts[3])
        return f"0x{int(ip_parts[0]):X}.{int(ip_parts[1]):04o}.0x{last:X}"
    elif n == 2:
        return f"0x{int(ip_parts[0]):X}.{int(ip_parts[1]):04o}.{int(ip_parts[2]):04o}.0x{int(ip_parts[3]):X}"

def dec_dec_merge_n(ip_parts, n):
    first = [str(int(part)) for part in ip_parts[:n - 1]]
    decimal = sum(int(ip_parts[i]) * (256 ** (3 - i)) for i in range(n - 1, 4))
    if first:
        return '.'.join(first) + '.' + str(decimal)
    else:
        return str(decimal)

def dec_hex_merge_n(ip_parts, n):
    first = [str(int(part)) for part in ip_parts[:n - 1]]
    decimal = sum(int(ip_parts[i]) * (256 ** (3 - i)) for i in range(n - 1, 4))
    return '.'.join(first) + '.' + f"0x{decimal:X}"

def dec_oct_merge_n(ip_parts, n):
    return '.'.join([str(int(part)) for part in ip_parts[:n]] + [f"{int(part):04o}" for part in ip_parts[n:]])

def dec_hex_n(ip_parts, n):
    return '.'.join([str(int(part)) for part in ip_parts[:n]] + [f"0x{int(part):X}" for part in ip_parts[n:]])

def dec_oct_n(ip_parts, n):
    decimal_parts = [str(int(part)) for part in ip_parts[:n]]  # Decimal, no leading zeros
    octal_parts = [f"{int(part):03o}" for part in ip_parts[n:]]   # Octal with leading zeros (3 digits)
    return '.'.join(decimal_parts + octal_parts)

def dec_oct_dec(ip_parts, n):
    if n == 1:
        return f"{int(ip_parts[0])}.{int(ip_parts[1]):04o}.{int(ip_parts[2]) * 256 + int(ip_parts[3])}"
    elif n == 2:
        return f"{int(ip_parts[0])}.{int(ip_parts[1]):04o}.{int(ip_parts[2]):04o}.{int(ip_parts[3])}"

def dec_hex_dec(ip_parts, n):
    if n == 1:
        return f"{int(ip_parts[0])}.0x{int(ip_parts[1]):X}.{int(ip_parts[2]) * 256 + int(ip_parts[3])}"
    elif n == 2:
        return f"{int(ip_parts[0])}.0x{int(ip_parts[1]):X}.0x{int(ip_parts[2]):X}.{int(ip_parts[3])}"

def dec_oct_hex(ip_parts, n):
    if n == 1:
        return f"{int(ip_parts[0])}.{int(ip_parts[1]):04o}.0x{int(ip_parts[2]) * 256 + int(ip_parts[3]):X}"
    elif n == 2:
        return f"{int(ip_parts[0])}.{int(ip_parts[1]):04o}.{int(ip_parts[2]):04o}.0x{int(ip_parts[3]):X}"

def dec_hex_oct(ip_parts, n):
    if n == 1:
        last = int(ip_parts[2]) * 256 + int(ip_parts[3])
        return f"{int(ip_parts[0])}.0x{int(ip_parts[1]):X}.{last:04o}"
    elif n == 2:
        return f"{int(ip_parts[0])}.0x{int(ip_parts[1]):X}.0x{int(ip_parts[2]):X}.{int(ip_parts[3]):04o}"

def oct_hex_merge_n(ip_parts, n):
    first = [f"{int(part):04o}" for part in ip_parts[:n - 1]]
    hex_num = sum(int(ip_parts[i]) * (256 ** (3 - i)) for i in range(n - 1, 4))
    return '.'.join(first) + '.' + f"0x{hex_num:X}"

def oct_dec_n(ip_parts, n):
    return '.'.join([f"{int(part):04o}" for part in ip_parts[:n]] + [str(int(part)) for part in ip_parts[n:]])

def oct_n(ip_parts, n):
    return '.'.join([f"{int(part):04o}" if i == n - 1 else part for i, part in enumerate(ip_parts)])

def oct_hex_n(ip_parts, n):
    return '.'.join([f"{int(part):04o}" for part in ip_parts[:n]] + [f"0x{int(part):X}" for part in ip_parts[n:]])

def oct_dec_merge_n(ip_parts, n):
    first = [f"{int(part):04o}" for part in ip_parts[:n - 1]]
    decimal = sum(int(ip_parts[i]) * (256 ** (3 - i)) for i in range(n - 1, 4))
    return '.'.join(first) + '.' + str(decimal)

def octal_padded_n(ip_parts, n):
    return '.'.join([f"{int(part):08o}" for part in ip_parts[:n]] + ip_parts[n:])

def oct_oct_merge_n(ip_parts, n):
    first = [f"{int(part):04o}" for part in ip_parts[:n - 1]]
    octal = sum(int(ip_parts[i]) * (256 ** (3 - i)) for i in range(n - 1, 4))

    if first:
        return '.'.join(first) + '.' + f"{octal:04o}"
    else:
        return f"0{octal:04o}"

def oct_hex_oct(ip_parts, n):
    if n == 1:
        return f"{int(ip_parts[0]):04o}.0x{int(ip_parts[1]):X}.{int(ip_parts[2]):04o}{int(ip_parts[3]):04o}"
    elif n == 2:
        return f"{int(ip_parts[0]):04o}.0x{int(ip_parts[1]):X}.0x{int(ip_parts[2]):X}.{int(ip_parts[3]):04o}"

def oct_dec_oct(ip_parts, n):
    if n == 1:
        return f"{int(ip_parts[0]):04o}.{int(ip_parts[1])}.{int(ip_parts[2]):04o}{int(ip_parts[3]):04o}"
    elif n == 2:
        return f"{int(ip_parts[0]):04o}.{int(ip_parts[1])}.{int(ip_parts[2])}.{int(ip_parts[3]):04o}"

def oct_dec_hex(ip_parts, n):
    if n == 1:
        return f"{int(ip_parts[0]):04o}.{int(ip_parts[1])}.0x{int(ip_parts[2]) * 256 + int(ip_parts[3]):X}"
    elif n == 2:
        return f"{int(ip_parts[0]):04o}.{int(ip_parts[1])}.{int(ip_parts[2])}.0x{int(ip_parts[3]):X}"

def oct_hex_dec(ip_parts, n):
    if n == 1:
        return f"{int(ip_parts[0]):04o}.0x{int(ip_parts[1]):X}.{int(ip_parts[2]) * 256 + int(ip_parts[3])}"
    elif n == 2:
        return f"{int(ip_parts[0]):04o}.0x{int(ip_parts[1]):X}.0x{int(ip_parts[2]):X}.{int(ip_parts[3])}"



def obfuscate_ip(ip, count=5):
    ip_parts = ip.split('.')
    obfuscated_ips = [
        hex_padded_n(ip_parts, 4),
        hex_padded_n(ip_parts, 3),
        hex_padded_n(ip_parts, 2),
        hex_padded_n(ip_parts, 1),

        hex_n(ip_parts, 4), # Duplicate dec_hex_n(ip_parts, 3), [X]
        hex_n(ip_parts, 3),
        hex_n(ip_parts, 2),
        # hex_n(ip_parts, 1), # Duplicate hex_dec_n(ip_parts, 4), [X]

        hex_dec_n(ip_parts, 4),
        hex_dec_n(ip_parts, 3), # Duplicate hex_dec_merge_n(ip_parts, 4), [X]
        hex_dec_n(ip_parts, 2),
        hex_dec_n(ip_parts, 1),

        # hex_oct_n(ip_parts, 4), # Duplicate hex_dec_n(ip_parts, 4) [X]
        hex_oct_n(ip_parts, 3), #
        hex_oct_n(ip_parts, 2), #
        hex_oct_n(ip_parts, 1), #

        # hex_dec_merge_n(ip_parts, 4), # Duplicated [X]
        hex_dec_merge_n(ip_parts, 3), #
        hex_dec_merge_n(ip_parts, 2), # 

        # hex_hex_merge_n(ip_parts, 4), # Duplicate hex_dec_n(ip_parts, 4) [X]
        hex_hex_merge_n(ip_parts, 3), #
        hex_hex_merge_n(ip_parts, 2), #
        hex_hex_merge_n(ip_parts, 1), # 


        # hex_oct_merge_n(ip_parts, 4), # Duplicate hex_oct_n(ip_parts, 3)  [X]
        hex_oct_merge_n(ip_parts, 3), # 
        hex_oct_merge_n(ip_parts, 2), #
        # hex_oct_merge_n(ip_parts, 1), # Duplicate oct_oct_merge_n(ip_parts, 1) [X]

        hex_oct_dec(ip_parts, 1), #
        hex_oct_dec(ip_parts, 2), #

        hex_dec_oct(ip_parts, 1), #
        hex_dec_oct(ip_parts, 2), #

        hex_dec_hex(ip_parts, 1), #
        hex_dec_hex(ip_parts, 2), #

        hex_oct_hex(ip_parts, 1), #
        hex_oct_hex(ip_parts, 2), # 

        # dec_hex_n(ip_parts, 3), # Duplicated [X]
        dec_hex_n(ip_parts, 2), #
        dec_hex_n(ip_parts, 1), #

        dec_oct_n(ip_parts, 3), # 
        dec_oct_n(ip_parts, 2), # 
        dec_oct_n(ip_parts, 1), # 

        dec_dec_merge_n(ip_parts, 1), # 
        dec_dec_merge_n(ip_parts, 2), #
        dec_dec_merge_n(ip_parts, 3), #
        # dec_dec_merge_n(ip_parts, 4), # Original IP address format [X]


        dec_hex_merge_n(ip_parts, 3), #
        dec_hex_merge_n(ip_parts, 2), #
        # dec_hex_merge_n(ip_parts, 1), # Duplicate hex_hex_merge_n(ip_parts, 1) [X]

        dec_oct_merge_n(ip_parts, 3), # Duplicate oct_n(ip_parts, 4), [X]
        dec_oct_merge_n(ip_parts, 2), #
        dec_oct_merge_n(ip_parts, 1), #

        dec_oct_dec(ip_parts, 1), #
        dec_oct_dec(ip_parts, 2), #

        dec_hex_dec(ip_parts, 1), #
        dec_hex_dec(ip_parts, 2), #

        dec_oct_hex(ip_parts, 1), #
        dec_oct_hex(ip_parts, 2), #

        dec_hex_oct(ip_parts, 1), #
        dec_hex_oct(ip_parts, 2), #

        # long_dec(ip_parts),
        octal_padded_n(ip_parts, 4),
        octal_padded_n(ip_parts, 3),
        octal_padded_n(ip_parts, 2),
        octal_padded_n(ip_parts, 1),

        # oct_n(ip_parts, 4), # Duplicate [X]
        oct_n(ip_parts, 3),
        oct_n(ip_parts, 2),
        oct_n(ip_parts, 1), # Duplicate

        oct_dec_n(ip_parts, 4),
        oct_dec_n(ip_parts, 3), 
        oct_dec_n(ip_parts, 2), 
        oct_dec_n(ip_parts, 1), 

        oct_hex_n(ip_parts, 3),
        oct_hex_n(ip_parts, 2),
        oct_hex_n(ip_parts, 1),

        oct_hex_merge_n(ip_parts, 3),
        oct_hex_merge_n(ip_parts, 2),
        # oct_hex_merge_n(ip_parts, 1),# Duplicate hex_hex_merge_n(ip_parts, 1) [X]

        oct_dec_merge_n(ip_parts, 3),
        oct_dec_merge_n(ip_parts, 2),
        # oct_dec_merge_n(ip_parts, 1), # Duplicate dec_dec_merge_n(ip_parts, 1) [X]
        
        oct_oct_merge_n(ip_parts, 3),
        oct_oct_merge_n(ip_parts, 2),
        oct_oct_merge_n(ip_parts, 1),

        oct_hex_oct(ip_parts,1),
        oct_hex_oct(ip_parts,2),

        oct_dec_oct(ip_parts,1),
        oct_dec_oct(ip_parts,2),

        oct_dec_hex(ip_parts,1),
        oct_dec_hex(ip_parts,2),

        oct_hex_dec(ip_parts,1),
        oct_hex_dec(ip_parts,2),
    ]
    return obfuscated_ips[:count]

def obfuscate_url(url, count=5, domain_list=None):
    encoded_urls = set()
    attempts = 0
    while len(encoded_urls) < count and attempts < 100:
        encoded_url = encode_random_chars(url)
        if domain_list:
            for domain in domain_list:
                modified_url = insert_domain_after_protocol(encoded_url, domain)
                encoded_urls.add(modified_url)
                if len(encoded_urls) == count:
                    break
        else:
            if encoded_url not in encoded_urls:
                encoded_urls.add(encoded_url)
        attempts += 1
    return list(encoded_urls)