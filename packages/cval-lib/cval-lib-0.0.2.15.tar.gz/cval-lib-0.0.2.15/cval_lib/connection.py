from requests import Session

from cval_lib.handlers.dataset import Dataset
from cval_lib.handlers.embedding import Embedding
from cval_lib.handlers.detection import Detection
from cval_lib.handlers.result import Result


class CVALConnection:
    def __init__(self, user_api_key: str):
        self._session = Session()
        self._session.headers = {'user_api_key': user_api_key}

    def dataset(self):
        """
        actions with dataset: : create, get, delete, update by ID or all (with some limits)
        :return: Dataset
        """
        return Dataset(session=self._session)

    def embedding(self, dataset_id: str, type_of_dataset: str):
        """
        actions with embedding: create, get, delete, update by ID or all (with some limits)
        :param dataset_id: id of dataset
        :param type_of_dataset: type of dataset (training, test, validation)
        :return: Embedding
        """
        return Embedding(self._session, dataset_id=dataset_id, type_of_dataset=type_of_dataset)

    def detection(self, ):
        """
        This method can be used to call a detection sampling or test
        :return: Detection
        """
        return Detection(self._session)

    def result(self):
        """
        This method can be used for polling
        :return: Result
        """
        return Result(self._session)

    def __del__(self):
        self._session.close()
        del self
