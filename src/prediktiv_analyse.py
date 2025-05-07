import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def prediktiv():
    #Sier hvilken data som skal brukes
    data = "data/weather_data.csv"
    
    try:
        df = pd.read_csv(data)
    except FileNotFoundError:
        print(f"Filen '{data}' finnes ikke. Kjør alternativ 2 i menyen først for å hente værdata.")
        return

    # Sjekk at nødvendige kolonner finnes
    if not {'wind_speed', 'precipitation', 'avg_temp'}.issubset(df.columns):
        print("Datasettet mangler nødvendige kolonner for prediktiv analyse.")
        return

    #Predikere gjennomsnittstemperatur basert på vindhastighet og nedbør
    #Resultatene er dårlige nå, men vil forhåpentligvis bli bedre med mer data
    X = df[['wind_speed', 'precipitation']]
    y = df['avg_temp']

    # Deler data inn i trenings- og testsett
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #Trener modellen
    modell = LinearRegression()
    modell.fit(X_train, y_train)

    #Gjør prediksjoner
    y_pred = modell.predict(X_test)

    #Mean Squared Error (MSE)
    mse = mean_squared_error(y_test, y_pred)
    #Root Mean Squared Error (RMSE)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    print("\nResultater fra prediktiv analyse:")
    print(f" - RMSE: {rmse:.2f}")
    print(f" - R²-score: {r2:.2f}")
    print("\nMerk: Resultatene vil forbedres med mer variert og historisk data.")

#For testing
if __name__ == "__main__":
    prediktiv()
