"""
    Kun
    ===
    Powerful fronted for ku-proxy
"""

import argparse
import logging
from time import sleep, time

from ku import ku, tcpsession
from ku import version as ku_version

from .util import CustomFormatter, genrancol, ansicol, flock
from .iautil import host_parse, resolve_host
from .kun_sessions import stream, transit
import statistics, curses
import traceback

version = '0.1.1'

print = flock(print) # lock print for multithreading

banner = \
f"""
 __    __                    
|  \  /  \                   
| $$ /  $$__    __  _______  
| $$/  $$|  \  |  \|       \ 
| $$  $$ | $$  | $$| $$$$$$$\\
| $$$$$\ | $$  | $$| $$  | $$
| $$ \$$\| $$__/ $$| $$  | $$
| $$  \$$ \$$    $$| $$  | $$
 \$$   \$$ \$$$$$$  \$$   \$$ v{version}
"""

def entry_point():
    pcolor = ansicol(*genrancol(1.37))
    print(pcolor, banner[1:], "\u001b[0m", sep='')

    parser = argparse.ArgumentParser(description="Powerful fronted for ku-proxy")
    parser.add_argument("-v", action="store_true", help="If passed, enabling verbose logging")
    parser.add_argument("-l", action='append', help="Proxy listen addr (allowed multiple and dualstack hostnames) (enclose ipv6 like [::1])", metavar="localhost:65535", required=True)
    parser.add_argument("-u", help="Proxy upstream server addr", metavar="localhost:8000", required=True)
    parser.add_argument("-7", help="Tells proxy to upstream over IPv6", action="store_true", dest='u6')
    parser.add_argument("-ll", action="store_true", help="If passed, enables low level debug logging (ku-proxy debug)")
    parser.add_argument("-mc", type=int, help="Maximum of parralel clients (connection over the limit will be refused)", default=-1, metavar="15")
    parser.add_argument("--nt", type=int, help="Number of simultaneous polling threads running", default=1, metavar="4")
    parser.add_argument("--transit", action="store_true", help="If passed, enables transit (no session orientated) displaying")
    parser.add_argument("--silent", action="store_true", help="If passed, disables connections related logging")
    args = parser.parse_args()

    logger = logging.getLogger("[")
    logger.setLevel(logging.DEBUG if args.v else logging.INFO)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter('[%(asctime)s] [%(levelname)s] %(name)s:  %(message)s', pcolor))
    logger.addHandler(stdout_handler)

    logging.getLogger("ku.devel").addHandler(stdout_handler)
    logging.getLogger("ku.devel").setLevel(logging.DEBUG if args.ll else logging.WARNING)

    logger.info(f"Running kun v{version} (ku v{ku_version})")

    listen = []
    for addr in args.l:
        ler = host_parse(addr)
        addreses = resolve_host(ler[1])
        for addr in addreses:
            addr = f"[{addr[1]}]" if addr[0] == 23 else addr[1]
                
            listen.append(addr)
            listen.append(ler[2])
            logger.info(f"\u001b[97mListening \u001b[92m-> \u001b[97m{addr}:{ler[2]}")

    upstream = host_parse(args.u)
    logger.info(f"\u001b[97mUpstream {ansicol(120, 120, 120)}({'v6' if upstream[0] is 23 else 'v6' if (args.u6 and upstream[0] == -1) else 'v4'}) \u001b[92m-> \u001b[97m{upstream[1]}:{upstream[2]}")
    session = tcpsession if args.silent else transit if args.transit else stream

    logger.info("Starting...")    
    proxy = ku(listen, upstream[1:], session, maxcon = args.mc, upstream_6 = args.u6, loglevel=logging.DEBUG if args.ll else logging.WARNING, parallelism=args.nt)
    logger.info("Started")

    if args.transit:
        def main_screen(screen, height, width):
            # Listen
            curses.init_pair(3, 12, curses.COLOR_BLACK)                
            for k, i in enumerate(range(0, len(listen), 2)):
                screen.addstr(k + 2, width - 36, f"Listening -> {listen[i]}:{listen[i+1]}"[:36], curses.color_pair(3))

            # Upstream
            curses.init_pair(4, 8, curses.COLOR_BLACK)
            screen.addstr(k + 4, width - 36, f"Upstream ({'v6' if upstream[0] is 23 else 'v6' if (args.u6 and upstream[0] == -1) else 'v4'}) -> {upstream[1]}:{upstream[2]}", curses.color_pair(4))

            # Sessions
            curses.init_pair(6, 13, curses.COLOR_BLACK)
            screen.addstr(0, 0, f"Active sessions [{len(proxy.ss)}]:", curses.color_pair(6))

            sess_offset = 1
            for i, session in enumerate(proxy.ss):
                curses.init_pair(5, 1, curses.COLOR_BLACK)
                screen.addstr(sess_offset + i, 5, str(session), curses.color_pair(5))

        def performance(screen, height, width):
            curses.init_pair(8, 13, curses.COLOR_BLACK)
            
            screen.addstr(0, 0, "Threads:", curses.color_pair(8))
            for i, thread in enumerate(proxy.threads):
                screen.addstr(1 + i, 0, f"  {thread}", curses.color_pair(8))

            conn = len(set(proxy.fd).difference(proxy.sockets))
            listen = len(proxy.sockets)

            curses.init_pair(9, 7, curses.COLOR_BLACK)
            screen.addstr(3 + i, 0, f"Descriptors[{len(proxy.fd) + len(proxy.wai)}]:", curses.color_pair(9))
            screen.addstr(4 + i, 0, f"  Listen / {listen}", curses.color_pair(9))
            screen.addstr(5 + i, 0, f"  Connected / {conn}", curses.color_pair(9))
            screen.addstr(6 + i, 0, f"  Sunrise / {len(proxy.wai)}", curses.color_pair(9))


        def transit_screen(screen):

            curses.start_color()
            curses.curs_set(0)
            screen.timeout(int(1000 / 25))
            fps = [0]
            button = 0
            screens = [main_screen, performance]
            current_screen = screens[0]

            while 7:
                if button == 99:
                    proxy.pause = not proxy.pause
                
                if button == 261:
                    ni = screens.index(current_screen) + 1
                    if 0 <= ni <= len(screens) - 1:
                        current_screen = screens[ni]
                    elif len(screens) - 1 < ni:
                        current_screen = screens[0]

                elif button == 260:
                    ni = screens.index(current_screen) - 1
                    if 0 <= ni <= len(screens):
                        current_screen = screens[ni]
                    elif ni < 0:
                        current_screen = screens[len(screens) - 1]

                render_begin = time()
                    
                screen.clear()
                height, width = screen.getmaxyx()

                # draw screen
                current_screen(screen, height, width)

                # Actionbar
                fps_fix = f"FPS: {round(statistics.median(fps), 2)}".ljust(10)
                state = f"State: {'PAUSED' if proxy.pause else 'RUNNING' if proxy.alive else 'STOPP'}"
                actionbar = f"{fps_fix}, {state}, {button}, {current_screen.__name__} [use arrows to switch screens]".ljust(width - 1)
                curses.init_pair(2, curses.COLOR_BLACK, 15)
                screen.addstr(height - 1, 0, actionbar, curses.color_pair(2))

                try:
                    screen.refresh()
                    button = screen.getch()
                except KeyboardInterrupt:
                    logger.info("Shutting down...")
                    proxy.shutdown()
                    logger.info("Exiting...")
                    break
                
                fps.append(round(1 / (time() - render_begin + 0.0001), 2))
                if len(fps) == 10:
                    del fps[0]

        try:
            curses.wrapper(transit_screen)
        except Exception as e:
            print(traceback.format_exc())
            proxy.shutdown()            

    else:
        while 7:
            try:
                if not min([t.is_alive() for t in proxy.threads]):
                    logger.warning(f"Proxy unexpectedly closed")
                    break
                sleep(0.07)
            except KeyboardInterrupt:
                logger.info("Shutting down...")
                proxy.shutdown()
                logger.info("Exiting...")
                break
