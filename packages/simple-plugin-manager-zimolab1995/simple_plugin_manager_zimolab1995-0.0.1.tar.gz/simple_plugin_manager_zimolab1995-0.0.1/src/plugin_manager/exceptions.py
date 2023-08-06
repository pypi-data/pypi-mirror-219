class PluginNotInstalled(RuntimeError):
    pass


class PluginNotLoaded(RuntimeError):
    pass


class InvalidPlugin(RuntimeError):
    pass


class PluginAlreadyInstalled(RuntimeError):
    pass
