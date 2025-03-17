# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import omni.ext

class MarkerPlotterExtension(omni.ext.IExt):
    """Extension for plotting marker positions in IsaacLab"""

    def on_startup(self, ext_id):
        print("[ext: markerplotter] Marker Position Plotter Extension startup")
        
        # Extension has been loaded
        # No specific initialization needed as MarkerPositionPlotter is used directly

    def on_shutdown(self):
        print("[ext: markerplotter] Marker Position Plotter Extension shutdown")
        
        # Any global cleanup would go here
        # Individual MarkerPositionPlotter instances handle their own cleanup