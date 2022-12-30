from unittest import TestCase

from main.graph import GraphDrawer


class ManualTestGraphDrawer(TestCase):

    def test_plot_year_popularity(self):
        graph_drawer = GraphDrawer()
        graph_drawer.plot_year_popularity()
