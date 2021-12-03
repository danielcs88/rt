# %%
import pandas as pd
import subprocess
import numpy as np
from pygments import highlight
from pygments.formatters.terminal256 import TerminalTrueColorFormatter
from pygments.lexers import UsdLexer


latest = pd.read_csv(
    "https://raw.githubusercontent.com/epiforecasts/covid-rt-estimates/master/subnational/united-states/cases/summary/rt.csv",
    usecols=["date", "state", "mean"],
    parse_dates=["date"],
    infer_datetime_format=True,
)


# %%
on_file = pd.read_csv("data/rt.csv", parse_dates=["date"], infer_datetime_format=True,)

latest_date = sorted(latest["date"].unique())[-1]
on_file = sorted(on_file["date"].unique())[-1]

latest_date = np.datetime_as_string(latest_date, unit="D")
on_file = np.datetime_as_string(on_file, unit="D")

if latest_date == on_file:
    print(
        highlight(
            f"No run: Data on file {on_file} and data online from epiforecasts.io {latest_date} are equal.",
            UsdLexer(),
            TerminalTrueColorFormatter(style="dracula"),
        ),
    )
else:
    print(
        highlight(
            f"Run: On file data is {on_file}, data online is {latest_date}",
            UsdLexer(),
            TerminalTrueColorFormatter(style="dracula"),
        )
    )
    subprocess.call(["sh", "./run.sh"])
