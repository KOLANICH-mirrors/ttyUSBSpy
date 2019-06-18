# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version Oct  8 2012)
# http://www.wxformbuilder.org/
##
# PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

import gettext

_ = gettext.gettext

###########################################################################
# Class ttyUsbSpy
###########################################################################


class ttyUsbSpy(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=_("ttyUsbSpy"), pos=wx.DefaultPosition, size=wx.Size(750, 517), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.Size(640, -1), wx.DefaultSize)

		self.m_toolBar1 = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
		self.m_toolBar1.AddTool(wx.ID_ANY, _("tool"), wx.Bitmap("core/gnome-panel-notification-area.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

		self.m_toolBar1.Realize()

		bSizer1 = wx.BoxSizer(wx.VERTICAL)

		bSizer71 = wx.BoxSizer(wx.HORIZONTAL)

		bSizer71.SetMinSize(wx.Size(-1, 30))
		m_comboBoxttyUSBChoices = []
		self.m_comboBoxttyUSB = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_comboBoxttyUSBChoices, 0)
		bSizer71.Add(self.m_comboBoxttyUSB, 0, wx.ALL, 5)

		self.m_buttonCapture = wx.Button(self, wx.ID_ANY, _("Capture"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer71.Add(self.m_buttonCapture, 0, wx.ALL, 5)

		self.m_buttonClean = wx.Button(self, wx.ID_ANY, _("Clean"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer71.Add(self.m_buttonClean, 0, wx.ALL, 5)

		bSizer71.AddSpacer(100)

		self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, _("Languaje"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText7.Wrap(-1)
		bSizer71.Add(self.m_staticText7, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		m_choice1Choices = []
		self.m_choice1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0)
		self.m_choice1.SetSelection(0)
		self.m_choice1.SetMinSize(wx.Size(150, -1))

		bSizer71.Add(self.m_choice1, 0, wx.ALL, 5)

		bSizer1.Add(bSizer71, 0, wx.EXPAND, 5)

		bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, _("Select File:"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText1.Wrap(-1)
		bSizer2.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.m_buttonfichero = wx.Button(self, wx.ID_ANY, _("file"), wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer2.Add(self.m_buttonfichero, 1, wx.ALL, 5)

		bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)

		bSizer5 = wx.BoxSizer(wx.VERTICAL)

		self.m_scrolledWindow1 = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize) # , wx.ALWAYS_SHOW_SB | wx.VSCROLL
		self.m_scrolledWindow1.SetScrollRate(5, 5)
		bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_grid1 = wx.grid.Grid(self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

		# Grid
		self.m_grid1.CreateGrid(0, 0)
		self.m_grid1.EnableEditing(False)
		self.m_grid1.EnableGridLines(True)
		self.m_grid1.EnableDragGridSize(False)
		self.m_grid1.SetMargins(0, 0)

		# Columns
		self.m_grid1.EnableDragColMove(False)
		self.m_grid1.EnableDragColSize(True)
		self.m_grid1.SetColLabelSize(30)
		self.m_grid1.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

		# Rows
		self.m_grid1.EnableDragRowSize(True)
		self.m_grid1.SetRowLabelSize(80)
		self.m_grid1.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

		# Label Appearance

		# Cell Defaults
		self.m_grid1.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
		bSizer7.Add(self.m_grid1, 1, wx.ALL | wx.EXPAND, 5)

		self.m_scrolledWindow1.SetSizer(bSizer7)
		self.m_scrolledWindow1.Layout()
		bSizer7.Fit(self.m_scrolledWindow1)
		bSizer5.Add(self.m_scrolledWindow1, 1, wx.EXPAND | wx.ALL, 5)

		bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, _("Dev:"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText5.Wrap(-1)
		bSizer6.Add(self.m_staticText5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		m_comboBoxdevChoices = []
		self.m_comboBoxdev = wx.ComboBox(self, wx.ID_ANY, _("-"), wx.DefaultPosition, wx.DefaultSize, m_comboBoxdevChoices, wx.CB_READONLY)
		bSizer6.Add(self.m_comboBoxdev, 0, wx.ALL, 5)

		self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, _("Modem Line Status"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText6.Wrap(-1)
		bSizer6.Add(self.m_staticText6, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.m_textCtrlStatus = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_textCtrlStatus.SetMinSize(wx.Size(250, -1))

		bSizer6.Add(self.m_textCtrlStatus, 0, wx.ALL, 5)

		bSizer5.Add(bSizer6, 0, 0, 5)

		sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Times")), wx.VERTICAL)

		bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, _("Start(T1)"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText2.Wrap(-1)
		bSizer9.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.m_textCtrlInicio = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_textCtrlInicio.SetMinSize(wx.Size(150, -1))

		bSizer9.Add(self.m_textCtrlInicio, 0, wx.ALL, 5)

		self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, _("End(T2)"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText3.Wrap(-1)
		bSizer9.Add(self.m_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.m_textCtrlFin = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_textCtrlFin.SetMinSize(wx.Size(150, -1))

		bSizer9.Add(self.m_textCtrlFin, 0, wx.ALL, 5)

		self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, _("Delta(T2-T1)(ms)"), wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText4.Wrap(-1)
		bSizer9.Add(self.m_staticText4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.m_textCtrlDelta = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_textCtrlDelta.SetMinSize(wx.Size(100, -1))

		bSizer9.Add(self.m_textCtrlDelta, 0, wx.ALL, 5)

		sbSizer1.Add(bSizer9, 0, wx.EXPAND, 5)

		bSizer5.Add(sbSizer1, 0, wx.EXPAND, 5)

		bSizer1.Add(bSizer5, 1, wx.EXPAND, 5)

		self.SetSizer(bSizer1)
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.Bind(wx.EVT_TOOL, self.OnToolHelp, id=wx.ID_ANY)
		self.m_buttonCapture.Bind(wx.EVT_BUTTON, self.OnButtonCapture)
		self.m_buttonClean.Bind(wx.EVT_BUTTON, self.OnBtnClean)
		self.m_choice1.Bind(wx.EVT_CHOICE, self.OnSelectLanguaje)
		self.m_buttonfichero.Bind(wx.EVT_BUTTON, self.OnBtnFichero)
		self.m_grid1.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnGridCellRightClick)
		self.m_grid1.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnGridSelectCell)
		self.m_comboBoxdev.Bind(wx.EVT_COMBOBOX, self.OnComboDevSelect)

	def __del__(self):
		pass

	# Virtual event handlers, overide them in your derived class
	def OnToolHelp(self, event):
		event.Skip()

	def OnButtonCapture(self, event):
		event.Skip()

	def OnBtnClean(self, event):
		event.Skip()

	def OnSelectLanguaje(self, event):
		event.Skip()

	def OnBtnFichero(self, event):
		event.Skip()

	def OnGridCellRightClick(self, event):
		event.Skip()

	def OnGridSelectCell(self, event):
		event.Skip()

	def OnComboDevSelect(self, event):
		event.Skip()
