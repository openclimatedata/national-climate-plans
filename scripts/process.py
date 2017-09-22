import glob
import os
import pandas as pd

from countrygroups import EUROPEAN_UNION as eu28
from shutil import copyfile
from pandas_datapackage_reader import read_datapackage
from pathlib import Path

root = Path(__file__).parents[1]
data_dir = root / "data"
ndcs_path = root / "cache/ndcs"
indcs_path = root / "cache/indcs"
latest_pdfs_path = root /  "pdfs"

# NDCs
ndcs = read_datapackage(ndcs_path)

# Enable categorical sorting for language.
ndcs['Language'] = pd.Categorical(
    ndcs['Language'],
    ["English", "Arabic", "Spanish", "French", "Russian"]
)
# Set Preference for kind of document.
ndcs['FileType'] = pd.Categorical(
    ndcs['FileType'],
    ["Translation", "NDC", "Addendum"]
)

ndcs = ndcs.set_index("Code")

# Give preference to English version if available.
ndcs = ndcs.sort_values(
    ["Party", "Language", "FileType"])[~ndcs.index.duplicated(keep='first')]

# Remove individual EU countries, ignoring errors for parties not yet
# having ratified Paris Agreement.
ndcs = ndcs.drop(eu28, errors="ignore")

ndcs["Kind"] = ndcs["Number"] + " NDC"

# INDCs
indcs = read_datapackage(indcs_path)

indcs['Language'] = pd.Categorical(
    indcs['Language'],
    ["English", "Arabic", "Spanish", "French", "Russian"]
)
indcs['FileType'] = pd.Categorical(
    indcs['FileType'],
    ["Translation", "INDC", "Addendum"]
)

indcs = indcs.set_index("Code")

indcs = indcs.sort_values(
    ["Party", "Language", "FileType"])[~indcs.index.duplicated(keep='first')]

indcs["Kind"] = "INDC"

# Number of INDCs submitted.
assert len(indcs) == 165

# Combined list, with NDC or INDC if no NDC available yet

latest = pd.concat([ndcs, indcs])
latest = latest[~latest.index.duplicated(keep='first')]

latest = latest[[
    "Party",
    "Kind",
    "Language",
    "Filename",
    "SubmissionDate",
    "EncodedAbsUrl"
]]
latest = latest.sort_values("Party")

latest.SubmissionDate = latest.SubmissionDate.dt.date

latest.to_csv(root / "data/nationally-determined-contributions.csv")

if not latest_pdfs_path.exists():
    latest_pdfs_path.mkdir()

files = glob.glob(str(latest_pdfs_path / "*.pdf"))
for item in files:
    os.remove(str(root / item))

# Copy latest NDC or INDC document
for idx, item in latest.iterrows():
    if item["Kind"] == "INDC":
        src = indcs_path / "pdfs" / item["Filename"]
    else:
        src = ndcs_path / "pdfs" / item["Filename"]
    dest = latest_pdfs_path / item["Filename"]
    copyfile(str(src), str(dest))
