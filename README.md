# MorphURL: IP and URL Obfuscator/Deobfuscator

MorphURL is a versatile command-line tool designed for obfuscating and deobfuscating IP addresses and URLs. It provides a range of techniques to transform IPs and URLs into less recognizable forms, enhancing privacy and security in various scenarios.  The tool also includes methods to revert the obfuscated values back to their original representations.

## Features

* **Multiple Obfuscation Techniques:** MorphURL offers a variety of IP obfuscation methods including hexadecimal, octal, decimal conversions, and combinations thereof. It also provides URL obfuscation through percent-encoding and domain masking.
* **URL Encoding and Domain Masking:** Obfuscate URLs by encoding random characters and masking them with dummy domains for enhanced privacy.
* **Batch Processing:**  Process single IPs/URLs or entire lists from input files efficiently.
* **Customizable Output:**  Direct output to the console or save results to a file.
* **Easy-to-Use CLI:**  Intuitive command-line interface with clear options and helpful messages.
* **Cross-Platform Compatibility:** Works seamlessly on various operating systems.

> [!IMPORTANT]
> **Please include protocol (e.g. `http://`, `https://`) if you want to obfuscate URLs & IPs.**


## Installation
1. With Docker (Recommended)
   1. Clone the repository:
      ```bash
      git clone https://github.com/whiteSHADOW1234/MorphURL.git
      ```
   2. Navigate to the project directory:
      ```bash
      cd MorphURL
      ```
   3. Install the required packages:
      ```bash
      docker build -t morphurl .
      ```   


1. Without Docker
   1. Clone the repository:
      ```bash
      git clone https://github.com/whiteSHADOW1234/MorphURL.git
      ```
   2. Navigate to the project directory:
      ```bash
      cd MorphURL
      ```
   3. Install the required packages:
      ```bash
      pip install -r requirements.txt
      ```

## Usage
MorphURL can be used in multiple ways:

### 1. Command-Line Interface (CLI)

You can use the tool directly from the command line with the following syntax:

```bash
python main.py --option <option_number> [--ip_or_url <ip_or_url>] [-f <input_file>] [--output <output_file>] [-c <count>] [-d <domains_file>]
```

*   `--option <option_number>` or `-op <option_number>`: Select the operation mode. Use `1` for obfuscation or `2` for deobfuscation. If no options are specified, the tool will start in interactive mode.

*   `--ip_or_url <ip_or_url>` or `-i <ip_or_url>`: The IP address or URL to process directly. If using a file, this parameter is used to specify the file path.

*   `-f <input_file>`: Path to a file containing IPs/URLs (one per line). This can be used instead of the `--ip_or_url` option for batch processing.

*   `--output <output_file>` or `-o <output_file>`: Path to the output file to save results.

*   `-c <count>`: Number of obfuscated variations to generate (default: 5). This is only used with obfuscation.

*   `--domains <domains_file>` or `-d <domains_file>`: Path to a file containing domains for URL masking (one per line), or the domain itself. This is only used with obfuscation.

### 2. Interactive Mode

If you run the tool without any command-line options, it will start in interactive mode and guide you through the process:

```bash
python main.py
```

The tool will prompt you to select the desired operation (obfuscate or deobfuscate) and provide necessary input.

### 3. Docker Mode
For the usage of Docker, you can execute the following commands to use either **Interactive** or **CLI Mode**.
```
docker run -it morphurl    # Interactive Mode
docker run morphurl --help # CLI Mode
```

## CLI Examples

**Obfuscate:**

```bash
python main.py -op 1 -i http://example.com
python main.py -op 1 -i http://example.com -c 3 -o obfuscated.txt
python main.py -op 1 -f input_URLs.txt -d domains.txt -o output.txt
```

**Deobfuscate:**

```bash
python main.py -op 2 -i 0x7f000001
python main.py -op 2 -i "http://example.com@192.168.0.1" -o deobfuscated.txt
python main.py -op 2 -f obfuscated.txt -o deobfuscated_ips.txt
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
