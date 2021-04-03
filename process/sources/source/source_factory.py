from .ship.scheduled_ship.scheduled_ship import ScheduledShip
from datetime import datetime, timedelta

class SourceFactory:

    def __init__(self):
        pass

    @staticmethod
    def get_initial_sources(debug):
        # {
        #   ('01-08-2016', '11-08-2016'): [
        #       '9:30',
        #       '13:00',
        #       '16:00'
        #   ]
        # }

        return [
            # Commented out because Hurtigruten is already included in port schedule
            # ScheduledShip(
            #     {
            #         ('01-06-2014', '31-08-2014'): [
            #             '14:00'
            #         ],
            #         ('01-06-2015', '31-08-2015'): [
            #             '14:00'
            #         ],
            #         ('01-06-2016', '31-08-2016'): [
            #             '14:00'
            #         ],
            #         ('01-06-2017', '31-08-2017'): [
            #             '14:00'
            #         ],
            #         ('01-06-2018', '31-08-2018'): [
            #             '14:00'
            #         ],
            #         ('01-06-2019', '31-08-2019'): [
            #             '14:00'
            #         ]
            #     },
            #     timedelta(minutes=20), # Harbour time
            #     datetime.now(),
            #     timedelta(minutes=20), # Manouvering time
            #     'Hurtigruten',
            #     debug
            # ),
            ScheduledShip(
                {
                    ('01-05-2015', '31-05-2015'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-06-2015', '31-08-2015'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '7:55',
                        '9:25',
                        '10:55',
                        '12:25',
                        '13:55',
                        '15:25',
                        '16:55',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-09-2015', '30-09-2015'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-10-2015', '31-10-2015'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-05-2016', '31-05-2016'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-06-2016', '31-08-2016'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '7:55',
                        '9:25',
                        '10:55',
                        '12:25',
                        '13:55',
                        '15:25',
                        '16:55',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-09-2016', '30-09-2016'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-10-2016', '31-10-2016'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25' # It's actually not departing here, but the morning after...
                    ],
                    # What we originally had for 2016
                    # ('01-05-2016', '11-08-2016'): [
                    #     '6:35', # It's actually not arriving here, but the night before...
                    #     '9:35',
                    #     '12:35',
                    #     '15:35',
                    #     '18:35' # It's actually not departing here, but the nmorning after...
                    # ],
                    ('01-05-2017', '31-05-2017'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-06-2017', '31-08-2017'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '7:55',
                        '9:25',
                        '10:55',
                        '12:25',
                        '13:55',
                        '15:25',
                        '16:55',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-09-2017', '30-09-2017'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-10-2017', '31-10-2017'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-04-2018', '30-04-2018'): [
                        '6:55', # It's actually not arriving here, but the night before...
                        '10:25',
                        '13:25',
                        '17:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-05-2018', '19-05-2018'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('20-05-2018', '10-09-2018'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '7:55',
                        '9:25',
                        '10:55',
                        '12:25',
                        '13:55',
                        '15:25',
                        '16:55',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('11-09-2018', '30-09-2018'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-10-2018', '31-10-2018'): [
                        '6:55', # It's actually not arriving here, but the night before...
                        '10:25',
                        '13:25',
                        '17:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-04-2019', '30-04-2019'): [
                        '7:55', # It's actually not arriving here, but the night before...
                        '11:25',
                        '14:25',
                        '17:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-05-2019', '19-05-2019'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('20-05-2019', '10-09-2019'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '7:55',
                        '9:25',
                        '10:55',
                        '12:25',
                        '13:55',
                        '15:25',
                        '16:55',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('11-09-2019', '30-09-2019'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                    ('01-10-2019', '31-10-2019'): [
                        '7:55', # It's actually not arriving here, but the night before...
                        '11:25',
                        '14:25',
                        '17:25' # It's actually not departing here, but the morning after...
                    ],
                    ('12-06-2020', '30-09-2020'): [
                        '6:25', # It's actually not arriving here, but the night before...
                        '9:25',
                        '12:25',
                        '15:25',
                        '18:25' # It's actually not departing here, but the morning after...
                    ],
                },
              timedelta(minutes=25), # Harbour time
              datetime.now(),
              timedelta(minutes=10), # Manouvering time
              'Ferry',
              debug
            )
        ]