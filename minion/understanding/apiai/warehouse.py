from . import base


class Warehouse(base.ApiaiBaseCommand):
    def _build_key(parameters):
        return 'warehouse:{what}:{where}'

    def understand(self, nervous_system, command, action, parameters, fulfillment):
        key = self._build_key(**parameters)
        
        

        print command, parameters, fulfillment
