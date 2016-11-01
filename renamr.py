#!/usr/bin/env python

"""A simple program that resize images in bulk and add text over it."""

import argparse
import datetime
import os
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

__author__ = 'Nicolas Richard'
__copyright__ = 'Copyright 2016, The Cogent Project'
__credits__ = ['Alexandra Latour-Verret']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Nicolas Richard'
__email__ = 'nicolas.richard@polymtl.ca'
__status__ = 'Prototype'

def check_date(value):
    """Insures that the format of a date argument is valid, i.e. YYYY-MM-DD."""
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentTypeError("%s is an invalid positive date value" % value)
    return value

def draw_text(x, y, img, drawer, font, text):
    """Draw a caption with an outline on the image."""
    width, _ = drawer.textsize(text, font)
    x = img.size[0] - width - 10
    drawer.text((x-1, y-1), text, font=font, fill='black')
    drawer.text((x+1, y-1), text, font=font, fill='black')
    drawer.text((x-1, y+1), text, font=font, fill='black')
    drawer.text((x+1, y+1), text, font=font, fill='black')
    drawer.text((x, y), text,(255,255,255), font=font)

def parse_arguments():
    """Parses the arguments that were provided with the program.
    It returns a tuple (array) containing the directory path, the base name, the captions and the date if it was
    provided."""
    parser = argparse.ArgumentParser(description='''Resizes and renames all the images found in a directory.
                                                 Prints a caption containing the name of the file, the date of creation
                                                 and a custom value.''')
    parser.add_argument('directory', nargs=1, help='The path of the directory containing the images.')
    parser.add_argument('base_name', nargs=1, help='The name that will be printed on each image with an incremental value')
    parser.add_argument('ratio', nargs=1, type=float, help='A value by which the size of the image will multiplied.')
    parser.add_argument('--date',
                        type=check_date,
                        metavar='D',
                        default=datetime.datetime.now().strftime("%Y-%m-%d"),
                        help='The timestamp to be printed on the images. The format must be YYYY-MM-DD')
    parser.add_argument('--captions', nargs='*', metavar='C', help='The captions to be printed on the images.')
    args = parser.parse_args()
    return args

def renamr(directory, base_name, ratio, captions, date):
    """Main function of the program"""
    i = 1
    path = os.path.join(os.path.dirname(__file__), directory)
    for file in os.listdir(path):
        if not file.endswith('.jpg'):
            continue
        img = Image.open(os.path.join(path, file))
        img = img.resize((int(img.size[0] * ratio), int(img.size[1] * ratio)), Image.ANTIALIAS)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('font.ttf', 20)
        x = 0
        y = 10
        for caption in captions:
            draw_text(x, y, img, draw, font, caption)
            y = y + 20
        draw_text(x, y, img, draw, font, date)
        draw_text(x, y + 20, img, draw, font, '%s-%03i' % (base_name, i))
        img.save('%s-%03i.jpg' % (os.path.join(path, base_name), i))
        i = i + 1
        os.remove(os.path.join(path, file))

if __name__=='__main__':
    args = parse_arguments()
    renamr(args.directory[0], args.base_name[0], args.ratio[0], args.captions, args.date)

