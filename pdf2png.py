#!/usr/bin/env python3

# Needs imagemagick to work (convert does the image conversion).
# Usage: ./pdf2png.py <PDF-File>

import os.path, subprocess, sys
from PyPDF2 import PdfFileReader

def convert_job(page):
    convert_args = ['convert', '-units', 'PixelsPerInch', '-density', '300',
                    '{}[{}]'.format(filename, page - 1), '-channel', 'RGBA',
                    '-fill', 'white', '-opaque', 'none',
                    '{}_'.format(basename) + pagenum_format_lz.format(page) +
                    '.png']
    return subprocess.Popen(convert_args)

if __name__ == '__main__':
    argc = len(sys.argv[1:])
    max_children = 4
    children = []
    next_job = 1
    finished_jobs = 0

    if argc > 0 and argc < 3:

        if os.path.exists(sys.argv[1]):
            filename = sys.argv[1]
            basename = os.path.basename(os.path.splitext(filename)[0])

            # Get page count
            with open(filename, 'rb') as pdfFile:
                pdfReader = PdfFileReader(pdfFile)
                pages = pdfReader.getNumPages()

            pagenum_digits = len(str(pages))
            pagenum_format = '{{:{}d}}'.format(pagenum_digits)
            pagenum_format_lz = '{{:0{}d}}'.format(pagenum_digits)
            pages_of_pages = pagenum_format + ' of ' + pagenum_format

            print('Starting conversion of {} pages.'.format(pages))

            print('\r' + pages_of_pages.format(finished_jobs, pages)
                  + ' converted.', end='')

            while finished_jobs < pages:
                if next_job <= pages and len(children) < max_children:
                    children.append(convert_job(next_job))
                    #print('There are currently {} processes running'.format(
                    #    len(children))
                    #)
                    next_job += 1
                else:
                    wait_for_me = children.pop(0)
                    wait_for_me.wait()
                    finished_jobs += 1
                    print('\r' + pages_of_pages.format(finished_jobs, pages)
                          + ' converted.', end='')

        else:
            print('Error: File "{}" does not exist!'.format(sys.argv[1]))

    else:
        print('Wrong number of arguments!')

    print()  # Newline before the next shell prompt.
