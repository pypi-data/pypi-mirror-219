#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   Script to harvest public committee data from Modern.Gov websites
   data is ingested into Preservica using the following hierarchy

   Folder -> Committee
        Folder -> Meeting
            Asset -> Meeting Documents


   Requires Python 3.8/3.9/3.10
   Requires pyPreservica
   python -m pip install pyPreservica pathvalidate bs4

"""
import pathlib
import tempfile
import xml.etree.ElementTree
from datetime import date
import datetime
import dateutil.parser as parser
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pyPreservica import *
import pkgutil

MGOV_NS = "https://moderngov.gov.uk/"

xml.etree.ElementTree.register_namespace("committee", "https://moderngov.gov.uk/committee")
xml.etree.ElementTree.register_namespace("meeting", "https://moderngov.gov.uk/meeting")
xml.etree.ElementTree.register_namespace("attachment", "https://moderngov.gov.uk/attachment")

logger = logging.getLogger(__name__)
LOG_FILENAME = f'modern-gov-ingest-{date.today()}.log'

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logger.setLevel(logging.INFO)

filehandler = logging.FileHandler(LOG_FILENAME, mode="a")
filehandler.setFormatter(formatter)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)
logger.addHandler(filehandler)


class PreservicaGov:
    def __init__(self, callback=None, stopCallback=None):
        self.callback = callback
        self.stopCallback = stopCallback
        if pathlib.Path('credentials.properties').is_file():
            if callback is not None:
                callback(f"Loading configuration from credentials.properties")
            logger.info(f"Loading configuration from credentials.properties")
            config = configparser.ConfigParser(interpolation=configparser.Interpolation())
            config.read('credentials.properties', encoding='utf-8')
            self.security_tag = config['Modern.Gov'].get('security.tag', 'closed')
            self.parent_folder = config['Modern.Gov'].get('parent.folder', '')
            self.client = EntityAPI()
            self.upload = UploadAPI()
            self.folder = self.client.folder(self.parent_folder)
            if callback is not None:
                callback(f"Found Parent Folder {self.folder.title}")
            logger.info(f"Found Parent Folder {self.folder.title}")
            if callback is not None:
                callback(f"Found Security Tag {self.security_tag}")
            logger.info(f"Found Security Tag {self.security_tag}")
            self.site_name = config['Modern.Gov'].get('site_name', '')
            if not self.site_name.endswith("/"):
                self.site_name = f"{self.site_name}/"
            if callback is not None:
                callback(f"Modern.Gov Site {self.site_name}")
            logger.info(f"Modern.Gov Site {self.site_name}")

            # read the dates from the properties file
            self.from_date = config['Modern.Gov'].get('committee.FromDate', '')
            self.to_date = config['Modern.Gov'].get('committee.ToDate', '')
            # parse the dates to check they are valid
            fromdate = parser.parse(self.from_date)
            todate = parser.parse(self.to_date)
            logger.info(f"Searching for content between {fromdate} and {todate}")
            self.committee_identifier = f"{self.site_name} committeeid"
            self.meeting_identifier = f"{self.site_name} meetingid"

            self.temp_meeting_image = tempfile.NamedTemporaryFile(delete=False)
            self.temp_meeting_image.write(pkgutil.get_data(__package__, 'images/meeting.png'))
            self.temp_meeting_image.close()

            self.committee_image = tempfile.NamedTemporaryFile(delete=False)
            self.committee_image.write(pkgutil.get_data(__package__, 'images/committee.png'))
            self.committee_image.close()
        else:
            logger.info(f"No configuration (credentials.properties) found")
            logger.info(f"An empty configuration file has been created for you")
            config = configparser.RawConfigParser(interpolation=None)
            config['credentials'] = {'username': '', 'password': '',  'server': ''}
            config['Modern.Gov'] = {'security.tag': '', 'site_name': '', 'parent.folder': '',
                                    'committee.FromDate': '01/01/1980', 'committee.ToDate': '01/01/2024'}

            with open('credentials.properties', 'wt', encoding="utf-8") as configfile:
                config.write(configfile)
            exit(1)

    def harvest(self):
        if self.site_name:
            if self.callback is not None:
                self.callback(f"Ingesting content from {self.site_name} into folder {self.folder.title}")
            logger.info(f"Ingesting content from {self.site_name} into folder {self.folder.title}")
            self.__main()

    def __add_meeting(self, meeting_id, meeting_date, committee_folder, committee_id):
        domain_url = self.site_name
        params = {"lmeetingid": str(meeting_id)}
        response = requests.get(f"{domain_url}/mgwebservice.asmx/GetMeeting", params=params, verify=True)
        if response.status_code != 200:
            if self.callback is not None:
                self.callback(f"Failed to fetch metadata for {response.url}")
            logger.error(f"Failed to fetch metadata for {response.url}")
            logger.error(response.content.decode("utf-8"))
            return
        if response.status_code == 200:
            meeting_response = response.content.decode("utf-8")
            meeting_response = meeting_response.replace("<meeting>",
                                                        f"<meeting xmlns=\"{MGOV_NS}meeting\">")

            meeting_response = meeting_response.replace("<div", "<![CDATA[<div")
            meeting_response = meeting_response.replace("</div>", "</div>]]>")

            meeting_object = xml.etree.ElementTree.fromstring(meeting_response)
            existing_meeting = self.client.identifier(self.meeting_identifier, str(meeting_id))
            if len(existing_meeting) == 0:

                d = datetime.datetime.strptime(meeting_date, '%d/%m/%Y')
                meeting_title = f"Meeting {d.date()}"

                meeting_location = meeting_object.find(".//{*}meetinglocation").text
                if self.callback is not None:
                    self.callback(f"Creating Meeting: {meeting_title}")
                logger.info(f"Creating Meeting: {meeting_title}")
                meeting_folder = self.client.create_folder(meeting_title, meeting_location, self.security_tag,
                                                           committee_folder.reference)
                self.client.add_identifier(meeting_folder, self.meeting_identifier, str(meeting_id))
                self.client.add_thumbnail(meeting_folder, self.temp_meeting_image.name)
            else:
                meeting_folder = existing_meeting.pop()
                if self.callback is not None:
                    self.callback(f"Found Existing Meeting: {meeting_folder.title}")
                logger.info(f"Found Existing Meeting: {meeting_folder.title}")
            meeting_folder = self.client.folder(meeting_folder.reference)
            meeting_metadata = self.client.metadata_for_entity(meeting_folder, f"{MGOV_NS}meeting")
            if meeting_metadata is None:
                m_date = meeting_object.find('.//{*}meetingdate')
                parse_date = parser.parse(meeting_date)
                m_date.text = f"{parse_date.isoformat()}Z"
                new_xml = xml.etree.ElementTree.tostring(meeting_object, encoding='UTF-8', xml_declaration=True).decode(
                    "utf-8")
                self.client.add_metadata(meeting_folder, f"{MGOV_NS}meeting", new_xml)

            #  try and fetch the link to the meeting minutes
            params = {"CId": committee_id, "MId": meeting_id}
            html_response = requests.get(f"{domain_url}/ieListDocuments.aspx", verify=True, params=params)
            html = html_response.content.decode("utf-8")
            soup = BeautifulSoup(html, 'html.parser')
            for item in soup.find("ul", class_="mgActionList").findAll('li'):
                href = item.contents[0]['href']
                if (f'documents/g{meeting_id}' in href) and ('.pdf' in href):
                    existing_docs = self.client.identifier(f"{domain_url} attachment", href)
                    if len(existing_docs) == 0:
                        pdf_response = requests.get(f"{domain_url}/{href}", stream=True, verify=True)
                        title = item.contents[0]['title']
                        title = title.replace("Link to", "")
                        file_name = sanitize_filename(title).strip()
                        if self.callback is not None:
                            self.callback(f"Adding Document: {file_name}")
                        logger.info(f"Adding Document: {file_name}")
                        with open(f'{file_name}.pdf', 'wb') as fd:
                            for chunk in pdf_response.iter_content(1024):
                                fd.write(chunk)
                            fd.close()
                            doc_identifiers = {f"{domain_url} attachment": href}
                            p = simple_asset_package(preservation_file=f'{file_name}.pdf', parent_folder=meeting_folder,
                                                     Title=title, Description=f'{file_name}.pdf',
                                                     SecurityTag=self.security_tag,
                                                     Identifiers=doc_identifiers)
                            self.upload.upload_zip_package(path_to_zip_package=p, folder=meeting_folder,
                                                           callback=UploadProgressConsoleCallback(p),
                                                           delete_after_upload=True)
                            os.remove(f'{file_name}.pdf')
                            time.sleep(10)

            linkeddocs = meeting_object.findall('.//{*}linkeddoc')
            for linkdodc in linkeddocs:
                attachment_id = linkdodc.find(f'.//{{*}}attachmentid').text
                title = linkdodc.find(f'.//{{*}}title').text
                owner_title = linkdodc.find(f'.//{{*}}ownertitle').text
                params = {"lAttachmentId": str(attachment_id)}
                response = requests.get(f"{domain_url}/mgWebService.asmx/GetAttachment", params=params, verify=True)
                if response.status_code == 200:
                    attachment_xml = response.content.decode("utf-8")
                    attachment_xml = attachment_xml.replace("<attachment>",
                                                            f"<attachment xmlns=\"{MGOV_NS}attachment\">")

                    attachment_response = xml.etree.ElementTree.fromstring(attachment_xml)
                    urlobject = attachment_response.find(f'.//{{*}}url')
                    if urlobject is not None:
                        url = urlobject.text.strip()
                        if url:
                            existing_docs = self.client.identifier(f"{domain_url} attachment", url)
                            if len(existing_docs) > 0:
                                if self.callback is not None:
                                    self.callback(f"Found Existing Document {title} skipping...")
                                logger.info(f"Found Existing Document {title} skipping...")
                            if len(existing_docs) == 0:
                                if self.callback is not None:
                                    self.callback(f"Adding Document: {title}")
                                logger.info(f"Adding Document: {title}")
                                pdf_response = requests.get(url, stream=True, verify=True)
                                file_name = sanitize_filename(title).strip()
                                if len(file_name) > 120:
                                    file_name = file_name[:100] + "..." + file_name[-10:]
                                with open(f'{file_name}.pdf', 'wb') as fd:
                                    for chunk in pdf_response.iter_content(1024):
                                        fd.write(chunk)
                                    fd.close()
                                doc_identifiers = {f"{domain_url} attachment": url}
                                asset_metadata = {f'{MGOV_NS}attachment': attachment_xml}
                                p = simple_asset_package(preservation_file=f'{file_name}.pdf',
                                                         parent_folder=meeting_folder,
                                                         Title=title, Description=owner_title,
                                                         SecurityTag=self.security_tag,
                                                         Identifiers=doc_identifiers, Asset_Metadata=asset_metadata)
                                self.upload.upload_zip_package(path_to_zip_package=p, folder=meeting_folder,
                                                               callback=UploadProgressConsoleCallback(p))
                                os.remove(f'{file_name}.pdf')
                                time.sleep(10)

    def __main(self):
        domain_url = self.site_name
        sFromDate = parser.parse(self.from_date).strftime("%d/%m/%Y")
        sToDate = parser.parse(self.to_date).strftime("%d/%m/%Y")
        response = requests.get(f"{domain_url}/mgwebservice.asmx/GetCommittees", verify=True)
        if response.status_code == 200:
            get_committees_response = response.content.decode("utf-8")
            committees_object = xml.etree.ElementTree.fromstring(get_committees_response)
            committees_count = int(committees_object.find(f'./committeescount').text)
            logger.info(f"Found {committees_count} Committees")
            committees = committees_object.findall(".//committee")
            for committee in committees:

                if self.stopCallback is not None:
                    if self.stopCallback():
                        break

                try:
                    committee_id = int(committee.find(".//committeeid").text)
                    title = committee.find(".//committeetitle").text
                    if committee.find(".//committeecategory") is not None:
                        category = committee.find(".//committeecategory").text
                    else:
                        category = ""

                    if self.callback is not None:
                        self.callback(f"Found Committee {title} with id {str(committee_id)}")
                    logger.info(f"Found Committee {title} with id {str(committee_id)}")
                    existing_committee = self.client.identifier(self.committee_identifier, str(committee_id))
                    if len(existing_committee) == 0:
                        if self.callback is not None:
                            self.callback(f"Creating New Committee: {title}")
                        logger.info(f"Creating New Committee: {title}")
                        committee_folder = self.client.create_folder(title, category, self.security_tag,
                                                                     self.parent_folder)
                        self.client.add_identifier(committee_folder, self.committee_identifier, str(committee_id))
                        self.client.add_thumbnail(committee_folder, self.committee_image.name)
                    else:
                        committee_folder = existing_committee.pop()
                        if self.callback is not None:
                            self.callback(f"Using Existing Committee: {title}")
                        logger.info(f"Using Existing Committee: {title}")
                    committee_folder = self.client.folder(committee_folder.reference)
                    params = {"lCommitteeId": committee_id, "sFromDate": sFromDate, "sToDate": sToDate}
                    response = requests.get(f"{domain_url}/mgwebservice.asmx/GetMeetings", params=params, verify=True)
                    if response.status_code == 200:
                        if self.callback is not None:
                            self.callback(f"Found List of Committee Meetings")
                        logger.info(f"Found List of Committee Meetings")
                        get_meetings_response = response.content.decode("utf-8")
                        get_meetings_response = get_meetings_response.replace("<getmeetings>",
                                                                              f"<getmeetings xmlns=\"{MGOV_NS}committee\">")
                        get_meetings_response = get_meetings_response.replace("<div", "<![CDATA[<div")
                        get_meetings_response = get_meetings_response.replace("</div>", "</div>]]>")

                        m = self.client.metadata_for_entity(committee_folder, f"{MGOV_NS}committee")
                        if not m:
                            self.client.add_metadata(committee_folder, f"{MGOV_NS}committee", get_meetings_response)

                        meetings_object = xml.etree.ElementTree.fromstring(get_meetings_response)

                        if meetings_object.find(".//{*}meetingscount") is not None:
                            meeting_count = int(meetings_object.find(".//{*}meetingscount").text.strip())
                            if self.callback is not None:
                                self.callback(f"Found {meeting_count} Meetings in Committee {title}")
                            logger.info(f"Found {meeting_count} Meetings in Committee {title}")

                        meetings = meetings_object.findall(".//{*}meeting")
                        for meeting in meetings:

                            if self.stopCallback is not None:
                                if self.stopCallback():
                                    break

                            meeting_id = int(meeting.find(".//{*}meetingid").text)
                            meeting_date = meeting.find(".//{*}meetingdate").text
                            if self.callback is not None:
                                self.callback(f"Adding Meeting {meeting_id}")
                            logger.info(f"Adding Meeting {meeting_id}")
                            self.__add_meeting(meeting_id, meeting_date, committee_folder, committee_id)

                except:
                    pass
