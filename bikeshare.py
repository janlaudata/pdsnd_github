import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Bitte geben Sie eine Stadt zum Analysieren (chicago, new york city oder washington) ein: ")

        if city.lower() in ["chicago", "new york city", "washington"]:
            print("Die Eingabe ist " + city)
            break
        else:
            print("Ungültige Eingabe. Bitte geben Sie eine der folgenden Städte ein: chicago, new york city oder washington.")

    months = ["january", "february", "march", "april", "may", "june"]

    while True:
        month = input("Bitte geben Sie einen Monatsnamen oder 'all' ein: ").lower()

        if month == "all" or month in months:
            if month == "all":
                print("Sie haben 'all' eingegeben. Das gilt für alle Monate.")
            else:
                print(f"Die Eingabe ist der Monat '{month.capitalize()}'.")
            break
        else:
            print("Ungültige Eingabe. Bitte geben Sie einen Monatsnamen oder 'all' ein.")

    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    while True:
        day = input("Bitte geben Sie einen Wochentag oder 'all' ein: ").lower()

        if day == "all" or day in days:
            if day == "all":
                print("Sie haben 'all' eingegeben. Das gilt für alle Wochentage.")
            else:
                print(f"Die Eingabe ist der Wochentag '{day.capitalize()}'.")
            break
        else:
            print("Ungültige Eingabe. Bitte geben Sie einen Wochentag oder 'all' ein.")

    print('-'*40)

    return city, month, day

def load_data(city, month, day):

# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    df['month'] = df['month'].astype(int)  # Konvertiere Monatszahl in int

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    month_counts = df['month'].value_counts()

    most_common_month_num = month_counts.idxmax()
    count = month_counts.max()

    months_names = ['Januar', 'Februar', 'März', 'April', 'Mai', 'June']
    most_common_month = months_names[most_common_month_num - 1]

    print("Häufigster Monat:", most_common_month)

    day_counts = df['day_of_week'].value_counts()
    most_common_day = day_counts.idxmax()
    count_day = day_counts.max()

    print(f"Häufigster Wochentag: {most_common_day} ({count_day} Vorkommnisse)")

    df['hour'] = df['Start Time'].dt.hour
    hour_counts = df['hour'].value_counts()
    most_common_hour = hour_counts.idxmax()
    count_hour = hour_counts.max()

    print(f"Häufigste Startstunde: {most_common_hour}:00 Uhr ({count_hour} Vorkommnisse)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Am häufigsten genutzte Startstation ermitteln
    most_common_start_station = df['Start Station'].mode().iloc[0]
    count_start_station = df['Start Station'].value_counts().max()

    # Am häufigsten genutzte Endstation ermitteln
    most_common_end_station = df['End Station'].mode().iloc[0]
    count_end_station = df['End Station'].value_counts().max()

    # Am häufigsten genutzte Verbindung ermitteln
    most_common_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    count_combination = df.groupby(['Start Station', 'End Station']).size().max()

    print(f"Häufigste Startstation: {most_common_start_station} ({count_start_station} Vorkommnisse)")
    print(f"Häufigste Endstation: {most_common_end_station} ({count_end_station} Vorkommnisse)")
    print(f"Häufigste Verbindung: Von '{most_common_combination[0]}' nach '{most_common_combination[1]}' ({count_combination} Vorkommnisse)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration ...\n')
    start_time = time.time()

    # Summe der Reisezeiten ermitteln
    total_travel_time_seconds = df['Trip Duration'].sum()

    # Durchschnittliche Reisezeit ermitteln
    average_travel_time_seconds = df['Trip Duration'].mean()

    # Formatieren der Zeit für die Ausgabe (in Tagen, Stunden, Minuten und Sekunden)
    total_travel_time_formatted = time.strftime("%d Tage %H Stunden %M Minuten %S Sekunden", time.gmtime(total_travel_time_seconds))
    average_travel_time_formatted = time.strftime("%H Stunden %M Minuten %S Sekunden", time.gmtime(average_travel_time_seconds))

    print(f"Gesamte Reisezeit: {total_travel_time_formatted}")
    print(f"Durchschnittliche Reisezeit: {average_travel_time_formatted}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    print('\nCalculating User Statistics...\n')
    start_time = time.time()

    # Anzahl der Benutzertypen zählen
    user_counts = df['User Type'].value_counts()

    print("Benutzertypen:")
    print(user_counts)

    if city != 'washington' and 'Gender' in df.columns and 'Birth Year' in df.columns:
        # Anzahl der Geschlechter zählen (falls 'Gender' vorhanden ist)
        gender_counts = df['Gender'].value_counts()

        # Ältestes, häufigstes und Jahrzehnt mit den meisten Einträgen ermitteln
        oldest_birth_year = df['Birth Year'].min()
        most_common_birth_year = df['Birth Year'].mode().iloc[0]
        most_common_decade_birth_year = most_common_birth_year // 10 * 10

        print("\nGeschlechter:")
        print(gender_counts)

        print("\nÄltestes Geburtsjahr:", int(oldest_birth_year))
        print("Meist vertretenes Geburtsjahr:", int(most_common_birth_year))
        print("Jahrzehnt mit den meisten Einträgen:", int(most_common_decade_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0

    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue? Enter yes or no: ").lower()

    
def main():

    while True:
        city, month, day = get_filters()  
        df = load_data(city,month,day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df) 
        user_stats(df,city)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break 
      
if __name__ == "__main__":
    main()