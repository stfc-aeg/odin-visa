import numpy as np
import pandas as pd

ITEM_DTYPE = np.dtype([("timestamp", "i8"), ("source", "f8"), ("reading", "f8")])

MeasurementNDArray = pd.DataFrame
