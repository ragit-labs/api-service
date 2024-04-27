import grpc
from ragit.context_service.context_service_pb2 import (
    UploadFileRequest,
    UploadFileResponse,
)
from ragit.context_service.context_service_pb2_grpc import ContextServiceStub


def main():
    max_size = 1024 * 1023
    channel = grpc.insecure_channel(
        "localhost:50051", options=[("grpc.max_receive_message_length", max_size)]
    )
    stub = ContextServiceStub(channel)

    def file_upload_iterator():
        with open("scripts/test_file.pdf", "rb") as f:
            while True:
                data = f.read(max_size)
                if not data:
                    break
                yield UploadFileRequest(
                    name="SAAS Playbook", file_type="PDF", buffer=data
                )

    for response in stub.UploadFile(file_upload_iterator()):
        print(response)


if __name__ == "__main__":
    main()
