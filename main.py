import argparse
import ic_env

def main():
    iset = ic_env.settings() # "iset" is a dictionary
    src_dir_path = iset["src_dir_path"]
    dst_dir_path = iset["dst_dir_path"]
    incoming_version = iset["version"]

    parser = argparse.ArgumentParser(prog='incoming')
    parser.add_argument("-s", "--src_dir_path", help="Source directory path", action="store")
    parser.add_argument("-d", "--dst_dir_path", help="Destination directory path", action="store")
    parser.add_argument("-e", "--user_ext", help="Extention list", action="store")
    parser.add_argument("-v", "--version", help="Version", action="version", version=incoming_version)
    args = parser.parse_args()

    
    if (args.src_dir_path != None and args.dst_dir_path != None):
        print(args(src_dir_path))
        print(args(dst_dir_path))

        if (args.user_ext != None):
            print(args.user_ext)
    else:
        print("preset use")

if __name__ == "__main__":
    main()