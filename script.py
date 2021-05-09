import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dataset', type=float, default=0)
    parser.add_argument('--output_dir', type=float, default=.3)
    
    args = parser.parse_args()