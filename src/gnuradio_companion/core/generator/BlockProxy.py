class BlockProxy:

    def __init__(self, real_block):
        self._real_block = real_block
        self.is_block = real_block.is_block
        self.enabled = real_block.enabled
        self.is_import = real_block.is_import
        self.key = real_block.key
        self.name = real_block.name
        self.is_snippet = real_block.is_snippet
        self.params = real_block.params
        self.is_variable = real_block.is_variable
        self.is_virtual_or_pad = real_block.is_virtual_or_pad
        self.sources = real_block.sources

        self.templates = getattr(real_block, 'templates', {})
        self.cpp_templates = getattr(real_block, 'cpp_templates', {})

    def get_bypassed(self):
        return self._real_block.get_bypassed()

    def is_virtual_sink(self):
        return self._real_block.is_virtual_sink()

    def is_virtual_source(self):
        return self._real_block.is_virtual_source()
