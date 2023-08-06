from PIL import Image
from scipy.fftpack import fft2, ifft2
import numpy as np
import cv2
from skimage.morphology import binary_opening, binary_closing, disk

import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from skimage import filters, img_as_float
from PIL import Image
import matplotlib.pylab as pylab

import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.util import random_noise
from skimage import feature
import numpy as np

def generate_noisy_square(size=128, rotation=15, sigma=4, noise_mode='speckle', noise_mean=0.05):
    image = np.zeros((size, size), dtype=float)
    image[size//4:-size//4, size//4:-size//4] = 1
    image = ndi.rotate(image, rotation, mode='constant')
    image = ndi.gaussian_filter(image, sigma)
    image = random_noise(image, mode=noise_mode, mean=noise_mean)
    return image

def canny_edge_detection(image):
    # Compute the Canny filter for two values of sigma
    edges1 = feature.canny(image)
    edges2 = feature.canny(image, sigma=3)
    return edges1, edges2



def apply_convolution(image, kernel):
    convolved_image = cv2.filter2D(image, -1, kernel)
    return convolved_image

def apply_correlation(image, kernel):
    correlated_image = cv2.filter2D(image, -1, kernel)
    return correlated_image

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)

def process_image(image_path):
    im = Image.open(image_path).convert('L')
    im_array = np.array(im)
    
    freq = fft2(im_array)
    im1 = ifft2(freq).real
    
    snr = signaltonoise(im1, axis=None)
    
    return im_array, im1, snr

def perform_fourier_transform(image_path):
    # Read input image and convert to grayscale
    img = cv2.imread(image_path, 0)

    # Calculate optimal size for Fourier transform
    optimalImg = cv2.copyMakeBorder(img, 0, cv2.getOptimalDFTSize(img.shape[0]) - img.shape[0], 0, cv2.getOptimalDFTSize(img.shape[1]) - img.shape[1], cv2.BORDER_CONSTANT, value=0)

    # Calculate the discrete Fourier transform
    dft_shift = np.fft.fftshift(cv2.dft(np.float32(optimalImg), flags=cv2.DFT_COMPLEX_OUTPUT))

    # Calculate magnitude spectrum
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) + 1)

    # Reconstruct the image using inverse Fourier transform
    result = cv2.magnitude(cv2.idft(np.fft.ifftshift(dft_shift))[:, :, 0], cv2.idft(np.fft.ifftshift(dft_shift))[:, :, 1])

    return optimalImg, magnitude_spectrum, result

def apply_log_transform(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path)

    # Apply log transform
    log_transformed = 255 * np.log(1 + img.astype(np.float32)) / np.log(1 + np.max(img))

    # Convert the data type
    log_transformed = log_transformed.astype(np.uint8)

    # Save the output image
    cv2.imwrite(output_path, log_transformed)



def apply_gamma_correction(image, gamma_values):
    gamma_corrected_images = []

    for gamma in gamma_values:
        gamma_corrected = np.array(255 * (image / 255) ** gamma, dtype='uint8')
        gamma_corrected_images.append(gamma_corrected)

    return gamma_corrected_images




def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image)
    plt.axis('off')

def plot_hist(channel, title=""):
    plt.hist(np.array(channel).ravel(), bins=256, range=(0, 256), color='r', alpha=0.3)
    plt.xlabel('Pixel Values', size=20)
    plt.ylabel('Frequency', size=20)
    plt.title(title, size=10)

def plot_original(im):
    im_r, im_g, im_b = im.split()
    plt.style.use('ggplot')
    plt.figure(figsize=(15, 5))
    plt.subplot(121)
    plot_image(im)
    plt.subplot(122)
    plot_hist(im_r, "Red Channel")
    plot_hist(im_g, "Green Channel")
    plot_hist(im_b, "Blue Channel")
    plt.yscale('log')
    plt.show()

def contrast(c):
    return 0 if c < 50 else (255 if c > 150 else int((255 * c - 22950) / 48))

def plot_stretched(imc):
    im_rc, im_gc, im_bc = imc.split()
    plt.style.use('ggplot')
    plt.figure(figsize=(15, 5))
    plt.subplot(121)
    plot_image(imc)
    plt.subplot(122)
    plot_hist(im_rc, "Contrast-Adjusted Red Channel")
    plot_hist(im_gc, "Contrast-Adjusted Green Channel")
    plot_hist(im_bc, "Contrast-Adjusted Blue Channel")
    plt.yscale('log')
    plt.show()



def histogram_equalization(image):
    hist = cv2.calcHist([image],[0],None,[256],[0,256])
    eq = cv2.equalizeHist(image)
    cdf = hist.cumsum()
    cdfnmhist = cdf * hist.max() / cdf.max()
    histeq = cv2.calcHist([eq],[0],None,[256],[0,256])
    cdfeq = histeq.cumsum()
    cdfnmhisteq = cdfeq * histeq.max() / cdf.max()
    
    return eq, hist, cdfnmhist, histeq, cdfnmhisteq


import cv2 as cv

def threshold_image(img, threshold_value):
    ret, thresh = cv.threshold(img, threshold_value, 255, cv.THRESH_BINARY)
    return thresh




import numpy as np
from scipy import signal

import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=20)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def apply_gradient(im):
    ker_x = np.array([[-1, 1]])
    ker_y = np.array([[-1], [1]])
    im_x = signal.convolve2d(im, ker_x, mode='same')
    im_y = signal.convolve2d(im, ker_y, mode='same')
    im_mag = np.sqrt(im_x ** 2 + im_y ** 2)
    im_dir = np.arctan2(im_y, im_x)
    return im_x, im_y, im_mag, im_dir

def apply_laplacian(im):
    ker_laplacian = np.array([[0, -1, 0],
                              [-1, 4, -1],
                              [0, -1, 0]])
    im1 = np.clip(signal.convolve2d(im, ker_laplacian, mode='same'), 0, 1)
    return im1




def plot_img(image, title=""):
    pylab.title(title, size=10)
    pylab.imshow(image)
    pylab.axis('off')


def sobel_edge_detection(image):
    edges_x = filters.sobel_h(image)
    edges_y = filters.sobel_v(image)
    return np.clip(edges_x, 0, 1), np.clip(edges_y, 0, 1)



def generate_noisy_square(size=128, rotation=15, sigma=4, noise_mode='speckle', noise_mean=0.05):
    image = np.zeros((size, size), dtype=float)
    image[size//4:-size//4, size//4:-size//4] = 1
    image = ndi.rotate(image, rotation, mode='constant')
    image = ndi.gaussian_filter(image, sigma)
    image = random_noise(image, mode=noise_mode, mean=noise_mean)
    return image

def canny_edge_detection(image):
    # Compute the Canny filter for two values of sigma
    edges1 = feature.canny(image)
    edges2 = feature.canny(image, sigma=3)
    return edges1, edges2
def plot_canny(image, title="", ax=None):
    if ax is None:
        ax = pylab.gca()
    ax.set_title(title, fontsize=10)
    ax.imshow(image, cmap='gray')
    ax.axis('off')



def erosion(image, kernel_size):
    return cv2.erode(image, np.ones((kernel_size, kernel_size), np.uint8), iterations=1)

def dilation(image, kernel_size):
    return cv2.dilate(image, np.ones((kernel_size, kernel_size), np.uint8), iterations=1)

def opening(image, disk_size):
    return binary_opening(image, disk(disk_size))

def closing(image, disk_size):
    return binary_closing(image, disk(disk_size))
def threshold_image(image, threshold_value):
    _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return binary_image



def load_image(file_path):
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def convert_to_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray

def threshold_image(image):
    ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

def segment_image(image):
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=15)
    bg = cv2.dilate(closing, kernel, iterations=1)
    dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0)
    ret, fg = cv2.threshold(dist_transform, 0.02 * dist_transform.max(), 255, 0)
    return fg

def plot_image(image, title=""):
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.title(title)
    plt.show()
def plot_images(image, title=""):
    plt.imshow(image, cmap='gray')
    plt.title(title, fontsize=10)
    plt.axis('off')