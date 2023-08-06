#!/usr/bin/env python

import emzed


def test_extract_chromatograms(data_path, regtest):
    peaks = emzed.io.load_table(data_path("peaks.table"))
    t = emzed.peak_picking.extract_chromatograms(peaks)
    print(t, file=regtest)

    assert "chromatogram" in t.col_names

    assert len(t[0].chromatogram) == 2
    rts, iis = t[0].chromatogram
    assert len(iis) == len(rts)

    assert len(iis) == 602
