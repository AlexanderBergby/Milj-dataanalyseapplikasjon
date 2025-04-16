import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

data = "data/weather_data.csv"  

df = pd.read_csv(data)

#Predikere gjennomsnittstemperatur basert på vindhastighet og nedbør
#Resultatene er dårlige nå, men vil forhåpentligvis bli bedre med mer data
X = df[['wind_speed', 'precipitation']]
y = df['avg_temp']

# Deler data inn i trenings- og testsett
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Trener modellen
modell = LinearRegression()
modell.fit(X_train, y_train)

# Gjør prediksjoner
y_pred = modell.predict(X_test)

# Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
# Root Mean Squared Error (RMSE)
rmse = mse ** 0.5

# Sjekker modellens ytelse
print("RMSE:", rmse)
print("R²-score:", r2_score(y_test, y_pred))