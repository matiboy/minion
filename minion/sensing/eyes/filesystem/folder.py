import minion.sensing.base
import minion.sensing.errors
import multiprocessing

logger = multiprocessing.get_logger()


class FolderWatcher(minion.sensing.base.BaseSensor):
    configuration = {}

    def _validate_configuration(self):
        if not self.configuration['folder']:
            raise minion.sensing.errors.ImproperlyConfigured('Folder is required for folder watcher')

        if not self.configuration['filetype']:
            raise minion.sensing.errors.ImproperlyConfigured('File type is required for folder watcher')
