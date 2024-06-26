import cv2
import os
import zmq
import time
import pickle
import struct


VIDEO_PATH = os.getenv(
    "DATA_FILE",
    default="./data/conus_20171021_20171022_30FPS.mp4",
)
PLAYBACK_PORT = os.getenv("PLAYBACK_PORT", default="5555")
PLAYBACK_HOST = os.getenv("PLAYBACK_HOST", default="*")  # bind - accept all


def split_frames(video):
    capture = cv2.VideoCapture(video)
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
    frames = []

    while True:
        success, frame = capture.read()
        if success:
            # cv2.imwrite(f"./frame_{frame_number}.jpg", frame)
            prefix = struct.pack(">QQ", int(width), int(height))
            frames.append(
                {
                    "width": width,
                    "height": height,
                    "data": prefix + pickle.dumps(frame),
                }
            )
        else:
            break
    capture.release()
    return frames


def main():
    print("splitting frames...", end="")
    frames = split_frames(VIDEO_PATH)
    print("complete.")
    print("")

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(f"tcp://{PLAYBACK_HOST}:{PLAYBACK_PORT}")

    count = 0
    while True:
        for frame in frames:
            publisher.send(frame["data"])
            print(f"published frame {count}")
            count = count + 1
            time.sleep(0.1)


if __name__ == "__main__":
    print("data_playback started.")
    main()
