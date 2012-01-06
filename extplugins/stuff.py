
import b3.plugin

class StuffPlugin(b3.plugin.Plugin):

    def startup(self):
        """\
        Initialize plugin settings
        """

        # get the admin plugin so we can register commands
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            # something is wrong, can't start without admin plugin
            self.error('Could not find admin plugin')
            return False

        # register our commands
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp
                func = self.getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)
    
    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None

    def _getDemoArg(self, data, client):
        if data:
            if data == "all":
                return "all"
            else:
                sclient = self._adminPlugin.findClientPrompt(data, client)
                if sclient is None:
                    return False
                return sclient.name 
        return None

    def cmd_startdemo(self, data, client, cmd):
        """\
        <player|all> - Start demo
        """
        who = self._getDemoArg(data, client)
        if who:
            client.message("Recording " + who)
            self.console.write("startserverdemo " + who)
        elif who is False:
            return False
        else:
            client.message("try !startdemo <player>|all")

    def cmd_stopdemo(self, data, client, cmd):
        """\
        <player|all> - Stop demo
        """
        who = self._getDemoArg(data, client)
        if who:
            client.message("Stopping recording " + who)
            self.console.write("stopserverdemo " + who)
        elif who is False:
            return False
        else:
            client.message("try !stopdemo <player>|all")


