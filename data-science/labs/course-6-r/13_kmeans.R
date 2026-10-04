# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 13: K-Means clustering
# Python equivalent: python/13_kmeans.py

# Step 1: Make the customer data, after setting the seed
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
# The variance ratio here is about 3,500,000,000 : 1 (var(customers$income) /
# var(customers$age) is 3.48 billion). [Corrected: this said 4,000,000,000.]
# Step 2: Scale it, and cluster into three
scaled <- scale(customers)

km <- kmeans(scaled, centers = 3, nstart = 25)
# nstart = 25 runs the algorithm 25 times from different random starts and
# keeps the best. K-Means converges to a LOCAL optimum that depends on
# initialisation, so a single run can be poor.

# Step 3: Read the clusters
km$cluster            # cluster assignment per observation
km$centers            # centroids, in SCALED units
km$size               # observations per cluster
km$tot.withinss       # total within-cluster sum of squares
km$betweenss / km$totss   # proportion of variance explained

# Step 4: Profile the clusters, and plot them
customers$cluster <- factor(km$cluster)
aggregate(. ~ cluster, data = customers, FUN = mean)   # profile in REAL units

plot(customers$income, customers$age, col = km$cluster, pch = 19,
     xlab = "Annual income", ylab = "Age", main = "Customer segments")

# --- CHOOSING k: the elbow method ---
# Step 5: Choose k by the elbow method
wss <- sapply(1:10, function(k) kmeans(scaled, k, nstart = 10)$tot.withinss)
plot(1:10, wss, type = "b", pch = 19,
     xlab = "Number of clusters k", ylab = "Within-cluster sum of squares")
# WSS always falls as k rises -- at k = n it is zero. The "elbow" is where
# extra clusters stop buying much.

# --- A less subjective alternative: the silhouette ---
# library(cluster)
# sil <- silhouette(km$cluster, dist(scaled)); mean(sil[, 3])

# COMPARE: without scaling, the clustering is driven by income alone.
# Step 6: Cluster without scaling, and compare
km_raw <- kmeans(customers[, 1:2], centers = 3, nstart = 25)
table(km$cluster, km_raw$cluster)   # the two solutions differ
