import click
import urllib.parse
from functions.IP_obfuscation import obfuscate_ip, obfuscate_url
from functions.URL_deobfuscation import deobfuscate_ip, deobfuscate_url
from functions.url_utils import is_ip_address

# ANSI escape codes for colors
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--option', '-op', 'option', type=int, help="Select a specific option for obfuscation or deobfuscation.")
@click.option('--ip_or_url', '-i','ip_or_url', help='The IP or URL to process.')
@click.option('--file', '-f', type=click.Path(exists=True), help='Input file (one IP/URL per line).')
@click.option('--output', '-o', type=click.Path(), help='Output file to save results.')
@click.option('--count', '-c', default=5, show_default=True, help='Number of obfuscated versions (obfuscate only).')
@click.option('--domains', '-d', 'domains',  help='Domains file for masking (obfuscate only).')
def cli(ctx, option, ip_or_url, file, output, count, domains):
    """
    MorphURL obfuscates and deobfuscates IP addresses and URLs.
    It provides various techniques for transforming IPs and URLs
    into less recognizable forms, and also methods to revert them
    back to their original representations.

    To get help for a specific command, run:
      python main.py --help

    To use IP obfuscation, please input IP addresses with protocols like 'http://' or 'https://'.
    """
    if ctx.invoked_subcommand is None:
        if option is not None:
            if option == 1:
                process_obfuscation(ip_or_url, count, domains, output, file)
            elif option == 2:
                process_deobfuscation(ip_or_url, output, file)
            elif option == 0:
                print(YELLOW + "Goodbye! Have a great day ~" + RESET)
            else:
                print(RED + "Invalid option. Please select 0, 1 or 2." + RESET)
        else:
            # Landing Page
            print(f"""
    __  ___                 __    __  ______  __
   /  |/  /___  _________  / /_  / / / / __ \\/ /
  / /|_/ / __ \\/ ___/ __ \\/ __ \\/ / / / /_/ / /
 / /  / / /_/ / /  / /_/ / / / / /_/ / _, _/ /___
/_/  /_/\\____/_/  / .___/_/ /_/\\____/_/ |_/_____/
                 /_/

{YELLOW}~ Welcome to the URL Obfuscation and Deobfuscation Tool ~{RESET}
MorphURL obfuscates and deobfuscates IP addresses and URLs.
It provides various techniques for transforming IPs and URLs
into less recognizable forms, and also methods to revert them
back to their original representations.

To use IP obfuscation, please input IP addresses with protocols like 'http://' or 'https://'.

Select an option below to get started:

0. Exit

1. Obfuscate an IP or URL:
    Transform an IP address or URL into obfuscated forms to
    make it harder to interpret. Optionally, provide a file
    of URLs or IPs for batch processing.

2. Deobfuscate an IP or URL:
    Reverse the obfuscation to recover the original IP or URL.

Examples:
    python main.py -op 1 -i http://example.com
    python main.py -op 2 -f obfuscated_urls.txt -o deobfuscated_results.txt

    """)
            while True:
                try:
                     option_selected = int(input(f"What script do you want to run ({GREEN}1{RESET} for obfuscate; {GREEN}2{RESET} for deobfuscate; {GREEN}0{RESET} to exit): "))
                     if option_selected in [0, 1, 2]:
                        break
                     else:
                        print(RED + "Invalid selection, please select 0, 1 or 2." + RESET)
                except ValueError:
                    print(RED + "Invalid input, please enter a number." + RESET)
            if option_selected == 0:
                print(YELLOW + "Exiting MorphURL tool." + RESET)
                return
            if option_selected == 1:
                ip_or_url = input("Enter the IP or URL to obfuscate or the path to the input file: ")
                output = input("Enter the path to the output file, or press enter to print in console: ")
                try:
                    count = int(input("Enter the count (how many obfuscated versions you want to generate, default is 5): "))
                except ValueError:
                    print(RED + "Invalid input, using default count of 5." + RESET)
                    count = 5
                domains = input("Enter the path to the domain file or a single domain, or press enter to skip: ")
                process_obfuscation(ip_or_url, count, domains, output)


            elif option_selected == 2:
                ip_or_url = input("Enter the IP or URL to deobfuscate or the path to the input file: ")
                output = input("Enter the path to the output file, or press enter to print in console: ")

                process_deobfuscation(ip_or_url, output)


def process_obfuscation(ip_or_url, count, domains, output, file = None):
    """Handles IP/URL obfuscation based on provided input."""
    inputs = []
    if file:
        with open(file, 'r', encoding="utf8") as f:
            inputs = [line.strip() for line in f]
    elif ip_or_url:
        if is_file_path(ip_or_url):
             try:
                 with open(ip_or_url, 'r', encoding="utf8") as f:
                     inputs = [line.strip() for line in f]
             except FileNotFoundError:
                 print(RED + f"Error: File not found: {ip_or_url}" + RESET)
                 return
        else:
             inputs = [ip_or_url]
    else:
        print(RED + "Provide either an IP/URL or an input file using -f." + RESET)
        return

    domain_list = []
    if domains:
        if  isinstance(domains, str):
             domain_list = [domains]
        else:
            with open(domains, 'r') as f:
                domain_list = [line.strip() for line in f]

    results = []
    for item in inputs:
        if is_ip_address(item):
            ip = urllib.parse.urlsplit(item).netloc
            obfuscated_ips = obfuscate_ip(ip, count)
            modified_items = []

            for obf_ip in obfuscated_ips:
                modified_url = item.replace(ip, obf_ip)
                encoded_urls = obfuscate_url(modified_url, count, domain_list)
                modified_items.extend(encoded_urls)

            results.extend(modified_items)
        else:
            encoded_urls = obfuscate_url(item, count, domain_list)
            results.extend(encoded_urls)

    if output:
        with open(output, 'w', encoding="utf8") as f:
            for result in results:
                f.write(f"{result}\n")
        print(GREEN + f"Results saved to {output}" + RESET)
    else:
        for result in results:
            print(result)



def process_deobfuscation(ip_or_url, output, file = None):
        """Handles IP/URL deobfuscation based on provided input."""
        inputs = []
        if file:
            with open(file, 'r', encoding="utf8") as f:
                inputs = [line.strip() for line in f]
        elif ip_or_url:
            if is_file_path(ip_or_url):
                try:
                    with open(ip_or_url, 'r', encoding="utf8") as f:
                        inputs = [line.strip() for line in f]
                except FileNotFoundError:
                        print(RED + f"Error: File not found: {ip_or_url}" + RESET)
                        return
            else:
                inputs = [ip_or_url]
        else:
            print(RED + "Provide either an IP/URL or an input file using -f." + RESET)
            return

        results = []
        for item in inputs:
            # Decode percent-encoded characters
            item = urllib.parse.unquote(item)
            # Remove HTTP basic auth
            protocol = urllib.parse.urlsplit(item).scheme
            protocol = 'http' if protocol == '' else protocol
            path = urllib.parse.urlsplit(item).path
            item = urllib.parse.urlsplit(item).netloc.split('@')[-1]
            item = f"{protocol}://{item}{path}"

            try:
                deobfuscated = deobfuscate_ip(item)
                if deobfuscated == "Invalid IP":
                    deobfuscated = deobfuscate_url(item)
                # Add protocol back to the URL, deobfuscate_url removes it
                deobfuscated = f"{protocol}://{deobfuscated}"
            except Exception as e:
                print(RED + f"Invalid URL provided: {item}, Error: {e}" + RESET)
                continue

            if output:
                results.append(f"{deobfuscated}")
            else:
                print(f"Original: {item}, Deobfuscated: {deobfuscated}")

        if output:
            with open(output, 'w', encoding="utf8") as outfile:
                for result in results:
                    outfile.write(f"{result}\n")
            print(GREEN + f"Results saved to {output}" + RESET)
        else:
            for result in results:
                print(result) #print to the console

def is_file_path(path):
    """Check if a string is a valid file path"""
    try:
        click.Path(exists = True).convert(path, None, None)
        return True
    except click.exceptions.BadParameter:
        return False


if __name__ == '__main__':
    cli()