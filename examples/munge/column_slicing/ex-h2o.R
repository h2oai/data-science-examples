library(h2o)
path <- "data/iris/iris_wheader.csv"
h2o.init()
df <- h2o.importFile(path)

# slice 1 column by index
c1 <- df[,1]

# slice 1 column by name
c1_1 <- df[, "sepal_len"]

# slice cols by vector of indexes
cols <- df[, 1:4]

# slice cols by vector of names
cols_1 <- df[, c("sepal_len", "sepal_wid", "petal_len", "petal_wid")]
