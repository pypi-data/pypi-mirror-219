def index():
    print("""
  Practical 1
  1a) K-Means Clustering:
      Clustering algorithms for unsupervised classification. Read a
      datafile grades_km_input.csv and apply k.means clustering. Plot the cluster data using
      R visualizations.

  1b) Apriori Algorithm (PBL):
      Implement Apriori Algorithm Recommending grocery items to a
      customer that is most frequently bought together, given a data set of transactions by
      customers of a store, using Ariory algorithm using Market_Basket_Optimisation.csv file.

-------------------------------------------------------------------------------------------------

  Practical 2
  2a) Regression Model:
      Import data from web storage – binary.csv. Name the dataset and do
      Logistic Regression to find out relation between variables that are affecting the
      admission of a student in an institute based on his or her GRE score, GPA obtained and rank
      of the student. Also check the model is fit or not.

  2b) MULTIPLE REGRESSION MODEL:
      Apply multiple regressions, if data have a continuous independent variable.
      Apply on above dataset – binary.csv.


  2c) Design a Simple Linear Regression Model using the above dataset.
      (HINT: consider GRE Score or GPA score as independent variable.

-------------------------------------------------------------------------------------------------

  Practical 3
  3a) Decision Tree:
      Implement Decision Tree classification technique using Social_Network_Ads.csv dataset.

  3b) SVM Classification:
      Implement SVM Classification technique using Social_Network_Ads.csv dataset.
      Evaluate the performance of classifier.

-------------------------------------------------------------------------------------------------

  Practical 4
  4a) Naïve Bayes Classification:
      Implement Naïve Bayes Classification technique using
      Social_Network_Ads.csv dataset. Evaluate the performance of classifier.

  4b) Text Analysis (PBL):
      Find the confusion matrix to find restaurant review based of sentiment analysis
      of Natural Language processing. Use Resaurentreviews.tsv file for your study.

-------------------------------------------------------------------------------------------------

  Practical 5
  Comparative Study of various machine learning models (Newly added):
  Take the inbuilt data file: iris and perform classification on that data using various
  classification models – Decision Tree, K Nearest Neighbour and Support Vector Machine.
  Find the confusion matrix for all three models and evaluate them by finding their accuracy.
  Find the algorithm which performs best on the given data file, out of all these three models.

-------------------------------------------------------------------------------------------------

  Practical 6
  Install, configure and run Hadoop and HDFS and explore HDFS on Windows

-------------------------------------------------------------------------------------------------

  Practical 7
  Implement word count / frequency programs using MapReduce.

-------------------------------------------------------------------------------------------------

  Practical 8
  Implement an application that stores big data in Hbase / MongoDB and manipulate it using R / Python.

-------------------------------------------------------------------------------------------------



          """)
          



def prog(num):
    if(num=="1a"):
        print(""" 


    dataset <- read.csv("Mall_Customers.csv")
    head(dataset)

    dataset <- dataset[4:5]
    head(dataset)

    wcss <- vector()
    for (i in 1:10) {
      wcss[i] <- sum(kmeans(dataset, i)$withinss)
    }

    plot(1:10, wcss, type = 'b',
         main = paste('The Elbow Method'),
         xlab = 'Number of Clusters',
         ylab = 'WSS')

    kmeans <- kmeans(x = dataset, centers = 5)
    y_means <- kmeans$cluster

    install.packages('cluster')
    library(cluster)

    clusplot(dataset,
             y_means,
             lines = 0,
             shade = TRUE,
             color = TRUE,
             labels = 2,
             main = paste('Clusters of Customers'),
             xlab = 'Annual Income',
             ylab = 'Spending score')
    


        
              """) 

        
    elif(num=="1b"):
        print("""

  install.packages('arules')
  install.packages('arulesViz')
  install.packages('RColorBrewer')

  library(arules)
  library(arulesViz)
  library(RColorBrewer)

  # import dataset
  data(Groceries)
  Groceries
  summary(Groceries)
  class(Groceries)

  # using apriori() function
  rules <- apriori(Groceries, parameter = list(supp = 0.02, conf = 0.2))
  summary(rules)

  # using inspect() function
  inspect(rules[1:10])

  # using itemFrequencyPlot() function
  arules::itemFrequencyPlot(Groceries, topN = 20,
                            col = brewer.pal(8, 'Pastel2'),
                            main = 'Relative Item Frequency Plot',
                            type = 'relative',
                            ylab = 'Item Frequency (Relative)')

  itemsets <- apriori(Groceries, parameter = list(minlen = 2, maxlen = 2, support = 0.02, target = 'frequent itemsets'))
  summary(itemsets)

  # using inspect() function
  inspect(itemsets[1:10])

  itemsets_3 <- apriori(Groceries, parameter = list(minlen = 3, maxlen = 3, support = 0.02, target = 'frequent itemsets'))
  summary(itemsets_3)

  # using inspect() function
  inspect(itemsets_3)
  
  install.packages('arules')
  install.packages('arulesViz')
  install.packages('RColorBrewer')

  library(arules)
  library(arulesViz)
  library(RColorBrewer)

  # import dataset
  data(Groceries)
  Groceries
  summary(Groceries)
  class(Groceries)

  # using apriori() function
  rules <- apriori(Groceries, parameter = list(supp = 0.02, conf = 0.2))
  summary(rules)

  # using inspect() function
  inspect(rules[1:10])

  # using itemFrequencyPlot() function
  arules::itemFrequencyPlot(Groceries, topN = 20,
                            col = brewer.pal(8, 'Pastel2'),
                            main = 'Relative Item Frequency Plot',
                            type = 'relative',
                            ylab = 'Item Frequency (Relative)')

  itemsets <- apriori(Groceries, parameter = list(minlen = 2, maxlen = 2, support = 0.02, target = 'frequent itemsets'))
  summary(itemsets)

  # using inspect() function
  inspect(itemsets[1:10])

  itemsets_3 <- apriori(Groceries, parameter = list(minlen = 3, maxlen = 3, support = 0.02, target = 'frequent itemsets'))
  summary(itemsets_3)

  # using inspect() function
  inspect(itemsets_3)
  
  install.packages('arules')
  install.packages('arulesViz')
  install.packages('RColorBrewer')

  library(arules)
  library(arulesViz)
  library(RColorBrewer)

  # import dataset
  data(Groceries)
  Groceries
  summary(Groceries)
  class(Groceries)

  # using apriori() function
  rules <- apriori(Groceries, parameter = list(supp = 0.02, conf = 0.2))
  summary(rules)

  # using inspect() function
  inspect(rules[1:10])

  # using itemFrequencyPlot() function
  arules::itemFrequencyPlot(Groceries, topN = 20,
                            col = brewer.pal(8, 'Pastel2'),
                            main = 'Relative Item Frequency Plot',
                            type = 'relative',
                            ylab = 'Item Frequency (Relative)')

  itemsets <- apriori(Groceries, parameter = list(minlen = 2, maxlen = 2, support = 0.02, target = 'frequent itemsets'))
  summary(itemsets)

  # using inspect() function
  inspect(itemsets[1:10])

  itemsets_3 <- apriori(Groceries, parameter = list(minlen = 3, maxlen = 3, support = 0.02, target = 'frequent itemsets'))
  summary(itemsets_3)

  # using inspect() function
  inspect(itemsets_3)
  

                """)
        
        

    elif(num=="2a"):
        print("""

  # Fetch data
  college <- read.csv('https://raw.githubusercontent.com/csquared/udacity-dlnd/master/nn/binary.csv')
  head(college)
  nrow(college)

  # Install required package
  # install.packages('caTools')

  # Load library
  library(caTools)

  # Splitting the dataset
  split <- sample.split(college, SplitRatio = 0.75)
  split

  training_reg <- subset(college, split == TRUE)
  test_reg <- subset(college, split == FALSE)

  # Training Model
  fit_logistic_model <- glm(admit ~ .,
                            data = training_reg,
                            family = 'binomial')

  # Predict test data based on model
  predict_reg <- predict(fit_logistic_model, test_reg, type = 'response')
  predict_reg

  # Plotting
  cdplot(as.factor(admit) ~ gpa, data = college)
  cdplot(as.factor(admit) ~ gre, data = college)
  cdplot(as.factor(admit) ~ rank, data = college)

  # Changing probabilities
  predict_reg <- ifelse(predict_reg > 0.5, 1, 0)
  predict_reg

  # Evaluating model
  # Using confusion matrix
  table(test_reg$admit, predict_reg)

                """)
        
    elif(num=="2b"):
        print("""


  # Fetch data
  college <- read.csv('https://raw.githubusercontent.com/csquared/udacity-dlnd/master/nn/binary.csv')
  head(college)
  nrow(college)

  # Install required package
  # install.packages('caTools')

  # Load library
  library(caTools)

  # Splitting the dataset
  split <- sample.split(college, SplitRatio = 0.75)
  split

  training_reg <- subset(college, split == 'TRUE')
  test_reg <- subset(college, split == 'FALSE')

  # Training Model
  fit_MRegressor_model <- lm(formula = admit ~ gre + gpa + rank,
                             data = training_reg)

  # Predict test data based on model
  predict_reg <- predict(fit_MRegressor_model, newdata = test_reg)
  predict_reg

  # Plotting
  cdplot(as.factor(admit) ~ gpa, data = college)
  cdplot(as.factor(admit) ~ gre, data = college)
  cdplot(as.factor(admit) ~ rank, data = college)

  # Changing probabilities
  predict_reg <- ifelse(predict_reg > 0.5, 1, 0)
  predict_reg

  # Evaluating model
  # Using confusion matrix
  table(test_reg$admit, predict_reg)
              

                """)
    
    elif(num=="2c"):
        print("""


college <- read.csv("https://raw.githubusercontent.com/csquared/udacity-dlnd/master/nn/binary.csv")
head(college)
nrow(college)
install.packages("caTools")
library(caTools)
split <- sample.split(college, SplitRatio = 0.75)
split
training_reg <- subset(college, split == "TRUE")
test_reg <- subset(college, split == "FALSE")
fit_MRegressor_model <- lm(formula = admit ~ gre + gpa + rank, data = training_reg)
predict_reg <- predict(fit_MRegressor_model, newdata = test_reg)
predict_reg
cdplot(as.factor(admit) ~ gpa, data = college)
cdplot(as.factor(admit) ~ gre, data = college)
cdplot(as.factor(admit) ~ rank, data = college)
              
                """)


    elif(num=="3a"):
        print("""


  # Read the dataset
  dataset <- read.csv("Social_Network_Ads.csv")
  print(dataset)

  # Subset the dataset
  dataset <- dataset[3:5]
  print(dataset)

  # Convert 'Purchased' column to factor
  dataset$Purchased <- factor(dataset$Purchased, levels = c(0, 1))
  print(dataset$Purchased)

  # Install and load required packages
  install.packages('caTools')
  library(caTools)

  # Splitting the dataset
  set.seed(123)
  split <- sample.split(dataset$Purchased, SplitRatio = 0.75)
  training_set <- subset(dataset, split == TRUE)
  test_set <- subset(dataset, split == FALSE)

  # Scaling the features
  training_set[-3] <- scale(training_set[-3])
  test_set[-3] <- scale(test_set[-3])
  print(test_set[-3])

  # Install and load 'rpart' package
  install.packages('rpart')
  library(rpart)

  # Train the classifier
  classifier <- rpart(formula = Purchased ~ ., data = training_set)
  y_pred <- predict(classifier, newdata = test_set[-3], type = 'class')
  print(y_pred)

  # Create confusion matrix
  cm <- table(test_set[, 3], y_pred)
  print(cm)

  # Install and load 'ElemStatLearn' package
  install.packages("ElemStatLearn")
  library(ElemStatLearn)

  # Prepare grid for visualization
  set <- training_set
  x1 <- seq(min(set[, 1])-1, max(set[, 1])+1, by = 0.01)
  x2 <- seq(min(set[, 1])-1, max(set[, 1])+1, by = 0.01)
  grid_set <- expand.grid(x1, x2)
  colnames(grid_set) <- c('Age', 'EstimatedSalary')
  y_grid <- predict(classifier, newdata = grid_set, type = "class")

  # Plot the decision boundaries
  plot(set[, -3],
       main = 'Decision Tree Classification (Training set)',
       xlab = 'Age', ylab = 'Estimated Salary',
       xlim = range(x1), ylim = range(x2))
  contour(x1, x2, matrix(as.numeric(y_grid), length(x1), length(x2)), add = TRUE)
  points(grid_set, pch = '.', col = ifelse(y_grid == 1, 'springgreen3', 'tomato'))
  points(set, pch = 21, bg = ifelse(set[,-3] == 1, 'green4', 'red3'))

  # Plot the decision tree
  plot(classifier)
  text(classifier)


                """)
        
    elif(num=="3b"):
        print("""


    # Read the dataset
    dataset <- read.csv("/Social_Network_Ads.csv")
    print(dataset)

    # Subset the dataset
    dataset <- dataset[3:5]
    print(dataset)

    # Convert "Purchased" column to factor
    dataset$Purchased <- factor(dataset$Purchased, levels = c(0, 1))
    print(dataset$Purchased)

    # Install and load required packages
    install.packages("e1071")
    library(e1071)

    # Splitting the dataset
    set.seed(123)
    split <- sample.split(dataset$Purchased, SplitRatio = 0.75)
    training_set <- subset(dataset, split == TRUE)
    test_set <- subset(dataset, split == FALSE)

    # Scaling the features
    training_set[-3] <- scale(training_set[-3])
    test_set[-3] <- scale(test_set[-3])
    print(test_set[-3])

    # Install and load "ElemStatLearn" package
    install.packages("ElemStatLearn")
    library(ElemStatLearn)

    # Train the SVM classifier
    classifier <- svm(formula = Purchased ~ ., data = training_set, type = "C-classification", kernel = "linear")
    y_pred <- predict(classifier, newdata = test_set[-3], type = "class")
    print(y_pred)

    # Create confusion matrix
    cm <- table(test_set[, 3], y_pred)
    print(cm)

    # Prepare grid for visualization
    set <- training_set
    x1 <- seq(min(set[, 1]) - 1, max(set[, 1]) + 1, by = 0.01)
    x2 <- seq(min(set[, 1]) - 1, max(set[, 1]) + 1, by = 0.01)
    grid_set <- expand.grid(x1, x2)
    colnames(grid_set) <- c("Age", "EstimatedSalary")
    y_grid <- predict(classifier, newdata = grid_set, type = "class")

    # Plot the SVM decision boundaries
    plot(set[, -3],
         main = "SVM (Training set)",
         xlab = "Age", ylab = "Estimated Salary",
         xlim = range(x1), ylim = range(x2))
    contour(x1, x2, matrix(as.numeric(y_grid), length(x1), length(x2)), add = TRUE)
    points(grid_set, pch = ".", col = ifelse(y_grid == 1, "springgreen3", "tomato"))
    points(set, pch = 21, bg = ifelse(set[, -3] == 1, "green4", "red3"))

    # Plot the SVM model
    plot(classifier)
    text(classifier)

                """)


    elif(num=="4a"):
        print("""


# Read the dataset
dataset <- read.csv("C:\\Users\\admin\\Downloads\\Social_Network_Ads.csv")
dataset <- dataset[3:5]
dataset$Purchased <- factor(dataset$Purchased, levels = c(0, 1))

# Install and load required packages
install.packages('caTools')
library(caTools)
install.packages('e1071')
library(e1071)

# Splitting the dataset
set.seed(123)
split <- sample.split(dataset$Purchased, SplitRatio = 0.75)
training_set <- subset(dataset, split == TRUE)
test_set <- subset(dataset, split == FALSE)

# Scaling the features
training_set[-3] <- scale(training_set[-3])
test_set[-3] <- scale(test_set[-3])

# Train the Naive Bayes classifier
classifier <- naiveBayes(x = training_set[-3], y = training_set$Purchased)
y_pred <- predict(classifier, newdata = test_set[-3])

# Create confusion matrix
cm <- table(test_set[, 3], y_pred)
print(cm)
        
                """)



    elif(num=="4b"):
        print(""" 


dataset_original <- read.delim('C:/Users/Aditi/Documents/RStudio Practicals/Restaurant_Reviews.tsv', quote = '', stringsAsFactors = FALSE)
install.packages('tm')
install.packages('SnowballC')
library(tm)
library(SnowballC)

corpus <- VCorpus(VectorSource(dataset_original$Review))
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeWords, stopwords())
corpus <- tm_map(corpus, stemDocument)
corpus <- tm_map(corpus, stripWhitespace)

dtm <- DocumentTermMatrix(corpus)
dtm <- removeSparseTerms(dtm, 0.999)
dataset <- as.data.frame(as.matrix(dtm))
dataset$Liked <- dataset_original$Liked
print(dataset$Liked)
dataset$Liked <- factor(dataset$Liked, levels = c(0, 1))

install.packages('caTools')
library(caTools)
set.seed(123)
split <- sample.split(dataset$Liked, SplitRatio = 0.8)
training_set <- subset(dataset, split == TRUE)
test_set <- subset(dataset, split == FALSE)

install.packages('randomForest')
library(randomForest)
classifier <- randomForest(x = training_set[-692], y = training_set$Liked, ntree = 10)
y_pred <- predict(classifier, newdata = test_set[-692])
cm <- table(test_set[, 692], y_pred)
print(cm)
         
            
        """)

    


    elif(num=="5"):
        print(""" 


  install.packages('rpart')
  install.packages('rpart.plot')
  install.packages('gmodels')
  install.packages('e1071')
  library(rpart)
  library(rpart.plot)
  library(gmodels)
  library(e1071)

  data(iris)
  summary(iris)

  # Normalize the continuous variables before performing any analysis on DATASET
  temp <- as.data.frame(scale(iris[,1:4]))
  temp$species <- iris$Species # Levels: setosa, versicolor, virginica
  summary(temp)

  # Splitting the dataset into the training set and test set
  install.packages('caTools')
  library(caTools)

  set.seed(123)
  split <- sample.split(temp$species, SplitRatio = 0.75)
  train <- subset(temp, split == TRUE)
  test <- subset(temp, split == FALSE)

  nrow(train)
  nrow(test)

  # 1. Decision Tree
  dt_classifier <- rpart(formula = species ~ ., data = train)

  # Predicting the test set results
  dt_y_pred <- predict(dt_classifier, newdata = test, type = 'class')
  print(dt_y_pred)

  # Making the confusion matrix for decision tree
  cm <- table(test$species, dt_y_pred)
  print(cm)

  # Accuracy of DT model
  DTaccu <- ((12 + 9 + 11) / nrow(test)) * 100 # True positive numbers of 3x3 confusion matrix
  DTaccu

  # 2. K-Nearest Neighbours
  install.packages('class')
  library(class)

  c1 <- train$species
  set.seed(1234)
  knn_y_pred <- knn(train[, 1:4], test[, 1:4], c1, k = 3)
  # knn_y_pred <- knn(train[,1:4], test[,1:4], c1, k = 5)

  # Confusion matrix of k-nearest neighbors
  cm <- table(test$species, knn_y_pred)
  print(cm)

  # Accuracy for KNN model
  KNNaccu <- ((12 + 11 + 11) / nrow(test)) * 100 # True positive numbers of 3x3 confusion matrix
  KNNaccu

  # 3. Support Vector Machine
  require(e1071)
  svmclassifier <- svm(species ~ ., data = train)
  svm_y_pred <- predict(svmclassifier, newdata = test)
  cm <- table(test$species, svm_y_pred)
  print(cm)

  # Accuracy of SVM model
  SVMaccu <- ((12 + 11 + 11) / nrow(test)) * 100 # True positive numbers of 3x3 confusion matrix
  SVMaccu

  # Decision Tree vs KNN
  which(dt_y_pred != knn_y_pred)

  # Decision Tree vs SVM
  which(dt_y_pred != svm_y_pred)

  # SVM vs KNN
  which(svm_y_pred != knn_y_pred) # Both are equal

  # Comparison of the accuracy of different models on testing dataset
  models <- data.frame(Technique = c('Decision Tree', 'kNN', 'SVM'), Accuracy_Percentage = c(88.88889, 94.44444, 94.44444))
  models

        """)
    
    
    elif(num=="6"):
        print("""

     Install, configure and run Hadoop and HDFS

               
                """)



    elif(num=="7"):
        print("""



  Open command prompt as administrator and run the following command to create an input
  and output folder on the Hadoop file system, to which we will be moving the sample.txt file
  for our analysis.

  C:\hadoop-3.3.0\sbin>start-dfs.cmd
  C:\hadoop-3.3.0\sbin>start-yarn.cmd
  C:\hadoop-3.3.0\bin>cd\ 
  C:\>hadoop dfsadmin -safemode leave
  C:\>hadoop fs -mkdir /input_dir

  Check it by giving the following URL at browser
  http://localhost:9870
  Utilities -> browse the file system

  C:\> hadoop fs -put C:/input.txt /input_dir
  C:\>Hadoop fs -ls /input_dir/
  C:\>hadoop dfs -cat /input_dir/input_file.txt

  C:\>hadoop jar C:/hadoop-3.3.0/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.0.jar wordcount /input_dir /output_dir
  C:\> hadoop jar C:/MapReduceClient.jar wordcount /input_dir /output_dir

  Now, check the output_dir on browser as follows:
  Click on output_dir → part-r-00000 → Head the file (first 32 K) and check the file content as
  the output.

  Alternatively, you may type the following command on CMD window as:
  C:\> hadoop dfs -cat /output_dir/*
              
   
                """)
    
    

    elif(num=="8"):
        print("""

  

  Install mongoDB

  Open new command prompt
  >> C:\users\admin> cd\
  >> C:\>md data\db
  >> C:\> cd C:\Program Files\MongoDB\Server\4.0\bin
  >> C:\Program Files\MongoDB\Server\4.0\bin> mongod
  (in case error then)
  >> C:\Program Files\MongoDB\Server\4.0\bin> mongod –repair

  Open new command prompt
  >> C:\users\admin> cd C:\Program Files\MongoDB\Server\4.0\bin
  >> C:\Program Files\MongoDB\Server\4.0\bin>mongo
  >> show dbs

  Open new command prompt and Install PyMongo
  >> C:\users\admin> pip install pymongo

  Code:
  import pymongo
  myclient = pymongo.MongoClient('mongodb://localhost:27017/')
  mydb = myclient['mybigdata']
  print(myclient.list_database_names())

  mycol = mydb['student']
  print(mydb.list_collection_names())

  mycol = mydb['student']
  mydict = {'name':'Beena', 'address':'Mumbai'}
  x = mycol.insert_one(mydict)

  mylist = [
    {'name':'Khyati', 'address':'Mumbai'},
    {'name':'Kruti', 'address':'Mumbai'},
    {'name':'Nidhi', 'address':'Pune'},
    {'name':'Komal', 'address':'Pune'}
  ]
  x = mycol.insert_many(mylist)

  Output:
  Check database and data inserted in collection
  >> show dbs
  >> use mybigdata
  >> show collections
  >> db.student.findOne()
  >> db.student.count()
  

         
                """)

    



    else:
        print("invalid input")



