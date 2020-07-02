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
            ScheduledShip(
                {
                    ('01-06-2014', '31-08-2014'): [
                        '14:00'
                    ],
                    ('01-06-2015', '31-08-2015'): [
                        '14:00'
                    ],
                    ('01-06-2016', '31-08-2016'): [
                        '14:00'
                    ],
                    ('01-06-2017', '31-08-2017'): [
                        '14:00'
                    ],
                    ('01-06-2018', '31-08-2018'): [
                        '14:00'
                    ],
                    ('01-06-2019', '31-08-2019'): [
                        '14:00'
                    ]
                },
                timedelta(minutes=20), # Harbour time
                datetime.now(),
                timedelta(minutes=20), # Manouvering time
                'Hurtigruten',
                debug
            )
            # ,
            # ScheduledShip(
            #     {
            #         ('01-08-2016', '11-08-2016'): [
            #             '9:30',
            #             '13:00',
            #             '16:00'
            #         ]
            #     },
            #   timedelta(minutes=20), # Harbour time
            #   datetime.now(),
            #   timedelta(minutes=20), # Manouvering time
            #   'Ferry',
            #   debug
            # )
        ]