import logging
from datetime import date
from pyPreservica import AdminAPI
import pkgutil

logger = logging.getLogger(__name__)
LOG_FILENAME = f'modern-gov-schema-{date.today()}.log'

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logger.setLevel(logging.INFO)

filehandler = logging.FileHandler(LOG_FILENAME, mode="a")
filehandler.setFormatter(formatter)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)
logger.addHandler(filehandler)

COMMITTEE_XSD = "https://moderngov.gov.uk/committee"
MEETING_XSD = "https://moderngov.gov.uk/meeting"
ATTACHMENT_XSD = "https://moderngov.gov.uk/attachment"

CMIS_XSD = "http://www.tessella.com/sdb/cmis/metadata"


class Schema:
    def load_cmis(self, callback=None):
        client = AdminAPI()
        if callback is not None:
            callback(f"Looking for Modern.Gov XML CMIS Transforms for UA")
        logger.info(f"Looking for Modern.Gov XML CMIS Transforms for UA")
        has_committee_cmis = False
        has_meeting_cmis = False
        has_attachment_cmis = False
        for transform in client.xml_transforms():
            if transform['FromSchemaUri'] == COMMITTEE_XSD:
                has_committee_cmis = True
                if callback is not None:
                    callback(f"Found Existing Modern.Gov Committee CMIS Transform")
                logger.info(f"Found Existing Modern.Gov Committee CMIS Transform")
            if transform['FromSchemaUri'] == MEETING_XSD:
                has_meeting_cmis = True
                if callback is not None:
                    callback(f"Found Existing Modern.Gov Meeting CMIS Transform")
                logger.info(f"Found Existing Modern.Gov Meeting CMIS Transform")
            if transform['FromSchemaUri'] == ATTACHMENT_XSD:
                has_attachment_cmis = True
                if callback is not None:
                    callback(f"Found Existing Modern.Gov Attachment CMIS Transform")
                logger.info(f"Found Existing Modern.Gov Attachment CMIS Transform")

        if not has_committee_cmis:
            if callback is not None:
                callback(f"Adding Modern.Gov Committee CMIS Transform")
            logger.info(f"Adding Modern.Gov Committee CMIS Transform")
            data = pkgutil.get_data(__package__, 'schema/mg-committee-CMIS.xsl')
            client.add_xml_transform("Modern.Gov Committee CMIS Transform", COMMITTEE_XSD, CMIS_XSD, "transform",
                                     "mg-committee-CMIS.xsl", data)
        if not has_meeting_cmis:
            if callback is not None:
                callback(f"Adding Modern.Gov Meeting Index")
            logger.info(f"Adding Modern.Gov Meeting Index")
            data = pkgutil.get_data(__package__, 'schema/mg-meeting-CMIS.xsl')
            client.add_xml_transform("Modern.Gov Meeting CMIS Transform", MEETING_XSD, CMIS_XSD, "transform",
                                     "mg-meeting-CMIS.xsl", data)
        if not has_attachment_cmis:
            if callback is not None:
                callback(f"Adding Modern.Gov Attachment Index")
            logger.info(f"Adding Modern.Gov Attachment Index")
            data = pkgutil.get_data(__package__, 'schema/mg-attachment-CMIS.xsl')
            client.add_xml_transform("Modern.Gov Attachment CMIS Transform", ATTACHMENT_XSD, CMIS_XSD, "transform",
                                     "mg-attachment-CMIS.xsl", data)

    def load_indexes(self):
        client = AdminAPI()

        logger.info(f"Looking for Modern.Gov XML Custom Indexes")
        has_committee_xml = False
        has_meeting_xml = False
        has_attachment_xml = False
        for document in client.xml_documents():
            if document['SchemaUri'] == "http://www.preservica.com/customindex/v1":
                if document['Name'] == "Modern.Gov Committee Index":
                    has_committee_xml = True
                    logger.info(f"Found Existing Modern.Gov Committee Index")
                if document['Name'] == "Modern.Gov Meeting Index":
                    has_meeting_xml = True
                    logger.info(f"Found ExistingModern.Gov Meeting Index")
                if document['Name'] == "Modern.Gov Attachment Index":
                    has_attachment_xml = True
                    logger.info(f"Found Existing Modern.Gov Attachment Index")

        if not has_committee_xml:
            logger.info(f"Adding Modern.Gov Committee Index")
            data = pkgutil.get_data(__package__, 'schema/mg-committee-Index.xml')
            client.add_xml_document("Modern.Gov Committee Index", data, "CustomIndexDefinition")
        if not has_meeting_xml:
            logger.info(f"Adding Modern.Gov Meeting Index")
            data = pkgutil.get_data(__package__, 'schema/mg-meeting-Index.xml')
            client.add_xml_document("Modern.Gov Meeting Index", data, "CustomIndexDefinition")
        if not has_attachment_xml:
            logger.info(f"Adding Modern.Gov Attachment Index")
            data = pkgutil.get_data(__package__, 'schema/mg-attachment-Index.xml')
            client.add_xml_document("Modern.Gov Attachment Index", data, "CustomIndexDefinition")

    def load_schema(self):
        client = AdminAPI()

        logger.info(f"Looking for Modern.Gov XML Schema Documents")
        has_committee_xsd = False
        has_meeting_xsd = False
        has_attachment_xsd = False
        for schema in client.xml_schemas():
            if schema['SchemaUri'] == COMMITTEE_XSD:
                has_committee_xsd = True
                logger.info(f"Found Existing Modern.Gov Committee Schema")
            if schema['SchemaUri'] == MEETING_XSD:
                has_meeting_xsd = True
                logger.info(f"Found ExistingModern.Gov Meeting Schema")
            if schema['SchemaUri'] == ATTACHMENT_XSD:
                has_attachment_xsd = True
                logger.info(f"Found Existing Modern.Gov Attachment Schema")

        if not has_committee_xsd:
            logger.info(f"Adding Modern.Gov Committee Schema")
            data = pkgutil.get_data(__package__, 'schema/mg-committee-schema.xsd')
            client.add_xml_schema("Modern.Gov Committee Schema", "XML Schema for Modern.Gov Committee",
                                  "mg-committee-schema.xsd", data)
        if not has_meeting_xsd:
            logger.info(f"Adding Modern.Gov Meeting Schema")
            data = pkgutil.get_data(__package__, 'schema/mg-meeting-schema.xsd')
            client.add_xml_schema("Modern.Gov Meeting Schema", "XML Schema for Modern.Gov Meeting",
                                  "mg-meeting-schema.xsd", data)
        if not has_attachment_xsd:
            logger.info(f"Adding Modern.Gov Attachment Schema")
            data = pkgutil.get_data(__package__, 'schema/mg-attachment-schema.xsd')
            client.add_xml_schema("Modern.Gov Attachment Schema", "XML Schema for Modern.Gov Attachments",
                                  "mg-attachment-schema.xsd", data)
