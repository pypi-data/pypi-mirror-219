import math
import ctypes
import win32gui
from ctypes import wintypes

__version__ = "2.0.2"

# Windows API Types
CS_HREDRAW = 0x0002
CS_VREDRAW = 0x0001
LRESULT = ctypes.c_long
CW_USEDEFAULT = -2147483648

# Windows API messages
WM_PAINT = 0x000F
WM_DESTROY = 0x0002
WM_MOUSEMOVE = 0x0200

# Windows API Constants
WNDCLASS_STYLES = CS_HREDRAW | CS_VREDRAW
WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, ctypes.c_long)

WS_CAPTION = 0x00C00000
WS_SYSMENU = 0x00080000
WS_MINIMIZEBOX = 0x00020000
WS_OVERLAPPED = WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX

# Windows API Functions
GetModuleHandle = ctypes.windll.kernel32.GetModuleHandleW
RegisterClass = ctypes.windll.user32.RegisterClassW
CreateWindowEx = ctypes.windll.user32.CreateWindowExW
DefWindowProc = ctypes.windll.user32.DefWindowProcW
PeekMessage = ctypes.windll.user32.PeekMessageW
TranslateMessage = ctypes.windll.user32.TranslateMessage
DispatchMessage = ctypes.windll.user32.DispatchMessageW
GetMessage = ctypes.windll.user32.GetMessageW
PostQuitMessage = ctypes.windll.user32.PostQuitMessage
ShowWindow = ctypes.windll.user32.ShowWindow
UpdateWindow = ctypes.windll.user32.UpdateWindow
GetDC = ctypes.windll.user32.GetDC
CreatePen = ctypes.windll.gdi32.CreatePen
SelectObject = ctypes.windll.gdi32.SelectObject
MoveToEx = ctypes.windll.gdi32.MoveToEx
LineTo = ctypes.windll.gdi32.LineTo
DeleteObject = ctypes.windll.gdi32.DeleteObject
ReleaseDC = ctypes.windll.user32.ReleaseDC
DestroyWindow = ctypes.windll.user32.DestroyWindow
UnregisterClass = ctypes.windll.user32.UnregisterClassW

class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [("hdc", wintypes.HDC),
                ("fErase", wintypes.BOOL),
                ("rcPaint", wintypes.RECT),
                ("fRestore", wintypes.BOOL),
                ("fIncUpdate", wintypes.BOOL),
                ("rgbReserved", wintypes.BYTE * 32)]

# Window Procedure
def wndProc(hwnd, msg, wParam, lParam):
    if msg == 0x000F:  # WM_PAINT
        ps = PAINTSTRUCT()
        hdc = ctypes.windll.user32.BeginPaint(hwnd, ctypes.byref(ps))
        ctypes.windll.user32.EndPaint(hwnd, ctypes.byref(ps))
        return 0
    
    elif msg == 0x0010:  # WM_DESTROY
        ctypes.windll.user32.PostQuitMessage(0)
        return 0
    
    else:
        return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wParam, lParam)

class WNDCLASS(ctypes.Structure):
    _fields_ = [("style", wintypes.UINT),
                ("lpfnWndProc", WNDPROC),
                ("cbClsExtra", wintypes.INT),
                ("cbWndExtra", wintypes.INT),
                ("hInstance", wintypes.HINSTANCE),
                ("hIcon", wintypes.HICON),
                ("hCursor", wintypes.HANDLE),
                ("hbrBackground", wintypes.HBRUSH),
                ("lpszMenuName", wintypes.LPCWSTR),
                ("lpszClassName", wintypes.LPCWSTR)]

class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [("hdc", wintypes.HDC),
                ("fErase", wintypes.BOOL),
                ("rcPaint", wintypes.RECT),
                ("fRestore", wintypes.BOOL),
                ("fIncUpdate", wintypes.BOOL),
                ("rgbReserved", wintypes.BYTE * 32)]

BeginPaint = ctypes.windll.user32.BeginPaint
BeginPaint.restype = wintypes.HDC
BeginPaint.argtypes = [wintypes.HWND, ctypes.POINTER(PAINTSTRUCT)]

EndPaint = ctypes.windll.user32.EndPaint
EndPaint.restype = wintypes.BOOL
EndPaint.argtypes = [wintypes.HWND, ctypes.POINTER(PAINTSTRUCT)]

class Graphic:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.hInstance = ctypes.windll.kernel32.GetModuleHandleW(None)

        className = "WINQ2DLGRAPHIC"
        self.wndClass = WNDCLASS()
        self.wndClass.style = WNDCLASS_STYLES
        self.wndClass.lpfnWndProc = WNDPROC(wndProc)
        self.wndClass.hInstance = self.hInstance
        self.wndClass.lpszClassName = className
        RegisterClass(ctypes.byref(self.wndClass))

        self.hWnd = ctypes.windll.user32.CreateWindowExW(0, className, "Q2DL", WS_OVERLAPPED,
                                   CW_USEDEFAULT, CW_USEDEFAULT, width, height,
                                   None, None, self.hInstance, None)

        self.canvas = self.hWnd  # Use the window handle as the canvas

    def update(self):
        hdc = ctypes.windll.user32.GetDC(self.hWnd)
        ps = PAINTSTRUCT()
        ctypes.windll.user32.BeginPaint(self.hWnd, ctypes.byref(ps))
        ctypes.windll.user32.EndPaint(self.hWnd, ctypes.byref(ps))
        ctypes.windll.user32.ReleaseDC(self.hWnd, hdc)
    
    def run(self):
        ShowWindow(self.hWnd, wintypes.SW_SHOWDEFAULT)
        UpdateWindow(self.hWnd)

        msg = wintypes.MSG()
        while GetMessage(ctypes.byref(msg), None, 0, 0) > 0:
            TranslateMessage(ctypes.byref(msg))
            DispatchMessage(ctypes.byref(msg))

    def rotate(self, point, angle):
        # Rotate a 3D point around the Y-axis
        x, y, z = point
        rad = math.radians(angle)
        cos_rad = math.cos(rad)
        sin_rad = math.sin(rad)
        new_x = x * cos_rad - z * sin_rad
        new_z = x * sin_rad + z * cos_rad
        return new_x, y, new_z

    def draw_line(self, x1, y1, x2, y2):
        # Draw a line on the canvas
        hdc = GetDC(self.hWnd)
        pen = CreatePen(0, 1, 0)
        oldPen = SelectObject(hdc, pen)

        x1_screen, y1_screen = self.convert_coordinates(x1, y1)
        x2_screen, y2_screen = self.convert_coordinates(x2, y2)

        MoveToEx(hdc, x1_screen, y1_screen, None)
        LineTo(hdc, x2_screen, y2_screen)

        SelectObject(hdc, oldPen)
        DeleteObject(pen)
        ReleaseDC(self.hWnd, hdc)

    def convert_coordinates(self, x, y):
        # Convert 3D coordinates to screen coordinates
        x_screen = int((x + 1) * self.width / 2)
        y_screen = int((1 - y) * self.height / 2)
        return x_screen, y_screen
    
    def clear_canvas(self):
        hdc = win32gui.GetDC(self.hWnd)
        brush = win32gui.GetStockObject(5)
        rect = (0, 0, self.width, self.height)
        win32gui.FillRect(hdc, rect, brush)
        win32gui.ReleaseDC(self.hWnd, hdc)
    
    def __del__(self):
        DestroyWindow(self.hWnd)
        UnregisterClass(self.wndClass.lpszClassName, self.hInstance)
