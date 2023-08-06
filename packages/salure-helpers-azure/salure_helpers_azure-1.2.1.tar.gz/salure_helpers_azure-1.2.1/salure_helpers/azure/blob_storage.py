from salure_helpers.salureconnect import SalureConnect
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from typing import Union, List
from datetime import datetime, timedelta


class BlobStorage(SalureConnect):
    def __init__(self, label: Union[str, List]):
        super().__init__()
        self.blob_service_client = self.__get_authentication(label=label)

    def __get_authentication(self, label):
        credentials = self.get_system_credential(system='azure-blob-storage', label=label)
        storage_account_name = credentials['storage_account_name']
        storage_account_key = credentials['storage_account_key']
        sas_token = generate_account_sas(
            account_name=storage_account_name,
            account_key=storage_account_key,
            resource_types=ResourceTypes(service=True, container=True, object=True),
            permission=AccountSasPermissions(read=True, write=True, list=True, delete=True, add=True, create=True, update=True, process=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net",
            credential=sas_token
        )

        return blob_service_client

    def get_containers(self):
        all_containers = self.blob_service_client.list_containers(include_metadata=True)
        container_list = []
        for container in all_containers:
            container_info = {
                'name': container.name,
                'last_modified': container.last_modified,
                'etag': container.etag,
                'lease_state': container.lease,
                'has_immutability_policy': container.has_immutability_policy,
                'has_legal_hold': container.has_legal_hold,
                'metadata': container.metadata
            }
            container_list.append(container_info)

        return container_list

    def get_container(self, container_name: str):
        """
        Get a container from the blob storage
        """
        container = self.blob_service_client.get_container_client(container_name)
        return container

    def create_container(self, container_name: str):
        """
        Create a container in the blob storage
        """
        response = self.blob_service_client.create_container(container_name)
        return response

    def update_container(self):
        pass

    def delete_container(self):
        pass

    def get_blobs(self):
        pass

    def create_blob(self):
        pass

    def delete_blob(self):
        pass

    def get_folders(self):
        pass

    def create_folder(self, container_name: str, folder_name: str):
        """
        Create a file with a 0 as content. Because the file is created, the folder is also created. After that the file and the folder are created,
        delete the file so the folder will stay. According to the azure docs, it should be possible to create empty files, but this is not working.
        """
        # Split the url and add the container and folder name in between the url
        original_url = self.blob_service_client.url.split('?')
        url = f"{original_url[0]}/{container_name}/{folder_name}/empty_file?{original_url[1]}"
        blob = BlobClient.from_blob_url(blob_url=url)

        # Now create the file and delete it so the folder will stay
        response = blob.upload_blob(b"0", blob_type='AppendBlob')
        blob.delete_blob()
        return response

    def delete_folder(self):
        pass
