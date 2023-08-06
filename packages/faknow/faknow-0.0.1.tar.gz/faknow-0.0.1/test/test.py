import argparse


def fun(x=None, y=None):
    print(x, y)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument()
    args = parser.parse_args()
    print(args.__dict__)
    fun(**args.__dict__)
