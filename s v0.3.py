from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk , Image
from ToDoDB import tododb
import configparser 
import time
import os

class background():
    def __init__( self ):
        self.wallpaperfn = wallpaperfn
        self.canvas      = Canvas( root , width = int( resx ) , height = int( resy ) )
        self.canvas.place( x = 0 , y = 0 )
        self.text        = self.canvas.create_text( 13 , 0 , text = "" , font = ( "Gill Sans MT" , 60 , "bold" ) , anchor = "nw" , fill = "white" )
        self.image       = None
        print( self.text ) 
    
    def wallpaperplace( self ):
        try:
            wallpaper.configure( image = self.wallpaperfn )

        except:
            img = Image.open( self.wallpaperfn )
            img = img.resize( ( int(resx) , int(resy) ) )
            self.image = ImageTk.PhotoImage( img )
            self.wallpaper = self.canvas.create_image( 0 , 0 , image = self.image , anchor = "nw" )

    def wallpaper( self ):
        self.wallpaper = filedialog.askopenfilename( title = "Open" )
        background.wallpaperplace( self )

    def clock( self ):
        clockt = time.strftime( "%H:%M" )
        self.canvas.itemconfig( self.text , text = clockt )
        print(clockt)
        root.after( 60000 , self.clock )


class todoli():
    def __init__( self ):
        self.canvas = Canvas( root , width = int( int( resx ) * 0.2 ) , height = int( int( resy ) * 0.3 ) , bg = "#FF752F" )
        self.canvas.place( x = int( int( resx ) * 0.8 ) , y = int( int( resy ) * 0.7 ) )
        self.canlist = []
        for k in range( 0 , 10 , 1 ):
            self.canlist.append( self.canvas.create_text( 0 , 18 * k + 2 , text = ""  , font = ( 10 ) , anchor = "nw" ) )
        self.conimg = Image.open( "gear.png" )
        self.conimg = ImageTk.PhotoImage( self.conimg )
        self.conbutton = Button( self.canvas , image = self.conimg , command = todoli.todoconf , borderwidth = 0 )
        self.conbutton.place( x = 249 , y = 206 )
        self.conbutton.bind( "<Enter>"  )
        self.conbutton.bind( "<Leave>"  )
        root.after( 60000 , todoli.addlist(self) )

    def addlist( self ):
        a = tododb.remind()
        k = 0
        n = 0
        for b in a:
            todotext = b[0][1] + " " * 10 + b[0][2] + " " * 10 + str( b[0][4] )
            if len( todotext ) > 43:
                todotext = todotext[:43] + "..."
            self.canvas.itemconfig( self.canlist[k] , text = todotext )
            k += 1

        for s in range( k , 10 , 1 ):
            self.canvas.itemconfig( self.canlist[s] , text = "" )

class todoconf():
    def __init__( self ) :
        self.root = Toplevel()
        self.root.title( "Reminder" )
        self.root.geometry( "600x600" )
        self.thing = []
        s = 0
        for k in tododb.list():
            text = str( k[0] ).ljust( 10 , " " ) + "|" + k[1].ljust( 14 , " " ) + "|" + k[2].ljust( 14 , " " ).title() + k[3].ljust( 10  , " " ) + "|" + str( k[4] ).ljust( 20 , " " )
            self.thing( text )
        self.confroot = Frame( root , height = 500 , width = 595 )
        self.confroot.place( x = 0 , y = 0 )
        self.conflist = Listbox( self.confroot , listvariable = self.thing , width = 500 , height = 400 )
        self.conflist.place( x = 5 , y = 5 )
        
        self.conflist.bind( "<Double-1>" , lambda:todoli.Detail() )

        self.buttons = Button( self.root , text = "asdasfdv" , command = lambda:todoconf.Detail )
        self.buttona = Button( self.root , text = "Add" , command = lambda:todoconf.todoadd() )

        self.buttons.place( x = 0 , y = 0 )
        self.buttona.place( x = 550 , y = 550 )

        self.root.mainloop()

    def Detail():
        i = self.conflist.curselection()
        self.detroot = Toplevel()
        self.detroot.title( "Detail" )
        self.detroot.geometry( "500x200" )
        text = self.conflist.get( self.conflist.curselection() )
        text = int( text.split( sep = "|" )[0] )
        text = tododb.select( text )



cfg = configparser.ConfigParser()

try:
    cfgf = open( "config.ini" , "r" , "UTF-8" )

except:
    wc = open( "config.ini" , "w" , encoding = "UTF-8" )
    wc.close()
    cfg.read( "config.ini" )
    cfg.add_section( "Resolution" )
    cfg.set( "Resolution" , "ResX" , "1366" )
    cfg.set( "Resolution" , "ResY" , "768" )
    cfg.add_section( "WallPaper" )
    cfg.set( "WallPaper" , "WallPaperFN" , "WallPaper.png" )
    cfg.write(open( "config.ini" , "w" ))

else:
    cfg.read( "config.ini" )

for k in cfg.keys():
    globals().update( cfg.items(k) )

root = Tk()
root.title( "PJS" )
root.resizable( width = False , height = False )
root.geometry( resx + "x" + resy + "-0+0" )

root.overrideredirect( False )



bg = background()
bg.wallpaperplace()
bg.clock()



root.mainloop()
