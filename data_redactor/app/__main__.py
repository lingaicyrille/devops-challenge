import cv2
import os
import pickle
import zmq
import struct


COLOR_BLACK = (0, 0, 0)
FILL_RECTANGLE = -1
REDACT_WIDTH = 100

PLAYBACK_PORT = os.getenv("PLAYBACK_PORT", default="5555")
PLAYBACK_HOST = os.getenv("PLAYBACK_HOST", default="localhost")
REDACTOR_PORT = os.getenv("REDACTOR_PORT", default="5556")
REDACTOR_HOST = os.getenv("REDACTOR_HOST", default="*")  # bind - access all


def redact_border(image, width, height, size):
    # top
    start_point = (0, 0)
    end_point = (width, size)
    image = cv2.rectangle(image, start_point, end_point, COLOR_BLACK, FILL_RECTANGLE)
    # right
    start_point = (width - size, 0)
    end_point = (width, height)
    image = cv2.rectangle(image, start_point, end_point, COLOR_BLACK, FILL_RECTANGLE)
    # bottom
    start_point = (0, height - size)
    end_point = (width, height)
    image = cv2.rectangle(image, start_point, end_point, COLOR_BLACK, FILL_RECTANGLE)
    # left
    start_point = (0, 0)
    end_point = (size, height)
    image = cv2.rectangle(image, start_point, end_point, COLOR_BLACK, FILL_RECTANGLE)

    return image


def data_redactor():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect(f"tcp://{PLAYBACK_HOST}:{PLAYBACK_PORT}")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")

    publisher = context.socket(zmq.PUB)
    publisher.bind(f"tcp://{REDACTOR_HOST}:{REDACTOR_PORT}")

    count = 0
    while True:
        data = subscriber.recv()
        width, height = struct.unpack(">QQ", data[0:16])
        image = pickle.loads(data[16:])

        image = redact_border(image, width, height, REDACT_WIDTH)
        # cv2.imwrite(f"./scratch/frame_{count}.jpg", image)
        data = data[0:16] + pickle.dumps(image)

        publisher.send(data)
        print(f"published frame {count}")
        count = count + 1


if __name__ == "__main__":
    print("data_redactor started.")
    data_redactor()
