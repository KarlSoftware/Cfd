# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2015-2017- qingfeng xia <qingfengxia@iesensor.com> *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "Command New Analysis from existing geometry and mesh files"
__author__ = "Qingfeng Xia"
__url__ = "http://www.freecadweb.org"

import os.path

import FreeCAD
from _CfdCommand import CfdCommand
import CfdTools

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore
    from PySide import QtGui
    from PySide.QtGui import QFileDialog  # in QtWidgets for Qt5


class _CommandCfdAnalysisFromMesh(CfdCommand):
    "the Cfd_AnalysisFromMesh command definition"
    def __init__(self):
        super(_CommandCfdAnalysisFromMesh, self).__init__()
        icon_path = os.path.join(CfdTools.getModulePath(), "Resources", "icons", "cfd-analysis-from-mesh.svg")
        self.resources = {'Pixmap': icon_path,
                          'MenuText': QtCore.QT_TRANSLATE_NOOP("Cfd_AnalysisFromMesh", "Analysis container"),
                          'Accel': "N, I",
                          'ToolTip': QtCore.QT_TRANSLATE_NOOP("Cfd_AnalysisFromMesh", "Creates a analysis container from existing geometry and mesh files")}
        self.is_active = 'with_document'

    def Activated(self):
        sel = FreeCADGui.Selection.getSelection()
        if (len(sel) == 1) and (sel[0].isDerivedFrom("Part::Feature")):
            # using existing part_feature, no need to import geometry, but get obj as link
            geo_file = sel[0]
        else:
            filters = u"BREP (*.brep *.brp);;STEP (*.step *.stp);;IGES (*.iges *.igs)"
            geo_file = QFileDialog.getOpenFileName(None, u"Open geometry files", u"./", filters)
        FreeCADGui.Selection.clearSelection()

        filters = u"IDES mesh (*.unv);;Med mesh(*.med);;VTK mesh (*.vtk *.vtu)"
        mesh_file = QFileDialog.getOpenFileName(None, u"Open mesh files", u"./", filters)
        # why return a tuple of filename and selectedfilter

        import CfdTools
        solver_name = 'OpenFOAM'
        CfdTools.createAnalysis(solver_name)

        FreeCADGui.addModule("CfdTools")
        FreeCADGui.doCommand("CfdTools.importGeometryAndMesh(u'{}', u'{}')".format(geo_file[0], mesh_file[0]))
        #CfdTools.importGeometryAndMesh(geo_file[0], mesh_file[0])
        FreeCADGui.addModule("FemGui")
        if FemGui.getActiveAnalysis():
            FreeCADGui.doCommand("FemGui.getActiveAnalysis().addObject(App.ActiveDocument.ActiveObject)")


if FreeCAD.GuiUp:
    FreeCADGui.addCommand('Cfd_AnalysisFromMesh', _CommandCfdAnalysisFromMesh())
