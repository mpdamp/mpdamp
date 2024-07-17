import logging
import wx
from amp import MpdAmpMain

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """The main function for MpdAmp"""
    app = wx.App()
    frame = MpdAmpMain(None, title='MpdAmpMain', size=(274,116), style=wx.NO_BORDER)
    frame.SetPosition((100, 100))
    frame.Show()
    frame.eq.SetPosition(frame.Position+(0, 116))
    frame.eq.Show()
    frame.pl.SetPosition(frame.eq.Position+(0, 116))
    frame.pl.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()