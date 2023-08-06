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


def fft():
    code = """
import matplotlib.pyplot as plt
from image_func import process_image

# Provide the path to the image file
image_path = r"C:\\Users\\arman\\Pictures\\floweer.jpg"

# Process the image using the process_image function from the sigtonoise package
processed_image, reconstructed_image, snr = process_image(image_path)

# Display the original image
plt.figure(figsize=(10, 5))
plt.imshow(processed_image, cmap='gray')
plt.axis('off')
plt.title('ORIGINAL IMAGE', size=15)
plt.show()

# Display the reconstructed image with SNR
plt.figure(figsize=(10, 5))
plt.imshow(reconstructed_image, cmap='gray')
plt.axis('off')
plt.title(f'IMAGE OBTAINED AFTER RECONSTRUCTION\nSNR: {snr:.2f}', size=15)
plt.show()
"""
    print(code)

def convolution():
    code="""
import cv2a
import numpy as np
from image_func import apply_convolution, apply_correlation
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread(r"C:\Users\arman\Pictures\floweer.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define a convolution kernel
conv_kernel = np.ones((3, 3), np.float32) / 9

# Perform convolution
convolved_image = apply_convolution(image, conv_kernel)

# Define a correlation kernel
corr_kernel = np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]])

# Perform correlation
correlated_image = apply_correlation(image, corr_kernel)

# Display the results or perform additional processing
# ...
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(image)
axes[0].axis('off')
axes[0].set_title('Original Image')

axes[1].imshow(convolved_image)
axes[1].axis('off')
axes[1].set_title('Convolved Image')

axes[2].imshow(correlated_image)
axes[2].axis('off')
axes[2].set_title('Correlated Image')

plt.tight_layout()
plt.show()
"""
    print(code)

def dft():
    code=""" import matplotlib.pyplot as plt
from image_func import perform_fourier_transform

# Specify the image path
image_path = r"C:\Users\arman\Pictures\floweer.jpg"

# Perform Fourier transform
optimalImg, DFT, result = perform_fourier_transform(image_path)

# Display the results
images = [optimalImg, DFT, result]
imageTitles = ['Input image', 'DFT', 'Reconstructed image']

for i in range(len(images)):
    plt.subplot(1, 3, i + 1)
    plt.imshow(images[i], cmap='gray')
    plt.title(imageTitles[i])
    plt.xticks([])
    plt.yticks([])

plt.show()
"""
    print(code)

def log():
    code="""import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_func import apply_log_transform

# Specify the image paths
input_image_path = r"C:\IP practicals\floweer.jpg"
output_image_path = r"C:\IP practicals\floweer1.jpg"

# Apply log transform
apply_log_transform(input_image_path, output_image_path)

# Display the original and log-transformed images
img = cv2.imread(input_image_path)
log_transformed = cv2.imread(output_image_path)

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(log_transformed, cv2.COLOR_BGR2RGB))
plt.title('Log-Transformed Image')

plt.show()
"""
    print(code)

def power():
    code="""import cv2
import numpy as np
from image_func import apply_gamma_correction

# Specify the image path
image_path = r"C:\IP practicals\floweer.jpg"

# Specify the gamma values
gamma_values = [0.1, 0.5, 1.2, 2.2, 5]

# Read the image
img = cv2.imread(image_path)

# Apply gamma correction
gamma_corrected_images = apply_gamma_correction(img, gamma_values)

# Display the original image
cv2.imshow('Original Image', img)
cv2.waitKey(0)

# Display the gamma-corrected images
for gamma_corrected in gamma_corrected_images:
    cv2.imshow('Gamma Corrected Image', gamma_corrected)
    cv2.waitKey(0)

cv2.destroyAllWindows()
"""
    print(code)

def contrast():
    code="""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from image_func import plot_original, plot_stretched, contrast

image_path = r"C:\IP practicals\floweer.jpg"
im = Image.open(image_path)

plot_original(im)

imc = im.point(contrast)

plot_stretched(imc)
"""
    print(code)

def histogram():
    code="""
import cv2
import matplotlib.pyplot as plt

from image_func import histogram_equalization

# Read the image
image_path = r"C:\IP practicals\floweer.jpg"
img = cv2.imread(image_path, 0)

# Perform histogram equalization
equalized_image, original_hist, original_cdf_hist, equalized_hist, equalized_cdf_hist = histogram_equalization(img)

# Plot the images and histograms
plt.subplot(221), plt.imshow(img, 'gray')
plt.subplot(222), plt.plot(original_hist), plt.plot(original_cdf_hist)
plt.subplot(223), plt.imshow(equalized_image, 'gray')
plt.subplot(224), plt.plot(equalized_hist), plt.plot(equalized_cdf_hist)
plt.xlim([0, 256])
plt.show()
"""
    print(code)

def threshold():
    code="""
import cv2
import numpy as np
from matplotlib import pyplot as plt
from image_func import threshold_image

# Load the image
img = cv2.imread(r"C:\IP practicals\floweer.jpg")
# Set the threshold value
threshold_value = 127

# Perform thresholding using the threshold_image function
thresh = threshold_image(img, threshold_value)

# Plot the images manually
titles = ['Original Image', 'Thresholded']
images = [img, thresh]
for i in range(2):
    plt.subplot(1, 2, i + 1)
    plt.imshow(images[i], 'gray', vmin=0, vmax=255)
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
"""
    print(code)

def gradient():
    code="""
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from image_func import plot_image, apply_gradient, apply_laplacian

im = rgb2gray(imread(r"C:\IP practicals\floweer.jpg"))

# Apply gradient
im_x, im_y, im_mag, im_dir = apply_gradient(im)

# Plot the gradient results
plt.gray()
plt.figure(figsize=(20, 15))
plt.subplot(231)
plot_image(im, 'Original')
plt.subplot(232)
plot_image(im_x, 'Gradient x')
plt.subplot(233)
plot_image(im_y, 'Gradient y')
plt.subplot(234)
plot_image(im_mag, '||Gradient||')
plt.legend(prop={'size': 20})
plt.show()

# Apply Laplacian
im1 = apply_laplacian(im)

# Plot the Laplacian result
plt.gray()
plt.figure(figsize=(10, 5))
plt.subplot(121)
plot_image(im, 'Original')
plt.subplot(122)
plot_image(im1, 'Laplacian Convolved')
plt.show()
"""
    print(code)

def sharpening():
    code="""
import numpy as np
from skimage import filters, img_as_float, color
from skimage.io import imread
import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def sharpen_image(image):
    blurred = filters.gaussian(image, sigma=3)
    detail = np.clip(image - blurred, 0, 1)
    alpha_values = [1, 5, 10]

    fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True, figsize=(15, 15))
    axes = axes.ravel()
    axes[0].set_title('Original Image', size=15)
    axes[0].imshow(image, cmap='gray')
    
    axes[1].set_title('Blurred Image (sigma=3)', size=15)
    axes[1].imshow(blurred, cmap='gray')
    
    axes[2].set_title('Detail Image', size=15)
    axes[2].imshow(detail, cmap='gray')
    for i, alpha in enumerate(alpha_values):
        sharpened = np.clip(image + alpha * detail, 0, 1)
        axes[3+i].imshow(sharpened, cmap='gray')
        axes[3+i].set_title(f'Sharpened Image (alpha={alpha})', size=15)
    for ax in axes:
        ax.axis('off')
    fig.tight_layout()
    plt.show()

# Load the grayscale image
image = color.rgb2gray(imread(r"C:\Users\Aditi\OneDrive\Pictures\IP\flower.jpg"))

# Perform sharpening and display the results
sharpen_image(image)
"""
    print(code)

def edge():
    code="""
import numpy as np
from skimage import filters, img_as_float, color
from skimage.io import imread
import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def sharpen_image(image):
    blurred = filters.gaussian(image, sigma=3)
    detail = np.clip(image - blurred, 0, 1)
    alpha_values = [1, 5, 10]

    fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True, figsize=(15, 15))
    axes = axes.ravel()
    axes[0].set_title('Original Image', size=15)
    axes[0].imshow(image, cmap='gray')
    
    axes[1].set_title('Blurred Image (sigma=3)', size=15)
    axes[1].imshow(blurred, cmap='gray')
    
    axes[2].set_title('Detail Image', size=15)
    axes[2].imshow(detail, cmap='gray')
    for i, alpha in enumerate(alpha_values):
        sharpened = np.clip(image + alpha * detail, 0, 1)
        axes[3+i].imshow(sharpened, cmap='gray')
        axes[3+i].set_title(f'Sharpened Image (alpha={alpha})', size=15)
    for ax in axes:
        ax.axis('off')
    fig.tight_layout()
    plt.show()

# Load the grayscale image
image = color.rgb2gray(imread(r"C:\Users\Aditi\OneDrive\Pictures\IP\flower.jpg"))

# Perform sharpening and display the results
sharpen_image(image)
"""
    print(code)

def canny():
    code="""
import matplotlib.pylab as pylab
from skimage import feature
from image_func import plot_canny, generate_noisy_square, canny_edge_detection

# Generate noisy image of a square
image = generate_noisy_square()

# Perform Canny edge detection
edges1, edges2 = canny_edge_detection(image)

# Display results
# Display results
fig, ax = pylab.subplots(nrows=1, ncols=3, figsize=(8, 3))

plot_canny(image, 'noisy image', ax=ax[0])

plot_canny(edges1, r'Canny filter, $\sigma=1$', ax=ax[1])

plot_canny(edges2, r'Canny filter, $\sigma=3$', ax=ax[2])

pylab.show()


"""
    print(code)

def sobel():
    code="""
from skimage.io import imread
from PIL import Image
import matplotlib.pylab as pylab
import numpy as np
from skimage import filters
from image_func import plot_image ,sobel_edge_detection

image_path = r"C:\IP practicals\floweer.jpg"

# Open and convert the image to grayscale
im = Image.open(image_path).convert('L')
im_array = np.array(im)
# Perform Sobel edge detection
edges_x, edges_y = sobel_edge_detection(im_array)

# Display the images
pylab.gray()
pylab.figure(figsize=(15, 15))
pylab.subplot(2, 2, 1)
plot_image(im, 'Original')
pylab.subplot(2, 2, 2)
plot_image(edges_x, 'Sobel X')
pylab.subplot(2, 2, 3)
plot_image(edges_y, 'Sobel Y')
pylab.subplot(2, 2, 4)
plot_image(edges_x + edges_y, 'Sobel X + Y')
pylab.subplots_adjust(wspace=0.1, hspace=0.1)
pylab.show()
"""
    print(code)

def erosion():
    code="""
import cv2
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.io import imread
import matplotlib.pylab as pylab
from image_func import threshold_image, erosion, dilation, opening, closing, plot_image


# Erosion and Dilation
img = cv2.imread(r"C:\IP practicals\floweer.jpg", 0)
bw_img = threshold_image(img, 127)

kernel_size = 5
img_erosion = erosion(img, kernel_size)
img_dilation = dilation(img, kernel_size)

plt.figure(figsize=(5, 5))
plot_image(img, "ORIGINAL IMAGE")
plt.show()
plot_image(img_erosion, "EROSION")
plt.show()
plot_image(img_dilation, "DILATION")
plt.show()

# Image opening and closing
im = rgb2gray(imread(r"C:\IP practicals\floweer.jpg"))
im[im <= 0.5] = 0
im[im > 0.5] = 1

disk_size = 6
im_opening = opening(im, disk_size)
im_closing = closing(im, disk_size)

pylab.gray()
pylab.figure(figsize=(20, 10))
plot_image(im, "original")
plot_image(im_opening, "opening with disk size 6")
plt.show()
plot_image(im_closing, "closing with disk size 6")
pylab.show()
"""
    print(code)

def segmentation():
    code="""
from image_func import load_image, convert_to_gray, threshold_image, segment_image,plot_images
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Loading original image
img = load_image(r'C:\IP practicals\floweer.jpg')

# Converting to grayscale
gray = convert_to_gray(img)

# Thresholding image
thresh = threshold_image(gray)

# Segmenting the image
segmented = segment_image(thresh)


# Displaying final output
plt.figure(figsize=(10, 10))
plt.subplot(2, 2, 1)
plot_images(img, "Original Image")
plt.subplot(2, 2, 2)
plot_images(gray, "Grayscale Image")
plt.subplot(2, 2, 3)
plot_images(thresh, "Threshold Image")
plt.subplot(2, 2, 4)
plot_images(segmented, "Segmented Image")
plt.tight_layout()
plt.show()
"""
    print(code)

def all():
    code="""
fft()
convolution()
dft()
log()
power()
contrast()
histogram()
threshold()
gradient()
sharpening()
edge()
canny()
sobel()
erosion()
segmentation()
"""
    print(code)



def spdSegmentation():
    code="""
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Loading original image
img = cv2.imread(r'bird.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Converting to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Converting to binary inverted image
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Segmenting the images
kernel = np.ones((3, 3), np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=15)
bg = cv2.dilate(closing, kernel, iterations=1)
dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0)
ret, fg = cv2.threshold(dist_transform, 0.02 * dist_transform.max(), 255, 0)

# Plotting the images
plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
plt.imshow(img, cmap="gray")
plt.axis('off')
plt.title("Original Image")

plt.subplot(2, 2, 2)
plt.imshow(gray, cmap="gray")
plt.axis('off')
plt.title("GrayScale Image")

plt.subplot(2, 2, 3)
plt.imshow(thresh, cmap="gray")
plt.axis('off')
plt.title("Threshold Image")

plt.subplot(2, 2, 4)
plt.imshow(fg, cmap="gray")
plt.axis('off')
plt.title("Segmented Image")

plt.show()
"""
    print(code)


def spdErosionDilation():
    code="""
import cv2
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.io import imread
import matplotlib.pylab as pylab
from image_func import threshold_image, erosion, dilation, opening, closing, plot_image


# Erosion and Dilation
img = cv2.imread(r"bird.jpg", 0)
bw_img = threshold_image(img)

kernel_size = 5
img_erosion = erosion(img, kernel_size)
img_dilation = dilation(img, kernel_size)

plt.figure(figsize=(5, 5))
plot_image(img, "ORIGINAL IMAGE")
plt.show()
plot_image(img_erosion, "EROSION")
plt.show()
plot_image(img_dilation, "DILATION")
plt.show()

# Image opening and closing
im = rgb2gray(imread(r"bird.jpg"))
im[im <= 0.5] = 0
im[im > 0.5] = 1

disk_size = 6
im_opening = opening(im, disk_size)
im_closing = closing(im, disk_size)

pylab.gray()
pylab.figure(figsize=(20, 10))
plot_image(im, "original")
plot_image(im_opening, "opening with disk size 6")
plt.show()
plot_image(im_closing, "closing with disk size 6")
pylab.show()
"""
    print(code)


def spdRobertPrewitt():
    code="""
import numpy as np
from skimage import filters
from PIL import Image
import matplotlib.pylab as pylab
from image_func import plot_img

def edge_detection(image_path):
    im = Image.open(image_path).convert('L')
    im_arr = np.asarray(im)
    pylab.gray()
    pylab.figure(figsize=(15, 15))
    pylab.subplot(3, 2, 1), plot_img(im, 'Original Image')
    edges = filters.roberts(im_arr)
    pylab.subplot(3, 2, 2), plot_img(edges, 'Roberts')
    edges = filters.scharr(im_arr)
    pylab.subplot(3, 2, 3), plot_img(edges, 'Scharr')
    edges = filters.sobel(im_arr)
    pylab.subplot(3, 2, 4), plot_img(edges, 'Sobel')
    edges = filters.prewitt(im_arr)
    pylab.subplot(3, 2, 5), plot_img(edges, 'Prewitt')
    edges = np.clip(filters.laplace(im_arr), 0, 1)
    pylab.subplot(3, 2, 6), plot_img(edges, 'Laplace')
    pylab.subplots_adjust(wspace=0.1, hspace=0.1)
    pylab.show()

# Set the path to the image
image_path = r"bird.jpg"

# Call the edge_detection function
edge_detection(image_path)
"""
    print(code)


def spdSobel():
    code="""
import numpy as np
from skimage import filters
from skimage.io import imread
import matplotlib.pyplot as plt

im = imread(r"bird.jpg", as_gray=True)

plt.gray()
fig, axes = plt.subplots(2, 2, figsize=(15, 15))

titles = ['Original', 'Sobel x', 'Sobel y', 'Sobel']
images = [im, filters.sobel_h(im), filters.sobel_v(im), filters.sobel(im)]

for ax, title, image in zip(axes.ravel(), titles, images):
    ax.imshow(np.clip(image, 0, 1), cmap='gray')
    ax.set_title(title)
    ax.axis('off')

plt.tight_layout()
plt.show()
"""
    print(code)


def spdCanny():
    code="""
import matplotlib.pyplot as plt
from skimage.util import random_noise
from skimage import feature

# Generate noisy image of a square
image = random_noise(feature.square(128), mode='speckle', mean=0.05)

# Compute the Canny filter for two values of sigma
edges1 = feature.canny(image)
edges2 = feature.canny(image, sigma=3)

# Display results
fig, ax = plt.subplots(1, 3, figsize=(8, 3))

ax[0].imshow(image, cmap='gray')
ax[0].set_title('noisy image', fontsize=10)

ax[1].imshow(edges1, cmap='gray')
ax[1].set_title(r'Canny filter, $\sigma=1$', fontsize=10)

ax[2].imshow(edges2, cmap='gray')
ax[2].set_title(r'Canny filter, $\sigma=3$', fontsize=10)

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()
"""
    print(code)


def spdSharpening():
    code="""
import numpy as np
from skimage import filters, img_as_float, color
from skimage.io import imread
import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def sharpen_image(image):
    blurred = filters.gaussian(image, sigma=3)
    detail = np.clip(image - blurred, 0, 1)
    alpha_values = [1, 5, 10]

    fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True, figsize=(15, 15))
    axes = axes.ravel()
    axes[0].set_title('Original Image', size=15)
    axes[0].imshow(image, cmap='gray')
    
    axes[1].set_title('Blurred Image (sigma=3)', size=15)
    axes[1].imshow(blurred, cmap='gray')
    
    axes[2].set_title('Detail Image', size=15)
    axes[2].imshow(detail, cmap='gray')
    for i, alpha in enumerate(alpha_values):
        sharpened = np.clip(image + alpha * detail, 0, 1)
        axes[3+i].imshow(sharpened, cmap='gray')
        axes[3+i].set_title(f'Sharpened Image (alpha={alpha})', size=15)
    for ax in axes:
        ax.axis('off')
    fig.tight_layout()
    plt.show()

# Load the grayscale image
image = color.rgb2gray(imread(r"flower.jpg"))

# Perform sharpening and display the results
sharpen_image(image)
"""
    print(code)


def spdGradientLaplacian():
    code="""
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from image_func import plot_image, apply_gradient, apply_laplacian

im = rgb2gray(imread(r"C:\IP practicals\floweer.jpg"))

# Apply gradient
im_x, im_y, im_mag, im_dir = apply_gradient(im)

# Plot the gradient results
plt.gray()
plt.figure(figsize=(20, 15))
plt.subplot(231)
plot_image(im, 'Original')
plt.subplot(232)
plot_image(im_x, 'Gradient x')
plt.subplot(233)
plot_image(im_y, 'Gradient y')
plt.subplot(234)
plot_image(im_mag, '||Gradient||')
plt.legend(prop={'size': 20})
plt.show()

# Apply Laplacian
im1 = apply_laplacian(im)

# Plot the Laplacian result
plt.gray()
plt.figure(figsize=(10, 5))
plt.subplot(121)
plot_image(im, 'Original')
plt.subplot(122)
plot_image(im1, 'Laplacian Convolved')
plt.show()
"""
    print(code)


def spdContrasting():
    code="""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image)
    plt.axis('off')
def plot_hist(channel, title=""):
    plt.hist(np.array(channel).ravel(), bins=256, range=(0, 256), color='r', alpha=0.3)
    plt.xlabel('Pixel Values', size=20)
    plt.ylabel('Frequency', size=20)
    plt.title(title, size=10)
image_path = r"flower.jpg"
im = Image.open(image_path)
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

imc = im.point(contrast)
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
"""
    print(code)


def spdThresholding():
    code="""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread(r"C:\Users\Aditi\Pictures\IP\flower.jpg", 0)
ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
ret, thresh2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
ret, thresh3 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
ret, thresh4 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)
ret, thresh5 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)
titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
for i in range(6):
    plt.subplot(2, 3, i + 1)
    plt.imshow(images[i], 'gray', vmin=0, vmax=255)
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
"""
    print(code)


def spdDFT():
    code="""
import numpy as np
import cv2
import matplotlib.pyplot as plt

img=cv2.imread(r"flower.jpg",0)

optimalImg=cv2.copyMakeBorder(img, 0, cv2.getOptimalDFTSize(img.shape[0])
                              -img.shape[0], 0, cv2.getOptimalDFTSize(img.shape[1])
                              -img.shape[1], cv2.BORDER_CONSTANT, value=0)
dft_shift=np.fft.fftshift(cv2.dft(np.float32(optimalImg), flags=cv2.DFT_COMPLEX_OUTPUT))
magnitude_spectrum=20*np.log(cv2.magnitude(dft_shift[:,:,0],
                                           dft_shift[:,:,1])+1)
result=cv2.magnitude(cv2.idft(np.fft.ifftshift(dft_shift))[:,:,0],
                     cv2.idft(np.fft.ifftshift(dft_shift))[:,:,1])

images=[optimalImg, magnitude_spectrum, result]
imagesTitles=["Input", "DFT", "Output"]

for i in range(len(images)):
    plt.subplot(1, 3, i+1)
    plt.imshow(images[i], cmap="gray")
    plt.title(imagesTitles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
"""
    print(code)


def spdConvCorr():
    code="""
import cv2
import matplotlib.pyplot as plt
import numpy as np
from image_func import apply_convolution, apply_correlation
img=cv2.imread(r"flower.jpg")
#img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

k1=np.ones((3,3), np.float32)/9
c1=apply_convolution(img, k1)

k2=np.array([[0, -1, 0],
             [-1, 5, -1],
             [0, -1, 0]])
c2=apply_correlation(img, k2)

fig, axes=plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(img)
axes[0].axis("off")
axes[0].set_title("Original")

axes[1].imshow(c1)
axes[1].axis("off")
axes[1].set_title("Convolution")
 
axes[2].imshow(c2)
axes[2].axis("off")
axes[2].set_title("Correlation")

plt.tight_layout()
plt.show()
"""
    print(code)


def spdHaar():
    code="""
import cv2
import numpy as np

# Load the image
image = cv2.imread(r"bird.jpg", 0)

# Convert the image to floating-point data type
image_float = np.float32(image)

# Apply the DCT
transformed = cv2.dct(image_float)

# Display the transformed image
cv2.imshow("Transformed Image", transformed)
"""
    print(code)


def spdColorModel():
    code="""
import cv2

# Load the image
image = cv2.imread(r"bird.jpg")

# Convert the image to a different color model
converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the transformed image
cv2.imshow("Converted Image", converted_image)
"""
    print(code)


def spdHistogram():
    code="""
import cv2
from matplotlib import pyplot as plt
img = cv2.imread(r"flower.jpg",0)
hist = cv2.calcHist([img],[0],None,[256],[0,256])
eq = cv2.equalizeHist(img)
cdf = hist.cumsum()
cdfnmhist = cdf * hist.max()/ cdf.max()
histeq = cv2.calcHist([eq],[0],None,[256],[0,256])
cdfeq = histeq.cumsum()
cdfnmhisteq = cdfeq * histeq.max()/ cdf.max()
plt.subplot(221), plt.imshow(img,'gray')
plt.subplot(222), plt.plot(hist), plt.plot(cdfnmhist)
plt.subplot(223), plt.imshow(eq,'gray')
plt.subplot(224), plt.plot(histeq), plt.plot(cdfnmhisteq)
plt.xlim([0,256])
plt.show()
"""
    print(code)


def spdPowerLaw():
    code="""
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Read the image
img = cv2.imread(r"flower.jpg")
# Display the original image
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()
# Define gamma values
gamma_values = [0.1, 0.5, 1.2, 2.2, 5]
# Apply gamma correction and save edited images
for gamma in gamma_values:
    gamma_corrected = np.array(255 * (img / 255) ** gamma, dtype='uint8')
    cv2.imwrite('gamma_transformed' + str(gamma) + '.jpg', gamma_corrected)
    plt.imshow(cv2.cvtColor(gamma_corrected, cv2.COLOR_BGR2RGB))
    plt.show()
"""
    print(code)


def spdLog():
    code="""
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Read the image
img = cv2.imread(r"C:\Users\Aditi\OneDrive\Pictures\IP\flower.jpg")
# Apply log transform
log_transformed = 255 * np.log(1 + img.astype(np.float32)) / np.log(1 + np.max(img))
# Convert the data type
log_transformed = log_transformed.astype(np.uint8)
# Save the output image
cv2.imwrite(r"C:\Users\Aditi\Pictures\IP\flower1.jpg", log_transformed)
# Display the original and log-transformed images
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(log_transformed, cv2.COLOR_BGR2RGB))
plt.title('Log-Transformed Image')
plt.show()
"""
    print(code)