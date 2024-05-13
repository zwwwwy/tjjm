library(dplyr)
library(readxl)
library(caret)
library(glmnet)
library(haven)
library(lmtest)
library(sandwich)
library(ivreg)
library(ridge)

y <- read.csv("./data/综合指数/医疗综合指数.csv")
x <- read.csv("./data/综合指数/人工智能综合指数.csv")
control <- read.csv("./控制变量结果/315.csv")
data <- data.frame(x = x[, 2], y = y[, 2], control = control[, -1])
data <- rename(data, c("人工智能综合指数" = "x", "医疗综合指数" = "y"))
result <- lm("医疗综合指数 ~ .", data = data)
summary(result)
data2 <- log(data + 0.001)
result2 <- lm("医疗综合指数 ~ .", data = data2)
print(summary(result2))

write.csv(summary(result2)$coefficients, "./报告结果/最小二乘回归结果.csv")

# 异方差稳健标准误
coeftest(result, vcov = vcovHC, type = "HC1")

data3 <- data[-1, ]
data3["工具变量"] <- x[-10, 2]


# 第一阶段回归
iv1.data <- data3[, -2]
# iv1.data <- iv1.data[, c(1, 7)]
iv1.result <- lm("人工智能综合指数 ~ .", data = iv1.data)
summary(iv1.result)
iv1.x <- iv1.data[, -1]
iv1.d.hat <- predict(iv1.result, iv1.x, se.fit = TRUE)
# 第二阶段回归

iv2.data <- data3[, -8]
iv2.data[, 1] <- iv1.d.hat
# iv2.data <- iv2.data[, c(1, 2)]
iv2.result <- lm("医疗综合指数 ~ .", data = iv2.data)
summary(iv2.result)

# 两阶段回归
model <- ivreg("医疗综合指数 ~ 人工智能综合指数 | 工具变量", data = data3)
summary(model)

# 岭回归
data
cv.result <- cv.glmnet(data[, -2], data[, 2], alpha = 0)
best.lambda <- cv.result$lambda.min
ridge.result <- glmnet(data[, -2], data[, 2], alpha = 0, lambda = best.lambda)
summary(ridge.result)
coef(ridge.result)

ridge.result2 <- linearRidge("医疗综合指数 ~ .", data2)
# write.csv(summary(ridge.result2)[6]$summaries$summary3$coefficients, "./报告结果/岭回归结果.csv")
summary(ridge.result2)

pred <- predict(ridge.result2, data2[, -2])
real <- data2[, 2]
r2 <- data.frame(pred = pred, real = real)
write.csv(r2, "r2.csv")
