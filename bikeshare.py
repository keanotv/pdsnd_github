import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# lists of months and short version of months to verify user input
months = ['january', 'february', 'march', 'april', 'may', 'june'] # 'july', 'august', 'september', 'october', 'november', 'december'
short_months = [month[:3] for month in months]

# lists of days and short version of days to verify user input
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
short_days = [day[:3] for day in days]

# lists of cities and acronym of cities to verify user input
cities = list(CITY_DATA.keys())
short_cities = []
for city in cities:
    city_words = city.split()
    acronym = ''
    for word in city_words:
        acronym += word[0]
    short_cities.append(acronym)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!\nWe will begin by selecting the city, month and/or day of the week of interest\nCurrently, only Chicago, New York City, and Washington are available.')

    global city, month, day
    # get user input for city (chicago, new york city, washington). Exits script if user enters 'q' 
    while True:
        city = input('Please enter city - Chicago (c), New York City (nyc) or Washington (w), exit (q): ').lower()
        if city in short_cities:
            city = cities[short_cities.index(city)]
            print('You have selected {}!\n'.format(city.title()))
            break
        elif city == 'q':
            print('Thank you for using Bikeshare data explorer :D')
            input('<Press Enter to exit>')
            break
    if city == 'q':
        return

    # get user input for month (all, january, february, ... , june). Exits script if user enters 'q' 
    while True:
        month = input('Please enter month from January to June (e.g. jan, feb, ...) or enter "all" for all months, exit (q): ').lower()
        if month in short_months:
            month = months[short_months.index(month)]
            print('You have selected {}!\n'.format(month.title()))
            break
        elif month == 'all':
            print('You have selected all months!\n')
            break
        elif month == 'q':
            print('Thank you for using Bikeshare data explorer :D')
            input('<Press Enter to exit>')
            break
    if month == 'q':
        return

    # get user input for day of week (all, monday, tuesday, ... sunday). Exits script if user enters 'q' 
    while True:
        day = input('Please enter day (e.g. mon, tue, ...) or enter "all" for all days, exit (q): ').lower()
        if day in short_days:
            day = days[short_days.index(day)]
            print('You have selected {}!\n'.format(day.title()))
            break
        elif day == 'all':
            print('You have selected all days!\n')
            break
        elif day == 'q':
            print('Thank you for using Bikeshare data explorer :D')
            input('<Press Enter to exit>')
            break
    if day == 'q':
        return

    # prints scope of data to be presented: city, month, day
    print('Let\'s look into the data for:\n{}'.format(city.title()))
    
    if month == 'all':
        print('All months')
    else:
        print(month.title())
    if day == 'all':
        print('All days')
    else:
        print(day.title() + 's')
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

    # extract month,day of week and start hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour
    
    # create new columns with start to end station combination
    df['Start End'] = df['Start Station'] + ' to ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        mc_month = df['month'].mode()[0]
        print('Most popular month: {}'.format(months[mc_month - 1].title()))

    # display the most common day of week
    if day == 'all':
        mc_dow = df['day_of_week'].mode()[0]
        print('Most popular day:   {}'.format(mc_dow))

    # display the most common start hour
    mc_start_hour = df['start_hour'].mode()[0]
    print('Most popular hour:  {}'.format(mc_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_start_stn = df['Start Station'].mode()[0]
    mc_start_stn_count = df['Start Station'].value_counts().max()
    print('Most popular start station: {} (Count: {})'.format(mc_start_stn, mc_start_stn_count))

    # display most commonly used end station
    mc_end_stn = df['End Station'].mode()[0]
    mc_end_stn_count = df['End Station'].value_counts().max()
    print('Most popular end station: {} (Count: {})'.format(mc_end_stn, mc_end_stn_count))

    # display most frequent combination of start station and end station trip
    mc_start_end_stn = df['Start End'].mode()[0]
    mc_start_end_stn_count = df['Start End'].value_counts().max()
    print('Most frequent start station and end station trip: {} (Count: {})'.format(mc_start_end_stn, mc_start_end_stn_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: {:.1f} seconds\n\t\tor {:.1f} minutes\n\t\tor {:.1f} hours\n\t\tor {:.2f} days\n'.format(total_travel_time, total_travel_time/60, total_travel_time/3600, total_travel_time/84600))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:  {:.1f} seconds\n\t\tor {:.1f} minutes\n\t\tor {:.2f} hours'.format(mean_travel_time, mean_travel_time/60, mean_travel_time/3600))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Subscribers: {}\nCustomers:   {}\n'.format(user_types[0], user_types[1]))

    # Display counts of gender
    if city != 'washington':
        gender = df['Gender'].value_counts()
        print('Male:   {}\nFemale: {}\n'.format(gender[0], gender[1]))

        # Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        year_count = df['Birth Year'].value_counts()
        most_common_year_percentage = (year_count.max()/year_count.sum()) * 100
        print('Earliest year of birth:    {}'.format(earliest))
        print('Most recent year of birth: {}'.format(most_recent))
        print('Most common year of birth: {} ({:.2f}% of users)'.format(most_common_year, most_common_year_percentage))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    start_loc = 0
    print('\nThere are {} rows of data within the selection'.format(len(df)))
    while True and start_loc == 0:
        view_data = input('Would you like to view 5 rows of individual trip data? (y/n)\n')
        if view_data == 'n':
            return print('Thank you for using Bikeshare data explorer :D')
        elif view_data == 'y':
            while start_loc < len(df):
                try:
                    print(df.iloc[start_loc:start_loc + 5])
                except:
                    print(df.iloc[start_loc:])
                start_loc += 5
                while True:
                    view_display = input("Do you wish to continue? (y/n): ").lower()
                    if view_display == 'n':
                        start_loc = len(df)
                        break
                    elif view_display == 'y':
                        break

def pause(duration=5):
    """Pauses for a short duration to give user time to read before continuing."""
    print('Proceeding in {} seconds...'.format(duration))
    print('-'*40)
    time.sleep(duration)

def main():
    while True:
        # handle errors and exit script if user enters 'q'
        try:
            city, month, day = get_filters()
            if day == 'q':
                break
        except:
            break
        df = load_data(city, month, day)

        time_stats(df)
        pause()
        station_stats(df)
        pause()
        trip_duration_stats(df)
        pause()
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart?(y/n)\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
