#!/usr/bin/python

import json
import sys

from openapi_spec_validator import validate_spec
from openapi_spec_validator import validate_spec, openapi_v2_spec_validator, \
    openapi_v30_spec_validator
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
from prance import ResolvingParser
from prance.util.formats import ParseError

from cvsvc_apirisk.score.base import ScoreNode
from cvsvc_apirisk.score.spec_security.sps_spec_util import QuerySpec
from cvsvc_apirisk.score.spec_security.security_attrs.sps_sec_attr07 import SpecSecSecurityAttr07


def reclimit_handler(limit, parsed_url, recursions=()):
    """Raise prance.util.url.ResolutionError."""
    path = []
    for rc in recursions:
        path.append('%s#/%s' % (rc[0], '/'.join(rc[1])))
    path = '\n'.join(path)

    return {}


class SpecSecMain(ScoreNode):

    def __init__(self, target_obj, target_filename, openapi_ver):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        super().__init__()

        self.target_obj = target_obj

        # Check for spec validity first
        try:
            if openapi_ver == 'v2':
                validate_spec(self.target_obj['raw_spec'], validator=openapi_v2_spec_validator)
            elif openapi_ver == 'v3':
                validate_spec(self.target_obj['raw_spec'], validator=openapi_v30_spec_validator)

            parse = ResolvingParser(
                url=target_filename,
                recursion_limit_handler=reclimit_handler)

        except OpenAPIValidationError as e:
            print(str(e))
            sys.exit(1)
        except ParseError:
            # Try again because prance's __parse_json() gets messed up because
            # of six.text_type(). Provide it a string rather than dict
            parse = ResolvingParser(spec_string=json.dumps(self.target_obj['raw_spec']),
                                    content_type='application/json', recursion_limit_handler=reclimit_handler)

        self.target_obj['spec_obj'] = parse.specification
        self.qspec = QuerySpec(spec_obj=self.target_obj['spec_obj'], openapi_ver =openapi_ver)

        self.add_child(SpecSecSecurityAttr07(self.qspec, openapi_ver))

    def __repr__(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        return 'sps-main'

    def compute(self):
        """
        Description

        Params
        ------
        p1 : float
            Param description
        p2 : int, optional
            Param description

        Returns
        -------
        result: int
            Result desc
        """
        # Compute the scores of children first
        for c_obj in self.children.values():
            c_obj.compute()

        # Compute the score+reason
        self.score = max([c_obj.score for c_obj in self.children.values()])
        self.meta = []
        for cobj in self.children.values():
            if cobj.meta is not None:
                self.meta.extend(cobj.meta)

        return
