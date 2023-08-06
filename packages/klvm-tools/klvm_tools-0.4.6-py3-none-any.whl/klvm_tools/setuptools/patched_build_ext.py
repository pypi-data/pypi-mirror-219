from distutils import log
from setuptools.command.build_ext import build_ext as _build_ext


class build_ext(_build_ext):

    def __init__(self, *args):
        _build_ext.__init__(self, *args)

    def has_klvm_extensions(self):
        return (
            self.distribution.klvm_extensions
            and len(self.distribution.klvm_extensions) > 0
        )

    def check_extensions_list(self, extensions):
        if extensions:
            _build_ext.check_extensions_list(self, extensions)

    def run(self):
        """Run build_klvm sub command """
        if self.has_klvm_extensions():
            log.info("running build_klvm")
            build_klvm = self.get_finalized_command("build_klvm")
            build_klvm.inplace = self.inplace
            build_klvm.run()

        _build_ext.run(self)
