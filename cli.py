import click
import ipaddress
import urllib.parse
from functions.IP_obfuscation import obfuscate_url, obfuscate_ip
from functions.URL_deobfuscation import deobfuscate_ip, deobfuscate_url
from functions.url_utils import is_ip_address

@click.group()
def cli():
    """
    MorphURL obfuscates and deobfuscates IP addresses and URLs. 
    It provides various techniques for transforming IPs and URLs
    into less recognizable forms, and also methods to revert them
    back to their original representations.
    """
    pass

@cli.command()
@click.argument('ip_or_url', required=False)
@click.option('-f', '--file', type=click.Path(exists=True), help='Input file (one IP/URL per line).')
@click.option('-c', '--count', default=5, show_default=True, help='Number of obfuscated versions (obfuscate only).')
@click.option('-o', '--output', type=click.Path(), help='Output file (obfuscate only).')
@click.option('-d', '--domains', type=click.Path(exists=True), help='Domains file for masking (obfuscate only).')
def obfuscate(ip_or_url, file, count, output, domains):
    """
    Obfuscates an IP address or URL.

    Examples:
      obfuscate 192.168.1.1
      obfuscate http://example.com -c 10
      obfuscate -f ips.txt -o obfuscated.txt
    """
    inputs = []
    if file:
        with open(file, 'r', encoding="utf8") as f:
            inputs = [line.strip() for line in f]
    elif ip_or_url:
        inputs = [ip_or_url]
    else:
        raise click.UsageError("Provide either an IP/URL or an input file using -f.")

    domain_list = []
    if domains:
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
        click.echo(f"Results saved to {output}")
    else:
        for result in results:
            click.echo(result)

@cli.command()
@click.argument('ip_or_url', required=False)
@click.option('-f', '--file', type=click.Path(exists=True), help='Input file (one IP/URL per line).')
@click.option('-o', '--output', type=click.Path(), help='Output file to save results.') 
def deobfuscate(ip_or_url, file, output):
    """
    Deobfuscates an IP address or URL.

    Examples:
      deobfuscate 0x7f.0.0.1
      deobfuscate http://domain.com@127.0.0.1
      deobfuscate -f obfuscated.txt -o deobfuscated.txt
    """
    inputs = []
    if file:
        with open(file, 'r', encoding="utf8") as f:
            inputs = [line.strip() for line in f]
    elif ip_or_url:
        inputs = [ip_or_url]
    else:
        raise click.UsageError("Provide either an IP/URL or an input file using -f.")

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
        except:
            click.echo("Invalid URL provided: ", item)

        if output:
            results.append(f"{deobfuscated}")
        else:
            click.echo(f"Original: {item}, Deobfuscated: {deobfuscated}")

        if output:
            with open(output, 'w', encoding="utf8") as outfile:
                for result in results:
                    outfile.write(f"{result}\n")  # Write each result to a new line
        else:
            for result in results:
                click.echo(result) #print to the console

if __name__ == '__main__':
    cli()