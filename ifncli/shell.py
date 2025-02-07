import sys
import os

from cliff.app import App
from cliff.commandmanager import CommandManager
from .commands import get_commands
from .appConfig import AppConfigManager

class MyApp(App):

    def build_option_parser(self, description, version):
        parser = super(MyApp, self).build_option_parser(
            description,
            version,
        )
        parser.add_argument(
            "-c",
            "--config",
            help="Config path (if not present will look IFN_CONFIG env variable",
            default=os.path.join('resources', 'config.yaml')
        )


        self.plugin = None

        try:
            from plugins import Plugin
            self.plugin = Plugin()
        except:
            pass

       # self.plugin_manager.build_option_parser(parser)

        return parser

    def initialize_app(self, argv):
        commands = get_commands()
        if self.plugin is not None:
            commands.extend(self.plugin.get_commands())
        for command in commands:
            if hasattr(command, 'name'):
                name = command.name
            else:
                name = command.__name__
            self.command_manager.add_command(name.lower(), command)

        self.appConfigManager = AppConfigManager(self.options.config)

def main(argv=sys.argv[1:]):
    if len(argv) == 0:
        default_command = os.getenv('IFNCLI_DEFAULT_COMMAND')
        if default_command is not None:
            argv = [default_command]

    app = MyApp(
            description="InfluenzaNet CLI",
            version="1.3",
            command_manager=CommandManager('ifncli'),
            deferred_help=True,
        )

    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main())