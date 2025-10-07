#!/usr/bin/env python3

import argparse
import torch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="Path to source .ckpt file")
    parser.add_argument("dst", help="Path to destination .ckpt file")
    args = parser.parse_args()

    obj = torch.load(args.src, map_location="cpu")
    if isinstance(obj, dict) and "state_dict" in obj:
        wrapped = obj
    else:
        wrapped = {"state_dict": obj}

    torch.save(wrapped, args.dst)
    print(f"Wrote wrapped checkpoint to {args.dst}")


if __name__ == "__main__":
    main()




