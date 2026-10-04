# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 15: Text mining and word cloud
# Python equivalent: python/15_text_mining.py

library(tm); library(wordcloud); library(RColorBrewer)

# Step 1: Enter the reviews
reviews <- c(
  "The data science course is excellent and the teaching is excellent",
  "Excellent course with excellent practical data examples",
  "The practical sessions are useful but the course is fast",
  "Data analysis practical work is the best part of this course",
  "Teaching on this course is good and the data examples are practical")

# --- THE PREPROCESSING PIPELINE -- each step earns marks ---
# Step 2: Clean the text: case, punctuation, numbers, stop words, stems
corpus <- Corpus(VectorSource(reviews))
corpus <- tm_map(corpus, content_transformer(tolower))   # case-fold
corpus <- tm_map(corpus, removePunctuation)              # "data." -> "data"
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removeWords, stopwords("english"))  # the, is, and...
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, stemDocument)                   # running -> run

# --- TERM-DOCUMENT MATRIX ---
# Step 3: Count the terms
tdm <- TermDocumentMatrix(corpus)
m <- as.matrix(tdm)
freq <- sort(rowSums(m), decreasing = TRUE)
head(freq, 10)
inspect(tdm)

# --- WORD CLOUD ---
# Step 4: Draw the word cloud and a bar chart
set.seed(42)
wordcloud(names(freq), freq, min.freq = 1, max.words = 100,
          random.order = FALSE, colors = brewer.pal(8, "Dark2"))

barplot(head(freq, 8), las = 2, col = "#1e7fbf",
        main = "Most frequent terms")

# --- TF-IDF: weight by how DISTINCTIVE a term is ---
# Step 5: Weight the terms by TF-IDF
tdm_tfidf <- TermDocumentMatrix(corpus,
               control = list(weighting = weightTfIdf))
# TF-IDF(t,d) = TF(t,d) * log(N / DF(t))
#
# "course" appears in all 5 documents, so DF = N = 5, log(5/5) = 0, and its
# TF-IDF is EXACTLY ZERO. A term present everywhere distinguishes nothing.
# That is the whole point of the weighting, and it is why TF-IDF beats raw
# counts for finding what a document is actually ABOUT.

# Step 6: Find the frequent and the associated terms
findFreqTerms(tdm, lowfreq = 3)
findAssocs(tdm, "practic", 0.5)     # note the STEM, not "practical"

# STEMMING vs LEMMATISATION (a standard two-mark question):
#   stemming       chops suffixes mechanically; may give a non-word
#                  "studies" -> "studi"      fast
#   lemmatisation  uses vocabulary and grammar; returns a real word
#                  "studies" -> "study"      slower, more accurate
