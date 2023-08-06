#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhangjian
# date: 2023/7/13


import logging
import threading
from collections import deque

import cv2
import numpy as np

from . import get_time_str, makedirs, setup_logger, MyTimer

class FrameInfo(object):
    def __init__(self, image, frame_idx, frame_elapsed_ms):
        self.image = image
        self.frame_idx = frame_idx
        self.frame_elapsed_ms = frame_elapsed_ms
        self.frame_mot_result = None

    def get_image(self):
        return self.image

    def get_frame_idx(self):
        return self.frame_idx

    def get_frame_elapsed_s(self):
        return self.frame_elapsed_ms / 1000

    def get_frame_elapsed_ms(self):
        return self.frame_elapsed_ms

    def set_det_ret(self, mot_result):
        self.frame_mot_result = mot_result

    def get_det_ret(self):
        return self.frame_mot_result


class VideoStreamReader(threading.Thread):
    def __init__(self, video_input_param, skip_frames=0, frame_queue_len=1, name='video_reader', log_level='INFO'):
        super(VideoStreamReader, self).__init__(name=name)
        self.logger = setup_logger('zj_utils', log_root=None, log_file_save_basename=None, level=log_level, screen=True,
                                   tofile=False, msecs=True)

        self.video_input_param = video_input_param
        self.mytimer = MyTimer()
        self.stopped = False
        self.frames_deque = deque(maxlen=frame_queue_len)
        self.skip_frames = skip_frames + 1
        self.logger.info('VideoReader init done.')

    def get_frames(self):
        return self.frames_deque

    def run(self, raw_image=False):
        self.logger.info('VideoReader running ...')
        self.cap = cv2.VideoCapture(self.video_input_param)
        # MYLOGGER.info(f'Load video stream from {self.video_input_param}')
        self.logger.info(f'Video is {"opened." if self.cap.isOpened() else "not opened."}')
        self.cap_fps = self.cap.get(5)
        height, width = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT), self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.logger.info(f'Video stream FPS: {self.cap_fps}\tshape: ({height}, {width})')
        frame_idx = 0
        while not self.stopped:
            self.mytimer.restart()
            ret, image = self.cap.read()
            # MYLOGGER.debug(
            #     f'---VideoReader--- cap read elapsed: {self.mytimer.elapsed():.2f}ms')
            if frame_idx % self.skip_frames != 0:
                continue
            if ret:
                if raw_image:
                    frame = image
                else:
                    frame = FrameInfo(image=image, frame_idx=frame_idx,
                                      frame_elapsed_ms=self.cap.get(cv2.CAP_PROP_POS_MSEC))
                self.frames_deque.append(frame)
                self.logger.debug(
                    f'---VideoReader--- Put Frame-{frame_idx} to the list ---- len-{len(self.frames_deque)}: '
                    f'{[x.get_frame_idx() for x in self.frames_deque]} elapsed: {self.mytimer.elapsed():.2f}ms')
            else:
                self.logger.debug(
                    f'---VideoReader--- READ NONE FRAME ---- len: {len(self.frames_deque)} {self.cap.isOpened()}')
                self.cap = cv2.VideoCapture(self.video_input_param)
                self.logger.info(f'Reloaded video stream')
                # self.logger.info(f'Reload video stream from {self.video_input_param}')
            frame_idx += 1

        self.cap.release()
        self.logger.info('Camera is closed.')

    def stop(self):
        self.stopped = True


def main():
    pass


if __name__ == '__main__':
    main()
