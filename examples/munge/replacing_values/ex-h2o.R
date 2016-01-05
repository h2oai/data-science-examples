library(h2o)
path <- "data/iris/iris_wheader.csv"
h2o.init()
df <- h2o.importFile(path)

# replace a single numerical datum
df[15,3] <- 2

# replace a single categorical datum
# unimplemented as of 3.6.0.8 (tibshirani)

# replace a whole column
df[,1] <- 3*df[,1]

# replace by row mask
df[df[,"sepal_len"] < 4.4, "sepal_len"] <- 22  # BUG: https://0xdata.atlassian.net/browse/PUBDEV-2520

# replacement with ifelse
df[,"sepal_len"] <- h2o.ifelse(df[,"sepal_len"] < 4.4, 22, df[,"sepal_len"])

# replace missing values with 0
df[is.na(df[,"sepal_len"]), "sepal_len"] <- 0

# alternative with ifelse
df[,"sepal_len"] <- h2o.ifelse(is.na(df[,"sepal_len"]), 0, df[,"sepal_len"])
