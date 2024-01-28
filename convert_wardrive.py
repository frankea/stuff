import argparse

def convert_wardrive_log(input_filename, output_filename):
    # Header lines to be added at the beginning of the output file
    header_lines = [
        "[WigleWifi-1.4],appRelease=[x],model=[ESP32S2],release=[x],device=[Flipper-dev],display=[MonochromeLCD],board=[FlipperDevBoard],Brand=[Flipper]\n",
        "MAC,SSID,AuthMode,FirstSeen,Channel,RSSI,CurrentLatitude,CurrentLongitude,AltitudeMeters,AccuracyMeters,Type\n"
    ]

    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        # Write the header lines to the output file
        for line in header_lines:
            outfile.write(line)

        for line in infile:
            line = line.strip()
            # Stop processing when '#stopscan' is encountered
            if line == '#stopscan':
                break

            # Check if the line starts with a digit (indicating a wardriving result line)
            if line.startswith('>') or (line and line[0].isdigit()):
                # If the line starts with '>', remove it
                if line.startswith('>'):
                    line = line[1:]

                # Split the line on '|' and then on ',' to get the data parts
                parts = line.split('|')
                if len(parts) < 2:
                    continue  # Skip incomplete lines

                data_parts = parts[1].split(',')
                if len(data_parts) < 10:
                    continue  # Ensure there are enough parts to extract data

                # Extract relevant data
                bssid = data_parts[0].strip()
                ssid = data_parts[1].strip()
                capabilities = data_parts[2].strip()  # Keep the original format with brackets
                first_seen = data_parts[3].strip()
                channel = data_parts[4].strip()
                rssi = data_parts[5].strip()
                latitude = data_parts[6].strip()
                longitude = data_parts[7].strip()
                altitude = data_parts[8].strip()
                accuracy = data_parts[9].strip().split(' ')[0]  # Assuming accuracy might be followed by 'WIFI' or other text

                # Format the line according to the specified format
                formatted_line = f'{bssid},{ssid},{capabilities},{first_seen},{channel},{rssi},{latitude},{longitude},{altitude},{accuracy},WIFI\n'

                # Write the formatted line to the output file
                outfile.write(formatted_line)

def main():
    parser = argparse.ArgumentParser(description='Convert Wardrive Results to Log Format')
    parser.add_argument('input_filename', help='Input file name containing wardrive results')
    parser.add_argument('output_filename', help='Output file name for the converted log')
    args = parser.parse_args()

    convert_wardrive_log(args.input_filename, args.output_filename)

if __name__ == '__main__':
    main()
