import json

from django.utils.safestring import mark_safe

from . import BarChartDataset


class Chart:
    type = 'bar'
    labels = []
    datasets = []

    def __init__(self, datasets=None, ):
        datasets.sort(key=lambda x: -len(x.data))
        self.datasets = datasets

    def __str__(self):
        return self.render()

    def get_labels(self):
        return self.datasets[0].labels

    def get_parsing(self):
        return self.datasets[0].parsing

    def get_datasets(self):
        datasets = []
        for dataset in self.datasets:
            datasets.append(dataset.get())
        return datasets

    def get_data(self):
        return {
            "labels": self.get_labels(),
            "datasets": self.get_datasets(),
        }

    def get_options(self):
        return {"parsing": self.get_parsing()}

    def get(self):
        return {
            "type": self.type,
            "data": self.get_data(),
            "options": self.get_options()
        }

    def render(self):
        value = self.get()
        return mark_safe("""<canvas data-dynamic-chart="true"
                                    data-chart='{data}'
                                    id="{id}"
                                    style="width: 100%"/>""".format(
            data=json.dumps(value, default=str),
            id="lol"
        ))


class BarChart(Chart):
    type = 'bar'
    dataset_class = BarChartDataset

    def get_options(self):
        return {
            **super().get_options(),
            "scales": {
                "y": {
                    "beginAtZero": True
                }
            }
        }


class LineChart(Chart):
    type = 'line'
