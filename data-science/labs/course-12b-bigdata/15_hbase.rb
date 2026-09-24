# Experiment 15 -- create and manage tables in HBase -- CRUD operations
#
# *** NOT EXECUTED ***
# This is the command sequence / program you submit on a real Hadoop cluster.
# Hadoop, Hive, Pig, Sqoop, Flume, HBase and ZooKeeper cannot be installed in
# the verification environment -- the Debian repositories that host them are
# blocked by the egress policy -- so this file has NEVER BEEN RUN here.
# Nothing in the notes claims an output for it.
#
# The runnable half is 15_hbase_model.py, which implements the same data model and runs it
#
# run with:  hbase shell 15_hbase.rb        (or paste into an interactive shell)

# --- CREATE -----------------------------------------------------------------
create 'sales', \
  {NAME => 'info',  VERSIONS => 3, COMPRESSION => 'SNAPPY'}, \
  {NAME => 'sales', VERSIONS => 3, TTL => 31536000}
#   COLUMN FAMILIES ARE FIXED AT CREATE TIME and expensive to change.
#   COLUMNS inside a family are free and need no declaration -- that is what
#   "schema-less" means in HBase, and it is only half true.
#   Keep families to two or three: each one is a separate store file, and a
#   flush of one flushes all of them.

list
describe 'sales'

# --- PUT --------------------------------------------------------------------
# row key = region#store#date#product -- composite, unique at the grain,
# and NOT monotonic. See the design table at the end.
put 'sales', 'South#Vijayawada#D1#Rice',  'info:product',  'Rice 5kg'
put 'sales', 'South#Vijayawada#D1#Rice',  'info:category', 'Grocery'
put 'sales', 'South#Vijayawada#D1#Rice',  'sales:qty',     '10'
put 'sales', 'South#Vijayawada#D1#Rice',  'sales:revenue', '2800'
put 'sales', 'North#Hyderabad#D2#Notebook', 'info:product', 'Notebook'
put 'sales', 'North#Hyderabad#D2#Notebook', 'sales:qty',    '20'

# --- GET --------------------------------------------------------------------
get 'sales', 'South#Vijayawada#D1#Rice'
get 'sales', 'South#Vijayawada#D1#Rice', 'sales'
get 'sales', 'South#Vijayawada#D1#Rice', {COLUMN => 'sales:qty', VERSIONS => 3}
#   a PUT to an existing cell ADDS A VERSION; it does not overwrite.

# --- SCAN -------------------------------------------------------------------
scan 'sales'
scan 'sales', {LIMIT => 5}
scan 'sales', {STARTROW => 'South', STOPROW => 'South~'}
#   '~' sorts after every printable ASCII letter, which is the idiomatic way
#   to write a prefix scan by hand. PrefixFilter does the same thing:
scan 'sales', {FILTER => "PrefixFilter('South')"}
scan 'sales', {FILTER => "SingleColumnValueFilter('info','category',=,'binary:Grocery')"}
#   ^ THIS IS A FULL TABLE SCAN. HBase has no secondary index. The filter runs
#     server-side, so less data crosses the network -- but every row is read.

# --- UPDATE, DELETE ---------------------------------------------------------
put    'sales', 'South#Vijayawada#D1#Rice', 'sales:qty', '11'   # = a new version
delete 'sales', 'South#Vijayawada#D1#Rice', 'info:category'
deleteall 'sales', 'North#Hyderabad#D2#Notebook'
#   A DELETE WRITES A TOMBSTONE. The table gets BIGGER. Data and marker are
#   both removed only at a major compaction:
major_compact 'sales'

# --- counters, which are atomic --------------------------------------------
incr 'sales', 'North#Hyderabad#D2#Notebook', 'sales:views', 1
get_counter 'sales', 'North#Hyderabad#D2#Notebook', 'sales:views'

# --- admin ------------------------------------------------------------------
count 'sales', INTERVAL => 100
disable 'sales'
alter 'sales', {NAME => 'info', VERSIONS => 5}
enable 'sales'
truncate 'sales'          # = disable + drop + recreate. Keeps the schema.
# drop 'sales'            # must be disabled first

# --- pre-splitting, which you do at create time or regret later ------------
create 'sales2', 'info', {SPLITS => ['East', 'North', 'South', 'West']}
#   without pre-splits the table starts as ONE region on ONE RegionServer, so
#   a bulk load runs single-threaded until the first split.

# --- row key design ---------------------------------------------------------
#   key                          writes go to     verdict
#   timestamp                    the last region  HOTSPOT
#   sequential id                the last region  HOTSPOT
#   md5(id) + id                 everywhere       good; range scans lost
#   region#store#date#product    by region        good; prefix scans work
#
#   You cannot have even write distribution AND range scans on the same
#   dimension. Choosing between them IS row-key design.
