from data import data
from glob import glob
import pandas as pd
import numpy as np
import os

source_path = input('Source Path:\n-> ')
write_path = input('Destination Path:\n-> ')

files = glob(os.path.join(source_path, '*.wav'))

input_df = pd.DataFrame(columns=['filePath', 'label'])

for aud in files:
    dt = data(aud, write_path)
    filePath, label = dt.process()
    input_df = input_df.append({'filePath': filePath, 'label': label}, ignore_index=True)




