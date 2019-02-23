Linter for CudaLint plugin.
Supports Groovy lexer.

You need to install groovyc from http://www.groovy-lang.org/download.html
And set GROOVY_HOME environment variable, to main groovy folder 
(inside this folder you can find directories: bin, lib, conf).

Configuration file is [CudaText]/settings/cuda_lint_groovyc.ini
Options:
- [op] "classpath" - list of class paths.
- [op] "sourcepath" - list of source paths.
    

Ported from https://github.com/alkuzad/SublimeLinter-contrib-groovyc
Author: Alexey T.
