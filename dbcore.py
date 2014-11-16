from dbconf import Dbconf

class Dbcore(Dbconf):
    def __init__(self, fields, entity):
        self.dconf=Dbconf().__dict__
        self.thefields=fields
        self.theentity=entity
        self.mod=''
        self.dbtype={}
        self.dbSetup()

    def dbSetup(self):
        self.dbtype={
            'mysql':['MySQLdb',self.entitySetup]
            }
            
        if self.dbtype.has_key(self.dconf['database']['dbtype']):
            self.mod=__import__(self.dbtype[self.dconf['database']["dbtype"]][0],globals(),locals(),[],-1)
            self.dbtype[self.dconf['database']['dbtype']][1](self.dconf['database']['dbtype'])
        else:
            print "Database type not supported"

    def dbConn(self):
        return self.mod.connect(user=self.dconf['database']['user'],
                                passwd=self.dconf['database']['passw'],
                                db=self.dconf['database']['dbname'],
                                host=self.dconf['database']['dbhost'],
                                port=self.dconf['database']['port'],
                                #ssl=self.dconf['database']['ssl'],
                                #connect_timeout=self.dconf['database']['connect_timeout'],

                                #THIS IS ADDITIONAL OPTIONS FOR MYSQL
                                #unix_socket=self.dconf['database']['unix_socket'],
                                #conv=self.dconf['database']['conv'],
                                #compress=self.dconf['database']['compress'],
                                #named_pipe=self.dconf['database']['named_pipe'],
                                #init_command=self.dconf['database']['init_command'],
                                #read_default_file=self.dconf['database']['read_default_file'],
                                #read_default_group=self.dconf['database']['read_default_group'],
                                #cursorclass=self.dconf['database']['cursorclass'],
                                #unicode=self.dconf['database']['unicode']
                                )

    def entitySetup(self,mydb):
        fieldtype={
            'mysql':
                   {
                       'chr':'CHAR',
                       'str':'VARCHAR',
                       'ttext':'TINYTEXT',
                       'text':'TEXT',
                       'mtext':'MEDIUMTEXT',
                       'ltext':'LONGTEXT',
                       'int':'INT',
                       'tint':'TINYINT',
                       'sint':'SMALLINT',
                       'mint':'MEDIUMINT',
                       'bint':'BIGINT',
                       'bit':'BIT',
                       'float':'FLOAT',
                       'dbl':'DOUBLE',
                       'dec':'DECIMAL',
                       'blob':'BLOB',
                       'date':'DATE',
                       'time':'TIME',
                       'year':'YEAR',
                       'dtime':'DATETIME',
                       'tstamp':'TIMESTAMP',
                       'enum':'ENUM'
                       }
            }
        
        if fieldtype.has_key(mydb):
            self.createEntity(fieldtype[mydb])

    def createEntity(self,myfields):
        d=self.thefields
        fl=""
        delimit=","
        n=0
        
        for x in d.keys():
            n+=1
            fnull="DEFAULT NULL"
            if n==len(d):
                delimit=""
            if d[x][2]=="not null":
                fnull="NOT NULL"
            if myfields[d[x][0]]=='text':
                fl+="%s %s %s %s" % (x, myfields[d[x][0]], fnull, delimit)
            else:
                fl+="%s %s(%s) %s %s" % (x, myfields[d[x][0]], d[x][1], fnull, delimit)
        db=self.dbConn()
        cursor=db.cursor()
        #print "Fields settings :",fl
        if self.dconf['database']['dbtype']=='mssql':
            cursor.execute("""IF NOT EXISTS
                               (  SELECT [name] 
                                  FROM sys.tables
                                  WHERE [name] = '%s'
                               )
                               CREATE TABLE %s (%s)""" % (self.theentity, self.theentity, fl))
        else:
            cursor.execute("""CREATE TABLE IF NOT EXISTS %s (%s);""" % (self.theentity, fl))

        cursor.close()

        #print "Your entity data :",d

    def createTheRow(self, val):
        fieldname=''
        fieldvalue=''
        num=0
        delimit=','
        if len(val)>0:
            for f in val.keys():
                num+=1
                if num==len(val):
                    delimit=''
                    
                fieldname+=f+delimit
                fieldvalue+="'"+val[f]+"'"+delimit
                
            db=self.dbConn()
            cursor=db.cursor()
            cursor.execute("""insert into %s(%s) values(%s);""" % (self.theentity,fieldname,fieldvalue))
            db.commit()
            affected_row=cursor.rowcount
            if affected_row>0:
                return 'Data added !'
            else:
                return 'Update failed !'
            
            cursor.close()

    def readTheRow(self, val):
        fieldvalue=''
        num=0
        lim=1
        lval=len(val)
        delimit=' and '
        if len(val)>0:
            if 'limit' in val.keys():
                lval=len(val)-1
            for f in val.keys():
                num+=1
                if f=='limit':
                    lim=val[f]
                    num-=1
                
                if num==lval:
                    delimit=''
                
                if f<>'limit':
                    fieldvalue+=f+"='"+str(val[f])+"'"+delimit
                
            db=self.dbConn()
            cursor=db.cursor()
            cursor.execute("""select * from %s where %s;""" % (self.theentity,fieldvalue))
            dt=cursor.fetchmany(lim)
            return dt
            cursor.close()

    def updateTheRow(self,val):
        fieldvalue=''
        search=''
        num=0
        delimit=','
        sdelimit=' and '
        lval=len(val)
        if len(val)>0:
            if 'search' in val.keys():
                lval=len(val)-1
                snum=0
                for s in val['search'].keys():
                    snum+=1
                    if snum==len(val['search']):
                        sdelimit=''
                        
                    search+=s+"='"+val['search'][s]+"'"+sdelimit
                    
            for f in val.keys():
                num+=1
                
                if f=='search':
                    search='where '+search

                if num==lval:
                    delimit=''

                if f<>'search':
                    fieldvalue+=f+"='"+val[f]+"'"+delimit

            db=self.dbConn()
            cursor=db.cursor()
            cursor.execute("""update %s set %s %s;""" % (self.theentity,fieldvalue,search))
            db.commit()
            affected_row=cursor.rowcount
            if affected_row>0:
                return 'Data updated !'
            else:
                return 'Update failed !'
            cursor.close()

    def delTheRow(self,val):
        fieldvalue=''
        num=0
        lval=len(val)
        delimit=' and '
        if len(val)>0:
            for f in val.keys():
                num+=1
                if num==lval:
                    delimit=''
                
                fieldvalue+=f+"='"+str(val[f])+"'"+delimit
                
            db=self.dbConn()
            cursor=db.cursor()
            cursor.execute("""delete from %s where %s;""" % (self.theentity,fieldvalue))
            db.commit()
            affected_row=cursor.rowcount
            if affected_row>0:
                return 'Data deleted !'
            else:
                return 'Update failed !'
            
            cursor.close()

    def execTheQuery(self,q):
        dt=''
        db=self.dbConn()
        cursor=db.cursor()
        cursor.execute(q)
        if q.find('select')>=0:
            dt=cursor.fetchall()
        else:
            db.commit()
            affected_row=cursor.rowcount
            if affected_row>0:
                return 'Query executed !'
            else:
                return 'Query failed !'
        return dt    
        cursor.close()
