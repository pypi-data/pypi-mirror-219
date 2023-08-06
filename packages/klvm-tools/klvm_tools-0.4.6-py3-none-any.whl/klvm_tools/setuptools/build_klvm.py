from distutils.cmd import Command
from distutils import log

from setuptools.dist import Distribution

from klvm_tools.klvmc import compile_klvm


Distribution.klvm_extensions = ()


class build_klvm(Command):
    """ Command for building klvm """

    description = "build klvm extensions"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        file_list = self.distribution.klvm_extensions
        for _ in file_list:
            log.info("build_klvm on %s" % _)
            target = "%s.hex" % _
            compile_klvm(_, target)
