import logging
import cv2 as cv
import asyncio


async def black_and_white(image_url: str):
    logging.basicConfig(level=logging.INFO)
    logging.info('image_proccessing.py black_and_white() started')

    image = cv.imread(image_url)
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imwrite(image_url, gray_image)

    logging.info('image_proccessing.py black_and_white() finished')
    return image_url


if __name__ == '__main__':
    asyncio.run(black_and_white('test.jpg'))
