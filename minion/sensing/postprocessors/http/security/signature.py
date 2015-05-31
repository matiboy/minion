import base64
import bcrypt
import minion.sensing.postprocessors
import minion.sensing.exceptions
import minion.core.components.exceptions
import minion.core.utils.functions
import multiprocessing

logger = multiprocessing.get_logger()


class InvalidSignature(Exception):
    pass


class SignaturePostProcessor(minion.sensing.postprocessors.BasePostprocessor):
    @minion.core.utils.functions.configuration_getter
    def _get_secret(self):
        return

    def _validate_configuration(self):
        if not self._get_secret():
            raise minion.core.components.exceptions.ImproperlyConfigured('Secret is required')

    def _get_hashable_data(self, data):
        keys = [x for x in data.keys() if x != 'signature']
        # Sort them alphabetically
        keys.sort()
        kv = map(lambda x: '{}={}'.format(x, data[x]), keys)
        return '&'.join(kv)

    def hash(self, data):
        return base64.urlsafe_b64encode(bcrypt.hashpw(self._get_hashable_data(data), data['salt']))

    def _compare_hashes(self, signature, hashed):
        return signature == hashed

    def process(self, data):
        # data must have a signature and a salt
        try:
            signature = data['signature']
            data['salt']
        except KeyError:
            raise minion.sensing.exceptions.DataReadError("Signature and salt are required")

        # Pick the post data contained in the hash
        if not self._compare_hashes(signature, self.hash(data)):
            raise minion.sensing.exceptions.DataReadError("Hash does not match signature")

        # Simply pass through
        return data
