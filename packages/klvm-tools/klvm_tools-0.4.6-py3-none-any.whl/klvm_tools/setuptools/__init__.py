from .build_klvm import build_klvm  # noqa
from .patch_build_ext import patch_build_ext
from .patched_build_ext import build_ext


def monkey_patch():
    patch_build_ext(build_ext)
