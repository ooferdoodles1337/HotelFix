import pandas as pd
import csv
import sys
import os

csv_file_path = "data/config/nationality_code.csv"
nationality_dict = {}

# Read CSV data into the dictionary
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        nationality_dict[row['รหัสสัญชาติ']] = row['รหัส icao']


def process_and_save_excel(input_filename, output_filename):
    # Read data from the input file
    df = pd.read_excel(input_filename)

    # Selecting and renaming columns
    df = df[['First Name\nชื่อ', 
             'Middle Name\nชื่อกลาง', 
             'Last Name\nนามสกุล',
             'Sex\nเพศ\n(M-ชาย,F-หญิง)',
             'Passport No.\nหนังสือเดินทาง',
             'Nationality\nสัญชาติ',
             'Date of Birth (mm/dd/yyyy) (A.D.)\nวันที่เกิด (ค.ศ.)',
             'Expire Date of Stay (mm/dd/yyyy) (A.D.)\nวันครบกำหนดอนุญาต (ค.ศ.)',
             ]]

    # Renaming columns
    df = df.rename(columns={
        'First Name\nชื่อ': 'ชื่อ\nFirst Name *',
        'Middle Name\nชื่อกลาง': 'ชื่อกลาง\nMiddle Name',
        'Last Name\nนามสกุล': 'นามสกุล\nLast Name',
        'Sex\nเพศ\n(M-ชาย,F-หญิง)': 'เพศ\nGender *',
        'Passport No.\nหนังสือเดินทาง': 'เลขหนังสือเดินทาง\nPassport No. *',
        'Nationality\nสัญชาติ': 'สัญชาติ\nNationality *',
        'Date of Birth (mm/dd/yyyy) (A.D.)\nวันที่เกิด (ค.ศ.)': 'วัน เดือน ปี เกิด\nBirth Date *\nDD/MM/YYYY(ค.ศ. / A.D.)',
        'Expire Date of Stay (mm/dd/yyyy) (A.D.)\nวันครบกำหนดอนุญาต (ค.ศ.)': 'วันที่แจ้งออกจากที่พัก\nCheck-out Date *\nDD/MM/YYYY(ค.ศ. / A.D.)',
    })

    # Add a new column 'เบอร์โทรศัพท์\nPhone No.' with NaN values
    df['เบอร์โทรศัพท์\nPhone No.'] = ''

    df['สัญชาติ\nNationality *'] = df['สัญชาติ\nNationality *'].apply(lambda x: nationality_dict.get(x, None))

    # Split the input filename into root and extension
    root, ext = os.path.splitext(input_filename)

    # Determine the output filename
    if output_filename is None:
        output_filename = root + '_processed.xlsx'

    # Save the processed data to a new Excel file
    df.to_excel(output_filename, index=False, sheet_name="แบบแจ้งที่พัก Inform Accom")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_filename> [output_filename]")
        sys.exit(1)

    input_filename = sys.argv[1]
    
    # Output filename is an optional argument
    output_filename = sys.argv[2] if len(sys.argv) > 2 else None

    process_and_save_excel(input_filename, output_filename)