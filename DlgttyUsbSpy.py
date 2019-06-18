#!/usr/bin/env python
#
# Copyright (C) 2013 koldo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import wx
import wx.html

# import wx.grid
import math
import os
import sys

import datetime
import subprocess
import logging
import glob
import signal
import platform
import locale

import pcapy
import core.ttyUsbSpy
from core.usbrevue import *
from collections import *
from copy import deepcopy
import copy

import gettext

_ = gettext.gettext


class dataPack:
	nowMs = 0
	xfer_type = 0
	epnum = 0
	data = "-"
	direc = "0"
	setup = "0"
	devnum = 0
	color = wx.WHITE
	realcolor = wx.WHITE


class RxTxDataTable(wx.grid.GridTableBase):
	def __init__(self):
		super().__init__()

		self.colLabels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "ASCII"]
		self.types = ["rel.", "abs.", "rel.+abs."]
		self.rowLabels = []
		#        self.dataTypes = [wx.grid.GRID_VALUE_FLOAT,
		#                          wx.grid.GRID_VALUE_FLOAT,
		#                          wx.grid.GRID_VALUE_STRING
		#                          ]

		self.tabledata = []
		self.listdata = []
		self.processedlistdata = []
		self.devnums = []
		self.rowsAdded = 0

		self.currentRows = 1
		self.currentCols = 17
		self.SelectedDevnum = "-"

	def getdata(self):
		return self.tabledata

	def setdata(self, data):
		self.tabledata = data
		self.Update()

		data = property(getdata, setdata)

	def GetNumberRows(self):
		return len(self.tabledata) // 17

	def GetNumberCols(self):
		return 17

	def IsEmptyCell(self, row, col):
		try:
			return not self.tabledata[row]
		except IndexError:
			return True

	def GetColLabelValue(self, col):
		return self.colLabels[col]

	def GetRowLabelValue(self, row):
		return self.rowLabels[row]

	def GetValue(self, row, col):
		val = self.tabledata[row][col]
		return val

	def SetValue(self, row, col, value, setup):
		sz_value = str(value).strip("[]")
		if sz_value == "-" or sz_value == "|" or setup == "DECODED":
			#            if setup == "DECODED":
			#                print "Metemos Decoded"
			#                self.tabledata[row][col] = setup
			#            else:
			#                self.tabledata[row][col] = sz_value
			self.tabledata[row][col] = sz_value
			sz_value = sz_value + " "
			self.file.write(sz_value)
		else:
			valorhex = hex(int(sz_value))
			self.tabledata[row][col] = valorhex
			valorhex = valorhex + " "
			self.file.write(valorhex)

	def GetAttr(self, row, col, kind):
		attr = wx.grid.GridCellAttr()
		data = self.processedlistdata[(row * 17) + col]

		attr.SetBackgroundColour(data.color)

		return attr

	def SetCellBackground(self, row, col, selected):
		i = (row * 17) + col
		data = self.processedlistdata[i]
		if not selected:
			data.color = data.realcolor
		else:
			data.color = wx.Colour(255, 100, 100)
		self.processedlistdata[i] = data

	###############################################################################
	# AppendRows
	#       Anadimos la fila de Tx y la de Rx donde anadiremos las 16 siguientes
	#   datos
	###############################################################################

	def AppendRows(self, num=1):
		entryTx = []

		for name in self.colLabels:
			entryTx.append("-")

		self.tabledata.append(entryTx)
		self.rowLabels.append("-")
		self.currentRows = self.currentRows + 1

	###############################################################################
	# DeleteRows
	#       Borramos una linea.
	#
	###############################################################################

	def DeleteRows(self, num=1):
		self.tabledata = self.tabledata[:-num]
		self.Update()

	###############################################################################
	# DeleteAllRows
	#       Borramos todas las linea.
	#
	###############################################################################

	def DeleteAllRows(self):
		tam = len(self.tabledata)
		cnt = 0
		print("Borrar lineas:" + repr(tam))
		while len(self.tabledata) > 0:
			self.tabledata = self.tabledata[:-1]
			self.currentRows = self.currentRows - 1
			cnt = cnt + 1
		msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, 1, cnt)  # The table  # what we did to it  # how many
		self.GetView().ProcessTableMessage(msg)
		del self.processedlistdata[:]
		self.currentRows = 0

	def DeleteListData(self):
		del self.listdata[:]

	def setColSize(self, grid):
		grid.SetDefaultColSize(35, resizeExistingCols=False)
		grid.SetDefaultCellFont(wx.Font(8, wx.MODERN, wx.ITALIC, wx.BOLD))
		grid.SetColSize(15, 230)
		grid.SetRowLabelSize(30)
		numfilas = self.GetNumberRows()

	def AddDataTable(self, pcappacket):
		data = dataPack()
		data.nowMs = pcappacket.nowMs
		data.xfer_type = pcappacket.xfer_type
		data.epnum = pcappacket.epnum
		data.data = pcappacket.data
		data.direc = pcappacket.direc
		data.devnum = pcappacket.devnum
		data.setup = pcappacket.setup

		self.listdata.append(data)

	###############################################################################
	# ShowDataTable
	#       Anadimos la fila de Tx y la de Rx donde anadiremos las 16 siguientes
	#   datos
	###############################################################################

	def ShowDataTable(self):

		self.file = open("./captures/file.txt", "w")
		for i in range(len(self.processedlistdata)):
			row = i // 17  # division entera
			col = i % 17  # resto division
			data = self.processedlistdata[i]
			if (i == 0 or col == 16) and (i < len(self.processedlistdata) - 1):
				self.AppendRows(17)
				# Enviamos mensaje de fila anadida para q actualize el grid
				msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)  # The table  # what we did to it  # how many
				self.GetView().ProcessTableMessage(msg)
			#                print "col:"+repr(col)+" i:"+repr(i)+" len(self.listdata)"+repr(len(self.processedlistdata))
			#                print "Data.setup:"+repr(data.setup)

			self.SetValue(row, col, data.data, data.setup)
		self.file.close()

	##
	# ProcessDataTable
	#       Tomando listdata donde estan todos los datos filtramos para obtener
	#   los bytes enviados, recibidos y los cambios de senales. Tambien se filtra
	#   por el devnum asociado al Rs232 si se requiere. En los paquetes en los que
	#   viene mas de un byte, se divide en un byte por paquete para visualizarlo mejor
	##
	def ProcessDataTable(self):
		a = 0
		print("ProcessDataTable[" + repr(len(self.listdata)) + "]")
		direcOld = "Inicio"
		dataVacio = dataPack()
		#        print "1.-self.SelectedDevnum:"+repr(self.SelectedDevnum)
		for i in range(len(self.listdata)):
			datalist = self.listdata[i]

			if datalist.direc == "Bo" or datalist.direc == "Bi" or datalist.direc == "Co" or datalist.direc == "Ci" or datalist.direc == "Ii":
				#                print "datalist:"+ repr(datalist.direc)
				row = a // 16  # division entera
				col = a % 16  # resto division
				data = dataPack()
				data.nowMs = datalist.nowMs
				data.xfer_type = datalist.xfer_type
				data.epnum = datalist.epnum
				data.setup = datalist.setup
				data.direc = datalist.direc
				data.devnum = datalist.devnum
				if datalist.direc != "Ii":
					self.addDevnum(data.devnum, data.setup)

				if self.SelectedDevnum == data.devnum or self.SelectedDevnum == "-":
					#                    print "2.-self.SelectedDevnum:"+repr(self.SelectedDevnum)
					#                    print "data.direc:"+repr(data.direc)+" direcOld:"+repr(direcOld)
					if ((data.direc != "Ci") and (data.direc != "Co")) or (((data.direc == "Co") and (data.setup != "0")) or ((data.direc == "Ci") and (data.setup != "0"))):
						# hemos filtrado los mensajes con setup 0 q llegan al hacer el cambio de senales
						#                        print "data.setup:"+repr(data.setup)
						if len(datalist.data) > 1:
							#                            print "datalist.data:"+repr(datalist.data)
							for b in range(len(datalist.data)):

								data.data = datalist.data[b]
								data.setup = datalist.setup

								if (data.direc == "Bo") or (data.direc == "Co"):
									data.color = wx.CYAN
									data.realcolor = wx.CYAN
								elif (data.direc == "Bi") or (data.direc == "Ci") or (data.direc == "Ii"):
									data.color = wx.GREEN
									data.realcolor = wx.GREEN
								self.processedlistdata.append(data)
								data = dataPack()
								data.nowMs = datalist.nowMs
								data.xfer_type = datalist.xfer_type
								data.epnum = datalist.epnum
								data.setup = datalist.setup
								data.direc = datalist.direc
								data.devnum = datalist.devnum

								if len(self.processedlistdata) % 17 == 16:
									# decoded line
									dataASCII = dataPack()
									dataASCII.color = wx.WHITE
									dataASCII.realcolor = wx.WHITE
									dataASCII.data = self.dataDecodeLastLine()
									dataASCII.setup = "DECODED"
									self.processedlistdata.append(dataASCII)
						#                                    print "DECODED1:"+repr(len(self.processedlistdata))

						else:
							data.data = datalist.data
							#                            print "2.-data.data:"+repr(data.data)
							if (data.direc == "Bo") or (data.direc == "Co"):
								data.color = wx.CYAN
								data.realcolor = wx.CYAN
							elif (data.direc == "Bi") or (data.direc == "Ci") or (data.direc == "Ii"):
								data.color = wx.GREEN
								data.realcolor = wx.GREEN
							self.processedlistdata.append(data)
							if len(self.processedlistdata) % 17 == 16:
								# decoded line
								dataASCII = dataPack()
								dataASCII.color = wx.WHITE
								dataASCII.realcolor = wx.WHITE
								dataASCII.data = self.dataDecodeLastLine()
								dataASCII.setup = "DECODED"
								self.processedlistdata.append(dataASCII)
		#                                print "DECODED2:"+repr(len(self.processedlistdata)//17)

		print("Processed[" + repr(len(self.processedlistdata)) + "]")
		falta = len(self.processedlistdata) % 17
		if falta != 0:
			dataEnd = dataPack()
			falta = 16 - falta
			dataEnd.nowMs = 0
			dataEnd.xfer_type = 0
			dataEnd.epnum = 0
			dataEnd.setup = 0
			dataEnd.direc = 0
			dataEnd.devnum = 0
			dataEnd.data = "-"
			dataEnd.color = wx.WHITE
			dataEnd.realcolor = wx.WHITE
			while falta > 0:
				falta = falta - 1
				self.processedlistdata.append(dataEnd)

			dataASCII = dataPack()
			dataASCII.color = wx.WHITE
			dataASCII.realcolor = wx.WHITE
			dataASCII.data = self.dataDecodeLastLine()
			dataASCII.setup = "DECODED"
			self.processedlistdata.append(dataASCII)

	##
	# dataDecodeLastLine
	#       Traducimos los bytes hexadecimales en codigo ASCII, y pone en la ultima
	#   columna
	##
	def dataDecodeLastLine(self):
		idx = len(self.processedlistdata) - 16
		sz_decoded = ""
		for i in range(16):
			row = i // 16  # division entera
			col = i % 16  # resto division
			data = self.processedlistdata[idx + i]
			sz_value = str(data.data)
			#            print "idx+i:" + repr(idx+i)+" sz_value:"+repr(sz_value)
			if sz_value != "-" and sz_value != "|":
				sz_value = str(data.data).strip("[]")
				intvalue = int(sz_value)

				if intvalue > 32 and intvalue < 127:
					sz_value = str(chr(intvalue))
				else:
					sz_value = "."
			sz_decoded = sz_decoded + sz_value
		return sz_decoded

	##
	# GetFecha
	#       Obtiene la tiempo de un dato
	#   @row Fila en la que se encuentra el dato
	#   @col Columna en la que se encuentra el dato
	##
	def GetFecha(self, row, col):
		if self.GetValue(row, col) != "-":
			i = row * 17 + col
			data = self.processedlistdata[i]
			return data.nowMs
		else:
			return 0

	def GetSetup(self, row, col):
		v = self.GetValue(row, col)
		if v != "-":
			i = row * 17 + col
			data = self.processedlistdata[i]

			return data.setup
		else:
			return None

	def addDevnum(self, devnum, setup):
		dev = str(devnum) + "(RS232)"
		if devnum in self.devnums:
			if setup != "0":
				cadena = setup.split(" ")
				if (cadena[1] == "22") and (cadena[0] == "21"):
					# El setup parece de un Rs232

					self.devnums[self.devnums.index(devnum)] = dev

		else:
			if dev not in self.devnums:
				self.devnums.append(devnum)

	def getDevnums(self, devnum):

		for i in range(len(self.devnums)):
			devnum.append(self.devnums[i])

	def setDevnum(self, devnum):
		self.SelectedDevnum = devnum

	def cleanDevnum(self):
		del self.devnums[:]

	def getProcessedListdata(self, listdata):
		for i in range(len(self.processedlistdata)):
			listdata.append(self.processedlistdata[i])

	def NumRows(self):
		return self.currentRows


class ViewPanel(wx.Panel):
	def __init__(self, parent):
		self.parentFrame = parent
		self.__attach_events()

		self.dt = RxTxDataTable()
		parent.m_grid1.SetTable(self.dt, False, wx.grid.Grid.wxGridSelectCells)
		self.dt.setColSize(parent.m_grid1)

	def __attach_events(self):
		print("attach events")

	#        self.Bind(wx.EVT_PAINT, self.OnPaint)
	#        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
	#        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
	#        self.Bind(wx.EVT_MOUSEWHEEL, self.OnZoom)
	#        self.Bind(wx.EVT_CLOSE, self.OnClose)

	def OnFichero(self, event):
		wildcard1 = "pcap (*.PCAP; *.pcap)|*.PCAP; *.pcap| All files (*)|*"
		dlg = wx.FileDialog(self, _("Select File"), self.path, "", wildcard1, wx.FD_OPEN)
		
		if dlg.ShowModal() == wx.ID_OK:
			self.path = dlg.GetPath()
			self.cargaFichero()
		dlg.Destroy()
		self.Refresh()

	def cargaFichero(self, path):
		self.path = path
		pcap = pcapy.open_offline(self.path)
		data = dataPack()
		while True:
			hdr, pack = pcap.next()
			if hdr is None:
				break  # EOF
			p = Packet(hdr, pack)

			p.get_dato_serie(data)

			if len(p.data) > 0 or ((data.direc == "Co" or data.direc == "Ci") and data.setup != 0):
				self.dt.AddDataTable(data)

		self.dt.ProcessDataTable()
		self.dt.ShowDataTable()

	def cargaTest(self):
		data = dataPack()
		for i in range(26):
			data.nowMs = 2 * i + 0.001
			data.xfer_type = i + 0.01
			data.epnum = i + 0.1
			data.data = i
			self.dt.AddDataTable(data)

		self.dt.ShowDataTable()

	def GetTime(self, row, col):
		fecha = self.dt.GetFecha(row, col)
		return fecha

	def GetSetup(self, row, col):
		setup = self.dt.GetSetup(row, col)
		return setup

	def SetSelection1(self, row, col):
		self.dt.SetSelection1(row, col)

	def SetSelection2(self, row, col):
		self.dt.SetSelection2(row, col)

	def EmptyGrid(self):
		self.dt.DeleteAllRows()

	def EmptyListData(self):
		self.dt.DeleteListData()

	def Devnums(self, devnum):
		self.dt.getDevnums(devnum)

	def setDevnum(self, devnum):
		self.dt.setDevnum(devnum)

	def cleanDevnum(self):
		self.dt.cleanDevnum()

	def processDataTable(self):
		self.dt.ProcessDataTable()

	def showDataTable(self):
		self.dt.ShowDataTable()

	def getProcessedListdata(self, listdata):
		self.dt.getProcessedListdata(listdata)

	def SetCellBackground(self, row, col, selected):
		self.dt.SetCellBackground(row, col, selected)

	def NumRows(self):
		return self.dt.NumRows()


aboutText = _(
	"""<p><b>ttyUSBSpy</b> decodes pcap files captured by por tcpdump\n
from serial port (tcpdump uses usbmon module to capture data, so \n
ttyUSBSpy only works with USB-RS232 conversor).</p>  \n
<p>Grid shows hexadecimal data in the serial port\n
 except in cases where appears\"|\", this indicates a change \n
 in the signals RTS/CTS, clicking shows the value in the modem line status</p>\n
<p>Captured data shows, Rs232 comunication and the comms\n
of the SO with the usb-Rs232 conversor chip. So we have \n
to choose the Dev number that identifies the Rs232 port\n
to filter the comms with the chip. </p>\n
<p><b>METHOD OF USE:</b></p>\n
<p> Left mouse button shows the time (T1) and the status of the byte or signal</p>\n
<p> Right mouse button shows the time (T2) and the status of the byte or signal \n
and delta time (T2-T1) in milliseconds</p>\n
<p> Send bytes or signals are shown in blue </p>\n
<p> Received bytes or signals are shown in green</p>\n
<p> Selected bytes or signals are shown in red </p>\n
\n
<p>It is running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.\n
See <a href=\"http://wiki.wxpython.org\">wxPython Wiki</a></p>\n
<b>ttyUSBViewer</b> is based on the dwaley/ USB Reverse Engineering Software """
)


class HtmlWindow(wx.html.HtmlWindow):
	def __init__(self, parent, id, size=(600, 400)):
		wx.html.HtmlWindow.__init__(self, parent, id, size=size)
		if "gtk2" in wx.PlatformInfo:
			self.SetStandardFonts()

	def OnLinkClicked(self, link):
		wx.LaunchDefaultBrowser(link.GetHref())


class AboutBox(wx.Dialog):
	def __init__(self):
		wx.Dialog.__init__(self, None, -1, "About ttyUSBViewer", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.TAB_TRAVERSAL)
		hwin = HtmlWindow(self, -1, size=(400, 200))
		vers = {}
		vers["python"] = sys.version.split()[0]
		vers["wxpy"] = wx.VERSION_STRING
		hwin.SetPage(aboutText % vers)
		btn = hwin.FindWindowById(wx.ID_OK)
		irep = hwin.GetInternalRepresentation()
		hwin.SetSize((irep.GetWidth() + 25, irep.GetHeight() + 10))
		self.SetClientSize(hwin.GetSize())
		self.CentreOnParent(wx.BOTH)
		self.SetFocus()


# Implementing ttyUsbViewer


class DlgttyUsbSpy(core.ttyUsbSpy.ttyUsbSpy):
	def __init__(self, parent):
		core.ttyUsbSpy.ttyUsbSpy.__init__(self, parent)
		self.CreateStatusBar(number=1, style=wx.STB_DEFAULT_STYLE, id=0, name="Status")
		
		self.SelectedT1 = False
		self.SelectedT2 = False
		self.listdata = []
		self.scroll = 0

		# Install gettext.  Once this is done, all strings enclosed in "_()" will automatically be translated.
		gettext.install("ttyUSBSpy", localedir="./locale")
		# Define supported languages
		self.presLan_en = gettext.translation("ttyUSBSpy", "./locale", languages=["en"])  # English
		self.presLan_es = gettext.translation("ttyUSBSpy", "./locale", languages=["es"])  # Spanish
		# Install English as the initial language
		#        self.presLan_en.install()
		self.presLan_es.install()
		#        self.UpdateText()

		for files in glob.glob("/dev/*ttyUSB*"):
			self.m_comboBoxttyUSB.Append(files)

		if self.m_comboBoxttyUSB.GetCount() > 0 and os.getuid() == 0:
			print("self.m_comboBoxttyUSB:" + repr(self.m_comboBoxttyUSB.GetCount()))
			self.m_buttonCapture.Enable()
		else:
			# Como no hay ttyUSB o no soy superuser deshabilito la posibilidad de capturar
			self.m_buttonCapture.Disable()

		# Handlers for ttyUsbViewer events.

	def OnToolHelp(self, event):
		print("OnToolHelp")
		dlg = AboutBox()
		dlg.ShowModal()
		dlg.Destroy()
		pass

	def UpdateText(self):
		""" Update all Text on the Application Frame. """
		# Set the Frame Title
		self.SetTitle(_("MiniApp"))
		# Define the String for the second wxStaticText label and the Status Bar
		str = _("Hello.  This is translatable.")
		# Set the wxStaticText label
		self.txt2.SetLabel(str)
		# Update the text for the Main Menubar Items
		self.menuBar.SetLabelTop(0, _("&File"))
		self.menuBar.SetLabelTop(1, _("&Language"))
		# Update the text and Help Strings for the File Menu Items
		self.menu1.SetLabel(MENU_FILE_EXIT, _("E&xit"))
		self.menu1.SetHelpString(MENU_FILE_EXIT, _("Quit Application"))
		# Update the text for the Language Menu Items.  (I do not want to update the Help Strings.)
		self.menu2.SetLabel(MENU_LANGUAGE_ENGLISH, _("&English"))
		self.menu2.SetLabel(MENU_LANGUAGE_SPANISH, _("&Spanish"))
		self.menu2.SetLabel(MENU_LANGUAGE_FRENCH, _("&French"))
		# Update the Status Bar Text
		self.SetStatusText(str)

		def OnSelectLanguaje(self, event):
			# TODO: Implement OnSelectLanguaje
			print("Idioma")
			pass

	def OnMouseEvent(self, event):
		print("Range select")
		print("row:" + repr(event.GetRow()))
		print("Col:" + repr(event.GetCol()))
		pass

	def OnGridSelectCell(self, event):
		if self.SelectedT1:
			self.view.SetCellBackground(self.OldRow, self.OldCol, False)
		#            print "1.-Apagar:"+repr(self.OldRow)+")("+repr(self.OldCol)+")"

		self.OldRow = event.GetRow()
		self.OldCol = event.GetCol()
		if self.SelectedT2:
			#            print "1.2-Apagar:"+repr(self.NewRow)+")("+repr(self.NewCol)+")"
			self.view.SetCellBackground(self.NewRow, self.NewCol, False)
			self.m_textCtrlFin.SetValue("-")
			self.m_textCtrlDelta.SetValue("-")
		fecha = self.view.GetTime(self.OldRow, self.OldCol)
		self.m_textCtrlInicio.SetValue(str(fecha))
		self.view.SetCellBackground(self.OldRow, self.OldCol, True)

		setup = self.view.GetSetup(self.OldRow, self.OldCol)
		if setup is not None:
			senal = self.DecodeSetup(setup)
			self.m_textCtrlStatus.SetValue(senal)

			self.m_grid1.ForceRefresh()
			self.SelectedT1 = True

		pass

	def OnGridCellRightClick(self, event):
		if self.SelectedT2:
			self.view.SetCellBackground(self.NewRow, self.NewCol, False)

		self.NewRow = event.GetRow()
		self.NewCol = event.GetCol()
		fecha1 = self.view.GetTime(self.NewRow, self.NewCol)
		self.m_textCtrlFin.SetValue(str(fecha1))
		self.view.SetCellBackground(self.NewRow, self.NewCol, True)

		if self.SelectedT1:
			#            self.m_grid1.SetCellBackgroundColour(self.OldRow, self.OldCol, wx.WHITE)
			fecha2 = self.view.GetTime(self.OldRow, self.OldCol)
			self.m_textCtrlDelta.SetValue(str(fecha1 - fecha2))

		self.SelectedT2 = True
		setup = self.view.GetSetup(self.NewRow, self.NewCol)
		if setup is not None:
			senal = self.DecodeSetup(setup)
			self.m_textCtrlStatus.SetValue(senal)
			self.m_grid1.ForceRefresh()
		pass

	def viewgrid(self):
		self.view = ViewPanel(self)
		return

	def OnBtnFichero(self, event):

		devnum = []
		wildcard1 = "PCAP (*.PCAP; *.pcap)|*.PCAP;*.pcap| All files (*.*)|*.*"
		dlg = wx.FileDialog(self, _("Select File"), os.getcwd(), "", wildcard1, wx.FD_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			self.chargeGridFromFile(path)

		dlg.Destroy()

	def OnButtonCapture(self, event):
		print("MyButton")

		if self.m_buttonCapture.GetLabelText() == _("Capture"):
			a = self.m_comboBoxttyUSB.GetValue()
			# lsusb | grep Serial
			output = subprocess.check_output("lsusb | grep Serial", shell=True)
			a = output.split(" ")
			bus = a[1]
			devnum = a[3]
			b = bus.strip("0")
			usbmon = "usbmon" + b

			# Capturar datos del conversor    tcpdump -i usbmon1 -w /data/usblog.pcap
			date = time.localtime()
			filedate = str(date.tm_year) + "-" + str(date.tm_mon) + "-" + str(date.tm_mday) + "-" + str(date.tm_hour) + str(date.tm_min) + str(date.tm_sec)
			self.captureFile = "./captures/usblog" + filedate + ".pcap"
			self.captura = subprocess.Popen(["tcpdump", "-i", usbmon, "-w", self.captureFile])

			self.m_buttonCapture.SetLabel(_("Stop"))
		else:
			self.captura.send_signal(signal.SIGINT)
			#            self.captura.kill()
			self.m_buttonCapture.SetLabel(_("Capture"))
			self.chargeGridFromFile(self.captureFile)

	# Clean the grid
	def OnBtnClean(self, event):
		self.view.EmptyGrid()

	def chargeGridFromFile(self, path):
		devnum = []
		self.view.EmptyGrid()
		self.view.EmptyListData()
		self.m_comboBoxdev.Clear()
		self.view.cleanDevnum()
		self.view.setDevnum("-")
		mypath = os.path.basename(path)
		self.SetStatusText("You selected: %s" % mypath)
		print("file:" + repr(path))
		self.m_buttonfichero.SetLabel(path)
		self.view.cargaFichero(path)
		self.view.Devnums(devnum)
		for i in range(len(devnum)):
			self.m_comboBoxdev.Append(str(devnum[i]))
			print("devnum[i]:" + repr(devnum[i]))

		self.m_grid1.SetColSize(16, 200)

	def OnComboDevSelect(self, event):
		# TODO: Implement OnComboDevSelect
		self.SelectedDevnum = self.m_comboBoxdev.GetValue()
		print("OnComboDevSelect:" + repr(self.SelectedDevnum))
		if "(RS232)" in self.SelectedDevnum:
			a = self.SelectedDevnum.split("(RS232)")
			self.SelectedDevnum = int(a[0])
		self.view.setDevnum(int(self.SelectedDevnum))
		self.view.EmptyGrid()
		self.view.processDataTable()
		self.view.showDataTable()

	###############################################################################
	# setLateralPanelTxt
	#       Decodes de bytes to ASCII code.
	#
	###############################################################################
	def setLateralPanelTxt(self):

		print("len(self.listdata):" + repr(len(self.listdata)))
		for i in range(len(self.listdata)):
			row = i // 16  # division entera
			col = i % 16  # resto division
			data = self.listdata[i]
			sz_value = str(data.data).strip("[]")

			if sz_value != "-" and sz_value != "|":
				intvalue = int(sz_value)

				if intvalue > 32 and intvalue < 127:
					sz_value = str(chr(intvalue))
				else:
					sz_value = "."

			if col == 15:
				self.m_richText1.AppendText(sz_value)
				self.m_richText1.AppendText("\n")
			else:
				self.m_richText1.AppendText(sz_value)

	###############################################################################
	# DecodeSetup
	#       Decodes de bytes of the signal state.
	#
	###############################################################################

	def DecodeSetup(self, setup):

		decoded = " "
		#print("setup:" +repr(setup))
		if setup != "0":
			cadena = setup.split(" ")
			if (cadena[1] == "22") and (cadena[0] == "21"):

				if int(cadena[2], 16) & 0x0200:
					decoded = decoded + "DTR "
				if int(cadena[2], 16) & 0x0100:
					decoded = decoded + "RTS "
			elif (cadena[1] == "32") and (cadena[0] == "161"):
				if int(cadena[8]) & 0x80:
					decoded = decoded + "CTS "

		decoded = decoded + "(" + setup + ")"
		return decoded


if __name__ == "__main__":
	# configure logging
	logging.basicConfig(format="--- [%(levelname)s] %(message)s", level=logging.DEBUG)

	print("Start ttyUsbView")

	app = wx.App(False)
	theFrame = DlgttyUsbSpy(None)
	theFrame.viewgrid()
	theFrame.Show()
	app.MainLoop()
