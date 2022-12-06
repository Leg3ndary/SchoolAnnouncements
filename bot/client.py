import datetime
import json
import re
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
        doc = (
            docs_service.documents()
            .get(documentId=self.DOCUMENT_ID)
            .execute()
            .get("body")
            .get("content")
        )

        full = await self.read_strucutural_elements(doc)
        organized = await self.organize_doc(full, True)

        if save:
            with open("data/doc.json", "w", encoding="utf8") as doc_file:
                doc_file.write(json.dumps(doc, indent=4))
            with open("data/full.md", "w", encoding="utf8") as full_file:
                full_file.write(full)

        return organized

    async def read_paragraph_element(self, element: dict) -> str:
        """
        Returns the text in the given ParagraphElement, this messy bit of parsing
        is how we get each separate line of text without all of it's odd
        formatting and fonts.
        """
        text_run = element.get("textRun")

        if not text_run:
            return ""

        text_style = text_run.get("textStyle")
        is_bolded = text_style.get("bold")
        is_underlined = text_style.get("underline")
        foreground = text_style.get("foregroundColor")
        if foreground:
            rgb_blue_color = foreground.get("color").get("rgbColor").get("blue")
        else:
            rgb_blue_color = None

        font_size = text_style.get("fontSize")
        if font_size:
            magnitude = font_size.get("magnitude")
        else:
            magnitude = None

        if "APHS DAILY ANNOUNCEMENTS" in text_run.get("content"):
            # For some reason the title shares the same stuff as days, so yes...
            return f"# {text_run.get('content', '')}"

        if is_bolded and is_underlined and rgb_blue_color == 1 and magnitude == 14:
            if text_run.get("content").strip() == "":
                return text_run.get("content")
            # Shouldn't ever return nothing but might happen...
            return f"## {text_run.get('content', '')}"

        # The club name/announcement name is always bolded and of magnitude 10!
        if is_bolded and magnitude == 10:
            return f"**{text_run.get('content', '').replace('-', '').strip()}**"

        return text_run.get("content", "")

    async def read_strucutural_elements(self, elements: Dict) -> str:
        """
        Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Parameters
        ----------
        elements: list
            a list of Structural Elements.

        Returns
        -------
        Not sure
        """
        text = ""
        flag = False
        for value in elements:
            if "paragraph" in value:
                elements = value.get("paragraph").get("elements")

                for elem in elements:
                    if elem.get("textRun"):
                        if "APHS DAILY ANNOUNCEMENTS - 2022 - 2023\n" in elem.get(
                            "textRun"
                        ).get("content"):
                            flag = True
                        # So we don't really want every announcement, that would take forever to parse
                        # Therefore we ignore anything not in the 2022/2023 school year
                        elif "SCHOOL YEAR 2021 - 2022\n" in elem.get("textRun").get(
                            "content"
                        ):
                            flag = False
                    if flag:
                        text += await self.read_paragraph_element(elem)

        return text

    async def organize_doc(self, text: str, save: bool = False) -> Dict[str, Union[str, dict]]:
        """
        Organize the text into a nice dict for us to use
        """
        full = {}

        days_split = text.split("## ")

        del days_split[0]  # Delete aphs daily announcements title stuff

        for day in days_split:
            temp_announcements = {}
            for announcement in day.split("\n\n**")[1:]:
                # Yes I know this is a hot mess of parsing, but our school's announcement writers can't decide on a single format to use so this is what we end up with
                a_info = list(filter(None, announcement.split("**")))
                if a_info:
                    if len(a_info) == 1:
                        pass
                    elif not a_info[0] == "\n":

                        cleansed = re.sub(r"^- ", "", a_info[1].strip())
                        if cleansed[0].isalpha():
                            if cleansed[0] == cleansed[0].lower():
                                cleansed = f"{a_info[0]} {cleansed}"
                        temp_announcements[a_info[0]] = cleansed

            day_info = day.split("\n\n")[0].strip().split(" ")
            day_name = day_info[0].capitalize()
            month = day_info[1][:3].capitalize()
            date = day_info[2].capitalize()
            year = datetime.datetime.now().year

            # So our school can't decide what format of dates to use, so we get stuck with just trying both hoping it'll work T-T
            try:
                datetime_info = datetime.datetime.strptime(
                    f"{day_name} {month} {date} {year}", "%A %b %d %Y"
                )
            except ValueError:
                datetime_info = datetime.datetime.strptime(
                    f"{day_name} {month} {date} {year}", "%A %d %b %Y"
                )
            temp_announcements["timestamp"] = int(datetime_info.timestamp())

            full[
                datetime_info.strftime("%A %B %d")
            ] = temp_announcements  # this will fail in 2023 if they start adding the year to announcements so hopefully they don't...

        if save:
            with open("data/announcements.json", "w", encoding="utf8") as announcements:
                json.dump(full, announcements, indent=4)
