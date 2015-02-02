#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
Description
  Converts a Europass CV or CV+ESP in JSON format to a Europass CV in PDF format.
Method
  POST
URL
  https://europass.cedefop.europa.eu/rest/v1/document/to/pdf-cv
Request Headers
  Required:
    Content-Type: application/json
  Optional:
    Accept-Language: xx (where xx is the two-letter code of the language the
    document should be translated to - see Localisation for further details) 
Request Body
  A Europass CV or CV+ESP in JSON v3.0 format.
Success Response
  HTTP Status: 200 OK

  Body: A Europass CV in PDF format.
'''
# cURL example:
#curl -k https://europass.cedefop.europa.eu/rest/v1/document/to/pdf-cv \
#-H "Content-Type: application/json" \
#-d @cv-in.json \
#-o cv-out.pdf

import requests
import json
import logging
import os
#import re
#import datetime
from pprint import pprint
#import codecs


class PyEuropass():
    # Europass supported languages
    EUROPASS_LANGS = {
        'bg': u'български',
        'es': u'español',
        'cs': u'čeština',
        'da': u'dansk',
        'de': u'Deutsch',
        'et': u'eesti keel',
        'el': u'ελληνικά',
        'en': u'english',
        'fr': u'français',
        'hr': u'hrvatski',
        'is': u'íslenska',
        'it': u'Italiano',
        'lv': u'latviešu valoda',
        'lt': u'lietuvių kalba',
        'hu': u'Magyar',
        'mt': u'Malti',
        'nl': u'Nederlands',
        'no': u'Norsk',
        'pl': u'polski',
        'pt': u'português',
        'ro': u'română',
        'sk': u'slovenčina',
        'sl': u'slovenščina',
        'fi': u'suomi',
        'sv': u'svenska',
        'tr': u'türkçe',
    }

    # Europass interoperability URLs
    EUROPASS_URLS = {
        # CV/CV+ESP -> CV (.odt) (OpenDocument)
        'json2opendoc_cv':
            'https://europass.cedefop.europa.eu/rest/v1/document/to/opendoc',
        # CV/CV+ESP -> CV (.pdf)
        'json2pdf_cv':
            'https://europass.cedefop.europa.eu/rest/v1/document/to/pdf-cv',
        # ESP/CV+ESP -> ESP (.pdf)
        'json2pdf_esp':
            'https://europass.cedefop.europa.eu/rest/v1/document/to/pdf-esp',
        # CV+ESP -> CV+ESP (.pdf)
        'json2pdf_cv_esp':
            'https://europass.cedefop.europa.eu/rest/v1/document/to/pdf',
        # CV/CV+ESP -> CV (.doc) (MS-Word2003)
        'json2word_cv':
            'https://europass.cedefop.europa.eu/rest/v1/document/to/word',
        # CV/CV+ESP -> CV (.xml)
        'json2xml_cv':
            'https://europass.cedefop.europa.eu/rest/v1/document/to/xml-cv',
        # ESP/CV+ESP -> ESP (.xml)
        'json2xml_esp':
            'https://europass.cedefop.europa.eu/rest/v1/document/to/xml-esp',
        # CV+ESP -> CV+ESP (.xml)
        'json2xml_cv_esp':
            'https://europass.cedefop.europa.eu/rest/v1/document/to/xml',
    }

    url_json2pdf = 'https://europass.cedefop.europa.eu/rest/v1/document/to/pdf-cv'
    url_json2word = 'https://europass.cedefop.europa.eu/rest/v1/document/to/word'
    url_json2opendoc = 'https://europass.cedefop.europa.eu/rest/v1/document/to/opendoc'

    # Europass response codes
    RET_CODE_OK = 200

    # Config logger
    logging.basicConfig(filename='{}.log'.format(__name__), level=logging.INFO)
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.INFO)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    _logger.addHandler(ch)

    def _get_request_headers(self, data_type='json', lang=None):
        # So far, only json allowed
        # XML support may be done in an uncertain future, if there is real need
        headers = {}
        if data_type == 'json':
            headers.update({'Content-Type': 'application/json;charset=utf-8',})
        else:
            msg = ('ERROR: Only json data is supported so far, '
                   'but you specified: {}'.format(data_type))
            self._logger.warning(msg)
            raise Exception(msg)

        if lang and self.EUROPASS_LANGS.get(lang, False):
            headers.update({'Accept-Language': lang,})
        else:
            self._logger.warning('You either have specified an unsupported '
                                 'language or no language at all.\n'
                                 'Europass default language will be used '
                                 'instead.')
        return headers

    def json2x(self, data=None, data_type='json', lang=None, url_type=None):
        self._logger.info('\njson2x: \n'
                          '    data_type={}\n'
                          '    lang={}\n'
                          '    url_type={}'
                          ''.format(data_type, lang, url_type))
        if data is None:
            self._logger.warning('json2x: WTF!')
            return None
        if not self.EUROPASS_URLS.get(url_type, False):
            self._logger.warning('json2x: WTF!')
            return None
        url = self.EUROPASS_URLS.get(url_type)
        content = None
        headers = self._get_request_headers(data_type=data_type, lang=lang)
        if data_type == 'json':
            # We need this to serialize data into JSON object
            # UTF-8 enconding is mandatory for sending to Europass
            data = json.dumps(data, encoding='utf-8')
            r = requests.post(url=url, headers=headers, data=data,)

            if r.status_code != self.RET_CODE_OK:
                msg = ('ERROR! Europass server returned code: {}\n'
                       '{}'.format(self.RET_CODE_OK))
                self._logger.error(msg)
                raise Exception(msg)
            else:
                msg = ('OK! Europass server returned code: {}'
                       ''.format(r.status_code, r.text))
                self._logger.info(msg)
                content = r.content
        else:
            msg = ('ERROR! Sorry, only JSON data supported so far. '
                   'You have tried: "{}" data type.'.format(data_type))
            self._logger.error(msg)
            raise Exception(msg)
        return content

    # CV/CV+ESP -> CV (.odt) (OpenDocument)
    def json2opendoc_cv(self, data=None, lang=None):
        url_type = 'json2opendoc_cv'
        content = self.json2x(data=data, data_type='json', lang=lang,
                              url_type=url_type)
        return content

    # CV/CV+ESP -> CV (.pdf)
    def json2pdf_cv(self, data=None, lang=None):
        url_type = 'json2pdf_cv'
        content = self.json2x(data=data, data_type='json', lang=lang,
                              url_type=url_type)
        return content

    # ESP/CV+ESP -> ESP (.pdf)
    def json2pdf_esp(self, data=None, lang=None):
        url_type = 'json2pdf_esp'
        content = self.json2x(data=data, data_type='json', lang=lang,
                              url_type=url_type)
        return content

    # CV+ESP -> CV+ESP (.pdf)
    def json2pdf_cv_esp(self, data=None, lang=None):
        url_type = 'json2pdf_cv_esp'
        content = self.json2x(data=data, data_type='json', lang=lang,
                              url_type=url_type)
        return content

    # CV/CV+ESP -> CV (.doc) (MS-Word2003)
    def json2word_cv(self, data=None, lang=None):
        url_type = 'json2word_cv'
        content = self.json2x(data=data, data_type='json', lang=lang,
                              url_type=url_type)
        return content

    # CV/CV+ESP -> CV (.xml)
    def json2xml_cv(self, data=None, lang=None):
        url_type = 'json2xml_cv'
        content = self.json2x(data=data, data_type='json', lang=lang,
                              url_type=url_type)
        return content

    # ESP/CV+ESP -> ESP (.xml)
    def json2xml_esp(self, data=None, lang=None):
        url_type = 'json2xml_esp'
        content = self.json2x(data=data, data_type='json', lang=lang,
                              url_type=url_type)
        return content

    # CV+ESP -> CV+ESP (.xml)
    def json2xml_cv_esp(self, data=None, lang=None):
        url_type = 'json2xml_cv_esp'
        content = self.json2x(data=data, data_type='json', lang=lang,
                              url_type=url_type)
        return content


# ACTUAL EXECUTION
print("---------------------------------")
if __name__ == "__main__":
    eup = PyEuropass()
    eup._logger.info('#############################')
    # Files
    in_files = {
        # CV/CV+ESP -> CV (.odt) (OpenDocument)
        'json2opendoc_cv':
            'examples/europass-cv-esp-example-v3.2.0.json',
        # CV/CV+ESP -> CV (.pdf)
        'json2pdf_cv':
            'examples/europass-cv-example-v3.2.0.json',
        # ESP/CV+ESP -> ESP (.pdf)
        'json2pdf_esp':
            'examples/europass-esp-example-v3.2.0.json',
        # CV+ESP -> CV+ESP (.pdf)
        'json2pdf_cv_esp':
            'examples/europass-cv-esp-example-v3.2.0.json',
        # CV/CV+ESP -> CV (.doc) (MS-Word2003)
        'json2word_cv':
            'examples/europass-cv-esp-example-v3.2.0.json',
        # CV/CV+ESP -> CV (.xml)
        'json2xml_cv':
            'examples/europass-cv-example-v3.2.0.json',
        # ESP/CV+ESP -> ESP (.xml)
        'json2xml_esp':
            'examples/europass-esp-example-v3.2.0.json',
        # CV+ESP -> CV+ESP (.xml)
        'json2xml_cv_esp':
            'examples/europass-cv-esp-example-v3.2.0.json',
    }
    out_files = {
        # CV/CV+ESP -> CV (.odt) (OpenDocument)
        'json2opendoc_cv': 'output/json2opendoc_cv.odt',
        # CV/CV+ESP -> CV (.pdf)
        'json2pdf_cv': 'output/json2pdf_cv.pdf',
        # ESP/CV+ESP -> ESP (.pdf)
        'json2pdf_esp': 'output/json2pdf_esp.pdf',
        # CV+ESP -> CV+ESP (.pdf)
        'json2pdf_cv_esp': 'output/json2pdf_cv_esp.pdf',
        # CV/CV+ESP -> CV (.doc) (MS-Word2003)
        'json2word_cv': 'output/json2word_cv.doc',
        # CV/CV+ESP -> CV (.xml)
        'json2xml_cv': 'output/json2xml_cv.xml',
        # ESP/CV+ESP -> ESP (.xml)
        'json2xml_esp': 'output/json2xml_esp.xml',
        # CV+ESP -> CV+ESP (.xml)
        'json2xml_cv_esp': 'output/json2xml_cv_esp.xml',
    }


    # Ej1
    res = None
    in_file = in_files.get('json2opendoc_cv')
    with open(in_file, 'r') as data_file:
        cv_json_data = json.load(data_file)
    res = eup.json2opendoc_cv(cv_json_data, 'es')
    if res:
        out_file = out_files.get('json2opendoc_cv')
        with open(out_file, 'wb') as fp:
            fp.write(res)
        eup._logger.info('File result in: {}'.format(out_file))
        eup._logger.info('-'*20)


    # Ej2
    res = None
    in_file = in_files.get('json2pdf_cv')
    with open(in_file, 'r') as data_file:
        cv_json_data = json.load(data_file)
    res = eup.json2pdf_cv(cv_json_data, 'es')
    if res:
        out_file = out_files.get('json2pdf_cv')
        with open(out_file, 'wb') as fp:
            fp.write(res)
        eup._logger.info('File result in: {}'.format(out_file))
        eup._logger.info('-'*20)


    # Ej3
    res = None
    in_file = in_files.get('json2pdf_esp')
    with open(in_file, 'r') as data_file:
        cv_json_data = json.load(data_file)
    res = eup.json2pdf_esp(cv_json_data, 'es')
    if res:
        out_file = out_files.get('json2pdf_esp')
        with open(out_file, 'wb') as fp:
            fp.write(res)
        eup._logger.info('File result in: {}'.format(out_file))
        eup._logger.info('-'*20)


    # Ej4
    res = None
    in_file = in_files.get('json2pdf_cv_esp')
    with open(in_file, 'r') as data_file:
        cv_json_data = json.load(data_file)
    res = eup.json2pdf_cv_esp(cv_json_data, 'es')
    if res:
        out_file = out_files.get('json2pdf_cv_esp')
        with open(out_file, 'wb') as fp:
            fp.write(res)
        eup._logger.info('File result in: {}'.format(out_file))
        eup._logger.info('-'*20)


    # Ej5
    res = None
    in_file = in_files.get('json2word_cv')
    with open(in_file, 'r') as data_file:
        cv_json_data = json.load(data_file)
    res = eup.json2word_cv(cv_json_data, 'es')
    if res:
        out_file = out_files.get('json2word_cv')
        with open(out_file, 'wb') as fp:
            fp.write(res)
        eup._logger.info('File result in: {}'.format(out_file))
        eup._logger.info('-'*20)


    # Ej6
    res = None
    in_file = 'examples/europass-cl-cv-example-v3.2.0.json'
    with open(in_file, 'r') as data_file:
        cv_json_data = json.load(data_file)
    res = eup.json2pdf_cv_esp(cv_json_data, 'es')
    if res:
        out_file = 'output/json2pdf_cv_esp__with_cl.pdf'
        with open(out_file, 'wb') as fp:
            fp.write(res)
        eup._logger.info('File result in: {}'.format(out_file))
        eup._logger.info('-'*20)


    # Ej7
    res = None
    in_file = 'examples/europass-lp-example-v3.2.0.json'
    with open(in_file, 'r') as data_file:
        cv_json_data = json.load(data_file)
    res = eup.json2pdf_esp(cv_json_data, 'es')
    if res:
        out_file = 'output/json2pdf_esp__with_lp.pdf'
        with open(out_file, 'wb') as fp:
            fp.write(res)
        eup._logger.info('File result in: {}'.format(out_file))
        eup._logger.info('-'*20)
        # This one does not work very well, as the result is empty,
        # for this input


    eup._logger.info('FINISHED =======================================')
