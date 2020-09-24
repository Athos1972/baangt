from gevent import monkey
monkey.patch_all()
from baangt.base.CliAndInteractive import run
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()
    run()