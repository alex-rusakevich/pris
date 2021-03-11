import pris.gui as pg
import pris, os, sys

if __name__ == "__main__":
    gui = pg.GUI("Pris screenshot helper v"+pris.VERSION, 
        os.path.dirname(os.path.realpath(sys.argv[0])))
    gui.start()
