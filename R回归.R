library(dplyr)
library(readxl)
library(caret)
library(glmnet)
library(haven)
library(lmtest)
library(sandwich)
library(ivreg)
library(ridge)
library(corrplot)
library(car)
library(cowplot)

y <- read.csv("./data/综合指数/医疗综合指数.csv")
x <- read.csv("./data/综合指数/人工智能综合指数.csv")
control <- read.csv("./控制变量结果/35.csv")
data <- data.frame(x = x[, 2], y = y[, 2], control = control[, -1])
data <- rename(data, c("Eco" = "control.人均GDP增长率", "Gover" = "control.政府卫生支出占比", "Popu" = "control.人口自然增长率加一", "Area" = "control.变异系数", "Index_AI" = "x", "Index_HM" = "y"))
result <- lm("Index_HM ~ .", data = data)
summary(result)
data2 <- log(data + 0.001)
result2 <- lm("Index_HM ~ Index_AI", data = data2)
print(summary(result2))
vif(result2)

write.csv(summary(result2)$coefficients, "./报告结果/最小二乘回归结果.csv")

# 异方差稳健标准误
coeftest(result, vcov = vcovHC, type = "HC1")

data3 <- data[-1, ]
data3["工具变量"] <- x[-10, 2]

# 相关系数图
corr <- cor(data2)
write.csv(corr, "./报告结果/相关系数.csv")
pdf("./报告结果/相关系数图.pdf", width = 8, height = 6)
corrplot.mixed(corr, upper = "circle", lower = "number", tl.col = "black", tl.cex = 0.8, tl.srt = 45, tl.pos = "lt")

dev.off()

# 第一阶段回归
iv1.data <- data3[, -2]
# iv1.data <- iv1.data[, c(1, 7)]
iv1.result <- lm("AI ~ .", data = iv1.data)
summary(iv1.result)
iv1.x <- iv1.data[, -1]
iv1.d.hat <- predict(iv1.result, iv1.x, se.fit = TRUE)
# 第二阶段回归

iv2.data <- data3[, -8]
iv2.data[, 1] <- iv1.d.hat$fit
# iv2.data <- iv2.data[, c(1, 2)]
iv2.result <- lm(HM ~ ., data = iv2.data[, -7])
summary(iv2.result)
data3
# 两阶段回归
model <- ivreg(HM ~ Eco + Popu + Gover + Area | AI | 工具变量, data = data3)
summary(model)

# 岭回归
data
cv.result <- cv.glmnet(data[, -2], data[, 2], alpha = 0)
best.lambda <- cv.result$lambda.min
ridge.result <- glmnet(data[, -2], data[, 2], alpha = 0, lambda = best.lambda)
summary(ridge.result)
coef(ridge.result)

ridge.result2 <- linearRidge("Index_HM ~ .", data2)
write.csv(summary(ridge.result2)[6]$summaries$summary3$coefficients, "./报告结果/岭回归结果.csv")
print(summary(ridge.result2))

# 岭回归图像
# lambdas <- seq(0.1, 3, length.out = 200)
X <- data2[, -2]
Y <- data2[, 2]
set.seed(42)
ridge.model <- cv.glmnet(X, Y, alpha = 0)
# pdf("./报告结果/岭回归mse-lambda.pdf", width = 8, height = 6)
par(mfrow = (c(1, 2)))
p_1 <- plot(ridge.model)
# dev.off()
# pdf("./报告结果/岭回归coff-lambda.pdf", width = 8, height = 6)
p_2 <- plot(ridge.model$glmnet, "lambda", label = TRUE)
# dev.off()
ridge.model$lambda.min
ridge.model$lambda.1se
coef(ridge.model, s = "lambda.min")

ridge_data <- data.frame(
    log_lambda = log(ridge.model$lambda),
    cvm = ridge.model$cvm,
    cvup = ridge.model$cvup,
    cvlo = ridge.model$cvlo
)

ggplot(ridge_data, aes(x = log_lambda, y = cvm)) +
    geom_point() +
    geom_errorbar(aes(ymin = cvlo, ymax = cvup), width = 0.2) +
    geom_vline(xintercept = log(ridge.model$lambda.min), linetype = "dashed", color = "red") +
    geom_vline(xintercept = log(ridge.model$lambda.1se), linetype = "dashed", color = "blue") +
    labs(
        title = "Cross-Validation Error",
        x = "log(lambda)",
        y = "CVM"
    ) +
    theme_minimal()


pred <- predict(ridge.result2, data2[, -2])
real <- data2[, 2]
r2 <- data.frame(pred = pred, real = real)
write.csv(r2, "r2.csv")

# PCA结果回归
x_pca <- read.csv("./data/综合指数/PCA_人工智能综合指数.csv")
PCA_data <- data
PCA_data[, "AI"] <- x_pca[, "f"]
PCA_data <- log(PCA_data + 0.001)
PCA_result <- lm("HM ~ .", data = PCA_data)
