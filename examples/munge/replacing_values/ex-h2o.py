import h2o 
h2o.init()
path = "data/iris/iris_wheader.csv"
df = h2o.import_file(path=path)

# replace a single numerical datum
df[14,2] = 2

# replace a single categorical datum
# unimplemented as of 3.6.0.8 (tibshirani)

# replace a whole column
df[0] = 3*df[0]

# replace by row mask
df[df["sepal_len"] < 4.4, "sepal_len"] = 22  # BUG: https://0xdata.atlassian.net/browse/PUBDEV-2520

# replacement with ifelse
df["sepal_len"] = (df["sepal_len"] < 4.4).ifelse(22, df["sepal_len"])

# replace missing values with 0
df[df["sepal_len"].isna(), "sepal_len"] <- 0

# alternative with ifelse
df["sepal_len"] <- (df["sepal_len"].isna()).ifelse(0, df["sepal_len"])  # note the parantheses!

