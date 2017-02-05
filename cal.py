'''FOR calendar'''
import sqlite3
import datetime
from Titem import *

class Cal(object):
    def __init__(self):
        self.Titems = []
        self.sync = False
        self.conn = sqlite3.connect('tasks.sqlite')
        self.create_table_sql()


    def add_Titems(self, titem,real=0):
        '''insert a item to sql'''
        newt = titem.get_all()
        cu0 =  self.conn.cursor()
        result = (self.find_max_id(),)
        result2 = (self.find_max_id(1),)
        if real == 0:
            save_sql = "INSERT INTO calendar values (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            result = result + newt
        else:
            save_sql = "INSERT INTO real_calendar values (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            result = result2 + newt
        
        print(result)
        cu0.execute(save_sql, result)
        self.conn.commit()
        cu0.close()

    def find_max_id(self,real=0):
        '''get max id in two different table'''
        cu0 = self.conn.cursor()
        if real == 0:
            find_max_index = "SELECT MAX(cal_id) FROM calendar"
        else:
            find_max_index = "SELECT MAX(cal_id) FROM real_calendar"
        try:
            cu0.execute(find_max_index)
            result = int(cu0.fetchone()[0])
        except:
            result = -1
        cu0.close()
        return result+1

    def fetch_cal_id(self, titem):
        '''get cal_id'''
        sql = "SELECT cal_id from calendar WHERE name = ? and start_day = ? and start_time = ?"
        cu0 = self.conn.cursor()
        data = titem.get_all()
        data = (data[0], data[1], data[3])
        cu0.execute(sql, data)
        result = cu0.fetchone()
        return result

    def update_efficience(self, titem, eff,real_titem=-1):
        '''update cal'''
        update_sql = "UPDATE calendar SET efficient = ? WHERE cal_id = ?"
        print(titem.get_name())
        data = (eff, self.fetch_cal_id(titem)[0])
        if real_titem != -1:
            self.add_Titems(real_titem, 1)
        cu0 = self.conn.cursor()
        cu0.execute(update_sql, data)
        self.conn.commit()
        cu0.close()

    def create_table_sql(self):
        '''create sql table'''
        create_table_sql = "CREATE TABLE IF NOT EXISTS calendar( \
                          `cal_id` int(11) NOT NULL,\
                          `name` varchar(100) NOT NULL,\
                          `start_day` varchar(20) DEFAULT NULL,\
                          `end_day` varchar(20) DEFAULT NULL,\
                          `start_time` varchar(20) DEFAULT NULL,\
                          `end_time` varchar(20) DEFAULT 0,\
                          `efficient` int(5) DEFAULT 0,\
                           `type` varchar(20) DEFAULT 0,\
                           `Deatil_type` varchar(20) DEFAULT 0,\
                          PRIMARY KEY (`cal_id`))"
        create_table_sql2 = "CREATE TABLE IF NOT EXISTS real_calendar( \
                          `cal_id` int(11) NOT NULL,\
                          `name` varchar(100) NOT NULL,\
                          `start_day` varchar(20) DEFAULT NULL,\
                          `end_day` varchar(20) DEFAULT NULL,\
                          `start_time` varchar(20) DEFAULT NULL,\
                          `end_time` varchar(20) DEFAULT 0,\
                          `efficient` int(5) DEFAULT 0,\
                           `type` varchar(20) DEFAULT 0,\
                           `Deatil_type` varchar(20) DEFAULT 0,\
                          PRIMARY KEY (`cal_id`))"
        cu = self.conn.cursor()
        cu.execute(create_table_sql)
        self.conn.commit()
        cu.execute(create_table_sql2)
        self.conn.commit()
        cu.close()


    def creat_new_day(self,day):
        '''create a day'''
        Y = day.year
        M = day.month
        D = day.day
        for i in range(8,23):
            thing1 = input(str(i)+":00 : ")
            thing2 = input(str(i)+":30 : ")
            tit1 = Titem(thing1)
            tit2 = Titem(thing2)
            tit1.start_time = datetime.datetime(Y, M, D, i, 0, 0)
            tit1.end_time = datetime.datetime(Y, M, D, i, 30, 0)
            tit2.start_time = datetime.datetime(Y, M, D, i, 30, 0)
            tit2.end_time = datetime.datetime(Y, M, D, i+1, 0, 0)
            self.add_Titems(tit1)
            if tit1.get_name() == tit2.get_name():
                tit1.combine(tit2)
            else:
                self.add_Titems(tit2)




    def add_all_Titems(self, day0):
        '''add all to '''
        sql = "Select * from calendar where start_day= ?"
        cu0 = self.conn.cursor()
        cu0.execute(sql, (day0,))
        result = cu0.fetchall()
        self.Titems.clear()
        for titem in result:
            titem = from_tuple_t(titem)
            self.Titems.append(titem)
        cu0.close()

    def print_all(self):
        '''print all'''
        print("--------------------")
        for one in self.Titems:
            print("%s-%s %s"%(one.start_time.strftime("%H:%M"), one.end_time.strftime("%H:%M"), one.get_name()))
            eff = input("efficient?")
            self.update_efficience(one, eff)
        print("---------------------")

    def write_to_csv(self, day0):
        '''write 2 csv file'''
        file = day0+".csv"
        self.add_all_Titems(day0)
        f = open(file,"w+", encoding="utf-8")
        f.write("Subject, Start Date, Start Time, End Date, End Time\n")
        for one in self.Titems:
            tup = one.get_all()
            str1 = '{0}, {1}, {2}, {3}, {4}'.format(tup[0], tup[1], tup[3], tup[2], tup[4])
            f.write(str1+"\n")
        f.close()


if __name__ == '__main__':
    AA = Cal()
    newday = datetime.datetime.now().date()+datetime.timedelta(days=1)
    #AA.add_all_Titems("2017-01-25")    
    #AA.print_all()
    #AA.creat_new_day(newday)
    AA.write_to_csv("2017-01-26")