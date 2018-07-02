#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Change2CUI=y
#AutoIt3Wrapper_Run_Tidy=y
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****
#include <GuiListView.au3>
#include <Excel.au3>
#include <GuiTreeView.au3>
#include <Date.au3>
#include <GuiToolbar.au3>

;Constant Variable Names -------------------------------------------------------------------------------------------------
Global $1, $2, $3, $4, $5, $6, $7, $8, $x, $number, $itemcounter, $oExcel, $oWorkbook, $HPE, $HPListView, $SysTree, $TreeSub, $HWnd, $hTreeview, $Runtime_FileName, $name
$HPE = "HPE Service Manager"
$FOLDER = "MCC"
$QUERYNAME = "MCC"
;Start SM9 ---------------------------------------------------------------------------------------------------------------
ShellExecute('C:\Program Files (x86)\HPE\Service Manager 9.50\Client\ServiceManager.exe')
ConsoleWrite("Starting Up SM9, Please wait" & @CRLF)

While 1

	If ControlGetText($HPE, '', 'Edit1') = 'To Do' Then ExitLoop
	Sleep(1000)
	RestartHandler()
WEnd

VIEWID()

_GUICtrlTreeView_SelectItem($SysTree, $TreeSub)
ControlFocus($HPE, "", $SysTree)
Sleep(5000)
Send("{ENTER}")
While 1

	If ControlGetText($HPE, '', 'Edit1') = 'Incident' Then ExitLoop
	Sleep(1000)
	RestartHandler()
WEnd
ControlFocus($HPE, "", $HPListView)


InitialStart()

LoopingHRLY("MCC_DATA.xlsx")


ProcessClose("ServiceManager.exe")
Sleep(1000)
ProcessClose("ServiceManager.exe")
Sleep(1000)

;ShellExecute('C:\MCC\MOB.vbs')
ShellExecute('C:\MCC\MCC_emailing.exe')


Func ExcelTitle()
	RunTimeOutput("Creating New Excel " & @CRLF)
	$oExcel = _Excel_Open()
	$oWorkbook = _Excel_BookNew($oExcel)

	_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, "INM", "A1")
	_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, "PRIO", "B1")
	_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, "STATUS", "C1")
	_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, "AG", "D1")
	_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, "CUSTOMER", "E1")
	_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, "CBI", "F1")
	_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, "TSI CREATION DATE", "G1")
	_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, "TITLE", "H1")


EndFunc   ;==>ExcelTitle

Func LoopingHRLY($name)

	ExcelTitle()
	Sleep(2000)
	WinActivate($HPE)
	ControlListView($HPE, "", $HPListView, "Select", 0)

	$x = 0
	RunTimeOutput("Inputting data to excel" & @CRLF)
	While 1

		$1 = ControlListView($HPE, "", $HPListView, "GetText", $x, 0)
		$2 = ControlListView($HPE, "", $HPListView, "GetText", $x, 1)
		$3 = ControlListView($HPE, "", $HPListView, "GetText", $x, 2)
		$4 = ControlListView($HPE, "", $HPListView, "GetText", $x, 3)
		$5 = ControlListView($HPE, "", $HPListView, "GetText", $x, 4)
		$6 = ControlListView($HPE, "", $HPListView, "GetText", $x, 5)
		$7 = ControlListView($HPE, "", $HPListView, "GetText", $x, 6)
		$8 = ControlListView($HPE, "", $HPListView, "GetText", $x, 7)
		If $1 = "" Then
			ExitLoop
		EndIf



		_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, $1, "A" & $x + 2)
		_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, $2, "B" & $x + 2)
		_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, $3, "C" & $x + 2)
		_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, $4, "D" & $x + 2)
		_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, $5, "E" & $x + 2)
		_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, $6, "F" & $x + 2)
		_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, $7, "G" & $x + 2)
		_Excel_RangeWrite($oWorkbook, $oWorkbook.Activesheet, $8, "H" & $x + 2)


		$x += 1
		ControlSend($HPE, "", $HPListView, "{DOWN}")

	WEnd

	_Excel_BookSaveAs($oWorkbook, "C:\" & $FOLDER & "\" & $name, Default, True)
	_Excel_Close($oExcel, True, True)
	RunTimeOutput("Excel Saved to C:\" & $FOLDER & @CRLF)

EndFunc   ;==>LoopingHRLY


Func RestartHandler()

	$WinExistCounter = 1
	While WinExists("Server not available...")

		RunTimeOutput("Server not available, Rebooting" & @CRLF)
		Sleep(1000)
		$WinExistCounter += 1
		If $WinExistCounter > 5 Then
			ProcessClose("ServiceManager.exe")
			Sleep(1000)
			ProcessClose("ServiceManager.exe")
			Sleep(1000)
			ProcessClose("ServiceManager.exe")
			Sleep(120000)
			Start_SM9()
			Sleep(5000)
			VIEWID()
			_GUICtrlTreeView_SelectItem($SysTree, $TreeSub)

			ControlFocus($HPE, "", $SysTree)
			Sleep(5000)
			Send("{ENTER}")
			Sleep(5000)
			ControlClick($HPE, "", $HPListView, "left", 1)

			InitialStart()

		EndIf

	WEnd

	$WinCCounter = 1
	While WinExists("Server Connection")

		RunTimeOutput("Server connection down, Rebooting" & @CRLF)
		Sleep(1000)
		$WinCCounter += 1
		If $WinCCounter > 5 Then
			ProcessClose("ServiceManager.exe")
			Sleep(1000)
			ProcessClose("ServiceManager.exe")
			Sleep(1000)
			ProcessClose("ServiceManager.exe")
			Sleep(120000)
			Start_SM9()
			Sleep(5000)
			VIEWID()
			_GUICtrlTreeView_SelectItem($SysTree, $TreeSub)
			ControlFocus($HPE, "", $SysTree)
			Sleep(5000)
			Send("{ENTER}")
			Sleep(5000)
			ControlClick($HPE, "", $HPListView, "left", 1)

			InitialStart()
			ExitLoop



		EndIf

	WEnd


	$WinCcCounter = 1
	While WinExists("Communication Error")

		RunTimeOutput("Server connection down, Rebooting" & @CRLF)
		Sleep(1000)
		$WinCcCounter += 1
		If $WinCcCounter > 5 Then
			ProcessClose("ServiceManager.exe")
			Sleep(1000)
			ProcessClose("ServiceManager.exe")
			Sleep(1000)
			ProcessClose("ServiceManager.exe")
			Sleep(120000)
			Start_SM9()
			Sleep(5000)
			VIEWID()
			_GUICtrlTreeView_SelectItem($SysTree, $TreeSub)
			ControlFocus($HPE, "", $SysTree)
			Sleep(5000)
			Send("{ENTER}")
			Sleep(5000)
			ControlClick($HPE, "", $HPListView, "left", 1)

			InitialStart()
			ExitLoop



		EndIf

	WEnd

;~ 	$WinCccCounter = 1
;~ 	While WinExists("Auto ")

;~ 		RunTimeOutput("Auto Logging" & @CRLF)
;~ 		Sleep(1000)
;~ 		$WinCccCounter += 1
;~ 		If $WinCccCounter > 5 Then
;~ 			ControlClick("Auto Login", "", "Button1")
;~ 			Sleep(10000)
;~ 			$hWindow = WinGetHandle($HPE)
;~ 			ConsoleWrite('Loading Connections Window' & @CR)
;~ 			While Not WinExists('Connections', 'Create, manage, and use connections')
;~ 				Sleep(1000)
;~ 			WEnd
;~ 			ConsoleWrite('Logging In...' & @CRLF)
;~ 			While WinExists('Connections', 'Create, manage, and use connections')
;~ 				ControlClick('Connections', '', 'Button13')
;~ 				Sleep(1000)
;~ 			WEnd
;~ 			While 1

;~ 				If ControlGetText($HPE, '', 'Edit1') = 'To Do' Then ExitLoop
;~ 				Sleep(1000)
;~ 				RestartHandler()
;~ 			WEnd
;~ 			Sleep(1000)
;~ 			VIEWID()
;~ 			_GUICtrlTreeView_SelectItem($SysTree, $TreeSub)

;~ 			ControlFocus($HPE, "", $SysTree)
;~ 			Sleep(5000)
;~ 			Send("{ENTER}")
;~ 			Sleep(5000)
;~ 			ControlClick($HPE, "", $HPListView, "left", 1)

;~ 			InitialStart()
;~ 			ExitLoop



;~ 		EndIf

;~ 	WEnd


	$WinupdateCounter = 1
	While WinExists("Windows Update")

		RunTimeOutput("Windows trying to update, closing SM9 to conduct restart" & @CRLF)
		Sleep(1000)
		$WinupdateCounter += 1
		If $WinupdateCounter > 5 Then
			WinActivate("Windows Update")


			Send("{Tab}")
			Send("{Down}")
			Send("{Down}")
			ControlClick("Windows Update", "", "Button2")

			ProcessClose("ServiceManager.exe")
			Sleep(1000)
			ProcessClose("ServiceManager.exe")
			Sleep(1000)
			ProcessClose("ServiceManager.exe")
			Sleep(120000)
			Start_SM9()
			Sleep(5000)
			VIEWID()
			_GUICtrlTreeView_SelectItem($SysTree, $TreeSub)

			ControlFocus($HPE, "", $SysTree)
			Sleep(5000)
			Send("{ENTER}")
			Sleep(5000)
			ControlClick($HPE, "", $HPListView, "left", 1)

			InitialStart()

		EndIf

	WEnd

EndFunc   ;==>RestartHandler

Func Start_SM9()
	If Not WinExists($HPE) Then
		ConsoleWrite('HPE Service Manager Window not found' & @CRLF)
		If FileExists('C:\Program Files (x86)\HPE\Service Manager 9.50\Client\ServiceManager.exe') Then
			ConsoleWrite('Loading ServiceManager.exe' & @CRLF)
			ShellExecute('C:\Program Files (x86)\HPE\Service Manager 9.50\Client\ServiceManager.exe')
			While Not WinExists($HPE)
				Sleep(100)
			WEnd
			ConsoleWrite('Loading Main Screen' & @CRLF)
			$hWindow = WinGetHandle('HPE Service Manager')
			While 1

				If ControlGetText($HPE, '', 'Edit1') = 'To Do' Then ExitLoop
				Sleep(1000)
				RestartHandler()
			WEnd
			Sleep(1000)
		Else
			ConsoleWrite('ServiceManager.exe file not found' & @CRLF)
			Exit
		EndIf
	EndIf
EndFunc   ;==>Start_SM9

Func GetSysListview32_ControlID()
	If Not WinExists($HPE) Then Exit
	$hWindow = WinActivate($HPE)
	$SysListView32_ClassCount = GetWindowsControl_Count('SysListView32')
	$bSysListView32Found = False
	For $Instance = 1 To $SysListView32_ClassCount
		$SysListView32_ControlID = 'SysListView32' & $Instance
		$hSysListView32 = ControlGetHandle($HPE, "", $SysListView32_ControlID)
		$hSysListView32_Visible = ControlCommand($hSysListView32, '', '', 'IsVisible', '')
		If $hSysListView32_Visible <> 1 Then ContinueLoop
		$bSysListView32Found = True
		$Return_Value = $SysListView32_ControlID
		ExitLoop
	Next
	If $bSysListView32Found = False Then $Return_Value = 'SysListView32 Control Not Found'
	Return $Return_Value
EndFunc   ;==>GetSysListview32_ControlID

Func GetSysTreeView32_ControlID()
	If Not WinExists("HPE Service Manager") Then Exit
	$hWindow = WinActivate("HPE Service Manager")
	$TreeViewControlCount = GetWindowsControl_Count('SysTreeView32')
	$bTreeViewControlFound = False
	For $i = 1 To $TreeViewControlCount
		$TreeView_ControlID = 'SysTreeView32' & $TreeViewControlCount
		$hTreeview = ControlGetHandle($hWindow, 'Connection - New_configuration', $TreeView_ControlID)
		If $hTreeview = 0 And @error <> 0 Then ContinueLoop
		If ControlCommand($hTreeview, '', '', 'IsVisible') <> 1 Then ContinueLoop
		$bTreeViewControlFound = True
		$Return_Value = $TreeView_ControlID
		ExitLoop
	Next
	If $bTreeViewControlFound = False Then $Return_Value = 'Control Not Found'
	Return $Return_Value
EndFunc   ;==>GetSysTreeView32_ControlID

Func GetWindowsControl_Count($sClass)
	$hWindow = WinActivate("HPE Service Manager")
	$sClassList = WinGetClassList($hWindow)
	$aClassList = StringSplit($sClassList, @CRLF, 2)
	_ArraySort($aClassList)
	_ArrayDelete($aClassList, 0)
	If StringLen($sClass) > 0 Then
		For $i = UBound($aClassList) - 1 To 0 Step -1
			If $aClassList[$i] <> $sClass Then
				_ArrayDelete($aClassList, $i)
			EndIf
		Next
	EndIf
	Return UBound($aClassList)
EndFunc   ;==>GetWindowsControl_Count

Func GetSysTreeView32_SubItemID($ViewName)
	$hWindow = WinActivate("HPE Service Manager")
	If $hTreeview = 0 Then
		$TreeViewControlCount = GetWindowsControl_Count('SysTreeView32')
		$bTreeViewControlFound = False
		For $i = 1 To $TreeViewControlCount
			$TreeView_ControlID = 'SysTreeView32' & $TreeViewControlCount
			$hTreeview = ControlGetHandle($hWindow, 'Connection - New_configuration', $TreeView_ControlID)
			If $hTreeview = 0 And @error <> 0 Then ContinueLoop
			If ControlCommand($hTreeview, '', '', 'IsVisible') <> 1 Then ContinueLoop
			$bTreeViewControlFound = True
			ExitLoop
		Next
		If $bTreeViewControlFound = False Then $Return_Value = 'SysTreeView32 Control Not Found'
	Else
		_GUICtrlTreeView_Expand($hTreeview, 0, False)
		ControlTreeView($hTreeview, '', '', 'Expand', '#0')
		$Root_ItemCount = ControlTreeView($hTreeview, '', '', 'GetItemCount', '#0')
		$bFavoritesandDashboardsFound = False
		For $j = 0 To $Root_ItemCount - 1
			$ItemID = '#0|#' & $j
			$ItemName = ControlTreeView($hTreeview, '', '', 'GetText', $ItemID)
			If $ItemName = 'Favorites and Dashboards' Then
				$bFavoritesandDashboardsFound = True
				ExitLoop
			EndIf
		Next
		If $bFavoritesandDashboardsFound = False Then
			$Return_Value = 'Favourites And Dashboards View Not Found'
		Else
			ControlTreeView($hTreeview, '', '', 'Expand', $ItemID)
			$FavoritesandDashboards_ItemCount = ControlTreeView($hTreeview, '', '', 'GetItemCount', $ItemID)
			$bViewNameFound = False
			For $k = 0 To $FavoritesandDashboards_ItemCount - 1
				$SubItemID = $ItemID & '|#' & $k
				$SubItemName = ControlTreeView($hTreeview, '', '', 'GetText', $SubItemID)
				If StringCompare($SubItemName, $ViewName) = 0 Then
					$bViewNameFound = True

					ControlTreeView($hTreeview, '', '', 'Select', $SubItemID)

					ExitLoop


				EndIf
			Next
			If $bViewNameFound = False Then
				$Return_Value = ''' & $ViewName & '' Not Found'
			Else
				$Return_Value = $SubItemID
			EndIf
		EndIf
	EndIf
	Return $Return_Value
EndFunc   ;==>GetSysTreeView32_SubItemID

Func RunTimeOutput($Message)
	ConsoleWrite(_Now() & @TAB & $Message)
	FileWrite($Runtime_FileName, _Now() & @TAB & $Message)
	$Runtime_FileName = FileOpen("C:\" & $FOLDER & "debug_" & @MDAY & @MON & @YEAR & "_.txt")
EndFunc   ;==>RunTimeOutput

Func VIEWID()
	$SysTree = GetSysTreeView32_ControlID()
	$TreeSub = GetSysTreeView32_SubItemID($QUERYNAME)
	$HPListView = GetSysListview32_ControlID()
	$HWnd = WinGetHandle("HPE Service Manager")
EndFunc   ;==>VIEWID

Func InitialStart()

	WinActivate("HPE Service Manager")
	$HPE = "HPE Service Manager"
	$Runtime_FileName = FileOpen("C:\" & $FOLDER & "\debug_" & @MDAY & @MON & @YEAR & "_.txt")
	$HWnd = WinGetHandle("HPE Service Manager")


EndFunc   ;==>InitialStart
