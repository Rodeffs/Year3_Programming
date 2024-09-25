
// макрос для определения количества байт в выровненной по DWORD строки пикселов в DIB 
// Width - длина строки в пикселах; BPP - бит на пиксел
#define BYTESPERLINE(Width, BPP) ((WORD)((((DWORD)(Width) * (DWORD)(BPP) + 31) >> 5)) << 2) 

BOOL SaveBitmapToBMPFile(CString &FileName, CBitmap &BMP, CDC &DC);
PBITMAPINFO CreateBitmapInfoStruct(HBITMAP hBmp);
