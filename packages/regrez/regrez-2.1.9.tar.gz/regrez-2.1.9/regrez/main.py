import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score
class ModelNotTrainedException(Exception):
    "You tried to test the model before training it."
    pass
class Simple:
    def __init__(self, csv_path, label_x, label_y):
        self.csv = csv_path
        self.x_label = label_x
        self.y_label = label_y
        self.file = pd.read_csv(self.csv)
        self.data = self.file[[self.x_label, self.y_label]]
        self.coef = 0
        self.intercept = 0
        self.x = np.asanyarray(self.data[[self.x_label]])
        self.y = np.asanyarray(self.data[[self.y_label]])
        self.reg = linear_model.LinearRegression()
    def TrainAndTest(self):
        file = pd.read_csv(self.csv)
        data = file[[self.x_label, self.y_label]]
        msk = np.random.rand(len(file)) < 0.8
        train = data[msk]
        test = data[~msk]
        reg = linear_model.LinearRegression()
        train_x = np.asanyarray(train[[self.x_label]])
        train_y = np.asanyarray(train[[self.y_label]])
        reg.fit(train_x, train_y)
        self.coef = reg.coef_
        self.intercept = reg.intercept_
        print(f"Coefficient -> {self.coef} | Intercept -> {reg.intercept_}")
        test_x = np.asanyarray(test[[self.x_label]])
        test_y = np.asanyarray(test[[self.y_label]])
        predicted_y = reg.predict(test_x)
        print("Mean absolute error: %.2f" % np.mean(np.absolute(predicted_y - test_y)))
        print("Residual sum of squares (MSE): %.2f" % np.mean((predicted_y - test_y) ** 2))
        print("R2-score: %.2f" % r2_score(test_y , predicted_y) )
    def Train(self):
        self.reg.fit(self.x, self.y)
        self.coef = self.reg.coef_
        self.intercept = self.reg.intercept_
        print(f"Coefficient -> {self.coef} | Intercept -> {self.reg.intercept_}")
    def Test(self, test_x, test_y):
        if(self.coef == 0):
            raise ModelNotTrainedException
        else:
            predicted_y = self.reg.predict(test_x)
            print("Mean absolute error: %.2f" % np.mean(np.absolute(predicted_y - test_y)))
            print("Residual sum of squares (MSE): %.2f" % np.mean((predicted_y - test_y) ** 2))
            print("R2-score: %.2f" % r2_score(test_y , predicted_y) )
    def Visualize(self):
        plt.scatter(self.data[self.x_label], self.data[self.y_label], color='blue')
        plt.plot(self.x, self.coef[0][0]*self.x + self.intercept[0], '-r')
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.show()
#---------------------------------------------------------------------------------------------------------------#
class Multiple:
    def __init__(self, csv_path, labels_x, labels_y): #Multiple("path", ["a", "b"], "c")
        self.csv = csv_path
        self.x_labels = labels_x
        self.y_labels = labels_y
        self.labels = labels_x + labels_y
        self.file = pd.read_csv(self.csv)
        self.data = self.file[self.labels]
        self.coef = 0
        self.intercept = 0
        self.x = np.asanyarray(self.data[self.x_labels])
        self.y = np.asanyarray(self.data[self.y_labels])
        self.reg = linear_model.LinearRegression()
    def TrainAndTest(self):
        file = pd.read_csv(self.csv)
        data = file[self.labels]
        msk = np.random.rand(len(file)) < 0.8
        train = data[msk]
        test = data[~msk]
        reg = linear_model.LinearRegression()
        train_x = np.asanyarray(train[self.x_labels])
        train_y = np.asanyarray(train[self.y_labels])
        reg.fit(train_x, train_y)
        self.coef = reg.coef_
        self.intercept = reg.intercept_
        print(f"Coefficient -> {self.coef} | Intercept -> {reg.intercept_}")
        test_x = np.asanyarray(test[self.x_labels])
        test_y = np.asanyarray(test[self.y_labels])
        predicted_y = reg.predict(test_x)

        print("Residual sum of squares (MSE): %.2f" % np.mean((predicted_y - test_y) ** 2))
        print("Variance score: %.2f" % reg.score(test_x , test_y) )
    def Train(self):
        self.reg.fit(self.x, self.y)
        self.coef = self.reg.coef_
        self.intercept = self.reg.intercept_
        print(f"Coefficient -> {self.coef} | Intercept -> {self.reg.intercept_}")
    def Test(self, test_x, test_y):
        if(self.coef == 0):
            raise ModelNotTrainedException
        else:
            predicted_y = self.reg.predict(test_x)
            print("Residual sum of squares (MSE): %.2f" % np.mean((predicted_y - test_y) ** 2))
            print("Variance score: %.2f" % self.reg.score(test_x , test_y) )