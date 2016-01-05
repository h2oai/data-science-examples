import h2o 
h2o.init()
path = "data/iris/iris_wheader.csv"
df = h2o.import_file(path=path)

# slice 1 column by index
c1 = df[:,0]

# slice 1 column by name
c1_1 = df[:, "sepal_len"]

# slice cols by list of indexes
cols = df[:, range(4)]

# slice cols by a list of names
cols_1 = df[:, ["sepal_len", "sepal_wid", "petal_len", "petal_wid"]]
