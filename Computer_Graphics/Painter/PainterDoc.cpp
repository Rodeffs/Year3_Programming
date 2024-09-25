// PainterDoc.cpp : implementation of the CPainterDoc class
//

#include "stdafx.h"
#include "Painter.h"

#include "PainterDoc.h"
#include "PainterView.h"
#include "PagePropertyDlg.h"
#include "Shapes.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CPainterDoc

IMPLEMENT_DYNCREATE(CPainterDoc, CDocument)

BEGIN_MESSAGE_MAP(CPainterDoc, CDocument)
	//{{AFX_MSG_MAP(CPainterDoc)
	ON_COMMAND(ID_FILE_PAGEPROPERTY, OnFilePageproperty)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CPainterDoc construction/destruction

CPainterDoc::CPainterDoc()
{
	// Режим отображения 1 лог. ед. = 0.01 мм
	m_wMap_Mode = MM_HIMETRIC;
	// Размер листа формата А4
	m_wSheet_Width = 21000;
	m_wSheet_Height = 29700;
	// Нет выбранной фигуры
	m_pSelShape=NULL;
}

CPainterDoc::~CPainterDoc()
{
	// Очистили список фигур
	ClearShapesList();
}

BOOL CPainterDoc::OnNewDocument()
{
	if (!CDocument::OnNewDocument())
		return FALSE;

	// TODO: add reinitialization code here
	// (SDI documents will reuse this document)
	
	// Нет выбранной фигуры
	m_pSelShape=NULL;

	// Очистили список фигур
	ClearShapesList();
	// Перерисовали
	UpdateAllViews(NULL);

	return TRUE;
}



/////////////////////////////////////////////////////////////////////////////
// CPainterDoc serialization

void CPainterDoc::Serialize(CArchive& ar)
{
	CString version;
	// Количество точек
	WORD Index=0, i=0, version_n=0; 
	CPoint point;

	CBasePoint *pPolygon=NULL; 
	if (ar.IsStoring()) // сохнаняем 
	{
		// Версию формата наших рисунков
		version_n=3;
		version.Format(_T("pr%d"), version_n);
		ar << version;
		// Режим отображения 
		ar << m_wMap_Mode;
		// Размер листа 
		ar << m_wSheet_Width;
		ar << m_wSheet_Height;
	}
	else // загружаем
	{
		// Версию формата
		ar >> version;
		//
		version_n=atoi((LPCSTR)(LPCTSTR)version.Right(1));
		switch(version_n) // в зависимости от версии формата 
		{
			case 2:
				pPolygon=new CPolygon;
				pPolygon->SetPen(RGB(0,0,0), 50, PS_GEOMETRIC);
				ar >> Index;
				// Загружаем значения координат точек
				for(i=0; i<Index; i++)
				{
					ar >> point;
					((CPolygon*)pPolygon)->m_PointsArray.Add(point);
				}
			case 3:
				// Режим отображения 
				ar >> m_wMap_Mode;
				// Размер листа 
				ar >> m_wSheet_Width;
				ar >> m_wSheet_Height;
				break;
			default: 
				AfxMessageBox(_T("Неизвестный формат"), MB_OK);
				return;
		}//switch(version)
	}
	
	// Выполняем сериализацию списка фигур
	m_ShapesList.Serialize(ar); 
	// Добавляем объект-полигон в голову списка
	if(pPolygon!=NULL)
		m_ShapesList.AddHead(pPolygon);
}



/////////////////////////////////////////////////////////////////////////////
// CPainterDoc diagnostics

#ifdef _DEBUG
void CPainterDoc::AssertValid() const
{
	CDocument::AssertValid();
}

void CPainterDoc::Dump(CDumpContext& dc) const
{
	CDocument::Dump(dc);
}
#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CPainterDoc commands


void CPainterDoc::OnFilePageproperty() 
{
	// TODO: Add your command handler code here
	//создаем объект - Диалог свойств листа
	CPagePropertyDlg PPDlg;
	//инициализируем параметры диалога текущими значениями
	//делим на 100, т.к. в диалоге размеры в мм
	PPDlg.m_uWidth=m_wSheet_Width/100;
	PPDlg.m_uHeight=m_wSheet_Height/100;
	//вызываем диалог
	if(PPDlg.DoModal()==IDOK)
	{	//запоминаем новые значения
		//умножаем на 100, т.к. 1 лог. ед. = 0.01 мм 
		m_wSheet_Width=PPDlg.m_uWidth*100;
		m_wSheet_Height=PPDlg.m_uHeight*100;
		//обновляем облик
		UpdateAllViews(NULL);
	}
	
}

void CPainterDoc::ClearShapesList()
{
	// Очистили список объектов
	POSITION pos=NULL;
	while(m_ShapesList.GetCount()>0) //пока в списке есть фигуры
		delete m_ShapesList.RemoveHead();//удаляем первую из них
}

CBasePoint* CPainterDoc::SelectShape(CPoint point)
{
	// Объект-область
	CRgn Rgn;
	// Указатель на элемент списка
	POSITION pos=NULL;
	// Начиная с хвоста списка
	if(m_ShapesList.GetCount()>0) pos=m_ShapesList.GetTailPosition();
	// проверим попадает ли точка point в какю-либо из фигур
	while(pos!=NULL) 
	{
		m_pSelShape=m_ShapesList.GetPrev(pos);
		// Очистим объект - область
		Rgn.DeleteObject();
		m_pSelShape->GetRegion(Rgn);
		// Точка попадает в фигуру - возвращаем указатель на фигуру
		if(Rgn.PtInRegion(point) ) return m_pSelShape;
	}
	// Если добрались до этого места, значит, не попали ни в какую фигуру
	return (m_pSelShape=NULL);
};

BOOL CPainterDoc::ChangeOrder(int code)
{
	if(m_pSelShape==NULL) return FALSE;
	CBasePoint *pShape=NULL;
	// Указатель на елемент списка
	POSITION pos=NULL, pastpos=NULL;
	// Начнем поиск с хвоста списка
	if(m_ShapesList.GetCount()>0) pos=m_ShapesList.GetTailPosition();
	// Найдем позицию объекта в списке
	while(pos!=NULL) 
	{
		if(m_pSelShape==m_ShapesList.GetAt(pos)) break;
		m_ShapesList.GetPrev(pos);
	}
	if(pos==NULL) return FALSE;
	// Нашли элемент с указателем на выделенный объект
	// меняем позицию элемента в списке 
	switch(code)
	{
		case TOP:
			m_ShapesList.RemoveAt(pos);
			m_ShapesList.AddTail(m_pSelShape);
			break;
		case BOTTOM:
			m_ShapesList.RemoveAt(pos);
			m_ShapesList.AddHead(m_pSelShape);
			break;
		case STEPUP:
			pastpos=pos;
			m_ShapesList.GetNext(pos);
			if(pos!=NULL)
			{
				m_ShapesList.RemoveAt(pastpos);
				m_ShapesList.InsertAfter(pos, m_pSelShape);
			}
			break;
		case STEPDOWN:
			pastpos=pos;
			m_ShapesList.GetPrev(pos);
			if(pos!=NULL)
			{
				m_ShapesList.RemoveAt(pastpos);
				m_ShapesList.InsertBefore(pos, m_pSelShape);
			}
			break;
	}

	return TRUE;				
};

BOOL CPainterDoc::DeleteSelected()
{
	if(m_pSelShape==NULL) return FALSE;
	CBasePoint *pShape=NULL;
	// Указатель на элемент списка
	POSITION pos=NULL, pastpos=NULL;
	// Начиная с хвоста списка
	if(m_ShapesList.GetCount()>0) pos=m_ShapesList.GetTailPosition();
	// Найдем позицию объекта в списке
	while(pos!=NULL) 
	{
		if(m_pSelShape==m_ShapesList.GetAt(pos)) break;
		m_ShapesList.GetPrev(pos);
	}
	if(pos!=NULL) // нащли его позицию
	{
		m_ShapesList.RemoveAt(pos);
		delete m_pSelShape;
		m_pSelShape=NULL;
		return TRUE;
	}
	return FALSE;
};

BOOL CPainterDoc::OnOpenDocument(LPCTSTR lpszPathName) 
{
	// Нет выбранной фигуры
	m_pSelShape=NULL;
	// Очистили список фигур
	ClearShapesList();

	if (!CDocument::OnOpenDocument(lpszPathName))
		return FALSE;
	
	// TODO: Add your specialized creation code here
	
	return TRUE;
}

void CPainterDoc::SetPatternForSelected(UINT Pattern_ID)
{
	if(m_pSelShape==NULL) return;
	m_pSelShape->SetBrush(RGB(0,0,0), Pattern_ID);
};