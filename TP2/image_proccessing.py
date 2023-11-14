import logging
import cv2 as cv
import asyncio
import os


async def black_and_white(image_url: str) -> str:
    logging.basicConfig(level=logging.INFO)
    logging.info('image_proccessing.py black_and_white() started')

    image = cv.imread(image_url)
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    filename, extension = os.path.splitext(image_url)
    bw_image_url = f"{filename}_bw{extension}"

    cv.imwrite(bw_image_url, gray_image)

    logging.info('image_proccessing.py black_and_white() finished')
    return bw_image_url

if __name__ == '__main__':
    asyncio.run(black_and_white('./test.jpeg'))
