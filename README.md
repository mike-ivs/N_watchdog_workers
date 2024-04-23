# N_watchdog_workers

A quick little script to demo running Watchdog threads in parallel with a very basic load balancing. Watchdog is a neat Python module to trigger workflows on file create/modify/delete events.

### watch.py

Contains two functions to create and configure the "watcher" treads, and the "file trigger" logic that specifies when to execute a workflow on a created/modified/deleted file.

### run_flow.py

The script to run (`__main__`) to trigger the watchers, and also specify the workflow to run on file trigger.


## The example

This quick example watchs a directory called `/test` for any created `.tar` files. The workflow triggers an untarring script than unpacks the `tar` bundle inside a `/test/dir/` directory, and then sleeps for `60s`. The example is configured to run in parallel with up to `N=3` jobs running simultaniously.
