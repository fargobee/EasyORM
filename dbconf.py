class Dbconf:
    def __init__(self):
        ##DO NOT EDIT THIS INIT
        self.database={}
        self.config()

    def config(self):
        self.database["dbtype"]="mysql"
        self.database["user"]="root"
        self.database["passw"]="root"
        self.database["dbname"]="test"
        self.database["dbhost"]="localhost"
        self.database["port"]=3306
        self.database["ssl"]={
            "ssl_ca":"/path/to/ssl/cert/auth",
            "ssl_cert":"/path/to/ssl/cert",
            "ssl_key":"/path/to/ssl/key"}
        self.database["connect_timeout"]=60

        #THIS IS ADDITIONAL OPTIONS FOR MYSQL
        #self.database["unix_socket"]=""
        #self.database["conv"]=""
        #self.database["compress"]=""
        #self.database["named_pipe"]=""
        #self.database["init_command"]=""
        #self.database["read_default_file"]=""
        #self.database["read_default_group"]=""
        #self.database["cursorclass"]=""
        #self.database["unicode"]=
