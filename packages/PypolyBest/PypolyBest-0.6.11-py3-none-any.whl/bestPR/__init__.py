#Libraries
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler

class polyBest:
    def __init__(data, X, y, param, split, scale):
        data.X = X
        data.y = y
        data.param=param
        data.split=split
        data.scale = scale

        data.msescore=[]
        data.maescore=[]
        
        X_train, X_test, y_train, y_test = train_test_split(data.X, data.y, test_size = data.split)
        
        if(scale):
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
        
        for i in range(len(data.param)):
            
            polynomial_features= PolynomialFeatures(degree=i+1)
            X_train_trf = polynomial_features.fit_transform(X_train)
            X_test_trf = polynomial_features.fit_transform(X_test)
            
            lasso1=Lasso(alpha=data.param[i])
            lasso1.fit(X_train_trf, y_train)
            y_predlasso1 = lasso1.predict(X_test_trf)
            
            err = mean_squared_error(y_predlasso1, y_test)
            data.msescore.append(err)
            err1 = mean_absolute_error(y_predlasso1, y_test)
            data.maescore.append(err1)

    def mseScore(data):
        return data.msescore
    def maeScore(data):
        return data.maescore



