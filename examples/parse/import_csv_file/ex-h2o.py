import h2o
h2o.init()
path = "data/iris/iris_wheader.csv"
df = h2o.import_file(path=path)
assert df.nrow == 150