import numpy as np

class Input:

    def __init__(self, contracted_power, fd, dates, items, bins_capacities, timeslot_numbers, bins_maximum, items_max, n_bins_per_hour, flexibilities, bins_export_prices, bins_import_prices, s_max, s_min, s_initial_soc, num_houses, houses_production, house_items, house_items_max, house_items_date, house_items_num, house_items_flex, house_s_soc, house_s_max, house_s_min):
        """

        """
        self.contracted_power = contracted_power
        self.first_date = fd
        self.dates = dates
        self.items = items
        self.bins_capacities = bins_capacities
        self.timeslot_numbers = timeslot_numbers
        self.bins_maximum = bins_maximum
        self.items_max = items_max
        self.n_bins_per_hour = n_bins_per_hour
        self.flexibilities = flexibilities
        self.bins_export_prices = bins_export_prices
        self.bins_import_prices = bins_import_prices
        self.s_max = s_max
        self.s_min = s_min
        self.s_initial_soc = s_initial_soc
        self.num_houses = num_houses
        self.houses_production = houses_production
        self.house_items = house_items
        self.house_items_max = house_items_max
        self.house_items_date = house_items_date
        self.house_items_num = house_items_num
        self.house_items_flex = house_items_flex
        self.house_s_soc = house_s_soc
        self.house_s_max = house_s_max
        self.house_s_min = house_s_min
