# Keras Progressbar with TQDM-like API.
I'm a big fan of how Keras' progressbar looks, but I was annoyed,
that there is no way to use it the same as TQDM progressbar. 
So, I published this tiny module, in order to avoid copy-pasting it
in every my project.

### Example usage
```python
import time
import pandas as pd
from keras_pbar import pbar

df = pd.read_csv("data.csv")
for identifier, sliced in pbar(df.group_by("id")):
    # Do some time consuming processing.
    time.sleep(2)
```
### Notes
It does not directly depend on `tensorflow`, so you can install it without.
But probably during import time, it will fail, when `keras` tries to import `tensorlfow`.
