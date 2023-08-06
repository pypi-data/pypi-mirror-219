#!/usr/bin/env python3
"""MadDAQ module data class."""
import numpy as np
from collections import namedtuple


def __dummy_cond__(xx):
    return True


class MadDAQModule(object):
    """Module data handling class."""

    SERIAL, SPARSE, SPARSE_ADJ = (1, 2, 4)

    def __init__(self, module, data_file, polarity=1.0, do_cluster=False):
        """INitialize.

        Args:
        ----
            module: The module daq ID.
            data_file: The hdf5 data file object.
            polarity (optional): Polarity of the signal. Defaults to 1.0.
            do_cluster (optional): If cluster analysis is done. Defaults to False.

        """
        path = "/modules/%s/data/maddaq" % module
        self.data = data_file[path]
        path = "/modules/%s/data/time" % module
        self.time = data_file[path]

        self.polarity = polarity
        self.do_cluster = do_cluster
        names = ['mod_id', 'evt_time', 'tdc']
        names.extend(self.data.dtype.names)
        self.type = namedtuple("MadDAQModuleData", names)

        # Get pedeestals
        self.P = data_file["/modules/%s/pedestal/pedestal" % module]
        self.N = data_file["/modules/%s/pedestal/noise" % module]
        self.Ptime = data_file["/modules/%s/pedestal/evt_time" % module]

        # This is the pedestal and noise values used by default
        self.pedestal = self.P[-1]
        self.noise = self.N[-1]
        self.ntot = self.pedestal.shape[0]
        self.full_noise = [[] for i in range(0, self.ntot)]

        # Get module configuration from header
        self.id = int(module)
        self.nchip = -1
        modules = data_file["/header/modules"]
        for m in modules:
            id = m & 0xff
            if id == int(module):
                self.nchip = (m >> 20) & 0xff
                break

        # Read configuration record
        config = data_file["/modules/%s/configuration" % module]
        self.firmware = config[0] | config[1] >> 16
        self.threshold = config[2]
        self.ro_mode = config[3]
        self.nadj = config[4]
        self.hold_delay = config[5]
        self.ctw = config[6]
        self.trg_type = config[7]
        self.nbias = config[8]
        self.mbias = config[9:]
        self.adjacents = [0]

        for ch in range(1, self.nadj+1):
            self.adjacents.extend((ch, -ch))

        self.adjacents = np.array(self.adjacents)
        self.debug = False
        self.evdisplay = None
        self.cnvs = None

        self.seed_cut = 5.0
        self.neigh_cut = 3.0

    @staticmethod
    def get_delta_time(evt_time, last_time):
        """Compute the TDC time.

        Args:
        ----
            evt_time: current TDC time
            last_time: last time

        Return:
        ------
            dt: time since last event
            last_time: last absolute time

        """
        if last_time > 0:
            if evt_time > last_time:
                dt = evt_time - last_time
            else:
                dt = evt_time + (0x40000000-last_time)
        else:
            dt = 0.0

        dt = (dt*25.0)/1000.0
        return dt, evt_time

    def is_serial(self):
        """Tell if this is 'serial' data."""
        return self.ro_mode == MadDAQModule.SERIAL

    def set_current_pedestal(self, which=-1):
        """Set the default pedestals from the file."""
        self.pedestal = self.P[which]
        self.noise = self.N[which]

    def set_pedestals(self, pedestals, noise):
        """Set pedestal and noise."""
        self.pedestal = pedestals
        self.noise = noise

    def get_pedestal(self, which=-1):
        """Return pedestal."""
        return self.P[which]

    def get_noise(self, which=-1):
        """Return noise."""
        return self.N[which]

    def save_pedestals(self, file_name, which=-1):
        """Saves pedestals and noise to file."""
        ped = self.get_pedestal(which)
        noise = self.get_noise(which)
        ofile = open(file_name, "wt")
        i = 0
        for P, N in zip(ped, noise):
            ofile.write("{}, {:.2f}, {:.2f}\n".format(i, P, N))
            i = i+1

        ofile.close()

    def set_debug(self, dbg):
        """Set debug flag."""
        self.debug = dbg
        self.evdisplay = None

    def find_clusters(self, data, sn, hint=None, seed_cut=5.0, neigh_cut=3.0):
        """Do cluster analysis."""
        out = []

        #
        # find the clusters
        #
        used = [False for x in range(0, self.ntot)]

        # Get the list of channels with signal over noise > 5
        if hint is None:
            channels = np.nonzero(sn > seed_cut)[0]

        else:
            channels = [int(hint)]

        for ch in channels:
            if used[ch]:
                continue

            clst = [ch]
            used[ch] = True

            j = ch-1
            while True:
                if j < 0:
                    break

                if sn[j] > neigh_cut and not used[j]:
                    clst.append(j)
                    used[j] = True
                    j = j - 1
                else:
                    break

            j = ch + 1
            while True:
                if j > self.ntot - 1:
                    break

                if sn[j] > neigh_cut and not used[j]:
                    clst.append(j)
                    used[j] = True
                    j = j + 1
                else:
                    break

            Eclst = 0.0
            chan = 0.0
            for i in clst:
                if data[i] > 0.0:
                    Eclst += data[i]
                    chan += i*data[i]

            if Eclst > 0:
                chan /= Eclst
                out.append((chan, Eclst))

        return out

    def analyze_serial(self, evt):
        """Analysis of data in serial."""
        # subtract pedestals
        try:
            data = evt.data - self.pedestal
        except ValueError:
            # Sometimes it says we are serial, but we aren't
            return []

        if self.polarity < 0.0:
            data *= -1.0

        # compute signal over noise
        sn = data/self.noise

        # compute common mode and remove it
        # TODO: This is better done on a chip by chip basis
        cmmd = np.mean(data[np.nonzero(abs(sn) < 5.0)])
        data -= cmmd

        #
        # find the clusters
        #
        out = self.find_clusters(data, sn, seed_cut=self.seed_cut, neigh_cut=self.neigh_cut)

        return out

    def analyze_sparse(self, evt):
        """Analysis of sparse + adjacent data."""
        #
        # TODO: think something smarter than rejecting
        #       events with naighbours outside the range
        #
        the_chan = evt.nchan
        try:
            if evt.chan < self.nadj or evt.chan + self.nadj >= self.ntot:
                val = evt.data[0] - self.pedestal[evt.chan]
                return [(evt.chan, val)]
        except Exception as w:
            print("chan {} nadj {} - {}".format(evt.chan, self.nadj, str(w)))

        if evt.chan < 0 or evt.chan > self.ntot:
            w = "xxx"
            print("chan {} nadj {} - {}".format(evt.chan, evt.nadj, str(w)))

        # Get the indices for the pedestals ans subtract pedestals
        indx = [indx + the_chan for indx in self.adjacents]
        data = evt.data - self.pedestal[indx]
        if self.polarity < 0.0:
            data *= -1.0

        #
        # Subtract Common mode
        # Ideally this has to be done on a chip by chip basis
        #
        if self.nadj > 3:
            cmmd = np.mean(data[1:])
            data -= cmmd
        else:
            cmmd = 0.0

        out = []
        if evt.romode == MadDAQModule.SPARSE_ADJ and self.do_cluster:
            vsn = data/self.noise[indx]
            E = 0.0
            X = 0.0
            nstrip = 0
            i = 0
            while i < len(data):
                if i == 0:
                    val = data[i]
                    E += val
                    X += self.adjacents[i]*val
                    nstrip += val
                    i += 1
                else:
                    ngood = 0
                    for j in (i, i+1):
                        if vsn[j] > 5.0:
                            val = data[j]
                            E += val
                            X += self.adjacents[j]*val
                            nstrip += val
                            ngood += 1

                    i += 2
                    if ngood == 0:
                        break

            if nstrip > 0:
                X /= nstrip
                out.append((evt.chan+X, E))

        else:
            out.append((evt.chan, data[0]))

        return out

    def process_event(self, evt):
        """Very simple event processing."""
        if evt.romode == MadDAQModule.SERIAL:
            return self.analyze_serial(evt)

        elif evt.romode == MadDAQModule.SPARSE_ADJ:
            return self.analyze_sparse(evt)

        elif evt.romode == MadDAQModule.SPARSE:
            print("SPARSE not implemented")
            return None

    def find_time(self, T):
        """Find the event with DAQ time closest to the given."""
        ntot = self.time.shape[0]
        aa = 0
        bb = ntot-1
        faa = self.time[aa]
        fbb = self.time[bb]
        last_indx = -1
        while True:
            indx = aa+int((bb-aa)/2)
            # print("[{} {}] f(a) {}".format(aa, bb, faa))
            if indx == aa:
                return aa

            val = self.time[indx]

            if val > T:
                bb = indx
                fbb = val

            elif val < T:
                aa = indx
                faa = val

            if abs(aa-bb) < 1:
                return aa

    def __iter__(self):
        """Return the iterator."""
        # return self.navigate()
        return ModuleDataIterator(self)

    def navigate(self, start=None, stop=None, condition=__dummy_cond__):
        """The actual iterator routine..

        If start and stop are the first and last event we want read
        condition is a boolean function that receives the module data.
        navigate will only return the events for which condition
        returns true.
        """
        nevts = self.data.shape[0]

        # chunk size os the same for data and time
        chunk_size = 10*self.data.chunks[0]

        if start is None:
            start = 0

        if stop is None:
            stop = nevts

        if stop > nevts:
            stop = nevts

        first_chunk = start/chunk_size
        last_chunk = stop/chunk_size + 1
        current_chunk = first_chunk

        offs = 0
        for indx in range(start, stop):
            if indx % chunk_size == 0:
                TS = self.time[indx:indx+chunk_size]
                DS = self.data[indx:indx+chunk_size]
                offs = indx

            values = [self.id, TS[indx-offs]]
            values.extend(DS[indx-offs])
            obj = self.type._make(values)
            if condition(obj):
                yield obj


class ModuleDataIterator(object):
    """Iterator for module data."""

    def __init__(self, module, start=None, stop=None, condition=__dummy_cond__):
        """The actual iterator.

        start and stop are the first and last event we want to read
        condition is a boolean function that receives the module data.
        The iterator will only return the events for which condition
        returns true.
        """
        self.M = module
        self.start = start
        self.stop = stop
        self.condition = condition
        self.nevts = self.M.data.shape[0]
        self.chunk_size = 20*self.M.data.chunks[0]
        self.first_chunk = None
        self.last_chunk = None
        self.current_chunk = None

        self.TS = None
        self.DS = None
        self.first_in_chunck = 0
        self.indx = 0

        self.init_iter()

    def init_iter(self):
        """Inititalize the iterator."""
        if self.indx > 0:
            return

        if self.start is None:
            self.start = 0

        if self.stop is None or self.stop > self.nevts:
            self.stop = self.nevts

        self.first_chunk = int(self.start/self.chunk_size)
        self.last_chunk = int(self.stop/self.chunk_size) + 1
        self.current_chunk = self.first_chunk
        self.end_of_chunk = (self.current_chunk + 1) * self.chunk_size
        if self.end_of_chunk > self.stop:
            self.end_of_chunk = self.stop

        # offs is the beginning of the chuck
        self.first_in_chunck = int(self.current_chunk*self.chunk_size)
        self.indx = self.start
        self.TS = None
        self.DS = None

        self.last_time = -1
        self.the_time = 0.0

    def __iter__(self):
        """Return iterator."""
        self.init_iter()
        return self

    def __next__(self):
        """Iterator ext method."""
        if self.indx >= self.stop:
            raise StopIteration

        else:
            while True:
                # index within chunck
                ii = self.indx - self.first_in_chunck

                if self.TS is None or ii % self.chunk_size == 0:
                    self.first_in_chunck = self.indx
                    if self.TS is not None:
                        self.current_chunk += 1
                        self.end_of_chunk = (self.current_chunk + 1) * self.chunk_size
                        if self.end_of_chunk > self.stop:
                            self.end_of_chunk = self.stop

                    self.TS = self.M.time[self.first_in_chunck:self.end_of_chunk]
                    self.DS = self.M.data[self.first_in_chunck:self.end_of_chunk]
                    ii = 0

                # The TDC
                dt, self.last_time = MadDAQModule.get_delta_time(int(self.DS[ii][2]), self.last_time)
                self.the_time += dt

                # Create the event object
                values = [self.M.id, self.TS[ii], self.the_time]
                values.extend(self.DS[ii])
                obj = self.M.type._make(values)

                self.indx += 1
                if self.indx >= self.stop:
                    # print("ultimo {}".format(self.M.id))
                    raise StopIteration

                if self.condition(obj):
                    return obj
