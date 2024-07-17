import logging
import os
import wx

class Skin():
    """A class representing a winamp 2 skin"""
    def __init__(self, path, name):

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug('__init__()')

        self.width = 274

        self.images = {}
        for k in ['MAIN.BMP', 'TITLEBAR.BMP', 'EQMAIN.BMP', 'PLEDIT.BMP', 'CBUTTONS.BMP']:
            self.images[k] = wx.Image(os.path.join(path, name, k), wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        
    def get_main(self) -> wx.Image:
        """Get the main image"""
        return self.images['MAIN.BMP'].GetSubBitmap(wx.Rect(0, 0, self.width, 116))
    
    def get_main_titlebar_active(self) -> wx.Image:
        """Get the main titlebar in active state"""
        return self.images['TITLEBAR.BMP'].GetSubBitmap(wx.Rect(27, 0, self.width, 14))
    
    def get_main_titlebar_shade_active(self) -> wx.Image:
        """Get the main titlebar in shade active state"""
        return self.images['TITLEBAR.BMP'].GetSubBitmap(wx.Rect(27, 30, self.width, 14))
    
    def get_eq(self) -> wx.Image:
        """Get the eq image"""
        return self.images['EQMAIN.BMP'].GetSubBitmap(wx.Rect(0, 0, self.width, 116))
    
    def get_eq_titlebar_active(self) -> wx.Image:
        """Get the eq titlebar in active state"""
        return self.images['EQMAIN.BMP'].GetSubBitmap(wx.Rect(0, 135, self.width, 14))

    def get_pl(self) -> wx.Image:
        """Get the playlsit image"""
        return self.images['PLEDIT.BMP'].GetSubBitmap(wx.Rect(26, 0, 100, 20))
    
    def get_transport_prev(self) -> wx.Image:
        """Get the transport button prev"""
        return self.images['CBUTTONS.BMP'].GetSubBitmap(wx.Rect(0, 0, 22, 17))
    
    def get_transport_play(self) -> wx.Image:
        """Get the transport button play"""
        return self.images['CBUTTONS.BMP'].GetSubBitmap(wx.Rect(23, 0, 22, 17))
    
    def get_transport_pause(self) -> wx.Image:
        """Get the transport button pause"""
        return self.images['CBUTTONS.BMP'].GetSubBitmap(wx.Rect(46, 0, 22, 17))
    
    def get_transport_stop(self) -> wx.Image:
        """Get the transport button stop"""
        return self.images['CBUTTONS.BMP'].GetSubBitmap(wx.Rect(69, 0, 22, 17))
    
    def get_transport_next(self) -> wx.Image:
        """Get the transport button next"""
        return self.images['CBUTTONS.BMP'].GetSubBitmap(wx.Rect(92, 0, 22, 17))

class MpdAmp(wx.Frame):
    """The base MpdAmp window"""
    def __init__(self, has_iconise: bool, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug('__init__()')

        self.has_iconise = has_iconise

    def snap_to(self, other: wx.Frame) -> None:
        snap_distance = 5
        other_pos = other.Position
        other_snap = other_pos + (0, other.Size.y)
        self_pos = self.Position
        if (other_snap.y - self_pos.y) < snap_distance and (other_snap.y - self_pos.y) > -snap_distance:
            self_pos.y = other_snap.y
        if (other_snap.x - self_pos.x) < snap_distance and (other_snap.x - self_pos.x) > -snap_distance:
            self_pos.x = other_snap.x
        self.SetPosition(self_pos)

    def mouse_up(self, event: wx.MouseEvent) -> None:
        self.rel_position = None
        event.Skip()

    def shade(self) -> None:
        self.logger.debug('shade()')

class MpdAmpMain(MpdAmp):
    """The Main MpdAmp window"""
    def __init__(self, *args, **kw):
        MpdAmp.__init__(self, True, *args, **kw)

        self.skin = Skin(os.path.join(os.curdir, 'skins'), 'base-2.91')

        panel = wx.Panel(self, size=(self.skin.width,116))

        main = wx.StaticBitmap(panel, wx.ID_ANY, self.skin.get_main(), size=(self.skin.width,116), pos=(0,0))
        titlebar = wx.StaticBitmap(panel, wx.ID_ANY, self.skin.get_main_titlebar_active(), size=(self.skin.width,14), pos=(0,0))

        prev = wx.StaticBitmap(panel, wx.ID_ANY, self.skin.get_transport_prev(), size=(22, 17), pos=(15, 87))
        play = wx.StaticBitmap(panel, wx.ID_ANY, self.skin.get_transport_play(), size=(22, 17), pos=(38, 87))
        pause = wx.StaticBitmap(panel, wx.ID_ANY, self.skin.get_transport_pause(), size=(22, 17), pos=(61, 87))
        stop = wx.StaticBitmap(panel, wx.ID_ANY, self.skin.get_transport_stop(), size=(22, 17), pos=(84, 87))
        next = wx.StaticBitmap(panel, wx.ID_ANY, self.skin.get_transport_next(), size=(22, 17), pos=(107, 87))

        self.eq = MpdAmpEq(self, self, title='MpdAmpEq', size=(self.skin.width,116), style=wx.NO_BORDER)
        self.pl = MpdAmpPlaylist(self, self, title='MpdAmpPlaylist', size=(self.skin.width,116), style=wx.NO_BORDER)

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
        
    def mouse_motion(self, event: wx.MouseEvent) -> None:
        if event.Dragging():
            #self.logger.debug('Drag position %s' % event.Position)
            main_pos = self.Position+event.Position-self.rel_position
            self.SetPosition(main_pos)
            
            #TODO: only move children if they are connected/touching

            eq_pos = self.Position-self.eq_position
            self.eq.SetPosition(eq_pos)
            
            pl_pos = self.Position-self.pl_position
            self.pl.SetPosition(pl_pos)
        event.Skip()

class MpdAmpEq(MpdAmp):
    """The EQ MpdAmp window"""
    def __init__(self, main, *args, **kw):
        MpdAmp.__init__(self, False, *args, **kw)

        self.main = main

        panel = wx.Panel(self, size=(self.main.skin.width,116))

        main = wx.StaticBitmap(panel, wx.ID_ANY, self.main.skin.get_eq(), size=(self.main.skin.width,116), pos=(0,0))
        titlebar = wx.StaticBitmap(panel, wx.ID_ANY, self.main.skin.get_eq_titlebar_active(), size=(self.main.skin.width,14), pos=(0,0))

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
        
    def mouse_motion(self, event: wx.MouseEvent) -> None:
        if event.Dragging():
            #self.logger.debug('Drag position %s' % event.Position)

            eq_pos = self.Position+event.Position-self.rel_position
            self.SetPosition(eq_pos)

            self.snap_to(self.main)
            
            self.snap_to(self.main.pl)
        event.Skip()

class MpdAmpPlaylist(MpdAmp):
    """The Playlist MpdAmp window"""
    def __init__(self, main, *args, **kw):
        MpdAmp.__init__(self, False, *args, **kw)

        self.main = main

        panel = wx.Panel(self, size=(self.main.skin.width,116))

        main = wx.StaticBitmap(panel, wx.ID_ANY, self.main.skin.get_pl(), size=(100,20), pos=(0,0))
        #titlebar = wx.StaticBitmap(panel, wx.ID_ANY, self.main.skin.get_eq_titlebar_active(), size=(self.main.skin.width,14), pos=(0,0))

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
        
    def mouse_motion(self, event: wx.MouseEvent) -> None:
        if event.Dragging():
            #self.logger.debug('Drag position %s' % event.Position)

            pl_pos = self.Position+event.Position-self.rel_position
            self.SetPosition(pl_pos)

            self.snap_to(self.main)
            
            self.snap_to(self.main.eq)
        event.Skip()

# TODO: abstract common window code
# TODO: window snapping
# TODO: all the skin
# TODO: use buttons or Rect intersects for interaction?
