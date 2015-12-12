library(ex)
path = ex.locate("data/iris/iris_wheader.csv")
df = read.csv(path)
stopifnot(nrow(df) == 150)
