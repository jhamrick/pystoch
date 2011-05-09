import pystoch_main
import cProfile
import pstats
import datetime
import pdb
import os

def profile(prog, args=[]):
    def run():
        args.insert(0, "profile.py")
        args.insert(1, prog)
        pystoch_main.run(prog, args)

    now = str(datetime.datetime.now())
    now = now.replace(" ", "_")
    pname = "/tmp/pystoch_profile_%s" % now

    try:
        cProfile.runctx('run()', globals(), locals(), filename=pname)

        trace = pstats.Stats(pname)
        trace.sort_stats('time').print_stats(20)
        pdb.set_trace()
        
    finally:
        os.remove(pname)

