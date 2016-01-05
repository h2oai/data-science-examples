import h2o 
h2o.init()
path = "data/iris/iris_wheader.csv"
df = h2o.import_file(path=path)

# slice 1 row by index
c1 = df[15,:]

# slice a ramge of rows
c1_1 = df[range(25,50,1), :]

# slice with a boolean mask
mask = df["sepal_len"] < 4.4
cols = df[mask,:]

# filter out missing values
mask = df["sepal_len"].isna()
cols = df[~mask,:]  # note how to perform a logical not with the '~'
