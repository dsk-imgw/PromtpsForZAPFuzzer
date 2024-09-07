import json
import os
import urllib.parse

def convert_txt_to_x(src_dir, dst_dir, enc):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for filename in os.listdir(src_dir):
        if filename.endswith(".txt"):
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_dir, filename)

            lines = ''
            with open(src_file, 'r', encoding = 'utf-8') as f_in, open(dst_file, 'w', encoding = 'utf-8') as f_out:
                for line in f_in:
                    line = line.strip()
                    if line.startswith('#'):
                        lines += line + '\n'
                    else:
                        #line = line.rstrip()
                        if enc == 'JSON':
                            lines += json.dumps(line) + '\n'
                        elif enc == 'URL':
                            lines += urllib.parse.quote(line) + '\n'
                f_out.write(lines.rstrip())

def main():
    src_dir = 'payloads'
    dst_dir = 'payloads_JsonEncoded'
    enc = 'JSON'
    convert_txt_to_x(src_dir, dst_dir, enc)

    dst_dir = 'payloads_UrlEncoded'
    enc = 'URL'
    convert_txt_to_x(src_dir, dst_dir, enc)


if __name__ == '__main__':
    main()