from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, TimestampType
from pyspark.sql.functions import *

import re
import os

"""
Liten DemoFiles
"""
import pyspark
from pyspark.sql import SparkSession

class DemoFiles:
    """
    Liten DemoFiles - Load demo files as a table from csv file
    """
    def __init__(self, spark, liten_data_dir):
        """
        Create and initialize Liten Cache
        """
        self._spark = spark
        self._data_dir = liten_data_dir + '/files/'
        self._weblog = 'weblog'
        self._syslog = 'syslog'
        self._emailserviceaccesslog = 'emailaccesslog'
        self._data_files = {self._weblog: [self._data_dir+"webserverlog_simple.log"],  
                            self._syslog: [self._data_dir+"linuxsystemlog_simple.log"],
                            self._emailserviceaccesslog: [self._data_dir+"emailservice_access.log"] }
        self._time_field = 'time'
        self._debug = False #modify this flag to enable verbose mode.
        pass

    def init(self):
        """
        Initialize Liten DemoFiles if not already initialized.
        Should be called only once. Used for demo purposes.
        """
        self.init_weblog()
        self.init_linux_syslog()
        self.init_emailaccesslog()
        pass

    def init_weblog(self):
        """
        Sample simple weblog server log
        """
        weblog_schema = StructType([ \
                                     StructField("ip",StringType(),True), \
                                     StructField(self._time_field,TimestampType(),True), \
                                     StructField("url",StringType(),True), \
                                     StructField("status", IntegerType(), True) \
                                    ])
        weblog_dfs = None
        for filename in self._data_files[self._weblog]:
            weblog_df = self._spark.read.\
                format('csv').\
                options(header='true').\
                options(delimiter=',').\
                options(timestampFormat='dd/MMM/yyyy:HH:mm:ss').\
                schema(weblog_schema).\
                load(filename)
            if weblog_dfs is None:
                weblog_dfs = weblog_df
            else:
                weblog_dfs.union(weblog_df)
        weblog_dfs.createOrReplaceTempView(self._weblog)
        return

    def init_emailaccesslog(self):
        """
        For now read csv, in future needs to be a database table
        csv file which has access logs of a email service. 
        Sample line. For more examples, look in samplelogfiles directory.
        2023-05-30 15:49:43,309,imap,machine291.dovecotservice.africa.mail.emailcompany.com,5077 ,14 ,202,[markasspam],/message/scan/id=messagehash6pgp5x598e ,hashun5xjw6zwrdbd ,60 ,[missingmailbox] ,inaccessible file ,bad encoding,74.229.170.153
        service, host, payload, latency, status, API, Q, reqId, CPULatency, ec, EC2, exception, clientIp
        For latest format, check in folder named logfilegenerationscripts.
        FORMATCSV = '%(asctime)s,%(service)s,%(host)s,%(payload)s ,%(latency)s ,%(status)s,[%(api)s],' \
         '/message/%(act)s/id=messagehash%(mes)s ,hash%(requestId)s ,%(CPUlatency)s ,[%(error_code1)s] ' \
         ',%(error_code2)s ,%(exception)s,%(clientip)-15s '

        Notes: #we will be ignoring MilliSecondsLine below field as it should ideally go with 'Time' field.
        Latency and most other time measurements are in milli seconds.
        """
        emailaccesslog_schema = StructType([ \
                                     StructField(self._time_field,TimestampType(),True), \
                                     StructField("milliSecondsLine", IntegerType(), True), \
                                     StructField("service", StringType(), True), \
                                     StructField("hostname",StringType(),True), \
                                     StructField("payloadSize", IntegerType(), True), \
                                     StructField("latency", IntegerType(), True), \
                                     StructField("status", IntegerType(), True), \
                                     StructField("api",StringType(),True), \
                                     StructField("messageUrl",StringType(),True), \
                                     StructField("hash",StringType(),True), \
                                     StructField("cpuLatency", IntegerType(), True), \
                                     StructField("errorCode", StringType(), True), \
                                     StructField("detailedErrorCode", StringType(), True), \
                                     StructField("exception", StringType(), True), \
                                     StructField("ip", StringType(), True) \
                                    ])
        emailaccesslog_dfs = None
        for filename in self._data_files[self._emailserviceaccesslog]:
            emailaccesslog_df = self._spark.read.\
                format('csv').\
                options(header='false').\
                options(delimiter=',').\
                option("ignoreLeadingWhiteSpace",'true').\
                option("ignoreTrailingWhiteSpace",'true').\
                options(timestampFormat='yyyy-MM-dd HH:mm:ss').\
                schema(emailaccesslog_schema).\
                load(filename)
            if emailaccesslog_dfs is None:
                emailaccesslog_dfs = emailaccesslog_df
            else:
                emailaccesslog_dfs.union(emailaccesslog_df)
        emailaccesslog_dfs.createOrReplaceTempView("emailaccesslog")
        return

    def init_linux_syslog(self):
        # For now read csv, in future needs to be a database table
        # extended ietf format:
        #  timestamp hostname process[pid]: message header message
        # example
        #  Jun 14 15:16:01 combo sshd(pam_unix)[19939]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
        # convert to a csv file like this first
        #  timestamp,hostname,process,pid,message
        # example
        #  Jun 14 15:16:01|combo|sshd(pam_unix)|19939|authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4
        def convert_to_csv(filename):
            syslog_file = open(filename, 'r')
            csv_file = filename+'.csv'
            syslog_csv = open(csv_file, 'w')
            log_line = syslog_file.readline()
            skips=0
            while log_line:
                log_line = log_line.strip()
                # Read log line and convert to csv format
                # sample log: Jun 14 15:16:01 combo sshd(pam_unix)[19939]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
                # output csv: Jun 14 15:16:01|combo|sshd(pam_unix)|19939|authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4
                log = re.findall("([\w]+\s+[0-9]+\s+[0-9:]+)\s+([\w]+)\s+([\w\(\)\-\.\s]+)\[([0-9]+)\]\:\s*(.*)",log_line)
                if len(log)>0:
                    f=log[0]
                    syslog_csv.write('|'.join(f)+'\n')
                else:
                    # Try another log line format with no pid
                    # sample log: Jun 15 04:06:20 combo logrotate: ALERT exited abnormally with [1] 
                    # output csv: Jun 15 04:06:20|combo|logrotate||ALERT exited abnormally with [1]
                    log = re.findall("([\w]+\s+[0-9]+\s+[0-9:]+)\s+([\w]+)\s+([\w\s\.\-\(\)]+)\:\s*(.*)",log_line)
                    if len(log)>0:
                        f=log[0]
                        syslog_csv.write(f"{f[0]}|{f[1]}|{f[2]}||{f[3]}\n")
                    else:
                        # Skip other log lines
                        skips = skips+1
                log_line = syslog_file.readline()
            syslog_file.close()
            syslog_csv.close()
            if skips>0:
                print(f"skipped {skips} lines") 
            return csv_file
        # Create schema and table now
        # TBD need a generic timestamp converter for the two given formats like -
        #syslog_df.select(to_timestamp(syslog_df.timestamp, ('MMM d HH:mm:ss','MMM dd HH:mm:ss'))).collect()
        syslog_schema = StructType([ \
                                     StructField(self._time_field,TimestampType(),True), \
                                     StructField("hostname",StringType(),True), \
                                     StructField("process",StringType(),True), \
                                     StructField("pid", IntegerType(), True), \
                                     StructField("message", StringType(), True) \
                                    ])
        syslog_dfs = None
        for filename in self._data_files[self._syslog]:
            csv_file = convert_to_csv(filename)
            # Use inferSchema as true if no schema provided
            syslog_df = self._spark.read.\
                format('csv').\
                options(header='false').\
                options(delimiter='|').\
                options(timestampFormat='MMM d HH:mm:ss').\
                schema(syslog_schema).\
                load(csv_file)
            if syslog_dfs is None:
                syslog_dfs = syslog_df
            else:
                syslog_dfs.union(syslog_df)
        syslog_dfs.createOrReplaceTempView("syslog")
        pass     
