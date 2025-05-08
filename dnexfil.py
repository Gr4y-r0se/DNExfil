import base64
import argparse
import sys

def extract_host_components(text):
    results = []
    lines = text.strip().splitlines()[1:]  # Skip the first line

    for line in lines:
        parts = line.split(',')
        if len(parts) >= 7:
            b64_data = parts[6]
            try:
                decoded = base64.b64decode(b64_data).decode('utf-8', errors='ignore')
                for decoded_line in decoded.splitlines():
                    if decoded_line.startswith("Host:"):
                        host = decoded_line[len("Host: "):].strip()
                        host_parts = host.split('.')
                        if len(host_parts) >= 3:
                            index = int(host_parts[0])       # Use the number for sorting
                            binary = host_parts[1]
                            chunk = host_parts[2]
                            results.append((index, binary, chunk))
                        break
            except Exception:
                pass  # Silently ignore decoding issues

    # Sort by the numeric index and return list of [binary, chunk] pairs
    results.sort(key=lambda x: x[0])
    return [[binary, chunk] for _, binary, chunk in results]

def reconstruct_file_from_dns_data(pairs, domain=None):
    reconstructed = []

    for binary, chunk in pairs:
        # Recreate original case pattern
        reconstructed_chunk = []
        for i, bit in enumerate(binary):
            if i < len(chunk):
                char = chunk[i]
                if bit == '1':
                    reconstructed_chunk.append(char.upper())
                else:
                    reconstructed_chunk.append(char.lower())
        reconstructed.append("".join(reconstructed_chunk))

    # Join all chunks into a full base64url string
    b64url = ''.join(reconstructed)

    # Convert base64url back to standard base64
    b64 = b64url.replace('-', '+').replace('_', '/')
    padding = '=' * ((4 - len(b64) % 4) % 4)
    b64 += padding

    try:
        decoded = base64.b64decode(b64).decode('utf-8')
        return decoded
    except Exception as e:
        raise ValueError(f"Failed to decode base64 data: {e}")

def html_to_data_uri(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    encoded = base64.b64encode(html_content.encode()).decode()
    return f"data:text/html;base64,{encoded}"

def main():
    parser = argparse.ArgumentParser(description="Decode DNS-exfiltrated data or convert HTML to data URI.")
    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--output", "-o", default="output.txt", help="Output file path")
    parser.add_argument("--data-uri", "-d", action="store_true", help="Convert HTML file to base64 data URI")

    args = parser.parse_args()

    if args.data_uri:
        if not args.input.lower().endswith(".html"):
            print("Error: --data-uri expects an HTML file from --input.")
            sys.exit(1)
        uri = html_to_data_uri(args.input)
        print(uri)
    else:
        with open(args.input, 'r', encoding='utf-8') as file:
            content = file.read()
        parts = extract_host_components(content)
        reconstructed = reconstruct_file_from_dns_data(parts)
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(reconstructed)
        print(f"Decoded output written to {args.output}")

if __name__ == "__main__":
    main()
