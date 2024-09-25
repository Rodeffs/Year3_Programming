#include "stdafx.h"
#include "SaveBMP.h"


PBITMAPINFO CreateBitmapInfoStruct(HBITMAP hBmp)
{ 
    BITMAP bmp; 
    PBITMAPINFO pbmi; 
    WORD    cClrBits; 
 
    // Получаем размер картинки и количество бит на пиксел (формат цвета)
    if (!GetObject(hBmp, sizeof(BITMAP), (LPSTR)&bmp)) 
        return NULL;
	
    // Преобразование формата цвета к стандартному числу бит
	if(bmp.bmBitsPixel>24) bmp.bmBitsPixel=24;
    cClrBits = (WORD)(bmp.bmBitsPixel); 
    if (cClrBits == 1) 
        cClrBits = 1; 
    else if (cClrBits <= 4) 
        cClrBits = 4; 
    else if (cClrBits <= 8) 
        cClrBits = 8; 
	else if (cClrBits <= 16) 
        cClrBits = 16; 
    else 
        cClrBits = 24; 
    
    // Выделяем память для структуры  BITMAPINFO
	// с учетом размера структуры BITMAPINFOHEADER  
	if (cClrBits < 16)  // учитываем также палитру цветов (массив структур RGBQUAD)
		pbmi = (PBITMAPINFO) new BYTE[	sizeof(BITMAPINFOHEADER) +
										sizeof(RGBQUAD) * (1<<cClrBits)];
    else  // палитры нет
		pbmi = (PBITMAPINFO) new BYTE[ sizeof(BITMAPINFOHEADER)];

  
    // Заполняем поля структуры BITMAPINFO
    pbmi->bmiHeader.biSize = sizeof(BITMAPINFOHEADER); 
    pbmi->bmiHeader.biWidth = bmp.bmWidth; 
    pbmi->bmiHeader.biHeight = bmp.bmHeight; 
    pbmi->bmiHeader.biPlanes = bmp.bmPlanes; 
    pbmi->bmiHeader.biBitCount = bmp.bmBitsPixel; 
	pbmi->bmiHeader.biXPelsPerMeter = 0;
	pbmi->bmiHeader.biYPelsPerMeter = 0; 

    if (cClrBits < 16) 
        pbmi->bmiHeader.biClrUsed = (1<<cClrBits);
     // Сжимать картинку не собираемся - ставим флаг BI_RGB 
	pbmi->bmiHeader.biCompression = BI_RGB; 
 
	// Вычисляем количество байт, требуемых для хранения изображения
	// с учетом количества пикселов и бит на пиксел.
    // В файле BMP строки должны быть выровнены на границу 4 байт,
	// поэтому длина строки в байтах определяется с помощью 
	// специального макроса (см. файл savebmp.h)
    pbmi->bmiHeader.biSizeImage =	BYTESPERLINE(pbmi->bmiHeader.biWidth, cClrBits)*
									pbmi->bmiHeader.biHeight; 
 
    // Считаем что все цвета нашей картинки важны 
    pbmi->bmiHeader.biClrImportant = 0; 
 
    return pbmi; 
} 


BOOL SaveBitmapToBMPFile(CString &FileName, CBitmap &BMP, CDC &DC) 
 { 
 
    HANDLE hf=NULL;             // указатель на файл
    BITMAPFILEHEADER hdr;       // заголовок BMP файла
    PBITMAPINFOHEADER pbih;     // заголовок картинки
    BYTE * pBits=NULL;			// указатель на растровые данные
    DWORD dwWidthBytes=0;       // длина строки растровых данных в байтах
    DWORD dwTmp=0;			    // для временных потребностей

	//Создаем структуру - заголовок растра
	PBITMAPINFO pbmi=CreateBitmapInfoStruct((HBITMAP)BMP);
 
    pbih = (PBITMAPINFOHEADER) pbmi; 
	
	// Выделяем память под растровые данные
	pBits =  new BYTE[pbih->biSizeImage];
    if (!pBits) return FALSE; 

    // Получаем растровые данные 
	// и таблицу цветов (массив стркутур RGBQUAD) если она есть
	if (!GetDIBits(DC.m_hDC, (HBITMAP)BMP, 0, (WORD) pbih->biHeight, 
                   pBits, pbmi, DIB_RGB_COLORS)) 
       return FALSE; 
		
 
    // Создаем файл на диске
    hf = CreateFile(FileName, 
                   GENERIC_READ | GENERIC_WRITE, 
                   (DWORD) 0, 
                   (LPSECURITY_ATTRIBUTES) NULL, 
                   CREATE_ALWAYS, 
                   FILE_ATTRIBUTE_NORMAL, 
                   (HANDLE) NULL); 
    if (hf == INVALID_HANDLE_VALUE) return FALSE; 
	// Идентификатор типа файла BMP: 0x42 = "B" 0x4d = "M"  
    hdr.bfType = 0x4d42;        
 
    // Размер всего файла вместе с заголовками и данными
    hdr.bfSize = (DWORD) (sizeof(BITMAPFILEHEADER) + 
					pbih->biSize + pbih->biClrUsed 
					* sizeof(RGBQUAD) + pbih->biSizeImage); 
    hdr.bfReserved1 = 0; 
    hdr.bfReserved2 = 0; 
 
    // Вычисляем смещение до начала растровых данных
    hdr.bfOffBits = (DWORD) sizeof(BITMAPFILEHEADER) + 
                    pbih->biSize + pbih->biClrUsed 
                    * sizeof (RGBQUAD); 
 
    // Записываем заголовок файла - структуру BITMAPFILEHEADER
    if (!WriteFile(hf, (LPVOID) &hdr, sizeof(BITMAPFILEHEADER), 
       (LPDWORD) &dwTmp, (LPOVERLAPPED) NULL)) 
       return FALSE;
 
    // Записываем заголовок картинки - структуру BITMAPINFOHEADER
	// и палитру - массив RGBQUAD 
 
    if (!WriteFile(hf, (LPVOID) pbih, sizeof(BITMAPINFOHEADER) 
                  + pbih->biClrUsed * sizeof (RGBQUAD), 
                  (LPDWORD) &dwTmp, (LPOVERLAPPED) NULL)) 
       return FALSE;
 
    // Записываем растровые данные
	dwWidthBytes = BYTESPERLINE(pbih->biWidth, pbih->biBitCount);
	LONG i=0, j=0;
    BYTE	*pCurStr=NULL;		// указатель на текущую строку
	
	pCurStr=pBits;
	for(i=0; i<pbih->biHeight; i++) // записываем по строкам
	{
		if (!WriteFile(hf, (LPSTR) pCurStr, (int) dwWidthBytes, 
                         (LPDWORD) &dwTmp, (LPOVERLAPPED) NULL)) 
			return FALSE;
		pCurStr+=dwWidthBytes;
    }
 
    // Закрываем файл
     if (!CloseHandle(hf)) return FALSE; 
 
    // Освобождаем память
    if(pBits!=NULL) delete[] pBits;
	if(pbmi!=NULL) delete[] pbmi;
	return TRUE;
} 
