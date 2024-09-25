// файл Shapes.cpp
////////////////////////////////////////
//реализация классов
#include "stdafx.h"
#include "shapes.h"
#include "global.h"
#include <math.h>

////////////////////////////////////////
// Реализация методов класса CBasePoint
CBasePoint::CBasePoint(): CPoint(0, 0)
{
	m_wSize=1;
	
	m_iPenStyle=PS_SOLID;
	m_iPenWidth=1;
	m_rgbPenColor=RGB(0,0,0);
	m_iBrushStyle=-1; // не используем штриховку
	m_rgbBrushColor=RGB(0,0,0);
	m_dwPattern_ID=0; // нет шаблона заливки
};

CBasePoint::CBasePoint(int x, int y, WORD s):CPoint(x, y)
{
	m_wSize=s;

	m_iPenStyle=PS_SOLID;
	m_iPenWidth=1;
	m_rgbPenColor=RGB(0,0,0);
	m_iBrushStyle=-1; // не используем штриховку
	m_rgbBrushColor=RGB(0,0,0);
	m_dwPattern_ID=0; // нет шаблона заливки
};

IMPLEMENT_SERIAL(CBasePoint, CObject , VERSIONABLE_SCHEMA|1)
void CBasePoint::Serialize(CArchive &ar)
{
	if(ar.IsStoring()) // сохранение
	{
		// Сохраняем параметры объекта
		ar<<x;
		ar<<y;
		ar<<m_wSize;
		ar<<m_iPenStyle;
		ar<<m_iPenWidth;
		ar<<m_rgbPenColor;
		ar<<m_iBrushStyle;
		ar<<m_rgbBrushColor;
		ar<<m_dwPattern_ID;
	}
	else	// чтение
	{
		// Получили версию формата
		int Version=ar.GetObjectSchema();
		// В зависимости от версии
		// можно выполнить различные варианты загрузки
		// Загружаем параметры объекта
		ar>>x;
		ar>>y;
		ar>>m_wSize;
		ar>>m_iPenStyle;
		ar>>m_iPenWidth;
		ar>>m_rgbPenColor;
		ar>>m_iBrushStyle;
		ar>>m_rgbBrushColor;
		ar>>m_dwPattern_ID;

		SetPen(m_rgbPenColor, m_iPenWidth, m_iPenStyle);
		SetBrush(m_rgbBrushColor, m_dwPattern_ID, m_iBrushStyle );
	}
};
BOOL CBasePoint::SetPen(COLORREF color, int width /*=1*/, int style/*=PS_SOLID*/)
{
	m_iPenStyle=style;
	m_iPenWidth=width;
	m_rgbPenColor=color;
	if(HPEN(m_Pen)!=NULL)	// если перо уже существует
		if(!m_Pen.DeleteObject()) return FALSE; // удалили старое перо
	// Создаем новое перо и возвращаем результат
	return m_Pen.CreatePen( m_iPenStyle, m_iPenWidth, m_rgbPenColor);
};
BOOL CBasePoint::SetBrush(COLORREF color, DWORD pattern /*=0*/, int style/*=-1*/)
{
	m_iBrushStyle=style;
	m_dwPattern_ID=pattern;
	m_rgbBrushColor=color;
	int res=1;
	if(HBRUSH(m_Brush)!=NULL)	// если кисть уже существует
		if(!m_Brush.DeleteObject()) return FALSE; // удалили старую кисть
	if(m_dwPattern_ID>0)	// есть шаблон заливки
	{
		CBitmap Pattern;
		if(!Pattern.LoadBitmap(m_dwPattern_ID)) return FALSE;
		return m_Brush.CreatePatternBrush(&Pattern);
	}
	if(m_iBrushStyle>=0)	// указан стиль штриховки
		return m_Brush.CreateHatchBrush( m_iBrushStyle, m_rgbBrushColor);
	// Создаем сплошную кисть и возвращаем результат
	return m_Brush.CreateSolidBrush(m_rgbBrushColor);
};



BOOL CBasePoint::PrepareDC(CDC *pDC)
{
	// Сохраняем состояние контекста устройства
	if(!pDC->SaveDC()) return FALSE;
	// Устанавливаем перо и кисть 
	if(HPEN(m_Pen)!=NULL)
		pDC->SelectObject(&m_Pen);
	if(HBRUSH(m_Brush)!=NULL)
		pDC->SelectObject(&m_Brush);
	return TRUE;
};

BOOL CBasePoint::RestoreDC(CDC *pDC)
{
	// Восстанавливаем состояние контекста устройства
	return pDC->RestoreDC(-1);
};

void CBasePoint::Show(CDC* pDC) 
{
	// Устанавливаем перео и кисть
	PrepareDC(pDC);
	// Рисуем кружок, обозначающий точку
	pDC->Ellipse(x-m_wSize, y-m_wSize, x+m_wSize, y+m_wSize);
	// Восстанавливаем контекст
	RestoreDC(pDC);
} 

void CBasePoint::GetRegion(CRgn &Rgn)
{
	Rgn.CreateEllipticRgn(x-m_wSize, y-m_wSize, x+m_wSize, y+m_wSize);
}

void CBasePoint::Transform(const CPoint &point0, double ang, int a, int b)
{
	CPoint res=::Transform(CPoint(x, y), CPoint(0,0), 0, a, b);
	 x=res.x; y=res.y;
};

BOOL CBasePoint::OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags, UINT nMyFlags) 
{
	BOOL res=TRUE;
	if(nMyFlags & SHIFT_HOLD) //поворот
		switch(nChar)
		{
			case 37: 
				Transform(CPoint(0,0), -ROTATE_STEP, 0, 0);
				break;
			case 39:
				Transform(CPoint(0,0), ROTATE_STEP, 0, 0);
				break;
			default:
				res=FALSE;
		}
	else //перенос
		switch(nChar)
		{
			case 38: // вверх
				Transform(CPoint(0,0), 0, 0, MOVE_STEP);
				break; 
			case 40: // вниз
				Transform(CPoint(0,0), 0, 0, -MOVE_STEP); 
				break;
			case 37: // влево
				Transform(CPoint(0,0), 0, -MOVE_STEP, 0);
				break;
			case 39: // вправо
				Transform(CPoint(0,0), 0, MOVE_STEP, 0);
				break;
			default:
				res=FALSE;
		}	
	return res;
}

////////////////////////////////////////
// Реализация методов класса CSquare

CSquare::CSquare(int x, int y, WORD s): CBasePoint(x, y, s)
{
	m_wSize=s;
} 

CSquare::CSquare(): CBasePoint()
{
	m_wSize=40;
} 

IMPLEMENT_SERIAL(CSquare, CObject, 1)
void CSquare::Serialize(CArchive &ar)
{
	CBasePoint::Serialize(ar);
}
void CSquare::Show(CDC* pDC) 
{
	int s=m_wSize/2;
	// Устанавливаем перео и кисть
	PrepareDC(pDC);
	// Рисуем квадрат
	pDC->Rectangle(x-s, y-s, x+s, y+s);
	// Восстанавливаем контекст
	RestoreDC(pDC);
} 

void CSquare::GetRegion(CRgn &Rgn)
{
	int s=m_wSize/2;
	Rgn.CreateRectRgn(x-s, y-s, x+s, y+s);
}

////////////////////////////////////////
// CSector implementation:

CSector::CSector() : CBasePoint() {
	m_wSize = 40;
}

CSector::CSector(int x, int y, WORD s) : CBasePoint(x, y, s) {
	m_wSize = s;
}

IMPLEMENT_SERIAL(CSector, CObject, 1);

void CSector::Serialize(CArchive& ar) {
	CBasePoint::Serialize(ar);
}

void CSector::Show(CDC* pDC) {

	// The pie is defined by the bounding rectangle (first two coords) and the endpoint (the last two)
	int s = m_wSize / 2;

	PrepareDC(pDC);

	pDC->Pie(x - s, y - s, x + s, y + s, x, y + s, x - s, y);

	RestoreDC(pDC);
}

void CSector::GetRegion(CRgn& Rgn) {
	int s = m_wSize / 2;

	Rgn.CreateRectRgn(x - s, y - s, x + s, y + s);
}

////////////////////////////////////////
// Реализация методов класса CPolygon

CPolygon::CPolygon(): CBasePoint()
{
	m_wSize=0;
	m_bPolygon=FALSE;
} 

CPolygon::~CPolygon()
{
	m_PointsArray.RemoveAll( );
} 


IMPLEMENT_SERIAL(CPolygon, CObject, 1)
void CPolygon::Serialize(CArchive &ar)
{
	if(ar.IsStoring()) // сохранение
	{
		// Сохраняем параметры объекта
		ar<<m_bPolygon;
	}
	else	// чтение
	{
		// Получили версию формата
		int Version=ar.GetObjectSchema();
		// В зависимости от версии
		// можно выполнить различные варианты загрузки
		// Загружаем параметры объекта
		ar>>m_bPolygon;
	}	
	m_PointsArray.Serialize(ar);
	CBasePoint::Serialize(ar);
}
void CPolygon::Show(CDC* pDC) 
{
	// Устанавливаем перео и кисть
	PrepareDC(pDC);
	// Рисуем 
	if(m_bPolygon)
		pDC->Polygon(m_PointsArray.GetData(), m_PointsArray.GetSize());
	else
		pDC->Polyline( m_PointsArray.GetData(), m_PointsArray.GetSize());
	// Восстанавливаем контекст
	RestoreDC(pDC);
} 

void CPolygon::GetRegion(CRgn &Rgn)
{
	Rgn. CreatePolygonRgn(m_PointsArray.GetData(), m_PointsArray.GetSize(), ALTERNATE);
}

void CPolygon::Transform(const CPoint &point0, double ang, int a, int b)
{
	for(int i=0; i<m_PointsArray.GetSize(); i++)
		m_PointsArray[i]=::Transform(m_PointsArray[i], m_PointsArray[0], ang, a, b);
};

/////////////////////////////////////////////////
//3D Polygon

IMPLEMENT_SERIAL(C3DPolygon, CPolygon, -1)
void C3DPolygon::Serialize(CArchive &ar)
{
	CPolygon::Serialize(ar);
	
	if(ar.IsStoring())
	{
	}
	else
	{
	}
	m_3DPointsArray.Serialize(ar);
	
};

void C3DPolygon::MakeProjection(Perspective P)
{
	// Перевод в радианы
	P.theta=P.theta*atan(1.0)/45.0; P.phi=P.phi*atan(1.0)/45.0;
	// Расчет коэффициентов матрицы преобразования
	// Если установлен режим отображения MM_TEXT, при котором начало координат
	// в верхнем левом углу, требуется лишь заменить на противоположный знак 
	// у коэффициентов второго столбца матрицы преобразования (перевернуть ось Y)

	double  st=sin(P.theta), ct=cos(P.theta), sp=sin(P.phi), cp=cos(P.phi),
	v11=-st,	v12=-cp*ct,	v13=-sp*ct,
	v21=ct,		v22=-cp*st,	v23=-sp*st,
				v32=sp,		v33=-cp,
	v41=P.dx,	v42=P.dy,	v43=P.rho;
	double x, y, z;
	double TempZ=0;
	//расчет видовых координат точек
	 m_PointsArray.SetSize(m_3DPointsArray.GetSize());
	for(int i=0; i<m_3DPointsArray.GetSize(); i++)
	{
		x=m_3DPointsArray[i].x-P.O.x;
		y=m_3DPointsArray[i].y-P.O.y;
		z=m_3DPointsArray[i].z-P.O.z;

		TempZ=v13*x+v23*y+v33*z+v43;
		m_PointsArray[i].x=(LONG)(v11*x+v21*y+v41+0.5);
		m_PointsArray[i].y=(LONG)(v12*x+v22*y+v32*z+v42+0.5);

		// Перспективные преобразования
		if(P.with_perspective)
		{
			m_PointsArray[i].x=(LONG)(P.d*m_PointsArray[i].x/TempZ +0.5);
			m_PointsArray[i].y=(LONG)(P.d*m_PointsArray[i].y/TempZ +0.5);
		}
		
		m_PointsArray[i].x+=(LONG)(P.O.x +0.5);
		m_PointsArray[i].y+=(LONG)(P.O.y +0.5);
	}
};

//////////////////////////////////////////////////////
C3DShape::C3DShape(): CBasePoint()
{
	m_Percpective.O.x=0;
	m_Percpective.O.y=0;
	m_Percpective.O.z=0;
	m_Percpective.rho=50000; //50 см. в режиме MM_HIMETRIC
	m_Percpective.theta=30;  
	m_Percpective.phi=30;
	m_Percpective.d=25000; //25 см. в режиме MM_HIMETRIC
	m_Percpective.with_perspective=TRUE;
	m_Percpective.dx=0;
	m_Percpective.dy=0;
}

C3DShape::~C3DShape()
{
	while(m_PtrPolygonList.GetCount()>0)
		delete m_PtrPolygonList.RemoveHead();
	
};

IMPLEMENT_SERIAL(C3DShape, CBasePoint, -1)
void C3DShape::Serialize(CArchive &ar)
{
	if(ar.IsStoring())
	{
		ar << m_Percpective.O.x;
		ar << m_Percpective.O.y;
		ar << m_Percpective.O.z;
		ar << m_Percpective.rho;
		ar << m_Percpective.theta;
		ar << m_Percpective.phi;
		ar << m_Percpective.d;
		ar << m_Percpective.with_perspective;
		ar << m_Percpective.dx;
		ar << m_Percpective.dy;
	}
	else
	{
		ar >> m_Percpective.O.x;
		ar >> m_Percpective.O.y;
		ar >> m_Percpective.O.z;
		ar >> m_Percpective.rho;
		ar >> m_Percpective.theta;
		ar >> m_Percpective.phi;
		ar >> m_Percpective.d;
		ar >> m_Percpective.with_perspective;
		ar >> m_Percpective.dx;
		ar >> m_Percpective.dy;

	}
	m_PtrPolygonList.Serialize(ar);
};

void C3DShape::Show(CDC *pDC)
{
	// Вывод всех полигонов
	POSITION Pos=NULL;
	if(m_PtrPolygonList.GetCount()>0)
		Pos=m_PtrPolygonList.GetHeadPosition();
	
	while(Pos!=NULL)
		m_PtrPolygonList.GetNext(Pos)->Show(pDC);
};


void C3DShape::GetRegion(CRgn &Rgn)
{
	// Конструируем  область захвата C3DShape,
	// в виде прямоугольника, охватывающего изображение 
	// фигуры на экране
	CRect Frame; // охватывающий прямоугольник
	POSITION Pos=NULL;
	int i=0;
	CPolygon *pPolygon=NULL;
	if(m_PtrPolygonList.GetCount()>0)
		Pos=m_PtrPolygonList.GetHeadPosition();
	// Инициализируем прямоугольник значениями первой точки первого полигона
	if(Pos!=NULL && (pPolygon=m_PtrPolygonList.GetAt(Pos))!=NULL && pPolygon->m_PointsArray.GetSize()>0)
	{
		Frame.left=Frame.right=pPolygon->m_PointsArray[0].x;
		Frame.top=Frame.bottom=pPolygon->m_PointsArray[0].y;
	}
	else return;
	// Получаем габариты фигуры	
	while(Pos!=NULL)
	{
		pPolygon=m_PtrPolygonList.GetNext(Pos);
		for(i=0; i<pPolygon->m_PointsArray.GetSize(); i++)
		{
			if(pPolygon->m_PointsArray[i].x<Frame.left) Frame.left=pPolygon->m_PointsArray[i].x;
			if(pPolygon->m_PointsArray[i].x>Frame.right) Frame.right=pPolygon->m_PointsArray[i].x;
			if(pPolygon->m_PointsArray[i].y>Frame.bottom) Frame.bottom=pPolygon->m_PointsArray[i].y;
			if(pPolygon->m_PointsArray[i].y<Frame.top) Frame.top=pPolygon->m_PointsArray[i].y;
		};
	}
	// Создаем область
	Rgn.CreateRectRgn(Frame.left, Frame.top, Frame.right, Frame.bottom);
}

	
void C3DShape::AddPolygon(C3DPolygon *pPolygon)
{
	m_PtrPolygonList.AddTail(pPolygon);	//добавили в список
	// расчет центра
	POSITION Pos=NULL;
	C3DPolygon* pCurPolygon=NULL;
	WORD Count=0, i=0;
	if(m_PtrPolygonList.GetCount()>0)
		Pos=m_PtrPolygonList.GetHeadPosition();
	while(Pos!=NULL)
	{
		pCurPolygon=(C3DPolygon*)m_PtrPolygonList.GetNext(Pos);
		for(i=0; i<pCurPolygon->m_3DPointsArray.GetSize(); i++)
		{
			m_Percpective.O.x+=pCurPolygon->m_3DPointsArray[i].x;	
			m_Percpective.O.y+=pCurPolygon->m_3DPointsArray[i].y;	
			m_Percpective.O.z+=pCurPolygon->m_3DPointsArray[i].z;	
		}
		Count+=i;
	}
	m_Percpective.O.x/=Count;
	m_Percpective.O.y/=Count;
	m_Percpective.O.z/=Count;
};


void C3DShape::MakeProjection()
{
	POSITION Pos=NULL;
	if(m_PtrPolygonList.GetCount()>0)
		Pos=m_PtrPolygonList.GetHeadPosition();
	while(Pos!=NULL)
		((C3DPolygon*)m_PtrPolygonList.GetNext(Pos))->MakeProjection(m_Percpective);
};

BOOL C3DShape::OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags, UINT nMyFlags)
{
	
	BOOL res=TRUE;
	if(nMyFlags & SHIFT_HOLD)
	switch(nChar)
	{
		case 38: m_Percpective.phi-=ROTATE_STEP; break;	//Up точка наблюдения выше
		case 40: m_Percpective.phi+=ROTATE_STEP; break;	//Down точка наблюдения ниже
		case 37: m_Percpective.theta-=ROTATE_STEP; break; //Left точка наблюдения левее
		case 39: m_Percpective.theta+=ROTATE_STEP; break; //Right точка наблюдения правее
		default: res=FALSE;
	}
	else
	if(nMyFlags & CTRL_HOLD)	 
	switch(nChar)
	{
		case 38: m_Percpective.d+=MOVE_STEP; break; //Up экран дальше
		case 40: m_Percpective.d-=MOVE_STEP; break; //Down экран ближе
		default: res=FALSE;
	}
	else
	{
		//перенос
		switch(nChar)
		{
			case 38:	m_Percpective.dy+= MOVE_STEP; break; // вверх
			case 40: 	m_Percpective.dy-= MOVE_STEP; break; // вниз
			case 37: 	m_Percpective.dx-= MOVE_STEP; break; // влево
			case 39:    m_Percpective.dx+= MOVE_STEP; break; // вправо
			// клавиша P вкл/выкл перспективные преобразования
			case 80:    m_Percpective.with_perspective=!m_Percpective.with_perspective;
						break; 
			default:	res=FALSE;
		}	
	}
	if(res)
		// Расчет проекции
		MakeProjection();
	return res;
};


/////////////////////////////////////////////////////////////////////////////////
// Глобальные функции для работы с поверхностями

int AddRsection(C3DShape *pShape, POINT3D *pSur, int x_size, int y_size, double level, COLORREF color)
{
	if(x_size<2 || y_size<2) return 0;
	// Полигон для временного хранения точек линии уровня
	C3DPolygon *pTempPolygon=new C3DPolygon();
	if(pTempPolygon==NULL) return 0; 
	// Разбиваем поверхность на треугольники и
	// пробуем найти пересечение для каждого треугольника и плоскости level.
	// Точки пересечения добавляем в pTempPolygon
	for(int x=0, y=0; y<y_size-1; y++)
		for(int x=0;  x<x_size-1; x++)
		{
			AddTriangleSection(pTempPolygon, &pSur[y*x_size+x], &pSur[(y+1)*x_size+x+1], &pSur[y*x_size+x+1], level);
			AddTriangleSection(pTempPolygon, &pSur[y*x_size+x], &pSur[(y+1)*x_size+x], &pSur[(y+1)*x_size+x+1], level);
		}
	// Из полученного набора точек создаем аккуратные полигончики
	// Для упрощения работы с точками получим ссылку на данные
	// Это конечно не лучшая иллюстрация принципов ООП, зато удобно :)
	CArray <POINT3D, POINT3D> &TempPointsArray=pTempPolygon->m_3DPointsArray;
	
	int pos=0, posmin=0;
	POINT3D EndSegPoint;
	double D=0, dcur=0, dmin=0; // расстояние между точками
	C3DPolygon *pSeg;
	BOOL fContinueSeg=TRUE; // флаг "продолжить текущий сегмент"
	// Вычисляем эталонное расстояние между точками - диагональ сетки на плоскости
	POINT3D P1=pSur[0], P2=pSur[x_size+1];	P1.z=P2.z=0;
	D=Dist(&P1, &P2);  
	// Пока во временном массиве осталась хотя бы пара точек
	// cсоздаем из массива сегменты сечения
	while(TempPointsArray.GetSize()-1>0)
	{
		// Новый сегмент - полигон
		pSeg=new C3DPolygon();	fContinueSeg=TRUE;
		if(pSeg==NULL) return 0;
		// Установим цвет
		pSeg->SetPen(color);
		// Первая точка-начало и конец сегмента
		pSeg->AddPoint(TempPointsArray[0]);
		EndSegPoint=TempPointsArray[0];
		// Удаляем точку из общего массива точек
		TempPointsArray.RemoveAt(0);
		// Продолжаем полигон
		while(fContinueSeg )
		{	
			posmin=0;
			dmin=D*2;
			// С начала массива
			// Выбираем ближайшую к концу сегмента точку 
			for(pos=0; pos<TempPointsArray.GetSize(); pos++)
			{
			  dcur=Dist(&EndSegPoint, &TempPointsArray[pos]);
			  if(dcur<dmin) 
			    {dmin=dcur; posmin=pos;}//запоминаем позицию(номер) ближайшей точки
			}
			if(dmin<=D) //расстояние до ближайшей точки меньше эталонного,
			{	
				//но все-таки точка не совпадает с концом сегмента,
				//поэтому добавим ее в сегмент
				if(dmin>D/1000) 
				{
					//Ближайшую точу в сегмент
					pSeg->AddPoint(TempPointsArray[posmin]);
					//Новая точка становиться концом сегмента
					EndSegPoint=TempPointsArray[posmin];
				}

				//Удаляем эту точку
				TempPointsArray.RemoveAt(posmin);
			}
			else //не нашли близкой к концу точки- закрываем сегмент
				fContinueSeg=FALSE;
		} ;
		//Проверим, может стоит замкнуть сегмент
		if(pSeg->m_3DPointsArray.GetSize()>2)
			if(Dist(&pSeg->m_3DPointsArray[0], &pSeg->m_3DPointsArray[pSeg->m_3DPointsArray.GetSize()-1])<D)
				pSeg->AddPoint(pSeg->m_3DPointsArray[0]);
		
			
		//Добавляем полигон в фигуру 
		pShape->AddPolygon(pSeg);
	} 	
	//Временный полигон нам больше не нужен
	delete pTempPolygon;
	return 1;
}



void AddTriangleSection(C3DPolygon *p3DPolygon, POINT3D *pP1, POINT3D *pP2, POINT3D *pP3, double level)
{
	int  f1,f2,f3;
	double x1,x2,x3,y1,y2,y3;
	POINT3D P1, P2;
	if(	!((pP1->z==level)&&(pP2->z==level)&&(pP3->z==level)) && //треугольник в плоскости
   		!((pP1->z>level)&&(pP2->z>level)&&(pP3->z>level)) &&   //треугольник и плоскость не пересекаются
		!((pP1->z<level)&&(pP2->z<level)&&(pP3->z<level)) )	   //треугольник и плоскость не пересекаются

   	if((pP1->z==level)&&(pP2->z==level))	//сторона в плоскости - добавляем
   	{
		p3DPolygon->AddPoint(*pP1);
		p3DPolygon->AddPoint(*pP2);
   	}
	else
		if((pP2->z==level)&&(pP3->z==level)) //сторона в плоскости - добавляем
   		{ 
   			p3DPolygon->AddPoint(*pP2);
			p3DPolygon->AddPoint(*pP3);
		}
   		else
   			if((pP3->z==level)&&(pP1->z==level)) //сторона в плоскости - добавляем
   		    { 
	   			p3DPolygon->AddPoint(*pP3);
				p3DPolygon->AddPoint(*pP1);
			}
   			else
   			{	// Находим 	пересечение каждой стороны треугольника с плоскостью
				 f1=CutCross(level,pP1, pP2, x1, y1); 
				 f2=CutCross(level,pP2, pP3, x2, y2);
				 f3=CutCross(level,pP3, pP1, x3, y3);
				 if(f1&&f2) 
				 { 
					P1.x=x1; P1.y=y1; P1.z=level; 
					P2.x=x2; P2.y=y2; P2.z=level; 
					p3DPolygon->AddPoint(P1);
					p3DPolygon->AddPoint(P2);
			     }
				 if(f2&&f3)
				 { 
					P1.x=x2; P1.y=y2; P1.z=level; 
					P2.x=x3; P2.y=y3; P2.z=level; 
					p3DPolygon->AddPoint(P1);
					p3DPolygon->AddPoint(P2);
				 }
				 if(f1&&f3)
				 { 
					P1.x=x1; P1.y=y1; P1.z=level; 
					P2.x=x3; P2.y=y3; P2.z=level; 
					p3DPolygon->AddPoint(P1);
					p3DPolygon->AddPoint(P2);
				 }
   }//~else
}

int CutCross(double level, POINT3D *pP1, POINT3D *pP2, double &x, double &y)
{ if( (pP1->z<level && pP2->z<level) || //отрезок под плоскостью level
      (pP1->z>level && pP2->z>level) ||	//отрезок над плоскостью level
	  (pP1->z==pP2->z)  ) 	 //отрезок в плоскости level
		{x=pP1->x; y=pP1->y; return 0;} 
  else
    {
	 x=pP2->x-(pP1->x-pP2->x)*(level-pP2->z)/(pP2->z-pP1->z);
	 y=pP2->y-(pP1->y-pP2->y)*(level-pP2->z)/(pP2->z-pP1->z);
	 return 1;
	}
}

double Dist(POINT3D *pP1, POINT3D* pP2)
{
	if(pP1==NULL||pP2==NULL) return 0;
	return sqrt(pow(pP1->x-pP2->x, 2)+pow(pP1->y-pP2->y, 2)+pow(pP1->z-pP2->z, 2));
};


