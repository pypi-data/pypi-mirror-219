from django.db.models import QuerySet


class ChartDataset:
    options = {}
    label = None
    labels = []
    clip = None
    order = 0
    parsing = False
    hidden = False
    stack = None
    data_type = None

    def __init__(self, data, keys, label_key, value_key, labels=None,
                 label=None,
                 options=None,
                 clip=None, order=None, parsing=None, hidden=None,
                 stack=None):
        if labels is None:
            labels = []

        self.keys = keys
        self.label_key = label_key
        self.value_key = value_key
        self.label = label
        data = self.prepare(data)
        self.data = self.map_data(data)
        self.labels = self.get_labels(data, labels)

    def prepare(self, data):
        if isinstance(data, QuerySet):
            self.data_type = 'object[]'
            return list(data.values(*self.keys))
        elif isinstance(data, dict):
            self.data_type = 'object'
            return data
        else:
            result = []
            first_item = data[0]
            if isinstance(first_item, dict):
                self.data_type = 'object[]'
                result.append({key: first_item[key] for key in self.keys})
                self.parsing = {
                    "xAxisKey": self.value_key,
                    "yAxisKey": self.label_key
                }
            elif not hasattr(first_item, '__dict__'):
                self.data_type = 'primitive'
                result.append(first_item)
            else:
                raise Exception("data must be of type QuerySet, list of primitive values or list of dict")
            return result

    def map_data(self, data):
        result = []
        if isinstance(data, QuerySet):
            result = list(data.values(*self.keys))
            self.parsing = {
                "xAxisKey": self.value_key,
                "yAxisKey": self.label_key
            }
        else:
            for item in data:
                if isinstance(item, dict):
                    result.append({key: item[key] for key in self.keys})
                    self.parsing = {
                        "xAxisKey": self.value_key,
                        "yAxisKey": self.label_key
                    }
                elif not hasattr(item, '__dict__'):
                    result.append(item)
                else:
                    raise Exception("data must be of type QuerySet, list of primitive values or list of dict")
        return result

    def get_labels(self, data, labels):
        # if not len(labels):
        return list(map(lambda x: x[self.label_key], data))
        # result = []
        # for label in labels:
        #     result.append(label[1])
        # return result

    def get(self):
        config = {
            "label": self.label,
            "data": self.data,
            "options": {}
        }
        if self.parsing:
            config['options']['parsing'] = self.parsing
        return config


class BarChartDataset(ChartDataset):
    def map_data(self, data):
        return list(item[self.value_key] for item in super().map_data(data))

    # properties = {
    #     "backgroundColor": 'rgba(0, 0, 0, 0.1)',
    #     "base": None,
    #     "barPercentage": 0.9,
    #     "barThickness": None,
    #     "borderColor": 'rgba(0, 0, 0, 0.1)',
    #     "borderSkipped": 'start',
    #     "borderWidth": 0,
    #     "borderRadius": 0,
    #     "categoryPercentage": 0.8,
    #     "grouped": True,
    #     "hoverBackgroundColor": None,
    #     "hoverBorderColor": None,
    #     "hoverBorderWidth": 1,
    #     "hoverBorderRadius": 0,
    #     "indexAxis": 'x',
    #     "inflateAmount": 'auto',
    #     "maxBarThickness": None,
    #     "minBarLength": None,
    #     "pointStyle": 'circle',
    #     "stack": 'bar',
    #     "order": 0,
    #     "skipNull": None,
    #     "xAxisID": None,
    #     "yAxisID": None,
    # }

    # def get(self):
    #     config = super().get()
    #     for key, value in self.properties.items():
    #         if value:
    #             config[key] = value
    #     return config


class LineChartDataset(ChartDataset):
    def map_data(self, data):
        return list(item[self.value_key] for item in super().map_data(data))
