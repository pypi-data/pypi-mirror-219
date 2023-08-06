import numpy as np

class Evaluation:

    def __init__(self, reg, dataframe, production_baseload = 0):
        """
        This class defines a set of energy metrics which allow to help identifying how good was the implemented strategy.
        In few words, it allows to calculate metrics for a specific dataset with the following columns (Date, Demand, Production and Netload).
        Some examples are the average power used from the grid, average power used from the PV and average power not used (wasted) from PV.

        Args:
            dataframe: the dataframe from where the metrics will be calculated
            production_baseload: the maximum value that can be acquired from the grid (from non-renewable sources) - used, for instance, to identify consumption peaks (default is 0)
            reg: Renewable Energy Generator instance in order to use some of its functions (optional)
        """
        self.reg = reg
        self.dataframe = dataframe
        self.production_baseload = production_baseload


    def get_average_power_used_from_grid(self):
        """
        Gets the average power used from the grid in the consumption profile (dataframe).

        Returns:
            average power used from the grid (in kW)
        """
        return self.dataframe.loc[self.dataframe.Netload > 0, 'Netload'].mean() / 1000

    def get_average_power_not_used_from_pv(self):
        """
        Gets the average power not used (wasted) from the PV in the consumption profile (dataframe).

        Returns:
            average power not used (wasted) from the PV (in kW)
        """
        return abs(self.dataframe.loc[self.dataframe.Netload <= 0, 'Netload'].mean()) / 1000

    def get_energy_exported_to_grid(self):
        """
        Gets the total energy not used from the production in kWh
        :return:
        """
        return self.dataframe['pExp_df'].sum()/1000

    def get_average_power_used_from_pv(self):
        """
        Gets the average power used from the PV in the consumption profile (dataframe).

        Returns:
            average power used from the PV (in kW)
        """
        return (abs(self.dataframe.loc[self.dataframe.Netload <= 0, 'Demand'].mean()/2) + abs(self.dataframe.loc[self.dataframe.Netload > 0, 'Production'].mean()/2)) / 1000

    def get_energy_used_from_grid(self):
        """
        Gets the total energy used from the grid in the consumption profile (dataframe) in 24 hours.

        Returns:
            total energy used from the grid (in kWh)
        """
        #return dataframe.loc[dataframe.Netload > 0].resample('H', on='Date').Netload.sum().values.mean() * 24 / 1000
        return self.get_average_power_used_from_grid()*24

    def get_energy_imported_from_grid(self):
        """
        Gets the total energy imported from the grid in kWh
        :return:
        """
        return self.dataframe['pImp_df'].sum()/1000

    def get_energy_not_used_from_pv(self):
        """
        Gets the total energy not used (wasted) from the PV in the consumption profile (dataframe) in 24 hours.

        Returns:
            total energy not used (wasted) from the PV (in kWh)
        """
        #return abs(dataframe.loc[dataframe.Netload <= 0].resample('H', on='Date').Netload.sum().values.mean() * 24 / 1000)
        return self.get_average_power_not_used_from_pv() * 24

    def get_energy_used_from_pv(self):
        """
        Gets the total energy used from the PV in the consumption profile (dataframe) in 24 hours.

        Returns:
            total energy used from the PV (in kWh)
        """
        #return (abs(dataframe.loc[dataframe.Netload <= 0].resample('H', on='Date').Demand.sum().values.mean() * 24) + abs(dataframe.loc[dataframe.Netload > 0].resample('H', on='Date').Production.sum().values.mean() * 24)) / 1000
        return self.get_average_power_used_from_pv() * 24

    def get_energy_used_from_production(self):
        """
        Gets the total energy used from the production in kWh
        :return:
        """
        return sum((self.dataframe['production_df'][i] - self.dataframe['pExp_df'][i])/1000 for i in np.arange(1,25) if self.dataframe['production_df'][i] >= self.dataframe['pExp_df'][i]) + sum((self.dataframe['production_df'][i]/1000 for i in np.arange(1,25) if self.dataframe['production_df'][i] < self.dataframe['pExp_df'][i])) + self.dataframe['evCharge_df'].sum().sum()/1000

    def get_maximum_grid_peak(self):
        """
        Gets the maximum grid peak in the consumption profile (dataframe).
        Returns the maximum consumption when the energy acquired from the grid is higher than the production_baseload parameter

        Returns:
            maximum grid peak (in kW)
        """
        return self.dataframe.loc[self.dataframe.Netload > self.production_baseload, 'Demand'].max() / 1000

    def get_minimum_grid_peak(self):
        """
        Gets the minimum grid peak in the consumption profile (dataframe).
        Returns the minimum consumption when the energy acquired from the grid is higher than the production_baseload parameter

        Returns:
            minimum grid peak (in kW)
        """
        return self.dataframe.loc[self.dataframe.Netload > self.production_baseload, 'Demand'].min() / 1000

    def get_maximum_magnitude_peak(self):
        """
        Gets the maximum magnitude peak in the consumption profile (dataframe).
        Returns the maximum value of energy acquired from the grid when the total is higher than the production_baseload parameter

        Returns:
            maximum magnitude peak (in kW)
        """
        return self.dataframe.loc[self.dataframe.Netload > self.production_baseload, 'Netload'].max() / 1000

    def get_minimum_magnitude_peak(self):
        """
        Gets the minimum magnitude peak in the consumption profile (dataframe).
        Returns the minimum value of energy acquired from the grid when the total is higher than the production_baseload parameter

        Returns:
            minimum magnitude peak (in kW)
        """
        return self.dataframe.loc[self.dataframe.Netload > self.production_baseload, 'Netload'].min() / 1000

    def get_peaks_number(self):
        """
        Gets the number of peaks in the consumption profile (dataframe).
        A peak is considered when the power acquired from the grid in a specific minute exceeds the production_baseload parameter (i.e. when the netload is higher than the production_dataframe parameter)

        Returns:
            number of peaks
        """
        return self.dataframe.loc[self.dataframe.Netload > self.production_baseload, 'Netload'].count()

    def get_timeslots_list_number(self, list_timeslots):
        """
        Gets the number of timeslots/activities in a specific list. It can be used in order to identify the number of placed timeslots (using, for instance, the placed_timeslots list) or to identify the number of unplaced timeslots (using, for instance, the not_placed_timeslots list).

        Args:
            list_timeslots: list of timeslots/activities

        Returns:
            number of timeslots/activities in a list
        """
        return len(self.reg.remove_duplicated_items(list_timeslots))

    def get_energy_of_timeslots_list(self, list_timeslots):
        """
        Gets the total energy used from the timeslots/activities presented in the list. It can be used in order to calculate the quantity of energy used from the placed timeslots (using, for instance, the placed_timeslots list) or to calculate the quantity of energy of the timeslots that were not placed (using, for instance, the not_placed_timeslots list)

        Args:
            list_timeslots: list of timeslots/activities

        Returns:
            total energy of the timeslots/activities of the list (in kWh)
        """
        return float(self.reg.calculate_timeslots_list_energy(list_timeslots)) / 1000

    def get_self_sufficiency(self):
        """
        Calculates the Self Sufficiency according to 2 metrics of this class: energy used from the PV and energy used from the grid.
        The Self Sufficiency (SS) measures the consumption amount supplied by generation with respect to the total consumption (independence from the grid).

        Returns:
            self sufficiency
        """
        return (self.get_energy_used_from_pv()/(self.get_energy_used_from_pv()+self.get_energy_used_from_grid()))

    def get_ss_without_storage(self):
        """
        Calculates the Self Sufficiency in %
        :return:
        """
        return self.get_energy_used_from_production() / (self.get_energy_imported_from_grid() + self.get_energy_used_from_production())*100

    def get_self_consumption(self):
        """
        Calculates the Self Consumption according to 2 metrics of this class: energy used from the PV and energy not used (wasted) from the PV.
        The Self-Consumption (SC) is the amount of electricity generated and consumed with respect to the total generation.

        Returns:
            self consumption
        """
        return (self.get_energy_used_from_pv()/(self.get_energy_used_from_pv()+self.get_energy_not_used_from_pv()))

    def get_sc(self):
        """
        Calculates the Self Consumption in %
        :return: 
        """
        return self.get_energy_used_from_production() / (self.get_energy_used_from_production() + self.get_energy_exported_to_grid())*100

    def get_costs(self, degradation_cost):
        """
        Calculates the costs of the system according to the degradation cost and the energy used from the grid.
        :param degradation_cost: degradation cost for each kWh
        :return: 
        """
        return (self.dataframe['importPrices_df']*self.dataframe['pImp_df']/1000 - self.dataframe['exportPrices_df']*self.dataframe['pExp_df']/1000).sum() + (self.dataframe['evCharge_df'].sum().sum()+self.dataframe['evDischarge_df'].sum().sum())/1000*degradation_cost

    def get_ss_with_storage(self):
        """
        Calculates the Self Sufficiency in % considering storage (considering charge, dsicharge, losses, eficiency, delta SOC, etc)
        :return: 
        """

        demand = self.dataframe['demand_df'].sum().sum()/1000
        production = self.dataframe['production_df'].sum()/1000
        export = self.get_energy_exported_to_grid()
        charge = self.dataframe['evCharge_df'].sum().sum()/1000
        discharge = self.dataframe['evDischarge_df'].sum().sum()/1000
        efficiency = 0.97
        loss = (1-efficiency) * (charge+discharge)
        ess_initial = self.dataframe['evSoc_df'].transpose().iloc[0].sum()/1000
        ess_final = self.dataframe['evSoc_df'].transpose().iloc[-1].sum()/1000
        delta_ess = ess_final - ess_initial
        grid = self.get_energy_imported_from_grid()

        used_prod = demand-grid
        not_used_prod = production - used_prod
        not_used_prod2 = export + loss
        k = production / (grid + production)


        print("k: ", k)
        print("demand: ", demand)
        print("production: ", production)
        print("export: ", export)
        print("charge: ", charge)
        print("discharge: ", discharge)
        print("loss: ", loss)
        print("ess_initial: ", ess_initial)
        print("ess_final: ", ess_final)
        print("delta_ess: ", delta_ess)
        print("used prod: ", used_prod)
        print("not used prod: ", not_used_prod)
        print(100 * (production - k * (export + loss + delta_ess)) / demand)
        print((production - export - loss)/demand)
        print((production - (export - self.get_energy_imported_from_grid()) + loss + delta_ess)/demand)

        return 100 * (production - k * (export + loss + delta_ess)) / demand

    def execute(self):
        """
        Calculates many metrics from this class.
        """

        print("Average Power used from Grid: " + str(self.get_average_power_used_from_grid()))
        print("Average Power not used from PV: " + str(self.get_average_power_not_used_from_pv()))
        print("Average Power used from PV: " + str(self.get_average_power_used_from_pv()))
        print("Energy used from Grid: " + str(self.get_energy_used_from_grid()))
        print("Energy not used from PV: " + str(self.get_energy_not_used_from_pv()))
        print("Energy used from PV: " + str(self.get_energy_used_from_pv()))
        print("Maximum Grid Peak: " + str(self.get_maximum_grid_peak()))
        print("Minimum Grid Peak: " + str(self.get_minimum_grid_peak()))
        print("Maximum Magnitude Peak: " + str(self.get_maximum_magnitude_peak()))
        print("Minimum Magnitude Peak: " + str(self.get_minimum_magnitude_peak()))
        print("Number of Peaks: " + str(self.get_peaks_number()))
        print("Self Sufficiency: " + str(self.get_self_sufficiency()))
        print("Self Consumption: " + str(self.get_self_consumption()))

        #dfFigure = pd.DataFrame(np.arange(20, 40), columns=['Val'])
        #dfFigure['Capacity'] = 35
        #dfFigure['Function'] = dfFigure.apply(lambda row: row.Capacity / row.Val - row.Capacity - min(0, row.Capacity - row.Val), axis=1)
        #create_table_figure(dfFigure)




if __name__ == '__main__':

    ev = Evaluation()
    ev.execute()