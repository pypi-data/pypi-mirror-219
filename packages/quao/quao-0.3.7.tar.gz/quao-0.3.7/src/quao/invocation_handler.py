"""
    QuaO Project invocation_handler.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from abc import abstractmethod

from . import Backend, ResponseUtils
from ..quao import RequestData


class InvocationHandler:
    def __init__(self, event):
        self.event = event

    def invoke(self):
        request_data = RequestData(self.event)
        backend = Backend(request_data)

        circuit = self.generate_circuit(request_data.input)

        job = backend.submit_job(circuit)

        response = ResponseUtils.generate_response(job)

        return response

    @abstractmethod
    def generate_circuit(self, invocation_input):
        pass
