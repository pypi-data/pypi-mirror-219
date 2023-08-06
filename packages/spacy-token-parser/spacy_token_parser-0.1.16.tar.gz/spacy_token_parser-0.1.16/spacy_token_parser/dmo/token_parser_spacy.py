#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform spaCy parse and retokenization """


import spacy
from spacy.tokens import Doc


from baseblock import BaseObject


class TokenParserSpacy(BaseObject):
    """ Perform spaCy parse and retokenization """

    def __init__(self):
        """ Change Log

        Created:
            13-Oct-2021
            craigtrim@gmail.com
            *   refactored out of 'parse-input-tokens' in pursuit of
                https://github.com/grafflr/graffl-core/issues/41
        Updated:
            16-Sept-2022
            craigtrim@gmail.com
            *   rename component
                https://github.com/craigtrim/spacy-token-parser/issues/3
        Updated:
            11-Mar-2023
            craigtrim@gmail.com
            *   fix apostrophe tokenization error
                https://github.com/craigtrim/spacy-token-parser/issues/6
        """
        BaseObject.__init__(self, __name__)
        self._nlp = spacy.load('en_core_web_sm')

    def process(self,
                input_text: str) -> Doc:
        """Perform actual spaCy parse and retokenize input

        Args:
            tokens (list): list of tokens

        Returns:
            Doc: spacy doc
        """
        doc = self._nlp(input_text)

        # ---------------------------------------------------------- ##
        # Purpose:    Deprecated Tokenization Fix maintained for reference purposes only
        # Reference:  https://github.com/craigtrim/spacy-token-parser/issues/6#issuecomment-1465015566
        # ---------------------------------------------------------- ##
        # self._nlp.tokenizer.rules = {
        #     key: value for key, value in
        #     self._nlp.tokenizer.rules.items()
        #     if "'" not in key and '’' not in key and '‘' not in key
        # }
        # ---------------------------------------------------------- ##

        # ---------------------------------------------------------- ##
        # Purpose:    Perform Retokenization
        # Reference:  https://github.com/grafflr/graffl-core/issues/1#issuecomment-935048135
        #             https://github.com/craigtrim/spacy-token-parser/issues/6#issuecomment-1465015390
        # ---------------------------------------------------------- ##
        position = [
            token.i for token in doc
            if token.i != 0 and token.text.startswith("'")
        ]

        with doc.retokenize() as retokenizer:
            for pos in position:
                retokenizer.merge(doc[pos - 1:pos + 1])

        return doc
