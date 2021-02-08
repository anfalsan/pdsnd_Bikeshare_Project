import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# The user is input one of the months of the first half of the year or all

def check_input_user(input_str, input_type):
    while True:
        input_read=input(input_str).lower()
        try:
            if input_read in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and input_type == 2:
                break
            elif input_read in ['sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','all'] and input_type == 3:
                break
            else:
                if input_type==1:
                    print('wrong city. your input should be chicago , new york city or washington')
                if input_type==2:
                    print('wrong month. your input should be')
                if input_type==3:
                    print('wrong day. your input should be')
        except ValueError:
            print('Sorry Error Input')
    return input_read

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check_input_user('Would you like to see data for chicago , new york city ,washington', 1)


    # TO DO: get user input for month (all, january, february, ... , june)
    month = check_input_user('which month?', 2)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_input_user('which day?', 3)
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june','all']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time=time.time()
    print('\nCalculating The Most Frequent Times of Travel...\n')
    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most common Month....', popular_month)
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day....', popular_day)
    # TO DO: display the most common start hour
    popular_hour=df['Hour'].mode()[0]
    print('Most common hour....', popular_hour)
    print("\nElapsed Time %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station
    popular_start_station= df['Start Station'].mode()[0]
    print('Most Start Station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station= df['End Station'].mode()[0]
    print('Most END Station:',popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    group_field=df.groupby(['Start Station','End Station'])
    popular_combination_Station=group_field.size().sort_values(ascending=False).head(1)
    print('\n Most frequent combination of Start station and End Station trip: \n',popular_combination_Station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print('Total Travel Time...',total_travel_time)
    # TO DO: display mean travel time
    avg_travel_time=df['Trip Duration'].mean()
    print('Avg Travel Time...',avg_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types

    print(df['User Type'].value_counts(),'\n ')
    if city != 'washington':
        # TO DO: Display counts of gender
        print(df['Gender'].value_counts(),'\n ')
    # TO DO: Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        print('Earliest Birth Year.....',earliest )
        most_recent = df['Birth Year'].max()
        print('Most common Birth Year...',most_recent )
        most_common = df['Birth Year'].mode()[0]
        print('Most common Birth.....',most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    display_raw_input = input("\nWould you like to see raw data? Enter 'yes' or 'no'\n").strip().lower()
    if display_raw_input in ("yes", "y"):
        i = 0
        while True:
            if (i + 10 > len(df.index) - 1):

                print(df.iloc[i:len(df.index), :])
                print("You've reached the end of the rows")
                break
            print(df.iloc[i:i + 10, :])
            i += 10

            show_next_five_input = input("\nWWould you like to see more row data? Enter 'yes' or 'no'\n").strip().lower()
            if show_next_five_input not in ("yes", "y"):
                break
            pd.set_option('display.max_columns', 200)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df.head())
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
