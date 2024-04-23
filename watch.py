import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileTrigger:
    """
    The FileTrigger sets up a series of watcher scripts to monitor a specified
    directory for created/modified/deleted files, and trigger a specified workflow.
    args:
    watch_dir: the directory to monitor for file changes
    patterns: filename patterns to decide which files trigger workflows
    FlowRunner: the function/workflow to run on a triggered file
    N_parallel: the maximum number of workflows to run in parallel
    """

    def __init__(self, watch_dir, patterns, FlowRunner=None, N_parallel=1):
        self.watch_dir = watch_dir
        self.patterns = patterns
        self.FlowRunner = FlowRunner
        self.observers = []

        # create N_parallel observer threads
        for _ in range(N_parallel):
            self.observers.append(Observer())
        self.N_parallel = N_parallel

    def run(self):

        # default to printing filename if no FlowRunner specified
        if not self.FlowRunner:
            self.FlowRunner = print

        # create watch_dir directory if it doesn't exist already
        if not os.path.isdir(self.watch_dir):
            os.mkdir(self.watch_dir)

        # change directory to watch dir
        os.chdir(self.watch_dir)

        # configure and initialise the N_parallel observer threads
        for n, observer in enumerate(self.observers):
            event_handler = Handler(self.FlowRunner, self.patterns, self.N_parallel, n)
            observer.schedule(event_handler, self.watch_dir, recursive=True)
            observer.start()

        # set this overseer to idle while observers running,
        # tear them down if error occurs
        try:
            while True:
                time.sleep(1)
        except:
            for observer in self.observers:
                observer.stop()
        for observer in self.observers:
            observer.join()


class Handler(FileSystemEventHandler):
    """
    This is the callback class for file events. You can edit it to trigger
    at file creation, modification or deletion, and have different behaviors for each.
    args:
    FlowRunner: the function/workflow to run on a triggered file
    patterns: filename patterns to decide which files trigger workflows
    max_N: the maximum number of workflows to run in parallel
    n: controls whether this observer/handler should trigger, or let others run instead
    """

    def __init__(self, FlowRunner, patterns, max_N, n):
        super(FileSystemEventHandler).__init__()
        self.logic_function = FlowRunner
        self.patterns = patterns
        self.max_N = max_N - 1  # base zero counting
        self.n = n

    def on_any_event(self, event):
        # trigger on file creation
        if event.event_type == "created":
            # ignore directory creation
            if event.is_directory:
                return None
            else:
                # check if created file matches specified patterns
                for pattern in self.patterns:
                    if event.src_path.endswith(pattern):
                        # only trigger this observer 1/Nth of the time
                        # only 1 observer will trigger at any given time
                        if self.n == self.max_N:
                            self.logic_function(event.src_path, self.n)
                        # cycle the internal tracking of observer executions
                        self.n += 1
                        if self.n > self.max_N:
                            self.n = 0
                        return None
        # elif (event.event_type == 'modified'):
        #     self.logic_function(event.src_path)
        #     return None
