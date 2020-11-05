

if __name__ == '__main__':
    # 1).exec
    # exec('from ZzClient.config.const import Config')
    # print(Config().img_path)

    # 2).importlib
    import importlib
    module_name = "ZzClient.config.const"
    class_name = "Config"

    module_object = importlib.import_module(module_name) # 将模块加载为对象
    module_class = getattr(module_object, class_name)
    print(module_class.img_path)
