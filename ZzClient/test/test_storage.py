from ZzClient.common.util.storage import LocalStorage

if __name__ == '__main__':
    print(LocalStorage.themeGet())
    print(LocalStorage.themeSet('dark'))