import os
import requests
from icrawler.builtin import GoogleImageCrawler
from PIL import Image
from aiogram.types import MediaGroup, InputFile

from config import PHTOTROOM_TOKEN


def main(filename, promt, count):
    remove_bg(filename, 'media/proccesing/image_no_background.png')
    find_images(promt, count)

    img = Image.open('media/proccesing/image_no_background.png')

    x, y = img.size

    photos = os.listdir('media/proccesing/photos/')

    for photo in photos:
        img2 = Image.open('media/proccesing/photos/' + photo)

        x2, y2 = img2.size

        if x > x2 or y > y2:
            img2 = img2.resize((x, y))

        else:
            x_1 = x2 / 2 - x / 2
            y_1 = y2 / 2 - y / 2

            x_2 = x2 / 2 + x / 2
            y_2 = y2 / 2 + y / 2

            img2 = img2.crop((x_1, y_1, x_2, y_2))

        img2.paste(img, img)
        img2.save('media/result/' + photo)

    count = 0
    for i in list(map(lambda x: 'media/result/' + x, os.listdir('media/result/'))):
        os.rename(i, 'media/result/' + str(count) + '.jpg')
        count += 1

    result_images = list(map(lambda x: 'media/result/' + x, os.listdir('media/result/')))

    media = MediaGroup()

    for i in result_images:
        media.attach_photo(InputFile(i))

    # for i in result_images[len(result_images) // 2:]:
    #     media2.attach_photo(InputFile(i))

    for photo in photos:
        os.remove('media/proccesing/photos/' + photo)

    return result_images

    # return media


def remove_bg(input_name, output_name):
    headers = {
        'x-api-key': PHTOTROOM_TOKEN,
    }

    files = {
        'image_file': open(input_name, 'rb'),
    }

    response = requests.post('https://sdk.photoroom.com/v1/segment', headers=headers, files=files)

    with open(output_name, 'wb') as f:
        f.write(response.content)


def find_images(keyword, count):
    try:
        google_crawler = GoogleImageCrawler(storage={'root_dir': 'media/proccesing/photos'})
        google_crawler.crawl(keyword=keyword, max_num=count)
    except:
        pass
