path <- "data/iris/iris_wheader.csv"
df <- read.csv(path)

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
