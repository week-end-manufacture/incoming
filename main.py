import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src_dir_path", help="Source directory path", action="store")
    parser.add_argument("-d", "--dst_dir_path", help="Destination directory path", action="store")
    parser.add_argument("-e", "--user_ext", help="Extention list", action="store")
    args = parser.parse_args()

    
    if (args.src_dir_path != None and args.dst_dir_path != None):
        print(args.src_dir_path)
        print(args.dst_dir_path)

    #settings = load_settings()
    #src_path = settings.get('src_path')
    #dst_path = settings.get('dst_path')

    print("IncomingDir")
    #if src_path == dst_path:
    #    print("src_path와 dst_path는 같을 수 없습니다.")
    #    return

if __name__ == "__main__":
    main()