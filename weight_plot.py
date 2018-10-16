import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime


class WeightPlotter(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def soup_boiler(self, soup:list):
        datetime_list = list()
        weight_list = list()
        for element in soup:
            if len(element.find_all('code', {'displayName': "Body weight Measured"})) > 0:
                weight = element.find('text').find('value').get_text()
                date = element.find('effectiveTime').find('low')['value']
                try:
                    weight = float(weight)
                    date = date.split('+')[0]
                    date = datetime.strptime(date, '%Y%m%d%H%M%S')
                except:
                    continue
                datetime_list.append(date)
                weight_list.append(weight)
        return datetime_list, weight_list

    def main(self):
        file = open(self.file_name, 'r', encoding='utf-8')
        content = file.read()
        soup = BeautifulSoup(content, 'xml')
        weight_soup = soup.find_all('observation', {'classCode': 'OBS', 'moodCode': 'EVN'})
        datetime_list, weight_list = self.soup_boiler(weight_soup)
        weight_series = pd.Series(weight_list, index=datetime_list)
        weight_series.plot('line', grid=True, figsize=(16,9))
        plt.savefig('weight_timeseries.png')


if __name__ == '__main__':
    file_name = 'apple_data_export/export_cda_20181016.xml'
    plotter = WeightPlotter(file_name)
    plotter.main()
