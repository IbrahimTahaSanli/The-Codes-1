from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk , Image
from ToDoDB import tododb
import configparser as cfg
import time
import os


cfg = cfg.ConfigParser()

try :
    cfgf = open( "config.ini" , "w" , "UTF-8" )

except :
    wc = open( "config.cfg" , "w" , encoding = "UTF-8" )
    wc.close()
    cfg.read( "config.ini" )
    cfg.add_section( "Resolution" )
    cfg.set( "Resolution" , "ResX" , "1366" )
    cfg.set( "Resolution" , "ResY" , "768" )  
    cfg.add_section( "WallPaper" )
    cfg.set( "WallPaper" , "WallPaperFN" , "WallPaper.png" )
    cfg.write(open( "config.cfg" , "w" ))

else :
    cfg.read( "config.ini" )

for k in cfg.keys():
    globals().update( cfg.items(k) )


maW = Tk()
maW.title( "PJS" )
maW.resizable( width = False , height = False )
maW.geometry( resx + "x" + resy )

maW.overrideredirect(False)

def clocks():

    global clockt
    clockt = time.strftime( "%H:%M" )
    wallpapercanvas.itemconfig( clocktd , text = clockt )
    maW.after( 60000 , clocks )
    
    return clockt


def wallpaperfl(key):

    global wall
    if key == "change" :
        wall = filedialog.askopenfilename( title = "Open" )

    elif key == "get" :
        try :
            os.path.isfile(wallpaperfn)
        
        except :
            drawwallpaper("change")
        
        else :
            wall = wallpaperfn
        
    return wall


def drawwallpaper(key):
    
    global img 
    img = Image.open( wallpaperfl(key) )
    img = img.resize( ( int( resx ) , int( resy ) ) )
    img = ImageTk.PhotoImage( img )
    wallpapercanvas.create_image( 0 , 0 , image = img , anchor = "nw" )
    
    return 



class todoli():
    def __init__(self):
        global todocanvas , todocanlist , todoconimg , todoconbut
        todocanvas = Canvas( maW , width = int( int( resx ) * 0.2 ) , height = int( int( resy ) * 0.3 ) , bg = "#FF752F" )
        todocanvas.place( x = int( int( resx) * 0.8 ) , y = int( int( resy ) * 0.7 ) )
        todocanlist = []
        for k in range( 0 , 10 , 1 ) :
            todocanlist.append( todocanvas.create_text( 0 , 18 * k + 2 , text = "" , font = ( 10 ) , anchor = "nw" ) )    
        todoconimg = Image.open( "gear.png" )
        todoconimg = ImageTk.PhotoImage( todoconimg )
        todoconbut = Button( todocanvas , image = img , command = lambda:todoli.todoconf() , borderwidth = 0 )
        todoconbut.place( x = 249 , y = 206 )
        todoconbut.config( relief = SUNKEN )        
        todoconbut.bind( "<Enter>" , todoli.animaen )
        todoconbut.bind( "<Leave>" , todoli.animale )
        maW.after( 60000 , todoli.addlist )

    def animaen( event ):
        x = 249
        y = 206
        global todoconbut 
        for k in range( 0 , 25 , 1):
            todoconbut.place( x = x - k , y = y - k )
            time.sleep( 0.015 )
            todocanvas.update()

    def animale( event ):
        x = 224
        y = 181
        global todoconbut
        for k in range( 0 , 25 , 1 ):
            todoconbut.place( x = x + k , y = y + k )
            time.sleep( 0.015 )
            todocanvas.update()
        
    def addlist():
        a = tododb.remind()
        k = 0
        n = 0
        for b in a :
            todotext = b[0][1] + " " * 10 + b[0][2] + " " * 10 + str( b[0][4] ) 
            if len( todotext ) > 43 :
                todotext = todotext[:43] + "..."
            todocanvas.itemconfig( todocanlist[k] , text = todotext)
            k += 1
        for s in range( k , 10 , 1 ):
            todocanvas.itemconfig( todocanlist[s] , text = "" )

    def todoconf():
        global todoconlis , todomaW , things , todoconfmaW
        todomaW = Toplevel()
        todomaW.title( "Reminder" )
        todomaW.geometry( "600x600" )
        things = []
        s = 0
        for k in tododb.list():
            text = str( k[0] ).ljust( 10 , " " ) + "|" + k[1].ljust( 14 , " " ) + "|" + k[2].ljust( 14 , " " ).title() + "|" + k[3].ljust( 10 , " " ) + "|" + str( k[4] ).ljust( 20 , " " )
            things.append( text )

        things = StringVar( value = things )
        todoconfmaW = Frame( todomaW , height = 500 , width = 595 )
        todoconfmaW.place( x = 0 , y = 0 )
        todoconlis = Listbox( todoconfmaW , listvariable = things , width = 500 , height = 400)
        todoconlis.place( x = 5 , y = 5)
        
        todoconlis.bind( "<Double-1>" , lambda:todoli.Detail() )
        

        s = Button( todomaW , text = "asjılpd" , command = lambda:todoli.Detail() )
        s.place( x = 0 , y = 0 )

        a = Button( todomaW , text = "Add" , command = lambda:todoli.todoadd() )
        a.place( x = 550 , y = 550 )


        todomaW.mainloop()
        
    def Detail():
        global things , todoconlis , tododet
        i = todoconlis.curselection() 
        tododet = Toplevel()
        tododet.title( "Detail" )
        tododet.geometry( "500x200" )
        text = todoconlis.get( todoconlis.curselection() )
        text = int( text.split( sep = "|" )[0] )
        text = tododb.select( text )

        no = Label( tododet , text = "No: " + str( text[0][0] ) )
        ti = Label( tododet , text = "Time: " + text[0][1] )
        da = Label( tododet , text = "Date: " + text[0][2] )
        re = Label( tododet , text = "Reminder: " + text[0][3] )
        th = Label( tododet , text = "Thing: " + str( text[0][4] ) )
        ta = Label( tododet , text = "ThingAd: " +  str( text[0][5] ) )

        no.grid( column = 1 , row = 1 )
        ti.grid( column = 3 , row = 1 )
        da.grid( column = 5 , row = 1 )
        re.grid( column = 1 , row = 2 )
        th.grid( column = 1 , row = 3 )
        ta.grid( column = 1 , row = 4 )


        dbutton = Button( tododet , text = "Delete" , command = lambda:todoli.dele( text ) )
        ubutton = Button( tododet , text = "Update" , command = lambda:todoli.todoup( text ) )   

        dbutton.grid( column = 2 , row = 5 )
        ubutton.grid( column = 4 , row = 5 )


        tododet.mainloop()

    def todoadd():
        todoaddW  = Toplevel()
        todoaddW.title( "Add" )
        todoaddW.geometry( "500x200" )
        recomboxl = [ "None" , "Month" , "Week" , "Day" , "Hour" ]

        Time     = Label( todoaddW , text = "Time: " )
        Date     = Label( todoaddW , text = "Date: " )
        Reminder = Label( todoaddW , text = "Reminder: " )
        Thing    = Label( todoaddW , text = "Thing: " )
        ThingAd  = Label( todoaddW , text = "ThingAd: " )

        global TimeEn1 , TimeEn2 , DateEn1 , DateEn2 , DateEn3 , Recombox , ThingEn , ThingAnE
        TimeEn1  = Entry( todoaddW , width = 2 )
        TimeEn2  = Entry( todoaddW , width = 2 )
        DateEn1  = Entry( todoaddW , width = 2 )
        DateEn2  = Entry( todoaddW , width = 2 )
        DateEn3  = Entry( todoaddW , width = 2 )
        Recombox = ttk.Combobox( todoaddW , values = recomboxl )
        ThingEn  = Entry( todoaddW , width = 10 )
        ThingAnE = Entry( todoaddW , width = 20 )

        Time.grid( column = 1 , row = 1 )
        Date.grid( column = 1 , row = 2 )
        Reminder.grid( column = 1 , row = 3 )
        Thing.grid( column = 1 , row = 4 )
        ThingAd.grid( column = 1 , row = 5 )

        TimeEn1.grid( column = 3 , row = 1 )
        TimeEn2.grid( column = 4 , row = 1 )
        DateEn1.grid( column = 3 , row = 2 )
        DateEn2.grid( column = 4 , row = 2 )
        DateEn3.grid( column = 5 , row = 2 )
        Recombox.grid( column = 3 , row = 3 )
        ThingEn.grid( column = 3 , row = 4 )
        ThingAnE.grid( column = 3 , row = 5 )

        k = 0

        def add():
            Time     = str( TimeEn1.get() + ":" + TimeEn2.get() )
            dat      = str( DateEn1.get() + ":" + DateEn2.get() + ":" + DateEn3.get() )
            reminder = Recombox.get()
            thi      = str( ThingEn.get() )
            thiad    = str( ThingAnE.get() )

            if thiad == "":
                thiad = None

            if reminder == "None":
                reminder = None

            global todoconfmaW

            tododb.add( Time , dat , reminder , thi , thiad  )
            todoconfmaW.update()
             
            todoaddW.destroy()

        abutton = Button( todoaddW , text = "Add" , command = lambda:add() )
        abutton.grid( column = 2 , row = 6  )

        todoaddW.mainloop()

    def dele( i ):
        global tododet , todomaW  
        tododb.delete( i )
        tododet.destroy()
        todomaW.update()

    def todoup( i ):
        todoupW = Toplevel()
        todoupW.title( "Update" )
        todoupW.geometry( "500x200" )
        list = [ "Time" , "Date" , "Reminder" , "Thing" , "ThingAd" ]
        text = i
        updatecombo = ttk.Combobox( todoupW , values = list )
        updatecombo.grid( column = 1 , row = 1 )
        updatecombo.bind( "<<ComboboxSelected>>" , lambda:update( updatecombo.get() ) )

        def update( i ):
            if i == "Time":
                lab1 = Label( todoupW , text = "Time( Old ): " + str( text[0][1] ) )
                lab2 = Label( todoupW , text = "Time( New ): " )
                ent1 = Entry( todoupW , width = 2 )
                ent2 = Entry( todoupW , width = 2 )
                ent1.insert( 0 , str( text[0][1] ).split( sep = ":" )[0] )
                ent2.insert( 0 , str( text[0][1] ).split( sep = ":" )[1] )
                lab1.grid( column = 1 , row = 2 )
                lab2.grid( column = 1 , row = 3 )
                ent1.grid( column = 2 , row = 3 )
                ent2.grid( column = 3 , row = 3 )
                text = str( ent1.get() ) + ":" + str( ent2.get() )

            elif i == "Date":
                lab1 = Label( todoupW , text = "Date( Old ): " + str( text[0][2] ) )
                lab2 = Label( todoupW , text = "Date( New ): " )
                ent1 = Entry( todoupW , width = 2 )
                ent2 = Entry( todoupW , width = 2 )
                ent3 = Entry( todoupW , width = 4 )
                ent1.insert( 0 , str( text[0][2] ).split( sep = ":" )[0] )
                ent2.insert( 0 , str( text[0][2] ).split( sep = ":" )[1] )
                ent3.insert( 0 , str( text[0][2] ).split( sep = ":" )[2] )
                lab1.grid( column = 1 , row = 2 )
                lab2.grid( column = 1 , row = 2 )
                ent1.grid( column = 2 , row = 3 )
                ent2.grid( column = 3 , row = 3 )
                ent3.grid( column = 3 , row = 3 )
                text = str( ent1.get() ) + ":" + str( ent2.get() ) + ":" + str( ent3.get() )

            elif i == "Reminder":
                lab1 = Label( todoupW , text = "Reminder( Old ): " + str( text[0][3] ) )
                lab2 = Label( todoupW , text = "Reminder( New ): " )
                lis  = [ "None" , "Month" , "Week" , "Day" , "Hour" ]
                com  = ttk.Combobox( todoupW , values = lis )
                lab1.grid( column = 1 , row = 2 )
                lab2.grid( column = 1 , row = 3 )
                com.grid( column = 2 , row = 3 )
                text = com.get()

            elif i == "Thing":
                lab1 = Label( todoupW , text = "Thing( Old ): " + str( text[0][4] ) )
                lab2 = Label( todoupW , text = "Thing( New ): " )
                ent  = Entry( todoupW )
                ent.insert( 0 , text[0][4] )
                lab1.grid( column = 1 , row = 2 )
                lab2.grid( column = 1 , row = 3 )
                ent.grid( column = 2 , row = 3 )
                text = ent.get()

            else:
                lab1 = Label( todoupW , text = "ThingAd( Old ): " + str( text[0][5]  ) ) 
                lab2 = Label( todoupW , text = "ThingAd( New ): " )
                ent  = Entry( todoupW )
                ent.insert( 0 , text[0][5] )
                lab1.grid( column = 1 , row = 2 )
                lab2.grid( column = 1 , row = 3 )
                ent.grid( column = 2 , row = 3 )
                text = ent.get()

            ubutton = Button( todoupW , text = "Update" , command = lambda:up( updatecombo.get() ) )
            ubutton.grid( column = 3 , row = 3 )


        def up():
            pass

        

        todoupW.mainloop()




wallpapercanvas =  Canvas( maW , width = int( resx ) , height = int( resy ) )
wallpapercanvas.place( x = 0 , y = 0 )


global clocktd

clocktd = wallpapercanvas.create_text( 13 , 0 , text = "0" , font = ( "Gill Sans MT" , 60 , "bold" ) , anchor = "nw" , fill = "white" ) 



clocks()
drawwallpaper("get")
tododb()
todoli()
todoli.addlist()
wallpapercanvas.tag_raise(clocktd)


maW.mainloop()
