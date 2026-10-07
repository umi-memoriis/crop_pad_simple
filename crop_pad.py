import argparse
from PIL import Image
import numpy as np

parser = argparse.ArgumentParser(description="Simple script to pad or crop an image")
parser.add_argument("input_file", help="the input image name")
parser.add_argument("output_file", help="the output image name")
parser.add_argument("output_size_x", help="the size of the image to output along the x axis")
parser.add_argument("output_size_y", help="the size of the image to output along the y axis")
parser.add_argument("rel_point_id", help="the location of the relative point. 1=tl, 2=bl, 3=br, 4=tr, 0=center")


def main():
    args = parser.parse_args()
    in_arr = np.array(Image.open(args.input_file))
    rp = int(args.rel_point_id)
    out_arr = np.zeros((int(args.output_size_y), int(args.output_size_x), in_arr.shape[2]), dtype=np.uint8)
    copy_dim = [min(in_arr.shape[0],out_arr.shape[0]),min(in_arr.shape[1],out_arr.shape[1]),in_arr.shape[2]]
    match rp:
        case 1:
            out_arr[:copy_dim[0],:copy_dim[1],:copy_dim[2]]=in_arr[:copy_dim[0],:copy_dim[1],:copy_dim[2]]
        case 2:
            out_arr[-copy_dim[0]:,:copy_dim[1],:copy_dim[2]]=in_arr[-copy_dim[0]:,:copy_dim[1],:copy_dim[2]]
        case 3:
            out_arr[-copy_dim[0]:,-copy_dim[1]:,:copy_dim[2]]=in_arr[-copy_dim[0]:,-copy_dim[1]:,:copy_dim[2]]
        case 4:
            out_arr[:copy_dim[0],-copy_dim[1]:,:copy_dim[2]]=in_arr[:copy_dim[0],-copy_dim[1]:,:copy_dim[2]]
        case 0:
            out_y = (out_arr.shape[0] - copy_dim[0]) // 2
            out_x = (out_arr.shape[1] - copy_dim[1]) // 2

            in_y = (in_arr.shape[0] - copy_dim[0]) // 2
            in_x = (in_arr.shape[1] - copy_dim[1]) // 2
            out_arr[out_y:out_y + copy_dim[0],out_x:out_x + copy_dim[1],:copy_dim[2]] = in_arr[in_y:in_y + copy_dim[0],in_x:in_x + copy_dim[1],:copy_dim[2]]
        case _:
            print("relative point id is not a valid id")
            return -1
    Image.fromarray(out_arr).save(args.output_file)


if __name__=="__main__":
    main()