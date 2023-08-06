### ENV variables:
 - `LOCAL_SPARK_EXECUTOR_MEMORY=32g`
 - `LOCAL_SPARK_DRIVER_MEMORY=32g`
 - `LOCAL_SPARK_DRIVE_MAX_RESULTS_SIZE=32g`
 - `LOCAL_SPARK_DRIVER_EXTRA_CLASS_PATH=/opt/oracle/instantclient_19_18/ojdbc8.jar`
 - `LOCAL_SPARK_HADOOP_FS_DEFAULT_FS=hdfs://<address>:<port>`
 - `LOCAL_SPARK_SQL_WAREHOUSE_DIR=hdfs://<address>:<port>/path/to/warehouse`


 - `REMOTE_SPARK_EXECUTOR_MEMORY=16g`
 - `REMOTE_SPARK_DRIVER_MEMORY=16g`
 - `REMOTE_SPARK_DRIVE_MAX_RESULTS_SIZE=16g`
 - `REMOTE_SPARK_MASTER=spark://<address>:<port>`
 - `REMOTE_SPARK_HADOOP_FS_DEFAULT_FS=hdfs://<address>:<port>`
 - `REMOTE_SPARK_SQL_WAREHOUSE_DIR=hdfs://<address>:<port>/path/to/warehouse`


 - `HADOOPNAMENODE_HOST=spark47`
 - `HADOOPNAMENODE_PORT=9000`


 - `IABS_PROD_IP=<encrypted text>`
 - `IABS_PROD_PORT=<encrypted text>`
 - `IABS_PROD_SID=<encrypted text>`
 - `IABS_PROD_USERNAME=<encrypted text>`
 - `IABS_PROD_PASSWORD=<encrypted text>`


 - `IABS_PREPROD_IP=<encrypted text>`
 - `IABS_PREPROD_PORT=<encrypted text>`
 - `IABS_PREPROD_SID=<encrypted text>`
 - `IABS_PREPROD_USERNAME=<encrypted text>`
 - `IABS_PREPROD_PASSWORD=<encrypted text>`


 - `RSTYLE_PROD_IP=<encrypted text>`
 - `RSTYLE_PROD_PORT=<encrypted text>`
 - `RSTYLE_PROD_SID=<encrypted text>`
 - `RSTYLE_PROD_USERNAME=<encrypted text>`
 - `RSTYLE_PROD_PASSWORD=<encrypted text>`


 - `RSTYLE_PREPROD_IP=<encrypted text>`
 - `RSTYLE_PREPROD_PORT=<encrypted text>`
 - `RSTYLE_PREPROD_SID=<encrypted text>`
 - `RSTYLE_PREPROD_USERNAME=<encrypted text>`
 - `RSTYLE_PREPROD_PASSWORD=<encrypted text>`


 - `MICROSERVICES_PROD_IP=<encrypted text>`
 - `MICROSERVICES_PROD_PORT=<encrypted text>`
 - `MICROSERVICES_PROD_USERNAME=<encrypted text>`
 - `MICROSERVICES_PROD_PASSWORD=<encrypted text>`


 - `MICROSERVICES_PREPROD_IP=<encrypted text>`
 - `MICROSERVICES_PREPROD_PORT=<encrypted text>`
 - `MICROSERVICES_PREPROD_USERNAME=<encrypted text>`
 - `MICROSERVICES_PREPROD_PASSWORD=<encrypted text>`

### BUILDING PACKAGE
 - `python3 setup.py sdist bdist_wheel`
 - `python3 -m twine upload --repository pypi dist/*`

### INSTALLATION:
 - `pip install amukhsimov-jupyter-templates-bigdata==0.0.9`