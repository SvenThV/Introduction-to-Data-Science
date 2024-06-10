import os
import pandas as pd

# Feature engineering is a crucial step in preparing your data for machine learning models. 
# Here, we'll extract additional features from the date column and demonstrate how to aggregate weather data if necessary.

# Load the datasets
base_path = '/mnt/data'  # Adjust this path to your dataset's location
train_file = os.path.join('Kaggle Competition', 'train.csv')
test_file = os.path.join('Kaggle Competition', 'test.csv')
wetter_file = os.path.join('Kaggle Competition', 'wetter.csv')
kiwo_file = os.path.join('Kaggle Competition', 'kiwo.csv')

train_df = pd.read_csv(train_file)
test_df = pd.read_csv(test_file)
wetter_df = pd.read_csv(wetter_file)
kiwo_df = pd.read_csv(kiwo_file)

# Convert date columns to datetime format
train_df['Datum'] = pd.to_datetime(train_df['Datum'])
test_df['Datum'] = pd.to_datetime(test_df['Datum'])
wetter_df['Datum'] = pd.to_datetime(wetter_df['Datum'])
kiwo_df['Datum'] = pd.to_datetime(kiwo_df['Datum'])

# Merge the datasets
train_df = pd.merge(train_df, wetter_df, on='Datum', how='left')
test_df = pd.merge(test_df, wetter_df, on='Datum', how='left')

train_df = pd.merge(train_df, kiwo_df, on='Datum', how='left')
test_df = pd.merge(test_df, kiwo_df, on='Datum', how='left')

train_df['KielerWoche'] = train_df['KielerWoche'].fillna(0)
test_df['KielerWoche'] = test_df['KielerWoche'].fillna(0)

# Handle missing values in weather-related columns
train_df['Bewoelkung'] = train_df['Bewoelkung'].fillna(train_df['Bewoelkung'].mean())
train_df['Temperatur'] = train_df['Temperatur'].fillna(train_df['Temperatur'].mean())
train_df['Windgeschwindigkeit'] = train_df['Windgeschwindigkeit'].fillna(train_df['Windgeschwindigkeit'].mean())
train_df['Wettercode'] = train_df['Wettercode'].fillna(train_df['Wettercode'].mode()[0])

test_df['Bewoelkung'] = test_df['Bewoelkung'].fillna(test_df['Bewoelkung'].mean())
test_df['Temperatur'] = test_df['Temperatur'].fillna(test_df['Temperatur'].mean())
test_df['Windgeschwindigkeit'] = test_df['Windgeschwindigkeit'].fillna(test_df['Windgeschwindigkeit'].mean())
test_df['Wettercode'] = test_df['Wettercode'].fillna(test_df['Wettercode'].mode()[0])

# Feature engineering: Extract additional features from the date column
def extract_date_features(df):
    df['Year'] = df['Datum'].dt.year
    df['Month'] = df['Datum'].dt.month
    df['Day'] = df['Datum'].dt.day
    df['DayOfWeek'] = df['Datum'].dt.dayofweek
    df['WeekOfYear'] = df['Datum'].dt.isocalendar().week
    df['Quarter'] = df['Datum'].dt.quarter
    return df

train_df = extract_date_features(train_df)
test_df = extract_date_features(test_df)

# Optional: Aggregate weather data (e.g., daily averages)
def aggregate_weather_data(df):
    weather_columns = ['Bewoelkung', 'Temperatur', 'Windgeschwindigkeit']
    weather_agg = df.groupby('Datum')[weather_columns].mean().reset_index()
    return weather_agg

train_weather_agg = aggregate_weather_data(train_df)
test_weather_agg = aggregate_weather_data(test_df)

# Merge aggregated weather data back to the main dataframes if necessary
train_df = pd.merge(train_df, train_weather_agg, on='Datum', suffixes=('', '_agg'), how='left')
test_df = pd.merge(test_df, test_weather_agg, on='Datum', suffixes=('', '_agg'), how='left')

# Display the first few rows of the modified training dataset to verify the changes
print(train_df.head())
print(test_df.head())
