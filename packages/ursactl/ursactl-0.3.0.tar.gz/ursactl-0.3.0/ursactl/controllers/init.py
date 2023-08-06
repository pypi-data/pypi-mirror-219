from pathlib import Path
import sys

from cement import Controller


class Init(Controller):
    """
    Provides the 'init' verb
    """

    class Meta:
        label = 'init'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'initialize a directory for use with Ursa Frontier'
        arguments = [
            (['--project'], {
                 'help': 'default project to use with this repository',
                 'dest': 'project',
                 'action': 'store'}),
            (['--dir', '--directory'], {
                 'help': 'directory to initialize (defaults to \'ursa\')',
                 'dest': 'directory',
                 'action': 'store',
                 'default': 'ursa'}),
        ]

    def _default(self):
        root = Path(self.app.pargs.directory)
        if not root.exists():
            root.mkdir(parents=True)
        elif not root.is_dir():
            print("Error: %s exists and is not a directory." % root)
            sys.exit(1)
        with (root / ".ursactl.conf").open(mode='w') as f:
            f.write("### Ursa Frontier Control configuration file\n[ursactl]\n\n")
            if self.app.pargs.project:
                f.write(f"project = {self.app.pargs.project}\n\n")

        for subdir in (
                       'data/transforms',
                       'data/generators',
                       'data/pipelines',
                       'data/datasets',
                       'planning/packages',
                       'planning/agents'
        ):
            (root / subdir).mkdir(parents=True, exist_ok=True)
            (root / subdir / '.keep').touch()
