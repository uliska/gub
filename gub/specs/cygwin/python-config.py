from gub import misc
python_config = misc.load_spec ('python-config')

class Python_config (python_config.Python_config):
    source = 'url://host/python-config-2.5.tar.gz'

class Python_config__cygwin (python_config.Python_config):
    source = 'url://host/python-config-2.6.tar.gz'
