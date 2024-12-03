# MorphURL: IP and URL Obfuscator/Deobfuscator

MorphURL is a versatile command-line tool designed for obfuscating and deobfuscating IP addresses and URLs. It provides a range of techniques to transform IPs and URLs into less recognizable forms, enhancing privacy and security in various scenarios.  The tool also includes methods to revert the obfuscated values back to their original representations.

## Features

* **Multiple Obfuscation Techniques:** MorphURL offers a variety of IP obfuscation methods including hexadecimal, octal, decimal conversions, and combinations thereof. It also provides URL obfuscation through percent-encoding and domain masking.
* **URL Encoding and Domain Masking:** Obfuscate URLs by encoding random characters and masking them with dummy domains for enhanced privacy.
* **Batch Processing:**  Process single IPs/URLs or entire lists from input files efficiently.
* **Customizable Output:**  Direct output to the console or save results to a file.
* **Easy-to-Use CLI:**  Intuitive command-line interface with clear options and helpful messages.
* **Cross-Platform Compatibility:** Works seamlessly on various operating systems.


## Installation

MorphURL requires Python 3.7 or higher.

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/MorphURL.git  # Replace with your repository URL
   ```
2. Navigate to the project directory:
   ```bash
   cd MorphURL
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt  # Create a requirements.txt with 'click' and 'ipaddress'
   ```

## Usage

### Obfuscate

```bash
python cli.py obfuscate <ip_or_url> [-c <count>] [-o <output_file>] [-d <domains_file>]  # Single IP/URL
python cli.py obfuscate -f <input_file> [-c <count>] [-o <output_file>] [-d <domains_file>]  # From file
```

*   `<ip_or_url>`: The IP address or URL to obfuscate.
*   `-f <input_file>`: Path to a file containing IPs/URLs (one per line).
*   `-c <count>`: Number of obfuscated variations to generate (default: 5).
*   `-o <output_file>`: Path to the output file to save results.
*   `-d <domains_file>`: Path to a file containing domains for URL masking (one per line).


### Deobfuscate

```bash
python cli.py deobfuscate <ip_or_url> [-o <output_file>] # Single IP/URL
python cli.py deobfuscate -f <input_file> [-o <output_file>] # From file

```

*   `<ip_or_url>`: The IP address or URL to deobfuscate.
*   `-f <input_file>`: Path to a file containing obfuscated IPs/URLs (one per line).
*   `-o <output_file>`: Path to the output file to save results.


## Examples

**Obfuscate:**

```bash
python cli.py obfuscate 192.168.1.1
python cli.py obfuscate http://example.com -c 3 -o obfuscated.txt
python cli.py obfuscate -f input.txt -d domains.txt -o output.txt
```

**Deobfuscate:**

```bash
python cli.py deobfuscate 0x7f000001
python cli.py deobfuscate "http://example.com@192.168.0.1" -o deobfuscated.txt
python cli.py deobfuscate -f obfuscated.txt -o deobfuscated_ips.txt

```


## Contributing

Contributions are welcome! Here's how you can contribute to MorphURL:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear messages.
4. Push your branch to your forked repository.
5. Create a pull request to the main repository.

## Contact

For any questions or suggestions, please create an issue on this GitHub repository.
