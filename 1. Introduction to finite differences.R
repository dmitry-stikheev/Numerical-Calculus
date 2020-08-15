## Numerical differentiation using Finite Differences
dt <- .3
t <- seq(from = -2, to = 4, by = dt)
f <- sin(t)

# Exact derivative
dfdt <- cos(t)

# Plotting
plot(t, f, type = "l", col = "black", lty = 2, lwd = 1, xlim = c(-2, 7), ylim = c(-1, 1.5))
grid(10, 10, col = "grey", lwd = 1)

lines(dfdt ~ t, col = "black", lwd = 2, lty = 1)
legend("topright", legend = c("Function", "Exact Derivative"), lty = c(2, 1), lwd = c(1, 2))

# Forward difference scheme
dfdtF <- (sin(t + dt) - sin(t)) / dt

# Backward difference scheme
dfdtB <- (sin(t) - sin(t - dt)) / dt 

# Central difference
dfdtC <- (sin(t + dt) - sin(t - dt)) / (2*dt)

# Plotting
lines(dfdtF ~ t, col = "blue", lwd = 1, lty = 1)   # forward
lines(dfdtB ~ t, col = "green", lwd = 1, lty = 1)  # backward
lines(dfdtC ~ t, col = "red", lwd = 1, lty = 1)    # central

legend("topright", legend = c("Function",
                              "Exact Derivative",
                              "Forward",
                              "Backward",
                              "Central"),
       lty = c(2, 1, 1, 1, 1), lwd = c(1, 2, 1, 1, 1),
       col = c(1, 1, "blue", "green", "red"))

#####
# You can play with the dt value, which by taking the smaller value improves 
# the approximation of the derivative. A relatively large value for dt in the current
# example was specified for illustration purposes. In a more advanced mathematical
# software, e.g. MatLab, one is allowed to zoom in the chart. Thus, it is much easier
# to detect the accuracy of the schemes presented in these lines of code.

## Treating f as a vector of data points, but not the output of the function
x <- seq(from = 0.1, to = 3, by = 0.1)
f <- sin(x)
plot(x, f, type = "o")

dx <- x[2] - x[1]
n <- length(f)

# At this point we can add noise to our vector in order to show that 
# dirty data magnifies the errors in the differentiation process

f <- sin(x) + 0.01*rnorm(x, 0, 1)

plot(x, f, type = "p")
curve(sin(x), add = TRUE)

dfdx <- rep(0, n)

# Using forward difference for the 1st value, backward difference for the last value, and central
# difference for the intermidiate points
dfdx[1] <- (f[2] - f[1]) / dx

for (i in 2:(n-1)) {
  dfdx[i] <- (f[i+1] - f[i-1]) / (2*dx)
}

dfdx[n] <- (f[n] - f[n-1]) / dx

# Plotting
plot(x, cos(x), type = "l", col = "black", lty = 1, lwd = 2)
grid(10, 10, col = "grey", lwd = 1)

lines(dfdx ~ x, col = "red", type = "p")
legend("topright", legend = c("Exact derivative", "Approximation"),
       lty = c(1, 1), lwd = c(2, 1), col = c("black", "red"))
