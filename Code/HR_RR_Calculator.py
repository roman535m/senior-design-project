import numpy as np
import time
from scipy import signal
from FaceDetection import FaceDetection


class HR_RR_Calculator(object):
    def __init__(self):
        self.frame_in = np.zeros((10, 10, 3), np.uint64)
        self.frame_ROI = np.zeros((10, 10, 3), np.uint64)
        self.frame_out = np.zeros((10, 10, 3), np.uint64)
        # FFT works best when we're processing 2^n elements
        self.buffer_size = 64
        self.times = []
        self.roi_buffer_list = []
        self.fps = 0.0
        self.fft = []
        self.freqs = []
        self.t0 = time.time()
        self.bpm = 0
        self.rrpm = 0
        self.fd = FaceDetection()
        self.hr_list = []
        self.uv = []
        self.sdaftm = 0
        self.std = 0
        self.uv_mean = 0
        self.bpms = []
        self.idx_bool = False

    def run(self, frame_in):
        self.frame_in = frame_in
        self.frame_out, self.frame_ROI = self.fd.face_detect(self.frame_in)

        # Record ROI value and the time it was extracted. We must have 1-to-1 list for FFT to work
        x = np.mean(self.frame_ROI[:, :, 1])
        self.roi_buffer_list.append(x)
        self.times.append(time.time() - self.t0)

        # We're only looking at the last "buffer_size" number of samples and times they were collected
        self.roi_buffer_list = self.roi_buffer_list[-self.buffer_size:]
        self.times = self.times[-self.buffer_size:]

        # Convert buffer list to numpy array
        roi_buffer_array = np.array(self.roi_buffer_list)

        # Once we accumulate enough samples we shall proceed
        if len(self.roi_buffer_list) == self.buffer_size:

            # FPS is also the sampling frequency (because the time was normalized to zero we can divide by last element
            self.fps = float(self.buffer_size) / (self.times[-1] - self.times[0])

            # ESTP is the evenly spaced time period divided into N samples where N is buffer_size
            # For example, if N = 20, t[-1] = 1.00, and t[0] = 0, we'd get [0.00, 0.05, 0.10, ... , 0.95, 1.00]
            estp = np.linspace(self.times[0], self.times[-1], self.buffer_size)

            sig = signal.detrend(roi_buffer_array)

            delta_t = (self.times[-1] - self.times[0]) / self.buffer_size
            self.freqs = np.fft.fftfreq(sig.size, delta_t)
            interpolated = np.interp(estp, self.times, sig)
            interpolated = np.hamming(self.buffer_size) * interpolated

            norm = interpolated / np.linalg.norm(interpolated)
            raw = np.fft.rfft(norm)
            self.fft = np.abs(raw) ** 2

            eligible_hr_freq_idx = np.where((self.freqs > 1.0) & (self.freqs < 1.6))
            eligible_rr_freq_idx = np.where((self.freqs > 0.18) & (self.freqs < 0.3))
            self.freqs = self.freqs * 60.0

            hr_freqs = self.freqs[eligible_hr_freq_idx]
            self.bpm = hr_freqs[np.argmax(self.fft[eligible_hr_freq_idx])]

            rr_freqs = self.freqs[eligible_rr_freq_idx]
            self.rrpm = rr_freqs[np.argmax(self.fft[eligible_rr_freq_idx])]

            self.hr_list.append(self.bpm)
            self.bpms.append(self.bpm)

            self.idx_bool = False

    def reset(self):
        self.times = []
        self.roi_buffer_list = []
        self.fps = 0
        self.fft = []
        self.freqs = []
        self.t0 = time.time()
        self.bpm = 0
        self.rrpm = 0
        self.fd = FaceDetection()
        self.hr_list = []
        self.uv = []
        self.sdaftm = 0
        self.std = 0
        self.uv_mean = 0

