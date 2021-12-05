class tododb():

    def __init__(self):

        import sqlite3
        import time 

        
        global cur , time
        connect = sqlite3.connect("ToDoDb.db")
        cur = connect.cursor()

        try:
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE ToDo( No INTEGER PRIMARY KEY AUTOINCREMENT , Time STRING , Date STRING , Reminder STRING , Thing STRING )")
            cur.execute("CREATE TABLE ToDoAd( No INTEGER PRIMARY KEY AUTOINCREMENT, ThingAd STRING , Time STRING , Date STRING )")
            print("New Table Created!")

        except:
            print("Connected To DB!")
            pass

    def add( Time , Date , Reminder  , Thing , ThingAd = None ):
        cur.execute( "INSERT INTO ToDoAd( Time , Date , ThingAd) VALUES( ? , ? , ?  )" , (Time , Date , ThingAd) )

        date = tododb.day( Date )
        time = tododb.min( Time )

        cur.execute("INSERT INTO ToDo( Time , Date , Reminder , Thing ) VALUES( ? , ? , ? , ? )" , ( time , date , Reminder , Thing ) )
        cur.execute("commit")


    def delete( no ):
        k = cur.execute("SELECT * From ToDo WHERE No = ?" , ( no , ) )
        cur.execute("DELETE FROM ToDoAd WHERE No = ? " , ( no , )) 
        cur.execute("DELETE FROM ToDo WHERE No = ?  " , ( no  , ) )
        cur.execute("commit")
        return k

    def update( No , Col , Thi ):
        if Col == "Date":
            cur.execute("UPDATE ToDoAd SET Date = ? WHERE No = ? " , ( Thi , No ))
            cur.execute("UPDATE ToDo SET Date = ? WHERE No = ? " , ( tododb.day( Thi ) , No ))

        elif Col == "Time":
            cur.execute("UPDATE ToDoAd SET Time = ? WHERE No = ? " , ( Thi , No ))
            cur.execute("UPDATE ToDo SET Time = ? WHERE No = ? " , ( tododb.min( Thi ) , No ))

        elif Col == "Reminder" :
            cur.execute("UPDATE ToDo SET Reminder = ? WHERE No = ? " , ( Thi , No ))

        elif Col == "Thing":
            cur.execute("UPDATE ToDo SET Thing = ? WHERE No = ? " , ( Thi , No ))

        elif Col == "ThingAd":
            cur.execute("UPDATE ToDoAd SET ThingAd = ? WHERE No = ? " , ( Thi  , No ))

        cur.execute("commit")
        

    def list():
        cur.execute("SELECT ToDo.No , ToDoAd.Time , ToDoAd.Date , ToDo.Reminder , ToDo.Thing , ToDoAd.ThingAd FROM ToDo , ToDoAd WHERE ToDo.No = ToDoAd.No") 
        return cur.fetchall()

    def remind(  ):
        "liste( No , Time , Date , Reminder , Thing , ThingAd )"
        nowdate = time.strftime("%d:%m:%Y")
        nowtime = time.strftime("%X")
        rem = []
        l   = []

        nowdate = tododb.day( nowdate )
        nowtime = tododb.min( nowtime )

        cur.execute("SELECT * FROM ToDo")
        for k in cur.fetchall():
            if k[3] != "None" :
                
                if k[3].lower() == "month" :
                    if -7 < k[2] - nowdate < 30 :
                        rem.append( k[0] )
                elif k[3].lower() == "week" :
                    if -7 < k[2] - nowdate < 7 :
                        rem.append( k[0] )
                elif k[3].lower() == "day" :
                    if -7 < k[2] - nowdate < 1 :
                        rem.append( k[0] )
                else :
                    if -7 < k[2] - nowdate < 1 :
                        if k[1] - nowtime < 10 :
                            rem.append( k[0] )

        for k in rem:
            cur.execute("SELECT ToDo.No , ToDoAd.Time , ToDoAd.Date , ToDo.Reminder , ToDo.Thing , ToDoAd.ThingAd FROM ToDo , ToDoAd WHERE ToDo.No = ? AND ToDo.No = ToDoAd.No" , ( k ,))
            l.append( cur.fetchall() )

        return l

    def day( Text ):
        Text  = Text.split( sep = ":")
        date  = 0
        date += int( ( int( Text[2]) - 1 ) * 365.6 )
        date += int( Text[1] ) * 30
        date += int( Text[0] )
        return date
    
    
    def min( Text ):
        Text  = Text.split( sep = ":" )
        time  = 0
        time += int( Text[1] )
        time += int( Text[0] ) * 60
        return time

    def select( k ):
        cur.execute("SELECT ToDo.No , ToDoAd.Time , ToDoAd.Date , ToDo.Reminder , ToDo.Thing , ToDoAd.ThingAd FROM ToDo , ToDoAd WHERE ToDo.No = ? AND ToDo.No = ToDoAd.No" , ( k ,))
        return cur.fetchall()
