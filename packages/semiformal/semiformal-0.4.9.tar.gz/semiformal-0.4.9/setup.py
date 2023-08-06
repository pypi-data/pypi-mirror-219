import glob
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


class build_ext_mixed_optimization_level(build_ext):
    def build_extensions(self):

        original_compile = self.compiler._compile
        def compile_mixed_optimization_level(obj, src, ext, cc_args, extra_postargs, pp_opts):
            if src == "src/scanner.c":
                extra_postargs = [s for s in extra_postargs if s not in ("-O3", "-O2", "-O1")] + ["-O0"]
            return original_compile(obj, src, ext, cc_args, extra_postargs, pp_opts)
        self.compiler._compile = compile_mixed_optimization_level
        try:
            build_ext.build_extensions(self)
        finally:
            del self.compiler._compile


setup_args = dict(
    cmdclass = {"build_ext": build_ext_mixed_optimization_level},
    ext_modules = [
        Extension(
            'semiformal._tokenizer',
            glob.glob('python/*.c') + glob.glob('src/*.c') + glob.glob('deps/**/[!utf8proc_data]*.c'),
            include_dirs = ['python', 'src', 'deps', 'deps/utf8proc'],
            define_macros = [('SEMIFORMAL_VERSION', '"0.4.9"')],
        )
    ]
)
setup(**setup_args)
