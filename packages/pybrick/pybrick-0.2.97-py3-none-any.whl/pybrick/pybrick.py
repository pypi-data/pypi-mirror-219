__version__="0.2.97"
__doc__="""
pybrick uses sqlalchemy to provide a convenient connection to Yellowbrick.
"""
import pdb
import os
import sys
import subprocess
import tempfile
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import PGDialect
import pandas as pd
import socket
import inspect
from io import StringIO

class YbConnector:
    """ A pytezza-esque connector to Yellowbrick. """
    def __init__(self,host,db,user,pw="",psql_compatible_version='13.7',ybhosts=None):
        """ """
        self.orig_host=host
        self.ybhosts=ybhosts
        self.host=self._resolveHost(host,ybhosts)
        self.db=db
        self.user=user
        self.pw=pw if pw else os.environ.get('YBPASSWORD')
        
        self.psql_compatible_version=psql_compatible_version
        self.dry_run_mode=False
        self.engine=None
        self.connection=self.getConnection()
    
    
    def _resolveHost(self,host,ybhosts,check_only=False):
        """ ybhosts may be a dict (with hosts at keys and IPs as values), or a file where
            each line contains a hostname, and then a space, and then the IP.
        """
        #If we resolve the host right away, great.
        try:
            _=socket.getaddrinfo(host,0,0,0,0)
            print("Yellowbrick host found at",host)
            return host
        except socket.gaierror as d:
            if check_only:
                return None
        
        if not ybhosts:
            print("No ybhosts provided.")
            return None
        
        #If DNS resolution fails try ybhosts.
        #If it's a dict, just do a blind get.
        if type(ybhosts)==dict:
            h=ybhosts.get(host)
            return self._resolveHost(h,None,True)
        
        #If it's not a dict, try it as a file.
        try:
            if os.path.isfile(ybhosts):
                ybhosts=self._getHosts(ybhosts)
                h=ybhosts.get(host)
                return self._resolveHost(h,None,True)
        except Exception as e:
            print("Unable to parse ybhosts:",e)
        
        print("Could not resolve Yellowbrick host:",host)
        return None
    
    
    def _getHosts(self,ybhosts):
        """ """
        lu={}
        with open(ybhosts,'r') as h:
            for line in h.readlines():
                line=line.strip()
                if line:
                    hname,ip=line.split(" ")[0:2]
                    lu[hname.strip()]=ip.strip()
        return lu
    
    def __del__(self):
        if hasattr(self,"connection"):
            try:
                self.disconnect()
            except:
                pass
        return
    
    def __repr__(self):
        """ """
        stat="CONNECTED"
        try:
            self.connection.execute(sa.text("select 1"))
        except:
            stat="DISCONNECTED"
            
        return(f"Yellowbrick connector for user {self.user} on host {self.host}.\n{stat}")
    
    def _checkConnection(self,reconnect=False):
        """ When using psycopg2 interactively, it's not unusual for the db
            connection to become invalid due to idle timeout.  Before issuing
            a query, check the connection and optionally reconnect if needed.
        """
        try:
            self.connection.execute(sa.text("select 1"))
        except Exception as e:
            if reconnect:
                self.disconnect()
                self.connection=self.getConnection()
            else:
                raise Exception("Connection problem: %s"%e, sys.exc_info()[2])
    
    def getEngine(self):
        """ """
        self._checkConnection()
        return self.engine
    
    def getConnection(self):
        """ """
        if not self.host:
            raise RuntimeError(f"Failed to reach {self.orig_host}")
        
        psql_vinfo=tuple([int(x) for x in self.psql_compatible_version.split(".")])
        PGDialect._get_server_version_info = lambda *args:psql_vinfo
        
        connection_url = sa.engine.URL.create(
            drivername="postgresql+psycopg2",
            username=self.user,
            password=self.pw,
            host=self.host,
            database=self.db,
        )
        
        try:
            self.engine=sa.create_engine(connection_url,pool_pre_ping=True)
            conn=self.engine.connect().execution_options(isolation_level="AUTOCOMMIT")
            return conn
        except Exception as e:
            raise RuntimeError(f"Error connecting to Yellowbrick:\n{e}")
    
    
    def disconnect(self):
        """ """
        if self.connection:
            self.connection.close()
        return
    
    
    def switchHost(self,newhost):
        """ """
        print(f"Switching Yellowbrick host from {self.host} to {newhost}")
        self.__init__(newhost,
                      self.db,
                      self.user,
                      self.pw,
                      self.psql_compatible_version,
                      ybhosts=self.ybhosts)
        return
    
    
    def query(self,query_to_run,dryRun=False,dumpTo=None,dumpAppend=False,printQuery=False):
        """ Query implies fetch data. """
        return self._query(query_to_run,withData=True,dryRun=dryRun,dumpTo=dumpTo,dumpAppend=dumpAppend,printQuery=printQuery)
    
    
    def execute(self,query_to_run,dryRun=False,dumpTo=None,dumpAppend=False,printQuery=False):
        """ Execute implies don't fetch data. """
        return self._query(query_to_run,withData=False,dryRun=dryRun,dumpTo=dumpTo,dumpAppend=dumpAppend,printQuery=printQuery)
    
    
    def _query(self,query_to_run,withResults=False,withData=False,dryRun=False,dumpTo=None,dumpAppend=False,printQuery=False):
        """ Query Yellowbrick, optionally returning a dataframe of results. """
        self._checkConnection(reconnect=True)
        
        df=None
        if dumpTo:
            mode="a+" if dumpAppend else "w+"
            open(os.path.join(".",dumpTo),mode).write(query_to_run)
        
        if dryRun:
            print("This is a dry run.  Not submitting:\n")
            print(query_to_run)
            return
        
        if printQuery:
            print(query_to_run)
        
        #withResults and withData are identical; phasing out the withResults.
        #In case of a conflict, err on the side of returning data.
        withData=max(withResults,withData)
        
        #Connect and execute, with or without returning results.  If there's a problem
        #print the details, and always close the connection.
        try:
            if withData:
                df=pd.read_sql(sa.text(query_to_run),self.getEngine())
            else:
                self.connection.execute(sa.text(query_to_run))
        except Exception as e:
            raise RuntimeError(f"There was an error while executing the SQL:\n{e}")
        
        return df
    
    
    def tableExists(self,table):
        """ """
        (db,tbl)=table.split(".")
        q=f"""
            select count(*) as rc
            from information_schema.tables
            where upper(table_schema)=upper('{db}')
              and upper(table_name)=upper('{tbl}')
        """
        d=self.query(q)
        return d.rc[0]>0
    
    
    def tableRowCount(self,table):
        """ """
        q=f"""
            select count(*) as rc
            from {table}
        """
        d=self.query(q)
        return d.rc[0]
    
    
    def sample(self,table,fields=None,limit=10,orderby=None):
       """ """
       h="Sample of "+table
       print(h+"\n"+("-"*len(h)))
       return self.query(f"select {fields if fields else '*'} from {table} order by {orderby if orderby else 'random()'} limit {limit}")
    
    
    def getDfDDL(self,src,ybTypes=None):
        """ """
        if not ybTypes:
            #If were weren't supplied types, guess them ourselves.
            ybTypes=self.getYbTypesFromDf(src)
            
        ddl = ""
        for i in range(len(src.columns)):
            #New DDL line for each element.  Trickiness to handle no-comma for last element.
            ddl+='    "%s" %s%s\n'%(src.columns[i],ybTypes[i],(i<len(src.columns)-1)*",")
            
        return ddl
    
    
    def loadBySio(self,src,target):
        """ """
        #Initialize and load a string buffer.
        buf = StringIO()
        sz=buf.write(src.to_csv(index=None,header=True))
        buf.seek(0)
        print("Buffer size in characters:",sz)
        
        if src.size>2000000:
            print('WARNING: You may experience out-of-memory errors when using dfToYb "lite" mode with a dataframe this size.')
        
        #Write the data into Yellowbrick.
        conn = self.engine.raw_connection()
        with conn.cursor() as c:
            c.copy_expert(f"COPY {target} FROM STDIN WITH CSV HEADER",buf)
        conn.commit()
        conn.close()
        
        print(f"Loaded {self.tableRowCount(target)} rows into {target}")
        assert src.shape[0]==self.tableRowCount(target),"Loaded count does not match source count!"
        return
    
    
    def dfToYb(self,src,target,distribute_on="random",clobber=False,ybTypes=None,verbose=False,ignoreLoadErrors=False,lite=False):
        """ Given a pandas df, push that table to yellowbrick, optionally replace the existing table in yellowbrick.
            If ybTypes immutable is provided, use those types and to hell with the consequences.
            Otherwise, infer the types.
        """
        def vprint(s):
            if verbose:
                print(s)
        
        print(f"Loading {src.shape[0]} rows and {src.shape[1]} columns into {target}")
        print(f"Dataframe size is approximately {src.memory_usage().sum()/1024/1024:0.2f} MB.")
        vprint(f"Here is a sample of the source data:\n{src.head(5)}")
        
        #If were weren't supplied types, guess them ourselves.
        if not ybTypes:
            ybTypes=self.getYbTypesFromDf(src)
        
        #Drop the table if we're instructed to clobber.
        if clobber:
            vprint(f"Dropping {target}")
            self.execute(f"drop table if exists {target};")
        
        #Use columns and datatypes to make a create-table statement.
        ddl = f"create table {target} ({self.getDfDDL(src,ybTypes)})"
        
        #Create the empty table if it doesn't exist.
        if not self.tableExists(target):
            self.execute(ddl,printQuery=verbose)
        
        #If lite mode, do it without ybload.
        if lite:
            vprint("Loading via string buffer...")
            self.loadBySio(src,target)
        
        #...otherwise, use the ybload utility.
        else:
            vprint("Loading by ybload...")
            os.environ["YBPASSWORD"]=self.pw
            
            dump=tempfile.mkstemp(".csv")[1]
            vprint(f"Dumping local data to {dump}")
            
            #Pandas changed lineterminator at version 1.5.0.  Use inspect to see which one we need.
            if 'lineterminator' in inspect.signature(pd.DataFrame.to_csv).parameters:
                src.to_csv(dump,index=False,header=True,lineterminator="\n")
            else:
                src.to_csv(dump,index=False,header=True,line_terminator="\n")
            vprint(f"Dumped {os.path.getsize(dump)/1024/1024:0.2f}MB.")
            
            if sys.platform=='win32':
                ybin=r"C:\Program Files\Yellowbrick Data\Client Tools\bin\ybload.exe"
            else:
                ybin="ybload"
            
            #You could also have run this with .call(cmd,shell=True):
            #cmd=rf'{ybin} --host {self.host} --username {self.user} --dbname {self.db} --max-bad-rows {maxbad} --csv-skip-header-line true --table {target} {dump}'
            cmd=[ybin,
                 '--host',self.host,
                 '--username',self.user,
                 '--dbname',self.db,
                 '--max-bad-rows',"0" if ignoreLoadErrors else "-1",
                 '--csv-skip-header-line','true',
                 '--table',target,
                 dump
            ]
            vprint(f"Running this now ===> {' '.join(cmd)}")
            
            try:
                res=subprocess.run(cmd,capture_output=True,check=True)
            except Exception as e:
                raise RuntimeError(f"There was a problem running ybload.  Make sure it's installed, is on your PATH, and that Java is installed:\n{e}")
            
            lrows = self.tableRowCount(target)
            if len(src)==lrows or clobber==False:
                print("YBload successful")
                vprint(f"Dumped {len(src)} rows, and then loaded {lrows} rows.")
            else:
                print("WARNING: The number of rows in {target} doesn't match the size of {src}")
        
        return
    
    #Alias
    df2Yb=dfToYb
    
    def getYbTypesFromDf(self,df):
        """ Try to map.  This is almost vulgar.
            Return a tuple the same size as dftypes."""
        default_yb = "varchar(255)"
        df2yb = {'int64':'bigint',
                 'int32':'bigint',
                 'float64':'float',
                 'float32':'float',
                 'object':'varchar(1024)'}
        ybtypes = []
        for t in df.dtypes:
            ybtypes.append(df2yb.get(t.name,default_yb))
        return(tuple(ybtypes))



def test(timeout_minutes=0.1):
    """ """
    import time
    print("=== Create a YB connector object ===")
    YB = YbConnector("ybr-01.eyc.com","dbo","cl2",ybhosts="/home/jovyan/ybhosts.txt")
    
    print("\n=== Drop, ctas, and select from a table ===")
    tt = "geatstanl.cjl_test"
    if YB.tableExists(tt):
        print(f"{tt} already exists.  Dropping.")
        YB.execute(f"drop table {tt}")
    
    YB.execute(f"create table {tt} as select 1 one,current_timestamp as ts")
    d=YB.query(f"select * from {tt}")
    print(type(d))
    print(d)
    
    print("\n=== Bulkload using ybload and string buffers ===")
    for loadmode in [True,False]:
        print(f"Loading with lite={loadmode}")
        data=pd.read_csv(r"ptest.csv")
        YB.dfToYb(data,tt+repr(loadmode),clobber=True,lite=loadmode)
        d=YB.query(f"select * from {tt} order by 1")
        print(d)
        print(f"{d.shape[0]} rows, {d.shape[1]} columns.")
    
    print("\n=== Timeout recovery ===")
    print(f"Make some tea.  This will run for {timeout_minutes} minutes.")
    time.sleep(float(timeout_minutes)*60)
    print(YB.query("select current_timestamp"))
    print("Test complete.")
    return True

if __name__=="__main__":
    """ """
    if len(sys.argv)>1:
       test(timeout_minutes=sys.argv[1])
    
