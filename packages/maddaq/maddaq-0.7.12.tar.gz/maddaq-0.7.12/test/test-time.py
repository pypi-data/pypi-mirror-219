#!/usr/bin/env python3
""" Test time in data
"""
import sys
from pathlib import Path
from maddaq import MadDAQData, MadDAQModule
import numpy as np
import collections


def get_period(maddaq):
    """Measure period or period.

    WE do this with an external trigger produced by a pulse generator.
    Same pulse for all the MB.

    Args:
    ----
        maddaq: The maddaq object.

    Return
    ------
        period (dict), std(dict) - period and deviation per MB id.

    """
    avg = {}
    last_time = {}
    for ievt, evt in enumerate(maddaq):
        evt_time = int(evt.time)
        mid = evt.mod_id
        board_id = int(int(mid)/10)
        ltim = last_time.get(mid, -1)
        if mid not in avg:
            avg[mid] = []

        dt, last_time[mid] = MadDAQModule.get_delta_time(evt_time, ltim)
        if dt != 0:
            avg[mid].append(dt)

        if ievt > 100:
            break

    period = {}
    rms = {}
    for key, val in avg.items():
        period[key] = np.mean(val)
        rms[key] = np.std(val)

    return period, rms


def main(fname):
    """fname is the input filename"""
    inp_file_path = Path(fname)
    if not inp_file_path.exists():
        print("Input file ", inp_file_path, " does not exist")
        return

    # open the maddaq file
    maddaq = MadDAQData(fname)
    maddaq.show_info()

    #  Get the ext. trigger period
    period, period_std = get_period(maddaq)
    nboard = len(period)

    last_time = {}
    last_tdc = {}
    for m in list(maddaq.modules.values()):
        last_tdc[m.id] = 0.0

    # Get events sorted by TDC
    maddaq.iter_key = 'tdc'

    # Title of output
    print("   Row   mid  evtcnt         time     deltaT (us)")

    delta_set = {}
    delta_board = []
    llog = collections.deque(maxlen=10)
    for ievt, evt in enumerate(maddaq):
        evt_time = int(evt.time)
        mid = evt.mod_id
        board_id = int(int(mid)/10)
        ltim = last_time.get(mid, -1)

        dt, last_time[mid] = MadDAQModule.get_delta_time(evt_time, ltim)

        if dt > 0:
            offs = abs(dt - period[mid])/period[mid]
            if offs > 0.05:
                print("{:>6d} {:3d} Divergence {:>10.3f} expected {:>10.3f}".format(ievt, mid, dt, period[mid]))

        delta = evt.tdc - last_tdc[mid]
        delta_period = abs(delta - period[mid])/period[mid]
        delta_set[mid] = (delta, delta_period)
        last_tdc[mid] = evt.tdc
        if dt == 0:
            delta_period = 0

        try:
            out = "{:>6d}   {:3d}  {:>6n} {:>12.3f} {:>10.3f} deltaP {:.4f} [{:12X}]".format(
                ievt, mid, evt.evtcnt, evt.tdc, dt, delta_period, evt_time)

        except Exception:
            out = "{:>6d}   {:3d}  {:>6n} {:>12.3f} {:>10.3f} deltaP {:.4f} [{:12X}]".format(
                ievt, mid, evt.evtcnt, evt.tdc, dt, 0.0, evt_time)

        llog.appendleft(out)
        if ievt < 50:
            print(out)

        # analysis
        if len(delta_set) == nboard:
            # Aqui
            T = []
            for key, val in delta_set.items():
                T.append(val[0])
                if abs(val[1])/period[key] > 0.1:
                    print("--Z delta {:12.4f} delta_period {:.4f} [{:>3d} {:6d}]".format(delta,
                                                                                         delta_period,
                                                                                         mid, ievt))

            std = np.std(T)
            if std > 1:
                print("========")
                print("{:10d} - Inter MB divergence: {:.6f}".format(ievt, T[1] - T[0]))
                for x in reversed(llog):
                    print(x)
                print("-")
            else:
                delta_board.append(T[1] - T[0])

            delta_set.clear()

    print("Average delta_board: {:.6f} - std {:.6f}".format(np.mean(delta_board), np.std(delta_board)))


if __name__ == "__main__":
    main(sys.argv[1])
