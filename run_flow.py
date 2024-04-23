import os
import time
from pathlib import Path
import tarfile

from watch import FileTrigger


def run_flow(event_file):
    # Do something with trigger file
    new_dir = Path("test/dir")
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    tar = tarfile.open(event_file)
    tar.extractall(path=new_dir)
    tar.close()
    os.remove(event_file)
    time.sleep(60)


if __name__ == "__main__":
    # Creates and starts the watcher
    trigger = FileTrigger(
        watch_dir=Path("/test"),
        patterns=[".tar"],
        FlowRunner=run_flow,
        N_parallel=3,
    )
    trigger.run()
