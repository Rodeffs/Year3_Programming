// PainterDoc.h : interface of the CPainterDoc class
//
/////////////////////////////////////////////////////////////////////////////

#if !defined(AFX_PAINTERDOC_H__F8B9924B_79CF_11D5_BB4A_20804AC10000__INCLUDED_)
#define AFX_PAINTERDOC_H__F8B9924B_79CF_11D5_BB4A_20804AC10000__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000


#define TOP			0
#define BOTTOM		1
#define STEPUP		2
#define STEPDOWN	3

class CBasePoint;
class CPainterDoc : public CDocument
{
protected: 
	CPainterDoc();
	DECLARE_DYNCREATE(CPainterDoc)

// Данные
public:
	// Ширина листа
	WORD m_wSheet_Width;
	// Высота листа
	WORD m_wSheet_Height;
	// Режим отображения
	WORD m_wMap_Mode;

	// Список указателей на объекты-фигуры
	CTypedPtrList<CObList, CBasePoint*> m_ShapesList;
	// Указатель на выбранную фигуру
	CBasePoint* m_pSelShape;  

	
// Методы
public:
	// Очистка списка объектов
	void ClearShapesList();
	// Выбор активной фигуры
	CBasePoint* SelectShape(CPoint point);
	// Изменение порядка следования активной фигуры в списке фигур
	BOOL ChangeOrder(int code);
	// Удалить выделенную фигуру
	BOOL DeleteSelected();

	// Установить шаблон для выделенной фигуры
	void SetPatternForSelected(UINT Pattern_ID);


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CPainterDoc)
	public:
	virtual BOOL OnNewDocument();
	virtual void Serialize(CArchive& ar);
	virtual BOOL OnOpenDocument(LPCTSTR lpszPathName);
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CPainterDoc();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// Generated message map functions
protected:
	//{{AFX_MSG(CPainterDoc)
	afx_msg void OnFilePageproperty();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_PAINTERDOC_H__F8B9924B_79CF_11D5_BB4A_20804AC10000__INCLUDED_)
