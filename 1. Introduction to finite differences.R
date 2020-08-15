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
