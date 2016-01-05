path <- "data/iris/iris_wheader.csv"
df <- read.csv(path)

# replace a single numerical datum
df[15,3] <- 2

# replace a single categorical datum
df[15,5] <- "versicolor"

# replace a whole column
df[,1] <- 3*df[,1]

# replace by row mask
df[df[,"sepal_len"] < 4.4, "sepal_len"] <- 22

# replacement with ifelse
df[,"sepal_len"] <- ifelse(df[,"sepal_len"] < 4.4, 22, df[,"sepal_len"])

# replace missing values with 0
df[is.na(df[,"sepal_len"]), "sepal_len"] <- 0

# alternative with ifelse
df[,"sepal_len"] <- ifelse(is.na(df[,"sepal_len"]), 0, df[,"sepal_len"])
