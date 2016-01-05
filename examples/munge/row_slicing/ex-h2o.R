library(h2o)
path <- "data/iris/iris_wheader.csv"
h2o.init()
df <- h2o.importFile(path)

# slice 1 row by index
c1 <- df[15,]

# slice a range of rows
c1_1 <- df[25:49,]

# slice with a boolean mask
mask <- df[,"sepal_len"] < 4.4 
cols <- df[mask,]

# filter out missing values
mask <- is.na(df[,"sepal_len"])
cols <- df[!mask,]
