from dbcore import Dbcore

class Orm:
    def __init__(self,**val):
        self.fields={}
        self.n=val
        self.model=self.__class__.__dict__
        self.modelName=self.__class__.__name__
        self.entityCheck(self.modelName)
    
    def entityCheck(self,var):
        if var == self.modelName:
            if self.verify()>0:
                print "Entity \"" + var + "\" ready to use"
            return 1
        if var == None or var == "":
            print "Entity cannot empty"
            return 0
        else:
            print "Entity \"" + var + "\" not exist in Your model"
            return 0

    def fieldsCheck(self,var):
        if var in self.model.keys():
            return 1
        else:
            print "Fields \"" + var + "\" not exist in model \"" + self.modelName + "\""
            return 0

    def verify(self):
        if len(self.model)>2:
            for x in self.model.keys():
                if x<>'__module__' and x<>'__doc__':
                    if self.fieldsCheck(x)<1:
                        break

                    if self.model[x]==None:
                            self.model[x]=""
                            break

                    print "Field \"%s\" data : \"%s\"" % (x,self.model[x])
                    self.fields[x]=self.model[x]

            if len(self.fields)==len(self.model)-2:
                self.dbcore=Dbcore(self.fields, self.modelName)
            else:
                print "Create entity \"%s\" FAILED" % self.modelName
            return 1
        else:
            print "Please check Your parameters"
            return 0

    def Create(self, **val):
        num=0
        for f in val.keys():
            if self.fieldsCheck(f):
                num+=1
                
        if num==len(val):
            self.dbcore=Dbcore(self.fields, self.modelName)
            return self.dbcore.createTheRow(val)

    def Read(self, **val):
        num=0
        lval=len(val)
        for f in val.keys():
            if f<>'limit':
                if self.fieldsCheck(f):
                    num+=1
            else:
                lval=len(val)-1
                
        if num==lval and num>0:
            self.dbcore=Dbcore(self.fields, self.modelName)
            return self.dbcore.readTheRow(val)

    def Update(self,**val):
        num=0
        lval=len(val)
        for f in val.keys():
            if f<>'search':
                if self.fieldsCheck(f):
                    num+=1     
            else:
                lval=len(val)-1
                
        if num==lval and num>0:
            self.dbcore=Dbcore(self.fields, self.modelName)
            return self.dbcore.updateTheRow(val)

    def Delete(self,**val):
        num=0
        lval=len(val)
        for f in val.keys():
            if self.fieldsCheck(f):
                num+=1
                
        if num==lval and num>0:
            self.dbcore=Dbcore(self.fields, self.modelName)
            return self.dbcore.delTheRow(val)

    def execQuery(self,q):
        if q<>'':
            self.dbcore=Dbcore(self.fields, self.modelName)
            return self.dbcore.execTheQuery(q)
        else:
            return 'No query executed'
