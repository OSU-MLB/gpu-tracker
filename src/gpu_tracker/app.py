from io import StringIO

import fabric
import pandas as pd

def run():
    list_of_hosts = [
        {
            "name": "MLB-001-4-2080-11GB",
            "host": "cse-c01176767d.coeit.osu.edu",
        },
        {
            "name": "MLB-002-4-2080-11GB",
            "host": "cse-cnc238812d.coeit.osu.edu",
        },
        {
            "name": "MLB-003-4-A6000-48GB",
            "host": "cse-cnc196874d.cse.ohio-state.edu",
        },
        {
            "name": "MLB-004-2-A5500-24GB",
            "host": "cse-c01188171s.coeit.osu.edu",
        },
        {
            "name": "MLB-005-8-6000Ada-48GB",
            "host": "cse-cnc197066s.coeit.osu.edu",
        },
        {
            "name": "ImageomicsServer",
            "host": "cse-cnc196909s.coeit.osu.edu",
        },
    ]
    command = "nvidia-smi --query-gpu index,memory.total,memory.reserved,memory.used,memory.free --format csv"
    
    for host in list_of_hosts:
        print('running')
        c = fabric.Connection(host["host"], user="carlyn.1", port=22)
        # TODO: for flexibility allow user to create config file. See: https://docs.fabfile.org/en/latest/api/connection.html
        try:
            results = c.run(command, hide='out')
        except:
            print(f"Something went wrong during execution for host {host['name']}")
            c.close()
            continue
        
        exit_code = results.exited
        if exit_code != 0:
            print(f"Something went wrong during execution for host {host['name']}")
            print(results.stderr)
            c.close()
            continue
        df = pd.read_csv(StringIO(results.stdout))
        
        print(f"Host: {host['name']}")
        print(f"Number of gpus: {len(df)}")
        print(df)
        c.close()
if __name__ == "__main__":
    run()