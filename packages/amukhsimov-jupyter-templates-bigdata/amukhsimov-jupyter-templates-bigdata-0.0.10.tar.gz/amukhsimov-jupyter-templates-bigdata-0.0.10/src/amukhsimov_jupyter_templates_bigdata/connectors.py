from dotenv import load_dotenv
import os
from pyspark.sql import SparkSession
import cx_Oracle
import psycopg2
from . import encode_text, decode_text

load_dotenv()

LOCAL_SPARK_EXECUTOR_MEMORY = os.getenv("LOCAL_SPARK_EXECUTOR_MEMORY", "32g")
LOCAL_SPARK_DRIVER_MEMORY = os.getenv("LOCAL_SPARK_DRIVER_MEMORY", "32g")
LOCAL_SPARK_DRIVE_MAX_RESULTS_SIZE = os.getenv("LOCAL_SPARK_DRIVE_MAX_RESULTS_SIZE", "32g")
LOCAL_SPARK_DRIVER_EXTRA_CLASS_PATH = os.getenv("LOCAL_SPARK_DRIVER_EXTRA_CLASS_PATH", None)
LOCAL_SPARK_HADOOP_FS_DEFAULT_FS = os.getenv("LOCAL_SPARK_HADOOP_FS_DEFAULT_FS", None)
LOCAL_SPARK_SQL_WAREHOUSE_DIR = os.getenv("LOCAL_SPARK_SQL_WAREHOUSE_DIR", None)
LOCAL_SPARK_CORES_MAX = os.getenv("LOCAL_SPARK_CORES_MAX", None)

REMOTE_SPARK_EXECUTOR_MEMORY = os.getenv("REMOTE_SPARK_EXECUTOR_MEMORY", "32g")
REMOTE_SPARK_DRIVER_MEMORY = os.getenv("REMOTE_SPARK_DRIVER_MEMORY", "32g")
REMOTE_SPARK_DRIVE_MAX_RESULTS_SIZE = os.getenv("REMOTE_SPARK_DRIVE_MAX_RESULTS_SIZE", "32g")
REMOTE_SPARK_MASTER = os.getenv("REMOTE_SPARK_MASTER", None)
# REMOTE_SPARK_DRIVER_EXTRA_CLASS_PATH = os.getenv("REMOTE_SPARK_DRIVER_EXTRA_CLASS_PATH", None)
REMOTE_SPARK_HADOOP_FS_DEFAULT_FS = os.getenv("REMOTE_SPARK_HADOOP_FS_DEFAULT_FS", None)
REMOTE_SPARK_SQL_WAREHOUSE_DIR = os.getenv("REMOTE_SPARK_SQL_WAREHOUSE_DIR", None)

HADOOPNAMENODE_HOST = os.getenv("HADOOPNAMENODE_HOST", None)
HADOOPNAMENODE_PORT = os.getenv("HADOOPNAMENODE_PORT", None)

IABS_PROD_IP = os.getenv("IABS_PROD_IP", None)
IABS_PROD_PORT = os.getenv("IABS_PROD_PORT", None)
IABS_PROD_SID = os.getenv("IABS_PROD_SID", None)
IABS_PROD_USERNAME = os.getenv("IABS_PROD_USERNAME", None)
IABS_PROD_PASSWORD = os.getenv("IABS_PROD_PASSWORD", None)

IABS_PREPROD_IP = os.getenv("IABS_PREPROD_IP", None)
IABS_PREPROD_PORT = os.getenv("IABS_PREPROD_PORT", None)
IABS_PREPROD_SID = os.getenv("IABS_PREPROD_SID", None)
IABS_PREPROD_USERNAME = os.getenv("IABS_PREPROD_USERNAME", None)
IABS_PREPROD_PASSWORD = os.getenv("IABS_PREPROD_PASSWORD", None)

RSTYLE_PROD_IP = os.getenv("RSTYLE_PROD_IP", None)
RSTYLE_PROD_PORT = os.getenv("RSTYLE_PROD_PORT", None)
RSTYLE_PROD_SID = os.getenv("RSTYLE_PROD_SID", None)
RSTYLE_PROD_USERNAME = os.getenv("RSTYLE_PROD_USERNAME", None)
RSTYLE_PROD_PASSWORD = os.getenv("RSTYLE_PROD_PASSWORD", None)

RSTYLE_PREPROD_IP = os.getenv("RSTYLE_PREPROD_IP", None)
RSTYLE_PREPROD_PORT = os.getenv("RSTYLE_PREPROD_PORT", None)
RSTYLE_PREPROD_SID = os.getenv("RSTYLE_PREPROD_SID", None)
RSTYLE_PREPROD_USERNAME = os.getenv("RSTYLE_PREPROD_USERNAME", None)
RSTYLE_PREPROD_PASSWORD = os.getenv("RSTYLE_PREPROD_PASSWORD", None)

MICROSERVICES_PROD_IP = os.getenv("MICROSERVICES_PROD_IP", None)
MICROSERVICES_PROD_PORT = os.getenv("MICROSERVICES_PROD_PORT", None)
MICROSERVICES_PROD_USERNAME = os.getenv("MICROSERVICES_PROD_USERNAME", None)
MICROSERVICES_PROD_PASSWORD = os.getenv("MICROSERVICES_PROD_PASSWORD", None)

MICROSERVICES_PREPROD_IP = os.getenv("MISROSERVICES_PREPROD_IP", None)
MICROSERVICES_PREPROD_PORT = os.getenv("MISROSERVICES_PREPROD_PORT", None)
MICROSERVICES_PREPROD_USERNAME = os.getenv("MISROSERVICES_PREPROD_USERNAME", None)
MICROSERVICES_PREPROD_PASSWORD = os.getenv("MISROSERVICES_PREPROD_PASSWORD", None)


class Connector:
    def __init__(self):
        pass

    def get_spark_connector(self, use_local_spark: bool, app_name: str):
        if use_local_spark:
            spark = SparkSession.builder \
                .config("spark.executor.memory", LOCAL_SPARK_EXECUTOR_MEMORY) \
                .config("spark.driver.memory", LOCAL_SPARK_DRIVER_MEMORY) \
                .config("spark.driver.maxResultsSize", LOCAL_SPARK_DRIVE_MAX_RESULTS_SIZE)

            if LOCAL_SPARK_DRIVER_EXTRA_CLASS_PATH is not None:
                spark = spark.config("spark.driver.extraClassPath", LOCAL_SPARK_DRIVER_EXTRA_CLASS_PATH)
            if LOCAL_SPARK_HADOOP_FS_DEFAULT_FS is not None:
                spark = spark.config("spark.hadoop.fs.defaultFS", LOCAL_SPARK_HADOOP_FS_DEFAULT_FS)
            if LOCAL_SPARK_SQL_WAREHOUSE_DIR is not None:
                spark = spark.config("spark.sql.warehouse.dir", LOCAL_SPARK_SQL_WAREHOUSE_DIR)
            if LOCAL_SPARK_CORES_MAX is not None:
                spark = spark.config("spark.cores.max", int(LOCAL_SPARK_CORES_MAX))

            return spark.appName(app_name).getOrCreate()
        else:  # use remote spark
            if not REMOTE_SPARK_MASTER:
                raise RuntimeError("No REMOTE_SPARK_MASTER variable found in environment")

            spark = SparkSession.builder \
                .config("spark.executor.memory", REMOTE_SPARK_EXECUTOR_MEMORY) \
                .config("spark.driver.memory", REMOTE_SPARK_DRIVER_MEMORY) \
                .config("spark.driver.maxResultsSize", REMOTE_SPARK_DRIVE_MAX_RESULTS_SIZE) \
                .master(REMOTE_SPARK_MASTER)

            # if LOCAL_SPARK_DRIVER_EXTRA_CLASS_PATH is not None:
            #     spark = spark.config("spark.driver.extraClassPath", LOCAL_SPARK_DRIVER_EXTRA_CLASS_PATH)
            if REMOTE_SPARK_HADOOP_FS_DEFAULT_FS is not None:
                spark = spark.config("spark.hadoop.fs.defaultFS", REMOTE_SPARK_HADOOP_FS_DEFAULT_FS)
            if REMOTE_SPARK_SQL_WAREHOUSE_DIR is not None:
                spark = spark.config("spark.sql.warehouse.dir", REMOTE_SPARK_SQL_WAREHOUSE_DIR)

            return spark.appName(app_name).getOrCreate()

    def get_namenode_addr(self):
        return HADOOPNAMENODE_HOST, HADOOPNAMENODE_PORT

    def _get_iabs_creds(self, env, master_password):
        if env == "prod":
            ip = decode_text(IABS_PROD_IP, master_password)
            port = decode_text(IABS_PROD_PORT, master_password)
            sid = decode_text(IABS_PROD_SID, master_password)
            username = decode_text(IABS_PROD_USERNAME, master_password)
            password = decode_text(IABS_PROD_PASSWORD, master_password)
        elif env == "preprod":
            ip = decode_text(IABS_PREPROD_IP, master_password)
            port = decode_text(IABS_PREPROD_PORT, master_password)
            sid = decode_text(IABS_PREPROD_SID, master_password)
            username = decode_text(IABS_PREPROD_USERNAME, master_password)
            password = decode_text(IABS_PREPROD_PASSWORD, master_password)
        else:
            raise ValueError(f"env '{env}' is unsupported for iabs")
        return ip, port, sid, username, password

    def get_iabs_connector(self, env, master_password):
        """
        :param env: 'prod'|'preprod'
        :return:
        """
        ip, port, sid, username, password = self._get_iabs_creds(env, master_password)
        dsn_tns_iabs = cx_Oracle.makedsn(ip, port, service_name=sid)
        return cx_Oracle.connect(user=username, password=password, dsn=dsn_tns_iabs, encoding="UTF-8")

    def get_iabs_jdbc(self, env, master_password):
        """
        :param env: 'prod'|'preprod'
        :return:
        """
        ip, port, sid, username, password = self._get_iabs_creds(env, master_password)
        return f"jdbc:oracle:thin:@{ip}:{port}:{sid}"

    def _get_rstyle_creds(self, env, master_password):
        if env == "prod":
            ip = decode_text(RSTYLE_PROD_IP, master_password)
            port = decode_text(RSTYLE_PROD_PORT, master_password)
            sid = decode_text(RSTYLE_PROD_SID, master_password)
            username = decode_text(RSTYLE_PROD_USERNAME, master_password)
            password = decode_text(RSTYLE_PROD_PASSWORD, master_password)
        elif env == "preprod":
            ip = decode_text(RSTYLE_PREPROD_IP, master_password)
            port = decode_text(RSTYLE_PREPROD_PORT, master_password)
            sid = decode_text(RSTYLE_PREPROD_SID, master_password)
            username = decode_text(RSTYLE_PREPROD_USERNAME, master_password)
            password = decode_text(RSTYLE_PREPROD_PASSWORD, master_password)
        else:
            raise ValueError(f"env '{env}' is unsupported for rstyle")
        return ip, port, sid, username, password

    def get_rstyle_connector(self, env, master_password):
        """
        :param env: 'prod'|'preprod'
        :return:
        """
        ip, port, sid, username, password = self._get_rstyle_creds(env, master_password)
        dsn_tns_iabs = cx_Oracle.makedsn(ip, port, service_name=sid)
        return cx_Oracle.connect(user=username, password=password, dsn=dsn_tns_iabs, encoding="UTF-8")

    def get_rstyle_jdbc(self, env, master_password):
        """
        :param env: 'prod'|'preprod'
        :return:
        """
        ip, port, sid, username, password = self._get_rstyle_creds(env, master_password)
        return f"jdbc:oracle:thin:@{ip}:{port}:{sid}"

    def _get_microservices_creds(self, env, master_password):
        if env == "prod":
            ip = decode_text(MICROSERVICES_PROD_IP, master_password)
            port = decode_text(MICROSERVICES_PROD_PORT, master_password)
            username = decode_text(MICROSERVICES_PROD_USERNAME, master_password)
            password = decode_text(MICROSERVICES_PROD_PASSWORD, master_password)
        elif env == "preprod":
            ip = decode_text(MICROSERVICES_PREPROD_IP, master_password)
            port = decode_text(MICROSERVICES_PREPROD_PORT, master_password)
            username = decode_text(MICROSERVICES_PREPROD_USERNAME, master_password)
            password = decode_text(MICROSERVICES_PREPROD_PASSWORD, master_password)
        else:
            raise ValueError(f"env '{env}' is unsupported for microservices")
        return ip, port, username, password

    def get_microservices_connector(self, env, database, master_password):
        """
        :param env: 'prod'|'preprod'
        :return:
        """
        ip, port, username, password = self._get_microservices_creds(env, master_password)

        return psycopg2.connect(host=ip, port=port, database=database, user=username, password=password)

    def get_microservices_jdbc(self, env, database, master_password):
        """
        :param env: 'prod'|'preprod'
        :return:
        """
        ip, port, username, password = self._get_microservices_creds(env, master_password)
        return f"jdbc:postgresql://{ip}:{port}/{database}"
