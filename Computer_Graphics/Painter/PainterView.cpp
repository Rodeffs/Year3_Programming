// PainterView.cpp : implementation of the CPainterView class
//

#include "stdafx.h"
#include "Painter.h"

#include "PainterDoc.h"
#include "PainterView.h"
#include "Shapes.h"
#include "Savebmp.h"
#include "Global.h"
#include <math.h>

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CPainterView

IMPLEMENT_DYNCREATE(CPainterView, CScrollView)

BEGIN_MESSAGE_MAP(CPainterView, CScrollView)
	//{{AFX_MSG_MAP(CPainterView)
	ON_WM_LBUTTONDOWN()
	ON_WM_ERASEBKGND()
	ON_COMMAND(ID_EDIT_ADDSHAPE_POINT, OnEditAddshapePoint)
	ON_COMMAND(ID_EDIT_ADDSHAPE_CIRCLE, OnEditAddshapeCircle)
	ON_COMMAND(ID_EDIT_ADDSHAPE_SQUARE, OnEditAddshapeSquare)

	// My code
	ON_COMMAND(ID_EDIT_ADDSHAPE_SECTOR, OnEditAddshapeSector)

	ON_COMMAND(ID_EDIT_SELECT, OnEditSelect)
	ON_WM_LBUTTONUP()
	ON_WM_MOUSEMOVE()
	ON_COMMAND(ID_EDIT_ADDSHAPE_POLYLINE, OnEditAddshapePolyline)
	ON_COMMAND(ID_EDIT_ADDSHAPE_POLYGON, OnEditAddshapePolygon)
	ON_WM_LBUTTONDBLCLK()
	ON_WM_KEYDOWN()
	ON_WM_KEYUP()
	ON_COMMAND(ID_EDIT_CHANGEORDER_TOP, OnEditChangeorderTop)
	ON_COMMAND(ID_EDIT_CHANGEORDER_STEPUP, OnEditChangeorderStepup)
	ON_COMMAND(ID_EDIT_CHANGEORDER_STEPDOWN, OnEditChangeorderStepdown)
	ON_COMMAND(ID_EDIT_CHANGEORDER_BOTTOM, OnEditChangeorderBottom)
	ON_COMMAND(ID_EDIT_DELETE, OnEditDelete)
	ON_COMMAND(ID_EDIT_ADDSHAPE_SURFACE, OnEditAddshapeSurface)
	//}}AFX_MSG_MAP
	// Standard printing commands
	ON_COMMAND(ID_FILE_PRINT, CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_DIRECT, CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_PREVIEW, CView::OnFilePrintPreview)
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CPainterView construction/destruction

CPainterView::CPainterView()
{
	// TODO: add construction code here
	m_CurOper=OP_NOOPER;
	m_nMyFlags=0;

	m_hcurCircle=AfxGetApp()->LoadCursor(IDC_CURSOR_CIRCLE);
	m_hcurSquare=AfxGetApp()->LoadCursor(IDC_CURSOR_SQUARE);
	m_hcurPolygon=AfxGetApp()->LoadCursor(IDC_CURSOR_POLYGON);
	m_hcurSurface=AfxGetApp()->LoadCursor(IDC_CURSOR_SURFACE);
	m_hcurSector = AfxGetApp()->LoadCursor(IDC_CURSOR_CIRCLE);
}

CPainterView::~CPainterView()
{
}

BOOL CPainterView::PreCreateWindow(CREATESTRUCT& cs)
{
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	return CView::PreCreateWindow(cs);
}

/////////////////////////////////////////////////////////////////////////////
// CPainterView drawing

void CPainterView::OnDraw(CDC* pDC)
{
	CPainterDoc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	// TODO: add draw code for native data here
	
	// Выводим все фигуры, хранящиеся в списке
	POSITION pos=NULL;
	CBasePoint* pShape=NULL;
	// Если в списке есть объекты
	if(pDoc->m_ShapesList.GetCount()>0)
		// Получим позицию первого объекта
		pos=pDoc->m_ShapesList.GetHeadPosition(); 
	while(pos!=NULL)
	{
		// Получим указатель на первый объект
		pShape=pDoc->m_ShapesList.GetNext(pos);
		// Нарисуем объект
		if(pShape!=NULL) pShape->Show(pDC);
	}
	// Выделяем активную фигуру
	if(m_CurOper==OP_SELECT)	MarkSelectedShape(pDC);
}

void CPainterView::DrawMoveLine(CPoint first_point, CPoint second_point)
{
	// Получим доступ к контексту устройства
	CClientDC dc(this);
	// Подготовим контекст устройства 
	OnPrepareDC(&dc); 	
	// Установим режим рисования инверсным цветом
	int OldMode=dc.SetROP2(R2_NOT);
	// Рисуем прямую между двумя точками
   	dc.MoveTo(first_point);	dc.LineTo(second_point);
	// Восстанавливаем прежний режим рисования
	dc.SetROP2(OldMode);
}

/////////////////////////////////////////////////////////////////////////////
// CPainterView printing

BOOL CPainterView::OnPreparePrinting(CPrintInfo* pInfo)
{
	return DoPreparePrinting(pInfo);
}

void CPainterView::OnBeginPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: add extra initialization before printing
}

void CPainterView::OnEndPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: add cleanup after printing
}

/////////////////////////////////////////////////////////////////////////////
// CPainterView diagnostics

#ifdef _DEBUG
void CPainterView::AssertValid() const
{
	CView::AssertValid();
}

void CPainterView::Dump(CDumpContext& dc) const
{
	CView::Dump(dc);
}

CPainterDoc* CPainterView::GetDocument() // non-debug version is inline
{
	ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(CPainterDoc)));
	return (CPainterDoc*)m_pDocument;
}
#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CPainterView message handlers

void CPainterView::OnLButtonDown(UINT nFlags, CPoint point) 
{
	// Получили указатель на объект-документ
	CPainterDoc *pDoc=GetDocument();
	CPoint	LogPoint=point;
	
	// Получим контекст устройства, на котором рисуем
	CDC *pDC=GetDC();
	// Подготовим контекст устройства 
	OnPrepareDC(pDC); 
	
	// Переведем физические координаты точки в логические
	pDC->DPtoLP(&LogPoint);
	// Освободим контекст устройства
	ReleaseDC(pDC);
	
	// Запоминаем точку
	m_CurMovePoint=m_FirstPoint=LogPoint;
	switch(m_CurOper)
	{
		case OP_LINE:
			// Последним в списке должен быть полигон
			((CPolygon*)pDoc->m_ShapesList.GetTail())->m_PointsArray.Add(LogPoint);
			// Указываем, что окно надо перерисовать
			Invalidate();
		break;
	}
	
	// Даем возможность стандартному обработчику
	// тоже поработать над этим сообщением
	
	CScrollView::OnLButtonDown(nFlags, point);
}

void CPainterView::OnLButtonUp(UINT nFlags, CPoint point) 
{
	// Получили указатель на объект-документ
	CPainterDoc *pDoc=GetDocument();
	CPoint	LogPoint=point;
	
	// Получим контекст устройства, на котором рисуем
	CDC *pDC=GetDC();
	// Подготовим контекст устройства метод базового класса
	OnPrepareDC(pDC); 
	
	// Переведем физические координаты точки в логические
	pDC->DPtoLP(&LogPoint);
	// Освободим контекст устройства
	ReleaseDC(pDC);
	switch(m_CurOper)
	{
	case OP_POINT:
	case OP_CIRCLE:
	case OP_SQUARE:
	case OP_SURFACE:
	case OP_SECTOR:
		AddShape(m_CurOper, m_FirstPoint, LogPoint);
		// Указываем, что окно надо перерисовать
		Invalidate();
	break;
	case OP_SELECT:
		pDoc->SelectShape(LogPoint);
		// Указываем, что окно надо перерисовать
		Invalidate();
	break;
	}

	// Даем возможность стандартному обработчику
	// тоже поработать над этим сообщением
	CScrollView::OnLButtonUp(nFlags, point);
}

void CPainterView::OnMouseMove(UINT nFlags, CPoint point) 
{
	// Получили указатель на объект-документ
	CPainterDoc *pDoc=GetDocument();
	CPoint	LogPoint=point;
	
	// Получим контекст устройства, на котором рисуем
	CDC *pDC=GetDC();
	// Подготовим контекст устройства метод базового класса
	OnPrepareDC(pDC); 
	
	// Переведем физические координаты точки в логические
	pDC->DPtoLP(&LogPoint);
	// Освободим контекст устройства
	ReleaseDC(pDC);
	
	switch(m_CurOper)
	{
		case OP_LINE:
			if(((CPolygon*)pDoc->m_ShapesList.GetTail())->
				m_PointsArray.GetSize()<=0) break;
			DrawMoveLine(m_FirstPoint, m_CurMovePoint);
			m_CurMovePoint=LogPoint;
			DrawMoveLine(m_FirstPoint, m_CurMovePoint);
		break;
		case OP_POINT:
		case OP_CIRCLE:
		case OP_SQUARE:
		case OP_SECTOR:
		case OP_SURFACE:
			if(nFlags==MK_LBUTTON) DrawMoveLine(m_FirstPoint, m_CurMovePoint);
			m_CurMovePoint=LogPoint;
			if(nFlags==MK_LBUTTON) DrawMoveLine(m_FirstPoint, m_CurMovePoint);
		break;
		default:
			::SetClassLong(GetSafeHwnd(), GCL_HCURSOR, (LONG)m_hcurDefault);
	}
	/* Для динамического изменения формы курсора можно использовать эту конструкцию
	//
	// Изменение формы курсора
	// Для того чтобы предотвратить мигание курсора,
	// установим "пустой" курсор по умолчанию
	::SetClassLong(GetSafeHwnd(), GCL_HCURSOR, NULL);
	// Установим курсор, соответствующий выполняемой операции 
	switch(m_CurOper)
	{
	case OP_CIRCLE:
		SetCursor(m_hcurCircle);
		break;
	case OP_SQUARE:
		SetCursor(m_hcurSquare);
		break;
	case OP_LINE:
		SetCursor(m_hcurPolygon);
		break;
	case OP_SURFACE:
		SetCursor(m_hcurSurface);
		break;
	default:
		::SetClassLong(GetSafeHwnd(), GCL_HCURSOR, (LONG)m_hcurDefault);
	}
	*/
	CScrollView::OnMouseMove(nFlags, point);
}
void CPainterView::OnLButtonDblClk(UINT nFlags, CPoint point) 
{
	switch(m_CurOper)
	{
	case OP_LINE:
		m_CurOper=OP_NOOPER;
	break;
	}
	CScrollView::OnLButtonDblClk(nFlags, point);
}

void CPainterView::OnUpdate(CView* pSender, LPARAM lHint, CObject* pHint) 
{
	// TODO: Add your specialized code here and/or call the base class
	// Получили указатель на объект-документ
	CPainterDoc *pDoc=GetDocument();
	CSize sizeTotal;
	// Ширина
	sizeTotal.cx = pDoc->m_wSheet_Width;
	// Высота
	sizeTotal.cy = pDoc->m_wSheet_Height;
	// Установим режим и размер листа
	SetScrollSizes(pDoc->m_wMap_Mode, sizeTotal);
	// Вызываем метод базаового класса
	CScrollView::OnUpdate(pSender, lHint, pHint); 
}

void CPainterView::OnPrepareDC(CDC* pDC, CPrintInfo* pInfo) 
{
	// Вызов метода базового класса
	CScrollView::OnPrepareDC(pDC, pInfo);
	// Получим указатель на документ
	CPainterDoc *pDoc=GetDocument();
	// Создадим точку в левом нижнем углу листа
	CPoint OriginPoint(0, -pDoc->m_wSheet_Height);
	// Переведем точку в координаты физического устройства
	pDC->LPtoDP(&OriginPoint); 
	// Установим эту точку в качестве начала координат физического устройства
	pDC->SetViewportOrg(OriginPoint);
	// Ограничим область доступную для рисования
	pDC->IntersectClipRect( 0,0, pDoc->m_wSheet_Width, pDoc->m_wSheet_Height);

}

BOOL CPainterView::OnEraseBkgnd(CDC* pDC) 
{
	// Вызвали метод базового класса   
    BOOL Res=CScrollView::OnEraseBkgnd(pDC);
	// Создали кисть серого цвета
	CBrush br( GetSysColor( COLOR_GRAYTEXT ) ); 
	// Выполнили заливку неиспользуемой области окна
    FillOutsideRect( pDC, &br );
	return Res;
}


void CPainterView::AddShape(int shape, CPoint first_point, CPoint second_point) 
{
	CPainterDoc *pDoc=GetDocument();
	CBasePoint *pShape=NULL;
	// Рассчет размера
	int size=0;
	size=(int) floor( sqrt((double)(second_point.x-first_point.x)*(second_point.x-first_point.x)+
				(second_point.y-first_point.y)*(second_point.y-first_point.y)) +0.5);

	switch(shape)
	{
	case OP_LINE:
	break;
	case OP_POINT:
		// Создаем объект - точку
		pShape=new CBasePoint(second_point.x, second_point.y, 100);
		// Светло-серая заливка
		pShape->SetBrush(RGB(200,200,200));
	break;
	case OP_CIRCLE:
		// Создаем объект - круг
		pShape=new CBasePoint(first_point.x, first_point.y, size);
		// Черная линия шириной 2 мм
		pShape->SetPen(RGB(0,0,0), 200, PS_GEOMETRIC);
		// Темно-серая заливка
		pShape->SetBrush(RGB(100,100,100));
	break;
	case OP_SQUARE:
		// Создаем объект - квадрат
		pShape=new CSquare(first_point.x, first_point.y, size*2);
		// Красная линия шириной 1 мм
		pShape->SetPen(RGB(200,0,0), 100, PS_GEOMETRIC);
		// Темно-серая диагональная штриховка
		pShape->SetBrush(RGB(100,100,100),0,HS_DIAGCROSS);
	break;
	case OP_SECTOR:
		// My code

		pShape = new CSector(first_point.x, first_point.y, size);
		pShape->SetPen(RGB(0, 0, 0), 1, PS_GEOMETRIC);
		pShape->SetBrush(RGB(0, 255, 0));
	break;
	case OP_SURFACE:
		// Создаем объект - поверхность
		pShape=AddSurface(first_point, size);
	break;
	}
	if(pShape!=NULL) // создали фигуру
	{
		// Добавляем в конец списка
		pDoc->m_ShapesList.AddTail(pShape);
		// Последняя фигура становится активной
		pDoc->m_pSelShape=pShape;
		// Указываем, что документ изменен
		pDoc->SetModifiedFlag();
	}
}

void CPainterView::OnEditAddshapePoint() 
{
	m_CurOper=OP_POINT;
	::SetClassLong(GetSafeHwnd(), GCL_HCURSOR, (LONG)m_hcurCircle);
}

void CPainterView::OnEditAddshapeCircle() 
{
	m_CurOper=OP_CIRCLE;
	::SetClassLong(GetSafeHwnd(), GCL_HCURSOR, (LONG)m_hcurCircle);
}

void CPainterView::OnEditAddshapeSquare() 
{
	m_CurOper=OP_SQUARE;
	::SetClassLong(GetSafeHwnd(), GCL_HCURSOR, (LONG)m_hcurSquare);
}

// My code
void CPainterView::OnEditAddshapeSector()
{
	m_CurOper = OP_SECTOR;
	::SetClassLong(GetSafeHwnd(), GCL_HCURSOR, (LONG)m_hcurSector);
}

void CPainterView::OnEditAddshapePolyline() 
{
	CBasePoint *pShape=new CPolygon;
	// Черная линия шириной 0.5 мм
	pShape->SetPen(RGB(0,0,0), 50, PS_GEOMETRIC);
	
	CPainterDoc *pDoc=GetDocument();
	// Добавляем в конец списка
	pDoc->m_ShapesList.AddTail(pShape);
	// Последняя фигура становится активной
	pDoc->m_pSelShape=pShape;
	// Указываем, что документ изменен
	pDoc->SetModifiedFlag();

	m_CurOper=OP_LINE;
	::SetClassLong(GetSafeHwnd(), GCL_HCURSOR, (LONG)m_hcurPolygon);
}

void CPainterView::OnEditAddshapePolygon() 
{
	CBasePoint *pShape=new CPolygon;
	// Темно-зеленая заливка
	pShape->SetBrush(RGB(0,100,0));
	// Черная линия шириной 0.5 мм
	pShape->SetPen(RGB(0,0,0), 50, PS_GEOMETRIC);

	// Так как pShape указатель на CBasePoint,
	// а метод SetPolygon() имеется только у класса CPolygon,
	// требуется преобразование типа указателя
	((CPolygon*)pShape)->SetPolygon(TRUE);

	CPainterDoc *pDoc=GetDocument();
	// Добавляем в конец списка
	pDoc->m_ShapesList.AddTail(pShape);
	// Последняя фигура становится активной
	pDoc->m_pSelShape=pShape;
	// Указываем, что документ изменен
	pDoc->SetModifiedFlag();
	
	m_CurOper=OP_LINE;
	::SetClassLong(GetSafeHwnd(), GCL_HCURSOR, (LONG)m_hcurPolygon);
}

void CPainterView::OnEditAddshapeSurface() 
{
	m_CurOper=OP_SURFACE;
	::SetClassLong(GetSafeHwnd(), GCL_HCURSOR, (LONG)m_hcurSurface);
}

const int _GRID_DENSITY=30;
const int _LEVELS_DENSITY=5;
CBasePoint* CPainterView::AddSurface(CPoint first_point, int size)
{
	C3DShape *pShape=NULL;
	pShape=new C3DShape();
	
	// Рассчитываем поверхность в заданной области
	// dx, dy - шаг сетки
	double	dx=(double)size*2/_GRID_DENSITY,
			dy=(double)size*2/_GRID_DENSITY;
	// Массив точек поверхности используется для временного хранения
	POINT3D point3d[_GRID_DENSITY*_GRID_DENSITY];
	

	// Создаем 3D объект - поверхность, как набор 3D полигонов
	C3DPolygon *p3DPolygon=NULL;
	// Добавляем "проволочки" вдоль оси Y 
	for(int i=0, j=0; i<_GRID_DENSITY; i++)
	{
		p3DPolygon=new C3DPolygon();
		for(j=0; j<_GRID_DENSITY; j++)
		{
			point3d[j*_GRID_DENSITY+i].x=first_point.x+dx*i - size;
			point3d[j*_GRID_DENSITY+i].y=first_point.y+dy*j - size;
			point3d[j*_GRID_DENSITY+i].z=ZFunction(	fabs(first_point.x-point3d[j*_GRID_DENSITY+i].x),
													fabs(first_point.y-point3d[j*_GRID_DENSITY+i].y));
			p3DPolygon->AddPoint(point3d[j*_GRID_DENSITY+i]);
		}
		pShape->AddPolygon(p3DPolygon);
	}
	double minz=point3d[0].z, maxz=point3d[0].z;
	// Добавляем "проволочки" вдоль оси X 
	for(int j=0; j<_GRID_DENSITY; j++)
	{
		p3DPolygon=new C3DPolygon();
		for(int i=0; i<_GRID_DENSITY; i++)
		{
			p3DPolygon->AddPoint(point3d[j*_GRID_DENSITY+i]);
			// Определяем пределы изменения Z 
			if(point3d[j*_GRID_DENSITY+i].z<minz) minz=point3d[j*_GRID_DENSITY+i].z; 
			if(point3d[j*_GRID_DENSITY+i].z>maxz) maxz=point3d[j*_GRID_DENSITY+i].z; 
		}
		pShape->AddPolygon(p3DPolygon);
	}

	// Строим линии уровня
	double l_step=(maxz-minz)/_LEVELS_DENSITY;
	int color_step=200/_LEVELS_DENSITY; //изменение цвета
	for(int i=0; i<_LEVELS_DENSITY; i++)
		AddRsection(pShape, point3d, _GRID_DENSITY, _GRID_DENSITY,
					minz + l_step/2 + l_step*i, RGB(0,0, 55+color_step*i));
			
	// Рассчитать проекцию на экран
	pShape->MakeProjection();
	return pShape;
};


void CPainterView::OnEditSelect() 
{
	m_CurOper=OP_SELECT;
}

void CPainterView::MarkSelectedShape(CDC *pDC)
{
	CPainterDoc *pDoc=GetDocument();
	CRgn Rgn;
	if(pDoc->m_pSelShape==NULL) return;

	pDoc->m_pSelShape->GetRegion(Rgn);
	// Пробуем получить прямоугольник, описывающий фигуру
	CRect Rect;
	int res=Rgn.GetRgnBox(&Rect);
	if(res!= ERROR && res!=NULLREGION)
		pDC-> InvertRect(&Rect);
}

void CPainterView::OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags) 
{
	CPainterDoc *pDoc=GetDocument();
	BOOL modified=FALSE;

	if(pDoc->m_pSelShape!=NULL)
		modified=pDoc->m_pSelShape->OnKeyDown(nChar, nRepCnt, nFlags, m_nMyFlags);
		
	switch(nChar)
	{
		case 16: m_nMyFlags=m_nMyFlags|SHIFT_HOLD; break; // Shift
		case 17: m_nMyFlags=m_nMyFlags|CTRL_HOLD; break; // Ctrl
	}	
		
	if(modified)
	{
		// Указываем, что документ изменен
		pDoc->SetModifiedFlag();
		// Указываем, что окно надо перерисовать
		Invalidate();
	}
	CScrollView::OnKeyDown(nChar, nRepCnt, nFlags);
}

void CPainterView::OnKeyUp(UINT nChar, UINT nRepCnt, UINT nFlags) 
{
	// TODO: Add your message handler code here and/or call default
	switch(nChar)
	{
		case 16: m_nMyFlags=m_nMyFlags^SHIFT_HOLD;	break; // Shift
		case 17: m_nMyFlags=m_nMyFlags^CTRL_HOLD;	break; // Ctrl
	}	
	CScrollView::OnKeyUp(nChar, nRepCnt, nFlags);
}


void CPainterView::OnEditChangeorderTop() 
{
	CPainterDoc *pDoc=GetDocument();
	if(pDoc->ChangeOrder(TOP))
	{
		// Указываем, что документ изменен
		pDoc->SetModifiedFlag();
		// Указываем, что окно надо перерисовать
		Invalidate();
	}
}

void CPainterView::OnEditChangeorderStepup() 
{
	CPainterDoc *pDoc=GetDocument();
	if(pDoc->ChangeOrder(STEPUP))
	{
		// Указываем, что документ изменен
		pDoc->SetModifiedFlag();
		// Указываем, что окно надо перерисовать
		Invalidate();
	}
}

void CPainterView::OnEditChangeorderStepdown() 
{
	CPainterDoc *pDoc=GetDocument();
	if(pDoc->ChangeOrder(STEPDOWN))
	{
		// Указываем, что документ изменен
		pDoc->SetModifiedFlag();
		// Указываем, что окно надо перерисовать
		Invalidate();
	}
}

void CPainterView::OnEditChangeorderBottom() 
{
	CPainterDoc *pDoc=GetDocument();
	if(pDoc->ChangeOrder(BOTTOM))
	{
		// Указываем, что документ изменен
		pDoc->SetModifiedFlag();
		// Указываем, что окно надо перерисовать
		Invalidate();
	}
}

void CPainterView::OnEditDelete() 
{
	// TODO: Add your command handler code here
	CPainterDoc *pDoc=GetDocument();
	if(pDoc->DeleteSelected())
	{
		// Указываем, что документ изменен
		pDoc->SetModifiedFlag();
		// Указываем, что окно надо перерисовать
		Invalidate();
	}
}
/*
int CPainterView::OnCreate(LPCREATESTRUCT lpCreateStruct) 
{
	if (CScrollView::OnCreate(lpCreateStruct) == -1)
		return -1;
	
	m_hcurDefault=(HCURSOR)::GetClassLong(GetSafeHwnd(), GCL_HCURSOR);
	return 0;
}
*/
void CPainterView::SaveBMP(CString &FileName)
{
	// Получим контекст устройства, на котором рисуем
	CDC *pwDC=GetDC();
	// Подготовим контекст устройства 
	OnPrepareDC(pwDC); 

	// Запомним прежнюю позицию прокрутки
	CPoint ScrollPos=GetScrollPosition();
	// Установим позицию прокрутки в начало, чтобы нарисовалась вся картинка
	ScrollToPosition(CPoint(0,0));

	
	// Контекст устройства для памяти, в которую будет происходить вывод
	CDC MemDC; 
	// Создадим контекст устройства совместимый с экраном
	MemDC.CreateCompatibleDC(pwDC);
	// Подготовим контекст.
	// Этот метод установит режим отображения, в котором мы работаем.
	OnPrepareDC(&MemDC); 
	
	// Узнаем логические и физические размеры рисунка
	// Получили указатель на объект-документ
	CPainterDoc *pDoc=GetDocument();
	CSize	SizeTotal,	// это логический размер
			SizeBMP;	// это физический размер	
	SizeTotal.cx = pDoc->m_wSheet_Width; // ширина
	SizeTotal.cy = pDoc->m_wSheet_Height; // высота
	SizeBMP=SizeTotal;
	MemDC.LPtoDP(&SizeBMP); // перевод логического размера в физический

	// Создадим растровою "заготовку", на которой будем рисовать
	CBitmap BMP;
	BMP.CreateCompatibleBitmap(pwDC, SizeBMP.cx, SizeBMP.cy);
	// Установим заготовку в контекст памяти
	MemDC.SelectObject(&BMP);
 
	// Белый фон
	CBrush brush;
	CBrush *pBrushOld;
	if(brush.CreateSolidBrush(RGB(255,255,255)))
	{
 		pBrushOld=MemDC.SelectObject(&brush);
 		MemDC.PatBlt(0, 0, SizeTotal.cx, SizeTotal.cy, PATCOPY);
		MemDC.SelectObject(pBrushOld);
	}

	// Вывод рисунка в контекст памяти
	OnDraw(&MemDC);
 
	// Теперь запишем полученную растровую картинку в файл
	SaveBitmapToBMPFile(FileName, BMP, MemDC);
	
	// Контекст экрана больше не нужен
	ReleaseDC(pwDC);
	// Вернем позицию прокрутки
	ScrollToPosition(ScrollPos);
}

void CPainterView::OnSaveBmp() 
{
	CPainterDoc *pDoc=GetDocument();
	// Из названия картинки формируем имя файла
	CString FileName=pDoc->GetTitle();
	if(FileName.ReverseFind('.')>-1)
		FileName=FileName.Left(FileName.ReverseFind('.'));
	// Фильтр файлов
	CString Filter=_T("BMP File (*.bmp)|*.bmp|All Files (*.*)|*.*||");
	CString DefExt=_T("BMP");
	CFileDialog SaveDlg(FALSE, (LPCTSTR)DefExt, (LPCTSTR)FileName,
						OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT,
						(LPCTSTR)Filter, this);
	if(SaveDlg.DoModal()==IDCANCEL) return;
	SaveBMP(SaveDlg.GetPathName());
}