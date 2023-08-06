"""
    QuaO Project backend.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
import io
from json import JSONDecodeError

import requests
from braket.circuits import Circuit
from qbraid import circuit_wrapper
from qiskit import transpile, Aer
from qiskit_ibm_provider import IBMProvider

from .data.job.job_response import JobResponse
from .data.request.request_data import RequestData
from .enum.http_header import HttpHeader
from .enum.job_status import JobStatus
from .enum.media_type import MediaType
from .enum.provider_type import ProviderType
from .enum.sdk import Sdk
from .enum.token_type import TokenType
from .factory.device_factory import DeviceFactory
from .factory.provider_factory import ProviderFactory
from .config.logging_config import *


class Backend:
    def __init__(self, request_data: RequestData):
        self.server_url = request_data.server_url
        self.sdk = request_data.sdk
        self.input = request_data.input
        self.shots = request_data.shots
        self.circuit_export_url = request_data.circuit_export_url
        self.device_id = request_data.device_id
        self.backend_data = None
        self.user_token = request_data.user_token
        self.user_identity = request_data.user_identity

    def submit_job(self, circuit) -> JobResponse:
        """

        @param circuit:
        @return:
        """
        logger.debug('Pre-execute job!')
        self.__pre_execute_job(circuit)

        logger.debug('Execute job!')
        job_response = self.__execute_job(circuit)

        logger.debug('Post-execute job!')
        self.__post_execute_job(circuit)

        return job_response

    @staticmethod
    def __get_qubit_number(circuit, sdk) -> int:
        """

        @param circuit:
        @param sdk:
        @return:
        """

        if Sdk.QISKIT.value.__eq__(sdk):
            return int(circuit.num_qubits)

        if Sdk.BRAKET.value.__eq__(sdk):
            return circuit.qubit_count

        return 0

    @staticmethod
    def __generate_backend_request(device_id, required_qubit):
        """

        @param device_id:
        @param required_qubit:
        @return:
        """

        backend_request = {
            "deviceId": device_id,
            "qubitAmount": required_qubit
        }

        return backend_request

    @staticmethod
    def __generate_backend_header(user_token):
        """

        @param user_token:
        """
        backend_header = {
            HttpHeader.AUTHORIZATION.value: TokenType.BEARER.value + ' ' + user_token
        }

        return backend_header

    def __set_backend_data(self, backend_request, backend_header):
        """

        @param backend_request:
        """

        response = requests.get(
            self.server_url,
            params=backend_request,
            headers=backend_header
        )
        if response.status_code == 200:
            try:
                self.backend_data = response.json().get("data")
            except JSONDecodeError:
                pass
        else:
            pass

    def __pre_execute_job(self, circuit):
        """

        @param circuit:
        """

        required_qubit = self.__get_qubit_number(circuit, self.sdk)
        backend_request = self.__generate_backend_request(self.device_id, required_qubit)
        backend_header = self.__generate_backend_header(self.user_token)

        logger.debug('Device selection request: {0}'.format(backend_request))

        self.__set_backend_data(backend_request, backend_header)

    def __execute_job(self, circuit) -> JobResponse:
        """

        @param circuit:
        @return:
        """

        error_job_response = JobResponse()
        error_job_response.job_status = JobStatus.ERROR.value
        error_job_response.user_identity = self.user_identity
        error_job_response.user_token = self.user_token

        shots = self.shots

        if circuit and self.backend_data:
            device_name = self.backend_data.get("deviceName")
            provider_tag = self.backend_data.get("providerTag")
            authentication = self.backend_data.get("authentication")

            try:
                logger.debug('Execute job with provider tag: {0}'.format(provider_tag))
                provider = ProviderFactory().create_provider(provider_tag, authentication)

                logger.debug('Execute job with device name: {0}'.format(device_name))
                device = DeviceFactory().create_device(provider, device_name, authentication,
                                                       self.sdk)

                job_response = device.run_circuit(circuit=circuit, shots=shots)
                job_response.user_identity = self.user_identity
                job_response.user_token = self.user_token

                return job_response

            except Exception as exception:
                error_job_response.job_result = {"error": str(exception)}

        elif self.backend_data is None:
            error_job_response.job_result = {"error": "Backend not found"}

        return error_job_response

    def __post_execute_job(self, circuit):
        """

        @param circuit:
        """

        self.__export_circuit(circuit)

    def __export_circuit(self, circuit):
        """
          Export circuit to svg file then send to QuaO server for saving
          Args:
              circuit: circuit will be exported
              @param circuit:
        """
        if self.circuit_export_url is None or len(self.circuit_export_url) < 1:
            return

        logger.debug("Preparing circuit figure...")
        transpiled_circuit = self.__transpile_circuit(circuit)
        circuit_figure = transpiled_circuit.draw(output='mpl', fold=-1)

        logger.debug("Converting circuit figure to svg file...")
        figure_buffer = io.BytesIO()
        circuit_figure.savefig(figure_buffer, format='svg', bbox_inches='tight')

        logger.debug("Sending circuit svg image to [{0}] with POST method ...".format(
            self.circuit_export_url))

        payload = {'circuit': (
            'circuit_figure',
            figure_buffer.getvalue(),
            MediaType.MULTIPART_FORM_DATA.value)}

        response = requests.post(url=self.circuit_export_url,
                                 headers=self.__generate_backend_header(self.user_token),
                                 files=payload)
        if response.ok:
            logger.debug("Sending request to QuaO backend successfully!")
        else:
            logger.debug("Sending request to QuaO backend failed with status {0}!".format(
                response.status_code))

    def __transpile_circuit(self, circuit):
        if isinstance(circuit, Circuit):
            return circuit_wrapper(circuit).transpile(Sdk.QISKIT.value)

        qiskit_device_name = self.backend_data.get("deviceName")

        if ProviderType.QUAO_QUANTUM_SIMULATOR.value.__eq__(self.backend_data.get("providerTag")):
            return transpile(circuits=circuit,
                             backend=Aer.get_backend(qiskit_device_name))

        provider = IBMProvider(token=self.backend_data.get("authentication").get('token'))
        backend = provider.get_backend(qiskit_device_name)

        return transpile(circuits=circuit, backend=backend)
