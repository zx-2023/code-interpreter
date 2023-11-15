import xlrd
import csv


def convert_to_csv(excel_file):
    workbook = xlrd.open_workbook(excel_file)
    all_worksheets = workbook.sheet_names()
    for worksheet_name in all_worksheets:
        worksheet = workbook.sheet_by_name(worksheet_name)
        with open(u'{}.csv'.format(worksheet_name), 'w', encoding="utf-8") as csv_file:
            wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            for row in range(worksheet.nrows):
                wr.writerow(worksheet.row_values(row))
    print(csv_file)

    return csv_file
