from config.config_parser import ConfigParser


def main():
    print("Hello from amazing!")


if __name__ == "__main__":
    cfg = ConfigParser("config.txt")
    my_dict = cfg.parse_file()
    print("hello")
    print(my_dict)
