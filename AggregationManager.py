import pandas as pd
import numpy as np

class AggregationManager:
    def __init__(self, eG, eN):
        self.eG = eG
        self.eN = eN


    # print num green delivery, normal delivery, total emissions
    def ReportStatsForPeriod(self,agents, period):
        green_emissions = sum([agent.Qrecords[period] * self.eG for agent in agents if agent.PlanRecords[period] == 'Green'])
        normal_emissions = sum([agent.Qrecords[period]* self.eN for agent in agents if agent.PlanRecords[period] == 'Normal'])
        total_emissions = float(green_emissions + normal_emissions)
        total_green = sum([1 for agent in agents if agent.PlanRecords[period] == 'Green'])
        total_normal = sum([1 for agent in agents if agent.PlanRecords[period] == 'Normal'])
        df_dict = {
            'TotalEmission': total_emissions,
            'GreenUsers': total_green,
            'NormalUsers': total_normal
        }
        df = pd.DataFrame(df_dict, index=[0])
        print(df)


    def ReportAllStats(self, agents, total_periods):
        df_dict = {}
        total_emissions = []
        total_green = []
        total_normal =[]

        for period in range(total_periods):
            green_emissions = sum(
                [agent.Qrecords[period] * self.eG for agent in agents if agent.PlanRecords[period] == 'Green'])
            normal_emissions = sum(
                [agent.Qrecords[period] * self.eN for agent in agents if agent.PlanRecords[period] == 'Normal'])
            period_emissions = float(green_emissions + normal_emissions)
            period_green = sum([1 for agent in agents if agent.PlanRecords[period] == 'Green'])
            period_normal = sum([1 for agent in agents if agent.PlanRecords[period] == 'Normal'])
            total_emissions.append(period_emissions)
            total_green.append(period_green)
            total_normal.append(period_normal)

        df_dict = {
            'Period': [i for i in range(total_periods)],
            'TotalEmission': total_emissions,
            'GreenUsers': total_green,
            'NormalUsers': total_normal
        }
        df = pd.DataFrame(df_dict)
        df.set_index('Period', inplace=True)
        print(df)
        #sort out printing


