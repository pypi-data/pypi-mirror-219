import os

from pydantic import BaseModel


class RunConfig(BaseModel):
    bleu: bool = True
    rouge: bool = True
    meteor: bool = True
    entail: bool = True
    function: bool = True

    def disable_all(self):
        self.bleu = False
        self.rouge = False
        self.meteor = False
        self.entail = False
        self.function = False

        return self

    def enable_all(self):
        self.bleu = True
        self.rouge = True
        self.meteor = True
        self.entail = True
        self.function = True

        return self

    def enable_bleu(self):
        self.bleu = True
        return self

    def enable_rouge(self):
        self.rouge = True
        return self

    def enable_meteor(self):
        self.meteor = True
        return self

    def enable_entail(self):
        self.entail = True
        return self

    def enable_function(self):
        self.function = True
        return self

    def disable_bleu(self):
        self.bleu = False
        return self

    def disable_rouge(self):
        self.rouge = False
        return self

    def disable_meteor(self):
        self.meteor = False
        return self

    def disable_entail(self):
        self.entail = False
        return self

    def disable_function(self):
        self.function = False
        return self


def load_config_from_str(folder_path):
    with open(os.path.join(folder_path, 'entail_config.py')) as fd:
        code = fd.read()
        local_ctx = {}
        exec(code, globals(), local_ctx)
        entailment = local_ctx.get('entailment_model', None)
        if entailment is None:
            entailment = RunConfig()
        config = local_ctx.get('config', None)
        if config is None:
            config = RunConfig()
        handler = local_ctx.get['handler']

        return config, handler, entailment
