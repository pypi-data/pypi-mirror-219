import functools
import logging
import platform
import os
import sched
import time
import pmg


log = logging.getLogger(__name__)

def get_os_name():
    os_name = f"{platform.system()} {platform.version()}"
    try:
        if os.path.isfile('/etc/os-release'):
            with open('/etc/os-release', 'rt', encoding='utf-8') as f:
                for line in f:
                    k, v = line.split('=')
                    if k == "PRETTY_NAME":
                        os_name = pmg.unquote(v.strip(), '"')
                        break
    except Exception:
        pass
    return f'{os_name} ({platform.platform()})'

def get_package_versions(*packages_start_with):
    versions = []
    import pkg_resources
    for pkg in iter(pkg_resources.working_set):
        dist = pkg_resources.get_distribution(pkg)
        if any([dist.project_name.startswith(package_name) for package_name in packages_start_with]):
            versions.append(f'{dist.project_name} {dist.version}')
    return sorted(versions)

def run_every(sleep_seconds, run_at_start=False, wait_after_fail=15):
    def wrapper(func):
        @functools.wraps(func)
        def looping_function(*args, **kwargs):
            @pmg.logwrap(log)
            def run_it():
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    log.exception('Exception during service function, pausing %d seconds...', wait_after_fail)
                    time.sleep(wait_after_fail)
            if run_at_start:
                run_it()
            sch = sched.scheduler()
            while True:
                sch.enter(sleep_seconds, 1, run_it)
                sch.run()
        return looping_function
    return wrapper