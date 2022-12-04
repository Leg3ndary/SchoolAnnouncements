import json
from typing import Dict, List, Union

import googleapiclient.discovery
from httplib2 import Http
from oauth2client import client, file, tools


class Wrapper:
    """
    The basic wrapper used to access the Google Docs API.
    """

    config: Dict[str, str]
    SCOPES: List[str] = ["https://www.googleapis.com/auth/documents.readonly"]
    DOCUMENT_ID: str
    DISCOVERY_DOC: str = "https://docs.googleapis.com/$discovery/rest?version=v1"

    def __init__(self) -> None:
        """
        Initializes the wrapper.
        """
        with open("credentials/config.json", "r", encoding="utf8") as credentials:
            self.config = json.loads(credentials.read())

        self.DOCUMENT_ID = self.config.get("Google").get("DOCID")

    async def get_credentials(self) -> dict:
        """
        Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth 2.0 flow is completed to obtain the new credentials. -Google
        """
        store = file.Storage("credentials/token.json")
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                "credentials/credentials.json", self.SCOPES
            )
            credentials = tools.run_flow(flow, store)
        return credentials

    async def save_doc(self, save: bool = False) -> Dict[str, Union[str, dict]]:
        """
        Save the doc by sending it back
        """
        credentials = await self.get_credentials()
        http = credentials.authorize(Http())
        docs_service = googleapiclient.discovery.build(
            "docs", "v1", http=http, discoveryServiceUrl=self.DISCOVERY_DOC
        )
        doc = docs_service.documents().get(documentId=self.DOCUMENT_ID).execute()
        if save:
            with open("data/doc.json", "w", encoding="utf8") as doc_file:
                doc_file.write(json.dumps(doc))
        return doc
