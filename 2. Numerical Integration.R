rm(list = ls())
graphics.off()

# Numerical integration with a fine data (assuming absense of measurement error)
a <- 0
b <- 10

dxf <- 0.01 # f stands for fine
xf <- seq(from = a, to = b, by = dxf)
yf <- sin(xf)
plot(yf ~ xf, type = "l", col = "blue")

dxc <- 0.1  # c stands for course data
xc <- seq(from = a, to = b, by = dxc)
yc <- sin(xc)

plot(yc ~ xc, type = "s", col = "red")
curve(sin(x), add = TRUE, col = "black")

n <- length(yc)

# Left-rectangle rule
area1 <- 0

for (i in 1:(n-1)) {
  area1 <- area1 + yc[i]*dxc
}

# Right-rectangle rule
area2 <- 0

for (i in 2:n) {
  area2 <- area2 + yc[i]*dxc
}

# Trapezoid rule
area3 <- 0

for (i in 1:(n-1)) {
  area3 <- area3 + (dxc / 2)*(yc[i] + yc[i+1])
}
