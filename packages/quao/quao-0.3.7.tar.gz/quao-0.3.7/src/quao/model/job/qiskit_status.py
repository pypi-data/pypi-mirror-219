"""
    QuaO Project job_status.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit_ibm_runtime import QiskitRuntimeService

from ...data.job.job_response import JobResponse
from ...enum.job_status import JobStatus
from ...enum.media_type import MediaType
from ...util.json_parser_util import JsonParserUtils
from ...config.logging_config import *


class Job:
    def __init__(self, channel, token, crn, provider_job_id, user_identity):
        self.channel = channel if channel else "ibm_quantum"
        self.token = token if token else ""
        self.crn = crn
        self.job_id = provider_job_id if provider_job_id else ""
        self.retrieve_job = self.__get_job()
        self.user_identity = user_identity

    def fetch_job(self) -> JobResponse:
        logger.info("Start get job info.")

        provider_job_id = self._get_provider_job_id()
        job_status = self._get_job_status()
        job_result_dictionary = {}
        content_type = None
        job_histogram = None
        execution_time = None

        try:
            if JobStatus.DONE.value.__eq__(job_status):
                logger.info("Try to get job result")

                job_result = self.retrieve_job.result()
                job_status = self._get_job_status()

                logger.info("Parsing job result")
                job_result_dictionary = self._parse_job_result(job_result)

                content_type = MediaType.APPLICATION_JSON.value

                logger.info("Producing histogram")
                job_histogram = self._produce_histogram_data(job_result)

                logger.debug('Calculating execution time ....')
                execution_time = self._get_execution_time(job_result_dictionary)
                logger.debug('Execution time calculation completed!')

        except Exception as exception:

            logger.info("Try to job result error.")
            job_result_dictionary = {
                "error": "Exception when invoke job on device: " + self.retrieve_job.backend().backend_name,
                "exception": str(exception)
            }

            job_status = JobStatus.ERROR.value

        return JobResponse(
            provider_job_id=provider_job_id,
            job_status=job_status,
            job_result=job_result_dictionary,
            content_type=content_type,
            job_histogram=job_histogram,
            user_identity=self.user_identity,
            execution_time=execution_time
        )

    def __get_job(self):
        logger.info("Has IBM token: {0}".format((self.token is not None) and (len(self.token) > 0)))

        service = QiskitRuntimeService(channel=self.channel,
                                       token=self.token,
                                       instance=self.crn)

        return service.job(job_id=self.job_id)

    def _get_provider_job_id(self) -> str:
        return self.retrieve_job.job_id()

    def _get_job_status(self) -> str:
        return self.retrieve_job.status().name

    @staticmethod
    def _produce_histogram_data(job_result) -> dict:
        try:
            histogram_data = job_result.get_counts()
        except Exception:
            histogram_data = None

        return histogram_data

    def _parse_job_result(self, job_result):
        if self.retrieve_job.program_id == 'sampler':
            return JsonParserUtils.parse(job_result.__dict__)
        return JsonParserUtils.parse(job_result.to_dict())

    @staticmethod
    def _get_execution_time(job_result):
        if 'metadata' not in job_result:
            return None

        metadata = job_result['metadata']

        if metadata is None \
                or not bool(metadata) \
                or 'time_taken_execute' not in metadata:
            return None

        return metadata['time_taken_execute']
