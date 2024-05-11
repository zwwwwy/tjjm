data <- read.csv("./data/data.csv")
data <- data[-1]

result <- lm("市场规模 ~ .", data = data)
summary(result)
