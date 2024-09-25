// PainterView.h : interface of the CPainterView class
//
/////////////////////////////////////////////////////////////////////////////

#if !defined(AFX_PAINTERVIEW_H__F8B9924D_79CF_11D5_BB4A_20804AC10000__INCLUDED_)
#define AFX_PAINTERVIEW_H__F8B9924D_79CF_11D5_BB4A_20804AC10000__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

// Определение операций
#define OP_NOOPER	0
#define OP_LINE		1
#define OP_POINT	2
#define OP_CIRCLE	3
#define OP_SQUARE	4
#define OP_SURFACE	5

// My code
#define OP_SECTOR	6

#define OP_SELECT	10

class CBasePoint;
class CPainterView : public CScrollView
{
protected: // create from serialization only
	CPainterView();
	DECLARE_DYNCREATE(CPainterView)

// Данные
public:
	// Текущая операция
	int m_CurOper;
	// Курсоры различных операций
	HCURSOR m_hcurCircle;	// рисуем круг
	HCURSOR m_hcurSquare;	// рисуем квадрат
	HCURSOR m_hcurPolygon;	// рисуем полилинию или полигон
	HCURSOR m_hcurSurface;	// рисуем поверхность

	// My code
	HCURSOR m_hcurSector;
	
	// Курсор "по умолчанию"
	HCURSOR m_hcurDefault;	// используем в операции выбора

	// Начальная и текущая точки операции 
	CPoint	m_FirstPoint, m_CurMovePoint;
	// Индикатор нажатия клавиш Shift, Ctrl
	UINT m_nMyFlags;
// Методы
	CPainterDoc* GetDocument();
	void AddShape(int shape, CPoint first_point, CPoint second_point);
	CBasePoint* AddSurface(CPoint first_point, int size);
	void MarkSelectedShape(CDC *pDC);
	void DrawMoveLine(CPoint first_point, CPoint second_point);
	void SaveBMP(CString &fname);
	
// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CPainterView)
	public:
	virtual void OnDraw(CDC* pDC);  // overridden to draw this view
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
	virtual void OnPrepareDC(CDC* pDC, CPrintInfo* pInfo = NULL);
	protected:
	virtual BOOL OnPreparePrinting(CPrintInfo* pInfo);
	virtual void OnBeginPrinting(CDC* pDC, CPrintInfo* pInfo);
	virtual void OnEndPrinting(CDC* pDC, CPrintInfo* pInfo);
	virtual void OnUpdate(CView* pSender, LPARAM lHint, CObject* pHint);
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CPainterView();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// Generated message map functions
protected:
	//{{AFX_MSG(CPainterView)
	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	afx_msg void OnEditAddshapePoint();
	afx_msg void OnEditAddshapeCircle();
	afx_msg void OnEditAddshapeSquare();
	afx_msg void OnEditSelect();
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	afx_msg void OnEditAddshapePolyline();
	afx_msg void OnEditAddshapePolygon();
	afx_msg void OnLButtonDblClk(UINT nFlags, CPoint point);
	afx_msg void OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags);
	afx_msg void OnKeyUp(UINT nChar, UINT nRepCnt, UINT nFlags);
	afx_msg void OnEditChangeorderTop();
	afx_msg void OnEditChangeorderStepup();
	afx_msg void OnEditChangeorderStepdown();
	afx_msg void OnEditChangeorderBottom();
	afx_msg void OnEditDelete();
	afx_msg void OnEditAddshapeSurface();
	//afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
	afx_msg void OnSaveBmp();
	
	// My code
	afx_msg void OnEditAddshapeSector();

	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

#ifndef _DEBUG  // debug version in PainterView.cpp
inline CPainterDoc* CPainterView::GetDocument()
   { return (CPainterDoc*)m_pDocument; }
#endif

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_PAINTERVIEW_H__F8B9924D_79CF_11D5_BB4A_20804AC10000__INCLUDED_)
