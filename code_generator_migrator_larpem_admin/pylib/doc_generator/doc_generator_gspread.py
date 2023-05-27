#!/usr/bin/env python3

import sys

import gspread

# from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials

from .doc_connector_gspread import DocConnectorGSpread


class DocGeneratorGSpread(object):
    """
    Generate documentation with google drive spreadsheet.

    Manage file configuration and Google authentication.

    This class generate instance of DocConnectorGSpread.
    """

    def __init__(
        self,
        path_client_secret,
        file_url,
        msg_email_share_document="Vous avez été ajouté dans le manuel du joueur éditable",
    ):
        self._file_url = file_url
        self._path_client_secret = path_client_secret

        self._gc = None
        self._gc_email = ""
        self._url = ""
        self._google_file = None
        self._doc_connector = None

        self._error = None

        self._msg_invite_share = msg_email_share_document

    def get_instance(self):
        """
        Return DocConnectorGSpread instance.
        :return: instance of DocConnectorGSpread
        """
        self._error = None

        # Return doc connector if is valid, else generate a new one
        if self._doc_connector:
            # Need to check if need to reload document
            self._doc_connector.check_has_permission()
            if self._doc_connector.is_auth_valid():
                return self._doc_connector

        status = self.connect(force_connect=True)
        if not status:
            return

        status = self.update_url(ignore_error=True)
        if not status:
            return

        obj = DocConnectorGSpread(
            self._gc, self._google_file, self._msg_invite_share
        )
        self._doc_connector = obj
        return obj

    def update_url(self, url=None, save=False, ignore_error=False):
        """
        Validate the url, open a new document and can save to configuration file.
        :param url: New URL to update.
        :param save: If True, save the url to configuration file if valid.
        :param ignore_error: Can update url without generate error.
        :return: True if success else False
        """
        has_open_file = False
        status = False

        if url:
            status = self._open_file_by_url(url)
            if status:
                has_open_file = True
                self._url = url
                self._doc_connector = None
            elif not ignore_error:
                return
        else:
            info = self._file_url
            if info:
                status = self._open_file_by_url(info)
                self._url = info
                has_open_file = True
                self._doc_connector = None
            elif not ignore_error:
                self._error = "Cannot open file from empty config."
                print(self._error, file=sys.stderr)
                return False

        if not has_open_file and not ignore_error:
            self._error = "Missing url to open the remote file."
            print(self._error, file=sys.stderr)
            return False

        # if has_open_file and save:
        #     # Open config file
        #     self._parser.config.update(
        #         "google_spreadsheet.file_url", url, save=True
        #     )

        return status

    def is_auth(self):
        """

        :return: If auth with oauth2
        """
        return bool(self._gc)

    def is_file_open(self):
        """

        :return: If auth with oauth2
        """
        return bool(self._google_file)

    def has_error(self):
        """

        :return: If instance of DocGeneratorGSpread contain error.
        """
        return bool(self._error)

    def get_error(self, create_object=True, force_error=False):
        """

        :param create_object: if return dict with key "error" or return the message in string
        :param force_error: if activate, generate an unknown error message.
        :return: information about error.
        """
        msg = self._error
        if not msg and force_error:
            msg = "Unknown error."

        if create_object:
            return {"error": msg}
        return msg

    def get_url(self):
        """
        Get the url of the remote document.
        :return: String of URL
        """
        return self._url

    def get_email_service(self):
        """
        Get email to communicate with google service.
        :return: string of email
        """
        return self._gc_email

    def connect(self, force_connect=False):
        """
        Do authentication with oauth2 of Google
        :return: Success if True else Fail
        """
        if self._gc is None or force_connect:
            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ]
            try:
                # Get credentials about oauth2 Service
                # credentials = gspread.service_account(self._path_client_secret, scope)
                credentials = Credentials.from_service_account_file(
                    self._path_client_secret, scopes=scope
                )
                # credentials = ServiceAccountCredentials.from_json_keyfile_name(
                #     self._path_client_secret, scope
                # )
            except FileNotFoundError:
                self._error = (
                    "Missing file %s to configure Google Drive Spreadsheets."
                    % self._path_client_secret
                )
                print(self._error, file=sys.stderr)
                return False

            # Send http request to get authorization
            self._gc = gspread.authorize(credentials)
            if not self._gc:
                self._error = "Cannot connect to Google API Drive."
                print(self._error, file=sys.stderr)
                return False

            # Store useful information about account
            self._gc_email = credentials.service_account_email

        # Reinitialize error
        self._error = None
        return True

    def _open_file_by_name(self, name):
        """
        Open remote file by name.
        :param name: type String name to open
        :return: bool True if success else False if fail
        """
        try:
            google_file = self._gc.open(name)
        except gspread.SpreadsheetNotFound:
            self._error = "Cannot open google file from name : %s" % name
            print(self._error, file=sys.stderr)
            return False

        self._google_file = google_file
        return True

    def _open_file_by_key(self, key):
        """
        Open remote file by key.
        :param key: type String key to open
        :return: bool True if success else False if fail
        """
        try:
            google_file = self._gc.open_by_key(key)
        except gspread.SpreadsheetNotFound:
            self._error = "Cannot open google file from key : %s" % key
            print(self._error, file=sys.stderr)
            return False

        self._google_file = google_file
        return True

    def _open_file_by_url(self, url):
        """
        Open remote file by url.
        :param url: type String url to open
        :return: bool True if success else False if fail
        """
        try:
            google_file = self._gc.open_by_url(url)
        except gspread.SpreadsheetNotFound:
            self._error = "Cannot open google file from url : %s" % url
            print(self._error, file=sys.stderr)
            return False
        except gspread.NoValidUrlKeyFound:
            self._error = "Cannot open google file from invalid url : %s" % url
            print(self._error, file=sys.stderr)
            return False

        self._google_file = google_file
        return True
