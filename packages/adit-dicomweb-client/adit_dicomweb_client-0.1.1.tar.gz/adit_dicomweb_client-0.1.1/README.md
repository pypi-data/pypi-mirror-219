# Adit DICOM Web Client

This is a simple Wrapper of the DICOM Web Client provided by the [dicomweb-client](https://dicomweb-client.readthedocs.io/en/latest/) library.
It is slighly adjusted and restricted to provide a simple python API to the DICOM Web API of [Adit](https://github.com/radexperts/adit).

## Installation

```bash
pip install adit-dicomweb-client
```

## Usage

```python
from adit_dicomweb_client import AditDicomWebClient

# Create a new client
client = AditDicomWebClient(
    adit_base_url,  # URL to the ADIT server
    dicom_server,  # AE title of the associated DICOM server
    auth_token,  # Authentication token for the ADIT server
)

# Find all studies
studies = client.find_studies()

# Find all series of a study
series = client.find_series(study_instance_uid)

# Find all series
series = client.find_series()

# Include additional query parameters
studies = client.find_studies({"PatientID": "1001"})

# Get a study
study = client.get_study(study_instance_uid)

# Get a series
series = client.get_series(study_instance_uid, series_instance_uid)

# Get study metadata
study_metadata = client.get_study_metadata(study_instance_uid)

# Get series metadata
series_metadata = client.get_series_metadata(study_instance_uid, series_instance_uid)

# Upload pydicom.Dataset instances
client.upload_instances(instance_list)


```