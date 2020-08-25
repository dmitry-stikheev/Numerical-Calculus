rm(list = ls())
graphics.off()


## Spring mass damper system

w <- 2*pi      # natural frequency
d <- 0.5      # damping ratio

A <- matrix(c(0, 1,
              -w^2, -2*d*w),
            byrow = TRUE,
            nrow = 2, 
            ncol = 2)

dt <- 0.1      # time step
T <- 10        # time to integrate (duration)
 
x0 <- c(1, 0)  # initial condition


# Iterating Forward Euler scheme
xF <- matrix(0, ncol = T / dt, nrow = 2)
tF <- rep(0, T / dt)
xF[, 1] <- x0 
tF[[1]] <- 0

for (i in 1:(T / dt - 1)) {
  tF[i+1] <- i*dt
  xF[, i+1] <- (diag(2) + A*dt) %*% xF[, i]
}

plot(tF, xF[1, ], type = "l",
     xlab = "Time",
     ylab = "Position")


# Iterating Backward Euler scheme
xB <- matrix(0, ncol = T / dt, nrow = 2)
tF <- rep(0, T / dt)
xB[, 1] <- x0
tF[1] <- 0

for (i in 1:(T / dt - 1)) {
  tF[i+1] <- i*dt
  xB[, i+1] <- solve(diag(2) - A*dt, diag(2)) %*% xB[, i]
}


lines(tF, xB[1, ], type = "l", col = "red")
legend("topright", legend = c("Forward Euler", "Backward Euler"),
       col = c("black", "red"), lty = c(1, 1), lwd = c(1, 1))
