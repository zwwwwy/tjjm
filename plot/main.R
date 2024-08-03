library(readxl)
library(ggplot2)

df <- read_excel("./main.xlsx")
ggplot(df, aes(x = x, y = y)) +
    geom_point(aes(shape = label, color = label), size = 3) +
    scale_x_continuous(breaks = seq(2013, 2022)) +
    labs(x = "年份", y = "取值")
ggsave("1.svg", width = 8, height = 6)


ggplot(df, aes(x = x, y = y)) +
    geom_line(aes(shape = label, color = label)) +
    scale_x_continuous(breaks = seq(2013, 2022)) +
    labs(x = "年份", y = "取值")
ggsave("2.svg", width = 8, height = 6)
