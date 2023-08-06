import platform

from testlibraryorsomething.test_functionality import addd


if __name__ == '__main__':
    if platform.system() not in ['Windows']:
        raise OSError(f"Unsupported operating system: {platform.system()}")
