import csv

def csv_to_markdown(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)

        max_widths = [len(h) for h in headers]
        for row in reader:
            max_widths = [max(len(str(cell)), width) for cell, width in zip(row, max_widths)]

        csv_file.seek(0)
        reader = csv.reader(csv_file)

        markdown_table = '|' + '|'.join(headers) + '|\n'
        markdown_table += '|' + '|'.join('-' * width for width in max_widths) + '|\n'

        for row in reader:
            markdown_table += '|' + '|'.join(row) + '|\n'

        return markdown_table

markdown_table = csv_to_markdown('./test_images.csv')
print(markdown_table)