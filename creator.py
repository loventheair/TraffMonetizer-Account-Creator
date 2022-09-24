from subprocess import PIPE
import subprocess
import os
import sys
import time

# count containers equals to how much ips you have and DON'T TOUCH TO COUNT!
count_container = 254
count = 2

# Don't touch anything there it's for cli arguments
token = sys.argv[1]
subnet = sys.argv[2]


try:
    # Check how many traffmonetizer containers are there
    test_command = "docker ps -qf 'name=TraffMonetizer_' | wc -l"
    test_process = subprocess.run(test_command, shell=True, check=True, universal_newlines=True, stdout=PIPE, stderr=PIPE)
    test_process_finish = int(test_process.stdout)

    # Do Job
    if test_process_finish >= count_container:
        print(f"{test_process_finish} container already active")
    else:
        while True:
            # if count not equals to count of containers (count_container) create new one until its equals
            if count != int(count_container):
                os.system(f"docker run -d --network=container:Peer2Profit_{subnet}.{count} --name TraffMonetizer_{subnet}.{count} traffmonetizer/cli start accept --token {token}")
                count = count + 1
                # a little time sleep for don't overheat machine
                time.sleep(0.5)
            else:
                # Print that work done (you will not see that because we will use it in background) and exit script (don't know really we need that)
                print("Work Done...")
                sys.exit()

except Exception as main_error:
    # That's just exception error output
    print(f"Main Error: {main_error}")