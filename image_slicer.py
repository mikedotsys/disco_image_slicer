from PIL import Image
import os
import numpy as np


def main():
    # pull image and get dimensions
    cut_mask = 192  # size of overlap between slices
    pre_files = 'E:/slices/pre/'  # images to slice go here
    write_files = 'E:/slices/procT/'  # output slices go here

    file_names = [fileName for fileName in os.listdir(pre_files) if fileName.endswith(".png")]

    for f in file_names:
        print('Start Image >>>' + f)
        input_image = Image.open(os.path.join(pre_files, f))
        width, height = input_image.size

        cord_hz = []
        cord_vt = []

        # set baseline values for coordinate generation based on image size
        print("Width: {} Height: {}".format(width, height))
        if width > height:
            hz_base_unit = 640
            vt_base_unit = 960
            sub_hz_unit = hz_base_unit - cut_mask
            sub_vt_unit = vt_base_unit - cut_mask
            hz_pre_slice = round(width / sub_hz_unit)
            vt_pre_slice = round(height / sub_vt_unit)
        else:
            hz_base_unit = 640
            vt_base_unit = 960
            sub_hz_unit = hz_base_unit - cut_mask
            sub_vt_unit = vt_base_unit - cut_mask
            hz_pre_slice = round(width / sub_hz_unit)
            vt_pre_slice = round(height / sub_vt_unit)

        start_hz = 0
        end_hz = hz_base_unit

        start_vt = 0
        end_vt = vt_base_unit

        hz_slice = 1
        vt_slice = 1

        print('Horizontal slices: ' + str(hz_pre_slice))
        print('Vertical slices: ' + str(vt_pre_slice))

        # plot slices
        # add horizontal slices to list
        while hz_slice <= hz_pre_slice:  # 1 < 10
            # if we are at the end coordinates work backwards from max width for last slice
            if hz_slice == hz_pre_slice or end_hz == width:
                cord_hz.append(width - hz_base_unit)
                cord_hz.append(width)
                break
            # process normally
            elif hz_slice < hz_pre_slice:
                cord_hz.append(start_hz)
                cord_hz.append(end_hz)
                hz_slice = hz_slice + 1
                if start_hz == 0:
                    start_hz = sub_hz_unit
                else:
                    start_hz = end_hz - cut_mask
                end_hz = start_hz + hz_base_unit

        # add vertical slices to list
        while vt_slice <= vt_pre_slice:
            
            # if we are at the end coordinates work backwards from max height for last slice
            if vt_slice == vt_pre_slice or end_vt == width:
                cord_vt.append(height - vt_base_unit)
                cord_vt.append(height)
                break
            # process normally
            elif vt_slice < vt_pre_slice:
                cord_vt.append(start_vt)
                cord_vt.append(end_vt)
                vt_slice = vt_slice + 1
                if start_vt == 0:
                    start_vt = sub_vt_unit
                else:
                    start_vt = end_vt - cut_mask
                end_vt = start_vt + vt_base_unit

        print(cord_hz)
        print(cord_vt)

        ### Create image coordinate grid

        crd_vvct = 0
        crd_hvct = None
        coordinate = []

        while crd_vvct < len(cord_vt):

            if crd_hvct is None:
                crd_hvct = 0
            elif crd_vvct % 2 == 0:
                crd_hvct = 0

            while crd_hvct < len(cord_hz):
                k = crd_hvct + 1
                l = crd_vvct + 1
                coordinate.append(
                    str(cord_hz[crd_hvct]) + ', ' + str(cord_vt[crd_vvct]) + ', ' + str(cord_hz[k]) + ', ' + str(
                        cord_vt[l]))
                crd_hvct = crd_hvct + 2
            crd_vvct = crd_vvct + 2

        print_row = 1
        for print_cord in coordinate:
            print(str("'" + print_cord + "', "), end="")
            if print_row % hz_pre_slice == 0:
                print('\r')
            print_row = print_row + 1

        cord_hz.clear()
        cord_vt.clear()

        ### Slice and dice baby ###

        row_num = 1
        slice_num = 0

        for points in coordinate:

            left, upper, right, lower = np.array([points.split(',')], dtype=int).T
            xy_loc = np.concatenate([left, upper, right, lower])
            slices = input_image.crop(xy_loc)

            output_slices = write_files + f.rsplit('.', 1)[0] + '_img_{}-{}.png'.format(row_num, slice_num + 1)

            slices.save(output_slices)
            print("Row: {} Slicing: {}".format(row_num, xy_loc))
            slice_num += 1
            if right == width:
                row_num += 1
        print('<<<Finish Image')
        print('')


if __name__ == "__main__":
    main()
