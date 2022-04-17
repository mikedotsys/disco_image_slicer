from PIL import Image
import numpy as np


def main():

    n = 0
    r = 0

    image = 'AutumnTower.png'
    input_image = Image.open(image)

    # Assumes image resolution of 3840x2304 (1280x768 upscale 3 times)
    coordinates = ["0,0,960,896", "832,0,1984,896", "1856,0,3008,896", "2880,0,3840,896", "0,704,960,1600",
                   "832,704,1984,1600", "1856,704,3008,1600", "2880,704,3840,1600", "0,1408,960,2304",
                   "832,1408,1984,2304", "1856,1408,3008,2304", "2880,1408,3840,2304"]

    for cord in coordinates:

        left, upper, right, lower = np.array([cord.split(',')], dtype=int).T
        xy_loc = np.concatenate([left, upper, right, lower])
        slices = input_image.crop((xy_loc))

        if n % 4 == 0:
            r += 1

        output_slices = 'AutumnTower_slice_img_{}-{}.png'.format(r, n + 1)

        slices.save(output_slices)
        print("Slicing: {}".format(xy_loc))
        n += 1


if __name__ == "__main__":
    main()
