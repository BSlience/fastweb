# coding:utf8

"""thrift gen hub code and fastweb config file

Usage:
    fastthrift <idl> [--pattern=<p>] [--outhub=<oh>] [--outconfig=<oc>]

Options:
    -h --help     Show this screen.
    -p --pattern=<p>  Pattern(sync|async). [default: async]
    -oh --outhub=<oh>   Output thrift hub module path. [default: .]
    -oc --outconfig=<oc>    Output load thrift of fastweb path. [default: .]
"""

import os

from fastweb.script import Script
from fastweb.util.log import recorder
from fastweb.accesspoint import docopt
from fastweb.util.python import filepath2pythonpath, load_module


class ThriftCommand(Script):

    def gen_thrift_auxiliary(self):
        """生成与thrift相关的桩代码（hub code）和配置文件"""

        cwd = os.getcwd()
        args = docopt(__doc__)
        language = None
        hub_package = None
        idl = args['<idl>']
        hub_path = args['--outhub']
        config_path = args['--outconfig']

        if args['--pattern'] == 'async':
            language = 'py:tornado'
            hub_package = 'async'
        elif args['--pattern'] == 'sync':
            language = 'py'
            hub_package = 'sync'

        # package 名字中不能存在`-`，无法导入
        hub_module_name = 'fastweb_thrift_{hub_package}'.format(hub_package=hub_package)
        hub_path = os.path.join(hub_path, hub_module_name)

        try:
            os.mkdir(hub_path)
        except OSError:
            pass

        command = 'thrift --gen {language} -out {out} {idl} '.format(language=language, idl=idl, out=hub_path)
        self.call_subprocess(command)
        recorder('INFO', 'thrift hub code module path: {hub}\nload thrift of fastweb path: {config}'.format(hub=hub_path,
                                                                                                            config=config_path))
        hub_package_path = filepath2pythonpath(hub_path)
        thrift_template = '# fastthrift gen template\n\n' \
                          '[service:service_name]\n' \
                          'name=\n' \
                          'port=\n' \
                          'thrift_module={hub}\n' \
                          'handlers=\n' \
                          'active='.format(hub=hub_package_path)

        recorder('CRITICAL', thrift_template)


def gen_thrift_auxiliary():
    ThriftCommand().gen_thrift_auxiliary()
