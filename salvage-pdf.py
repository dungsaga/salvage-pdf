#!/usr/bin/env python3
import re, zlib, sys

def main(argv):
    print("Salvage text from a broken pdf file")
    print("Usage: salvage-pdf.py <input_file.pdf> <output_file.txt>")
    pdf = open(argv[1], "rb").read()
    output = salvage_pdf(pdf)
    with open(argv[2], "wb") as file: file.write(output)

def salvage_pdf(pdf):
    output = []
    stream = re.compile(rb'/FlateDecode.*?stream(.*?)endstream', re.S)
    for s in stream.findall(pdf):
        s = s.strip(b'\r\n')
        try:
            print(f"stream-{len(output):03}:")
            data = extract_text(zlib.decompress(s))
            if data: output.append(data)
        except:
            pass # ignore decompression failures
    return b"\n\n".join(output)

def extract_text(data):
    # extract lines ending with Tj or TJ
    lines = [line for line in data.split(b"\n") if (line[-2:]==b'Tj' or line[-2:]==b'TJ')]
    # remove everything except plain text inside (xxx)Tj or [(xxx)...(yyy)]TJ
    text = [re.sub(b'^.*?\(|\)Tj|\)\]TJ|\).+?\(', b'', line) for line in lines]
    return b"\n".join(text)

if __name__ == "__main__": main(sys.argv)
