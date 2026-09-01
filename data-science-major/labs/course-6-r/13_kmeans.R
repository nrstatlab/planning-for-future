# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 13: K-Means clustering
# Python equivalent: python/13_kmeans.py

set.seed(42)     # ALWAYS, or your clusters differ on every run

customers <- data.frame(
  income = c(rnorm(20, 300000, 40000),
             rnorm(20, 900000, 60000),
             rnorm(20, 1500000, 80000)),
  age    = c(rnorm(20, 28, 4), rnorm(20, 45, 5), rnorm(20, 38, 6))
)

# --- SCALING IS MANDATORY ---
# income spans ~1,200,000; age spans ~40. Euclidean distance is therefore
# driven almost entirely by income, and age contributes nothing.
# The variance ratio here is roughly 4,000,000,000 : 1.
scaled <- scale(customers)

km <- kmeans(scaled, centers = 3, nstart = 25)
# nstart = 25 runs the algorithm 25 times from different random starts and
# keeps the best. K-Means converges to a LOCAL optimum that depends on
# initialisation, so a single run can be poor.

km$cluster            # cluster assignment per observation
km$centers            # centroids, in SCALED units
km$size               # observations per cluster
km$tot.withinss       # total within-cluster sum of squares
km$betweenss / km$totss   # proportion of variance explained

customers$cluster <- factor(km$cluster)
aggregate(. ~ cluster, data = customers, FUN = mean)   # profile in REAL units

plot(customers$income, customers$age, col = km$cluster, pch = 19,
     xlab = "Annual income", ylab = "Age", main = "Customer segments")

# --- CHOOSING k: the elbow method ---
wss <- sapply(1:10, function(k) kmeans(scaled, k, nstart = 10)$tot.withinss)
plot(1:10, wss, type = "b", pch = 19,
     xlab = "Number of clusters k", ylab = "Within-cluster sum of squares")
# WSS always falls as k rises -- at k = n it is zero. The "elbow" is where
# extra clusters stop buying much.

# --- A less subjective alternative: the silhouette ---
# library(cluster)
# sil <- silhouette(km$cluster, dist(scaled)); mean(sil[, 3])

# COMPARE: without scaling, the clustering is driven by income alone.
km_raw <- kmeans(customers[, 1:2], centers = 3, nstart = 25)
table(km$cluster, km_raw$cluster)   # the two solutions differ
