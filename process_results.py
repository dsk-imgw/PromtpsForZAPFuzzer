import uuid
import argparse
import re
import pandas as pd
import openpyxl

DATA_DIR = 'data'

def process_file(input_file, output_prefix = None):

    try:
        text_data = ''
        excel_data = []
        with open(input_file, 'r', encoding = 'utf-8') as f:
            text_data = f.read()

        pattern = re.compile(r"=+\s*(\d+)\s*=+\n(.*?)(?=\n=|\Z)", re.DOTALL)
        matches = pattern.findall(text_data)

        file_prefix = ''     
        if output_prefix:
            file_prefix = output_prefix
        else:
            file_prefix = str(uuid.uuid4())

        for match in matches:
            file_number = match[0]
            data = match[1].strip()
            
            file_name_txt = DATA_DIR + '/' + file_prefix + '-' + file_number + '.txt'
            with open(file_name_txt, "w", encoding = 'utf-8') as f:
                f.write(data)        
            excel_data.append([file_number, data])

        file_name_xlsx = DATA_DIR + '/' + file_prefix + '.xlsx'
        df = pd.DataFrame(excel_data, columns = ['#', 'リクエスト・レスポンス'])
        df.to_excel(file_name_xlsx, index = False)
        wb1 = openpyxl.load_workbook(filename = file_name_xlsx)
        ws1 = wb1.worksheets[0]
        ws1.column_dimensions['B'].width = 200
        font = openpyxl.styles.Font(name = 'Meiryo UI')
        for row in ws1:
            for cell in row:
                ws1[cell.coordinate].font = font
        wrap_text = openpyxl.styles.Alignment(wrapText = True)
        for cell in ws1['B:B']:
            cell.alignment = wrap_text
        wb1.save(file_name_xlsx)

    except FileNotFoundError:
        print(f"ファイルが見つかりません: {input_file}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def main():
    parser = argparse.ArgumentParser(description='ZAP でエクスポートした HTTP リクエスト・レスポンス ファイルを、ペイロードごとのファイルに分割する。')
    parser.add_argument('input_file', help='入力ファイル（ZAP でエクスポートした HTTP リクエスト/レスポンス ファイル）名')
    parser.add_argument('-p', '--prefix', help='出力ファイル名の接頭辞。未指定時は、適当な UUID が設定される。')
    args = parser.parse_args()

    process_file(args.input_file, args.prefix)

if __name__ == '__main__':
    main()