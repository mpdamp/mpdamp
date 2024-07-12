import logging
import os
import wx

logging.basicConfig(level=logging.DEBUG)

class Skin():
    """A class representing a winamp 2 skin"""
    def __init__(self, path, name):

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug('__init__()')

        self.images = {}
        for k in ['MAIN.BMP', 'TITLEBAR.BMP', 'EQMAIN.BMP']:
            self.images[k] = wx.Image(os.path.join(path, name, k), wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        
    def get_main(self) -> wx.Image:
        """Get the main image"""
        return self.images['MAIN.BMP'].GetSubBitmap(wx.Rect(0, 0, 275, 116))
    
    def get_main_titlebar_active(self) -> wx.Image:
        """Get the main titlebar in active state"""
        return self.images['TITLEBAR.BMP'].GetSubBitmap(wx.Rect(27, 0, 275, 14))
    
    def get_main_titlebar_shade_active(self) -> wx.Image:
        """Get the main titlebar in shade active state"""
        return self.images['TITLEBAR.BMP'].GetSubBitmap(wx.Rect(27, 30, 275, 14))
    
    def get_eq(self) -> wx.Image:
        """Get the eq image"""
        return self.images['EQMAIN.BMP'].GetSubBitmap(wx.Rect(0, 0, 275, 116))
    
    def get_eq_titlebar_active(self) -> wx.Image:
        """Get the eq titlebar in active state"""
        return self.images['EQMAIN.BMP'].GetSubBitmap(wx.Rect(0, 135, 275, 14))

class MpdAmpMain(wx.Frame):
    """The Main MpdAmp window"""
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug('__init__()')

        panel = wx.Panel(self, size=(275,116))

        self.skin = Skin(os.path.join(os.curdir, 'skins'), 'base-2.91')

        main = wx.StaticBitmap(panel, wx.ID_ANY, self.skin.get_main(), size=(275,116), pos=(0,0))
        titlebar = wx.StaticBitmap(panel, wx.ID_ANY, self.skin.get_main_titlebar_active(), size=(275,14), pos=(0,0))

        self.eq = MpdAmpEq(self, self, title='MpdAmpEq', size=(275,116), style=wx.NO_BORDER)
        self.pl = MpdAmpPlaylist(self, self, title='MpdAmpPlaylist', size=(275,116), style=wx.NO_BORDER)

        self.rel_position = None
        self.eq_position = None
        self.pl_position = None

        main.Bind(wx.EVT_LEFT_DOWN, self.mouse_down)
        main.Bind(wx.EVT_LEFT_UP, self.mouse_up)
        main.Bind(wx.EVT_MOTION, self.mouse_motion)

    def mouse_down(self, event: wx.MouseEvent) -> None:
        #self.logger.debug('Event position %s' % event.Position)
        #self.logger.debug('Frame position %s' % self.Position)
        mouse_point = wx.Rect(event.Position.x, event.Position.y, 1, 1)
        if wx.Rect(265, 4, 9, 9).Intersects(mouse_point):
            self.Close()
        elif wx.Rect(254, 4, 9, 9).Intersects(mouse_point):
            self.shade()
        elif wx.Rect(245, 4, 9, 9).Intersects(mouse_point):
            self.Iconize()
        else:
            self.rel_position = event.Position
            self.eq_position = self.Position - self.eq.Position
            self.pl_position = self.Position - self.pl.Position
        event.Skip()

    def shade(self) -> None:
        self.logger.debug('shade()')

    def mouse_up(self, event: wx.MouseEvent) -> None:
        self.rel_position = None
        event.Skip()
        
    def mouse_motion(self, event: wx.MouseEvent) -> None:
        if event.Dragging():
            #self.logger.debug('Drag position %s' % event.Position)
            self.SetPosition(self.Position+event.Position-self.rel_position)
            self.eq.SetPosition(self.Position-self.eq_position)
            self.pl.SetPosition(self.Position-self.pl_position)
        event.Skip()

class MpdAmpEq(wx.Frame):
    """The EQ MpdAmp window"""
    def __init__(self, main, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug('__init__()')

        self.main = main

        panel = wx.Panel(self, size=(275,116))

        main = wx.StaticBitmap(panel, wx.ID_ANY, self.main.skin.get_eq(), size=(275,116), pos=(0,0))
        titlebar = wx.StaticBitmap(panel, wx.ID_ANY, self.main.skin.get_eq_titlebar_active(), size=(275,14), pos=(0,0))

        self.rel_position = None

        main.Bind(wx.EVT_LEFT_DOWN, self.mouse_down)
        main.Bind(wx.EVT_LEFT_UP, self.mouse_up)
        main.Bind(wx.EVT_MOTION, self.mouse_motion)

    def mouse_down(self, event: wx.MouseEvent) -> None:
        #self.logger.debug('Event position %s' % event.Position)
        #self.logger.debug('Frame position %s' % self.Position)
        mouse_point = wx.Rect(event.Position.x, event.Position.y, 1, 1)
        if wx.Rect(265, 4, 9, 9).Intersects(mouse_point):
            self.Close()
        elif wx.Rect(254, 4, 9, 9).Intersects(mouse_point):
            self.shade()
        else:
            self.rel_position = event.Position
        event.Skip()

    def shade(self) -> None:
        self.logger.debug('shade()')

    def mouse_up(self, event: wx.MouseEvent) -> None:
        self.rel_position = None
        event.Skip()
        
    def mouse_motion(self, event: wx.MouseEvent) -> None:
        if event.Dragging():
            #self.logger.debug('Drag position %s' % event.Position)
            self.SetPosition(self.Position+event.Position-self.rel_position)
        event.Skip()

class MpdAmpPlaylist(wx.Frame):
    """The Playlist MpdAmp window"""
    def __init__(self, main, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug('__init__()')

        self.main = main

        panel = wx.Panel(self, size=(275,116))

        #main = wx.StaticBitmap(panel, wx.ID_ANY, self.main.skin.get_eq(), size=(275,116), pos=(0,0))
        #titlebar = wx.StaticBitmap(panel, wx.ID_ANY, self.main.skin.get_eq_titlebar_active(), size=(275,14), pos=(0,0))

        self.rel_position = None

        #main.Bind(wx.EVT_LEFT_DOWN, self.mouse_down)
        #main.Bind(wx.EVT_LEFT_UP, self.mouse_up)
        #main.Bind(wx.EVT_MOTION, self.mouse_motion)

    def mouse_down(self, event: wx.MouseEvent) -> None:
        #self.logger.debug('Event position %s' % event.Position)
        #self.logger.debug('Frame position %s' % self.Position)
        mouse_point = wx.Rect(event.Position.x, event.Position.y, 1, 1)
        if wx.Rect(265, 4, 9, 9).Intersects(mouse_point):
            self.Close()
        elif wx.Rect(254, 4, 9, 9).Intersects(mouse_point):
            self.shade()
        else:
            self.rel_position = event.Position
        event.Skip()

    def shade(self) -> None:
        self.logger.debug('shade()')

    def mouse_up(self, event: wx.MouseEvent) -> None:
        self.rel_position = None
        event.Skip()
        
    def mouse_motion(self, event: wx.MouseEvent) -> None:
        if event.Dragging():
            #self.logger.debug('Drag position %s' % event.Position)
            self.SetPosition(self.Position+event.Position-self.rel_position)
        event.Skip()

# TODO: abstract common window code
# TODO: window snapping
# TODO: all the skin
# TODO: use buttons or Rect intersects for interaction?

def main():
    """The main function for MpdAmp"""
    app = wx.App()
    frame = MpdAmpMain(None, title='MpdAmpMain', size=(275,116), style=wx.NO_BORDER)
    frame.SetPosition((100, 100))
    frame.Show()
    frame.eq.SetPosition(frame.Position+(0, 116))
    frame.eq.Show()
    frame.pl.SetPosition(frame.eq.Position+(0, 116))
    frame.pl.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()