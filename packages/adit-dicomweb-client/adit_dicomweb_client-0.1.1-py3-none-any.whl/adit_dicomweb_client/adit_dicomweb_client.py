from typing import List, Optional

from dicomweb_client import DICOMwebClient
from pydicom.dataset import Dataset


class AditDicomWebClient:
    """
    This class is a wrapper around the DICOMwebClient class, which is
    provided by the dicomweb-client library. This class implements a
    client to the ADIT DICOMweb server.
    """

    def __init__(
        self,
        adit_base_url: str,
        dicom_server: str,
        auth_token: str,
        dicomweb_root: str = "dicom-web",
        qido_prefix: str = "qidors",
        wado_prefix: str = "wadors",
        stow_prefix: str = "stowrs",
    ):
        """
        Constructor of the AditDicomWebClient class.

        :param adit_base_url: The base URL of the ADIT server.
        :param dicom_server: The name of the DICOM server.
        :param auth_token: The authentication token.
        :param dicomweb_root: The root of the DICOMweb server.
        :param qido_prefix: The prefix of the QIDO-RS service.
        :param wado_prefix: The prefix of the WADO-RS service.
        :param stow_prefix: The prefix of the STOW-RS service.
        """
        self.adit_base_url = adit_base_url
        self.dicom_server = dicom_server
        self.auth_token = auth_token
        self.dicomweb_root = dicomweb_root
        self.qido_prefix = qido_prefix
        self.wado_prefix = wado_prefix
        self.stow_prefix = stow_prefix

        self.url = f"{adit_base_url}/{dicomweb_root}/{dicom_server}"

        self.dicomweb_client = DICOMwebClient(
            url=self.url,
            qido_url_prefix=qido_prefix,
            wado_url_prefix=wado_prefix,
            stow_url_prefix=stow_prefix,
            headers={"Authorization": f"Token {auth_token}"},
        )

    def find_studies(self, query: Optional[dict] = None) -> List[Dataset]:
        """
        This method queries the ADIT DICOMweb server for studies.

        :param query: Additional query filters.
        :return: The response of the ADIT DICOMweb server.
        """
        results = self.dicomweb_client.search_for_studies(search_filters=query)
        return [Dataset.from_json(result) for result in results]

    def find_series(
        self, study_instance_uid: Optional[str] = None, query: Optional[dict] = None
    ) -> List[Dataset]:
        """
        This method queries the ADIT DICOMweb server for series.

        :param study_instance_uid: The study instance UID of the study.
        :param query: Additional query filters.
        :return: The response of the ADIT DICOMweb server.
        """
        if study_instance_uid:
            results = self.dicomweb_client.search_for_series(
                study_instance_uid=study_instance_uid, search_filters=query
            )
        else:
            results = self.dicomweb_client.search_for_series(search_filters=query)

        return [Dataset.from_json(result) for result in results]

    def get_study(self, study_instance_uid: str) -> List[Dataset]:
        """
        This method queries the ADIT DICOMweb server for a study and retrieves
        it.

        :param study_instance_uid: The study instance UID of the study.
        :return: The response of the ADIT DICOMweb server.
        """
        results = self.dicomweb_client.retrieve_study(study_instance_uid=study_instance_uid)
        return results

    def get_series(self, study_instance_uid: str, series_instance_uid: str) -> List[Dataset]:
        """
        This method queries the ADIT DICOMweb server for a series and retrieves
        it.

        :param study_instance_uid: The study instance UID of the study.
        :param series_instance_uid: The series instance UID of the series.
        :return: The response of the ADIT DICOMweb server.
        """
        results = self.dicomweb_client.retrieve_series(
            study_instance_uid=study_instance_uid, series_instance_uid=series_instance_uid
        )
        return results

    def get_study_metadata(self, study_instance_uid: str) -> List[Dataset]:
        """
        This method queries the ADIT DICOMweb server for a study and retrieves
        its metadata.

        :param study_instance_uid: The study instance UID of the study.
        :return: The response of the ADIT DICOMweb server.
        """
        results = self.dicomweb_client.retrieve_study_metadata(study_instance_uid)
        return [Dataset.from_json(result) for result in results]

    def get_series_metadata(
        self, study_instance_uid: str, series_instance_uid: str
    ) -> List[Dataset]:
        """
        This method queries the ADIT DICOMweb server for a series and retrieves
        its metadata.

        :param study_instance_uid: The study instance UID of the study.
        :param series_instance_uid: The series instance UID of the series.
        :return: The response of the ADIT DICOMweb server.
        """
        results = self.dicomweb_client.retrieve_series_metadata(
            study_instance_uid=study_instance_uid, series_instance_uid=series_instance_uid
        )
        return [Dataset.from_json(result) for result in results]

    def upload_instances(self, instances: List[Dataset]) -> List[Dataset]:
        """
        This method uploads DICOM instances to the ADIT DICOMweb server.

        :param instances: The DICOM instances to upload.
        :return: The response of the ADIT DICOMweb server.
        """
        results = []
        for ds in instances:
            results.append(self.dicomweb_client.store_instances([ds]))
        return results
