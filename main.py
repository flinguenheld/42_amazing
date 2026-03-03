from config.config_file import ConfigFile


def main():
    print("Hello from amazing!")


if __name__ == "__main__":
    cfg = ConfigFile("config/config.txt")
    my_dict = cfg.parse_file()
    print("hello")
    print(my_dict)
