"""
dataSet
===============================================================================
"""

from defcon.objects.dataSet import DataSet as defconDataSet

class DataSet(defconDataSet):
    def __init__(self, font=None):
        super().__init__(font)
        self._dirty = False
