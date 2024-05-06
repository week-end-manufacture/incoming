

def main():
    settings = load_settings()
    src_path = settings.get('src_path')
    dst_path = settings.get('dst_path')

    print("IncomingDir")
    if src_path == dst_path:
        print("src_path와 dst_path는 같을 수 없습니다.")
        return

if __name__ == "__main__":
    main()