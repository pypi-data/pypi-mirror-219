from endesive import pdf, signer

import datetime
import hashlib
import base64
import io


import requests
import jwt


from . import psuhsm
from . import psucms
from . import exception


class PSUSigner:
    def __init__(
        self,
        code,
        secret,
        agent_key,
        jwt_secret=None,
        api_url=None,
    ):
        self.jwt_secret = jwt_secret
        self.agent_key = agent_key
        self.code = code
        self.secret = secret
        self.hsm = None

        if jwt_secret:
            self.hsm = psuhsm.JWTSecretPSUHSM(
                code=code,
                secret=secret,
                jwt_secret=jwt_secret,
                agent_key=agent_key,
                api_url=api_url,
            )
        else:
            self.hsm = psuhsm.SecretPSUHSM(
                code=code, secret=secret, agent_key=agent_key, api_url=api_url
            )

        # function stuff
        self.original_signer = signer.sign
        signer.sign = self.sign_cms

    def sign_byte(self, datau, dct, **kwargs):
        self.hsm.set_sign_parameters(**kwargs)
        datas = psucms.sign(datau, dct, None, None, [], "sha256", self.hsm)

        output = io.ByteIO()

        io.write(datau)
        io.write(output)

        return output

    def sign_file(self, input_name, dct, output_name, **kwargs):
        datau = b""
        with open(input_name, "rb") as fp:
            datau = fp.read()

        if not datau:
            raise exception.PSUSignException("No Input Data")

        self.hsm.set_sign_parameters(**kwargs)
        datas = psucms.sign(datau, dct, None, None, [], "sha256", self.hsm)

        with open(output_name, "wb") as fp:
            fp.write(datau)
            fp.write(datas)

    def sign_cms(
        self,
        datau,
        key,
        cert,
        othercerts,
        hashalgo,
        attrs=True,
        signed_value=None,
        hsm=None,
        pss=False,
        timestampurl=None,
        timestampcredentials=None,
        timestamp_req_options=None,
        ocspurl=None,
        ocspissuer=None,
    ):
        # print(
        #     datau,
        #     key,
        #     cert,
        #     othercerts,
        #     hashalgo,
        #     attrs,
        #     signed_value,
        #     hsm,
        #     pss,
        #     timestampurl,
        #     timestampcredentials,
        #     timestamp_req_options,
        #     ocspurl,
        #     ocspissuer,
        # )

        if hsm and isinstance(hsm, psuhsm.PSUHSM):
            if signed_value is None:
                signed_value = getattr(hashlib, hashalgo)(datau).digest()

            return hsm.sign(None, signed_value, "HA256")

        return self.original_signer(
            datau,
            key,
            cert,
            othercerts,
            hashalgo,
            attrs,
            signed_value,
            hsm,
            pss,
            timestampurl,
            timestampcredentials,
            timestamp_req_options,
            ocspurl,
            ocspissuer,
        )
