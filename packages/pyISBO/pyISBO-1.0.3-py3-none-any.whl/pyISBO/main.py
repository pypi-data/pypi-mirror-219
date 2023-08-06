from SBO_pulp.AutoRegression import AR
import pandas as pd

data = pd.read_excel("OperationData.xlsx")
parameterInfo = pd.read_excel("OperationData.xlsx", 1)
y = data.pop("y")
m = AR(parameterInfo, "neg_mean_squared_error")
m.fit(data, y)
m.MIP_transform()
m.optimize()
print(m.optimizedParameter)
print(m.output)