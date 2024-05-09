import argparse
import env

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src_dir_path", help="Source directory path", action="store")
    parser.add_argument("-d", "--dst_dir_path", help="Destination directory path", action="store")
    parser.add_argument("-e", "--user_ext", help="Extention list", action="store")
    args = parser.parse_args()

    
    if (args.src_dir_path != None and args.dst_dir_path != None):
        print(args(src_dir_path))
        print(args(dst_dir_path))

        if (args.user_ext != None):
            print(args.user_ext)
    else:
        print("preset use")

idset = env.from_jsonc() # "idset" is a dictionary
src_dir_path = idset["src_dir_path"]
dst_dir_path = idset["dst_dir_path"]

if __name__ == "__main__":
    main()