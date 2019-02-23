import os
import tempfile
import cudatext as app
from cuda_lint import Linter

if os.name=='nt':
    GROOVY_BINARY = 'groovyc.bat'
else:
    GROOVY_BINARY = 'groovyc'

fn_config = os.path.join(app.app_path(app.APP_DIR_SETTINGS), 'cuda_lint_groovyc.ini')


class Groovy(Linter):

    syntax = 'Groovy'
    tempfile_suffix = "-"

    regex = r'''(?sx)(.*?:\ # Filepath part
                \d+:\ # Line part, we ignore it as we have it later
                (?P<message>.*?)\s* # Error message till @
                @\ line\ (?P<line>\d+),\ column\ (?P<col>\d+)\. # line and column, ends with dot
                ''' \
                '{}'.format(os.linesep) +\
                r'''\s*(?P<code>.*?)\n # 2line - code snippet of error, it has to end with unix newline
                ''' \
                r'|.*) # The last resort match - if we do not match error, match anything to silence info from SL'

    multiline = True

    defaults = {
        'classpath': None,
        'sourcepath': None,
    }

    on_stderr = None

    def cmd(self):
        cmd = (GROOVY_BINARY,)

        classpath = app.ini_read(fn_config, 'op', 'classpath', '')
        sourcepath = app.ini_read(fn_config, 'op', 'sourcepath', '')

        if classpath:
            cmd += ('-classpath', '"'+classpath+'"')

        if sourcepath:
            cmd += ('--sourcepath', '"'+sourcepath+'"')

        _tempdir = tempfile.TemporaryDirectory(prefix="cudalint-groovyc-")
        cmd += ('-d', '"'+_tempdir.name+'"')

        return cmd

    def run(self, cmd, code=None):
        with self._tempdir:
            return super().run(cmd, code)

    def split_match(self, match):
        match, line, col, error, warning, message, near = super().split_match(match)

        if line is None:
            return match, 0, 0, None, None, None, None
        return match, line, col, error, warning, message, near
