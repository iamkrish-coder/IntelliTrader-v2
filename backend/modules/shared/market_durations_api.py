import calendar
import datetime as dt
from ..shared.market_holidays_api import market_holidays


class MarketDurations:
    def __init__(self, depth, timeframe):
        self.depth = depth
        self.timeframe = timeframe

    def calculate_all_durations(self):
        all_durations = {}

        if 'today' in self.timeframe:
            all_durations['today'] = self.get_duration_today(self.depth)
        elif 'minute' in self.timeframe:
            all_durations['minute'] = self.get_duration_minutes(self.depth)
        elif 'hour' in self.timeframe:
            all_durations['hour'] = self.get_duration_hour(self.depth)
        elif 'day' in self.timeframe:
            all_durations['day'] = self.get_duration_day(self.depth)
        elif 'week' in self.timeframe:
            all_durations['week'] = self.get_duration_week(self.depth)
        elif 'month' in self.timeframe:
            all_durations['month'] = self.get_duration_month(self.depth)
        else:
            pass

        return all_durations

    def get_duration_today(self, depth=1):

        duration_in_days = 0
        min_duration = 1 if depth > 1 else depth
        trading_holidays = self.get_market_holidays()
        today = dt.date.today()

        for i in range(0, min_duration):
            current_weekday = today.weekday()

            if current_weekday == 0:  # Monday
                duration_in_days += 3
            elif current_weekday == 6:  # Sunday
                duration_in_days += 2
            elif current_weekday == 5:  # Saturday
                duration_in_days += 1
            else:
                duration_in_days += 1  # Other Days

            # Iterate over the trading holidays and check if they fall within the depth or min_duration
            for holiday in trading_holidays:
                holiday_date = holiday['date']
                current_holiday = (today - holiday_date).days

                # Check if the holiday is not on a Saturday (5) or Sunday (6)
                if current_holiday < 0:
                    break

                if 0 <= current_holiday <= (min_duration + duration_in_days) \
                        and holiday_date.weekday() != 5 and holiday_date.weekday() != 6:
                    duration_in_days += 1

            today -= dt.timedelta(days=duration_in_days)

        return duration_in_days

    def get_duration_minutes(self, depth):

        duration_in_days = 0
        min_duration = depth if depth > 1 else 2
        trading_holidays = self.get_market_holidays()
        today = dt.date.today()

        for i in range(0, min_duration):
            current_weekday = today.weekday()

            if current_weekday == 0:  # Monday
                duration_in_days += 3
            elif current_weekday == 6:  # Sunday
                duration_in_days += 2
            elif current_weekday == 5:  # Saturday
                duration_in_days += 1
            else:
                duration_in_days += 1  # Other Days

            # Iterate over the trading holidays and check if they fall within the depth or min_duration
            for holiday in trading_holidays:
                holiday_date = holiday['date']
                current_holiday = (today - holiday_date).days

                # Check if the holiday is not on a Saturday (5) or Sunday (6)
                if current_holiday < 0:
                    break

                if 0 <= current_holiday <= min_duration \
                        and holiday_date.weekday() != 5 and holiday_date.weekday() != 6:
                    duration_in_days += 1

            today -= dt.timedelta(days=duration_in_days)

        return duration_in_days

    def get_duration_hour(self, depth):

        duration_in_days = 0
        min_duration = depth if depth > 1 else 2
        trading_holidays = self.get_market_holidays()
        today = dt.date.today()

        for i in range(0, min_duration):
            current_weekday = today.weekday()

            if current_weekday == 0:  # Monday
                duration_in_days += 3
            elif current_weekday == 6:  # Sunday
                duration_in_days += 2
            elif current_weekday == 5:  # Saturday
                duration_in_days += 1
            else:
                duration_in_days += 1  # Other Days

            # Iterate over the trading holidays and check if they fall within the depth or min_duration
            for holiday in trading_holidays:
                holiday_date = holiday['date']
                current_holiday = (today - holiday_date).days

                # Check if the holiday is not on a Saturday (5) or Sunday (6)
                if current_holiday < 0:
                    break

                if 0 <= current_holiday <= min_duration \
                        and holiday_date.weekday() != 5 and holiday_date.weekday() != 6:
                    duration_in_days += 1

            today -= dt.timedelta(days=duration_in_days)

        return duration_in_days

    def get_duration_day(self, depth):

        duration_in_days = 0
        min_duration = depth if depth > 1 else 2
        trading_holidays = self.get_market_holidays()
        today = dt.date.today()

        for i in range(0, min_duration):
            current_weekday = today.weekday()

            if current_weekday == 0:  # Monday
                duration_in_days += 3
            elif current_weekday == 6:  # Sunday
                duration_in_days += 2
            elif current_weekday == 5:  # Saturday
                duration_in_days += 1
            else:
                duration_in_days += 1  # Other Days

            # Iterate over the trading holidays and check if they fall within the depth or min_duration
            for holiday in trading_holidays:
                holiday_date = holiday['date']
                current_holiday = (today - holiday_date).days

                # Check if the holiday is not on a Saturday (5) or Sunday (6)
                if current_holiday < 0:
                    break

                if 0 <= current_holiday <= min_duration \
                        and holiday_date.weekday() != 5 and holiday_date.weekday() != 6:
                    duration_in_days += 1

            today -= dt.timedelta(days=duration_in_days)

        return duration_in_days

    @staticmethod
    def get_duration_week(depth):

        duration_in_days = 0
        min_duration = depth if depth > 1 else 2
        today = dt.date.today()

        for i in range(min_duration):
            if i == 0:
                # Get the number of days in the current week until today
                duration_in_days += today.weekday() + 1
            else:
                # Add 7 days for each subsequent week
                duration_in_days += 7

        return duration_in_days

    @staticmethod
    def get_duration_month(depth):

        duration_in_days = 0
        min_duration = depth if depth > 1 else 2
        today = dt.date.today()
        current_year = today.year
        current_month = today.month
        current_day = today.day

        for i in range(0, min_duration):
            month = 12 if current_month - i == 0 else current_month - i
            days_in_month = calendar.monthrange(current_year, month)[1]
            if i == 0:
                duration_in_days = current_day
            else:
                duration_in_days += days_in_month

        return duration_in_days

    @staticmethod
    def get_market_holidays():
        # URL of the NSE India webpage containing holiday information
        url = "https://zerodha.com/marketintel/holiday-calendar/"

        # Scrape holiday data from the webpage
        nse_holiday_information = market_holidays(url)

        return nse_holiday_information
