#!/usr/bin/env python3.4

# Needs imagemagick to work (convert does the image conversion).
# Usage: ./pdf2png.py <PDF-File> <Number of Pages>

import os.path, subprocess, sys

def convert_job(page):
    convert_args = ['convert', '-units', 'PixelsPerInch', '-density', '400',
                    '{}[{}]'.format(filename, page - 1), '-channel', 'RGBA',
                    '-fill', 'white', '-opaque', 'none', '{}_{:03d}.png'.format(
                        basename, page)]
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

            if argc == 2:
                pages = int(sys.argv[2])
                print("test")
            else:
                pages = count_pages(filename)

            print('Starting conversion of {} pages.'.format(pages))

            print('\r{:3d} of {:3d} pages converted.'.format(finished_jobs,
                                                             pages), end='')

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
                    print('\r{:3d} of {:3d} pages converted.'.format(
                        finished_jobs, pages), end='')

        else:
            print('Error: File "{}" does not exist!'.format(sys.argv[1]))

    else:
        print('Wrong number of arguments!')

    print()
