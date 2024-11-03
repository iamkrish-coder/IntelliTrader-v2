# backend/modules/configurations/shared_parameters.py

class SharedParameters:
    def __init__(self, settings):
        self.params = settings

    def initialize(self):
        self.set_parameters()

    def set_parameters(self):
        # Extract top-level parameter names dynamically
        param_names = [key for key in self.params.keys() if not isinstance(self.params[key], dict)]

        for param_name in param_names:
            value = self.params.get(param_name)
            setattr(self, param_name, value)

    def get_parameters(self):
        flat_params = {}
        for key, value in self.params.items():
            if isinstance(value, dict):
                flat_params.update({f"{key}.{subkey}": subvalue for subkey, subvalue in value.items()})
            else:
                flat_params[key] = value
        return flat_params
