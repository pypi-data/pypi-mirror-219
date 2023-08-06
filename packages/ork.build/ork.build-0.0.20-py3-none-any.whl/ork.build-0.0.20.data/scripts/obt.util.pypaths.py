#!python 

import os
import sys
import site
import obt.path

def print_env_var(name, default):
    value = os.getenv(name, default)
    print(f"{name}: {value}")

print( "######################################################")

print_env_var('PYTHONPATH', sys.path)
print_env_var('PYTHONHOME', sys.prefix)
print_env_var('PYTHONSTARTUP', 'Not set')
print_env_var('PYTHONUSERBASE', site.USER_BASE)
print_env_var('PYTHONEXECUTABLE', sys.executable)
print_env_var('PYTHONWARNINGS', 'Not set')
print_env_var('PYTHONNOUSERSITE', 'Not set (User site directory is added to sys.path)')
print_env_var('PYTHONUNBUFFERED', 'Not set (Buffered I/O is used for stdout and stderr)')

print( "######################################################")

print( "obt-pkg-path: %s" % obt.path.obt_module_path() )
print( "obt-data-base: %s" % obt.path.obt_data_base() )
print( "obt-modules-base: %s" % obt.path.obt_modules_base() )
print( "running_from_pip: %s" % obt.path.running_from_pip() )