// MainFrm.cpp : implementation of the CMainFrame class
//

#include "stdafx.h"
#include "Painter.h"
#include "PainterDoc.h"

#include "MainFrm.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CMainFrame

IMPLEMENT_DYNCREATE(CMainFrame, CFrameWnd)

BEGIN_MESSAGE_MAP(CMainFrame, CFrameWnd)
	//{{AFX_MSG_MAP(CMainFrame)
		// NOTE - the ClassWizard will add and remove mapping macros here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	ON_WM_CREATE()
	//}}AFX_MSG_MAP
	ON_WM_NOTIFYFORMAT()
END_MESSAGE_MAP()

static UINT indicators[] =
{
	ID_SEPARATOR,           // status line indicator
	ID_INDICATOR_CAPS,
	ID_INDICATOR_NUM,
	ID_INDICATOR_SCRL,
};

/////////////////////////////////////////////////////////////////////////////
// CMainFrame construction/destruction

CMainFrame::CMainFrame()
{
	// TODO: add member initialization code here
	
}

CMainFrame::~CMainFrame()
{
}

int CMainFrame::OnCreate(LPCREATESTRUCT lpCreateStruct)
{
	if (CFrameWnd::OnCreate(lpCreateStruct) == -1)
		return -1;
	
	if (!m_wndToolBar.CreateEx(this, TBSTYLE_FLAT, WS_CHILD | WS_VISIBLE | CBRS_TOP
		| CBRS_GRIPPER | CBRS_TOOLTIPS | CBRS_FLYBY | CBRS_SIZE_DYNAMIC) ||
		!m_wndToolBar.LoadToolBar(IDR_MAINFRAME))
	{
		TRACE0("Failed to create toolbar\n");
		return -1;      // fail to create
	}

	if (!m_wndStatusBar.Create(this) ||
		!m_wndStatusBar.SetIndicators(indicators,
		  sizeof(indicators)/sizeof(UINT)))
	{
		TRACE0("Failed to create status bar\n");
		return -1;      // fail to create
	}

	// TODO: Delete these three lines if you don't want the toolbar to
	//  be dockable
	m_wndToolBar.EnableDocking(CBRS_ALIGN_ANY);
	EnableDocking(CBRS_ALIGN_ANY);
	DockControlBar(&m_wndToolBar);

	// панель изображений
	if (!m_dlgBarImages.Create(this, IDD_IMAGES, WS_CHILD | CBRS_BOTTOM, 
      IDD_IMAGES))
	{
		TRACE0("Failed to create dialog bar\n");
		return -1;    
	}
	m_dlgBarImages.ShowWindow(SW_SHOW);
	FillPatternsList();

	return 0;
}

BOOL CMainFrame::PreCreateWindow(CREATESTRUCT& cs)
{
	if( !CFrameWnd::PreCreateWindow(cs) )
		return FALSE;
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	return TRUE;
}

/////////////////////////////////////////////////////////////////////////////
// CMainFrame diagnostics

#ifdef _DEBUG
void CMainFrame::AssertValid() const
{
	CFrameWnd::AssertValid();
}

void CMainFrame::Dump(CDumpContext& dc) const
{
	CFrameWnd::Dump(dc);
}

#endif //_DEBUG


#define N_PATTERNS 8
void CMainFrame::FillPatternsList() 
{
	m_PatternsList.DeleteImageList();
	// —оздаем список изображений
	m_PatternsList.Create( 32, 32, ILC_COLOR24, 0, 1 );

	// «агружаем все изображени€ и добавл€ем в список изображение
	CBitmap bm;
	int index=0; // индекс добавленной картинки 

	bm.LoadBitmap(IDB_PATTERN0);
	index=m_PatternsList.Add(&bm, RGB(0, 0, 0)); 	bm.DeleteObject( );

	bm.LoadBitmap(IDB_PATTERN1);
	index=m_PatternsList.Add(&bm, RGB(0, 0, 0)); 	bm.DeleteObject( );

	bm.LoadBitmap(IDB_PATTERN2);
	index=m_PatternsList.Add(&bm, RGB(0, 0, 0)); 	bm.DeleteObject( );
	
	bm.LoadBitmap(IDB_PATTERN3);
	index=m_PatternsList.Add(&bm, RGB(0, 0, 0)); 	bm.DeleteObject( );
	
	bm.LoadBitmap(IDB_PATTERN4);
	index=m_PatternsList.Add(&bm, RGB(0, 0, 0)); 	bm.DeleteObject( );
	
	bm.LoadBitmap(IDB_PATTERN5);   
	index=m_PatternsList.Add(&bm, RGB(0, 0, 0)); 	bm.DeleteObject( );
	
	bm.LoadBitmap(IDB_PATTERN6);
	index=m_PatternsList.Add(&bm, RGB(0, 0, 0)); 	bm.DeleteObject( );
	
	bm.LoadBitmap(IDB_PATTERN7);
	index=m_PatternsList.Add(&bm, RGB(0, 0, 0)); 	bm.DeleteObject( );

/*
		// «агрузка шаблонов заливки из файлов BMP на диске
		
		CString Path, PatternName; 
		// ѕолучили название текущего директори€
		GetCurrentDirectory( MAX_PATH, Path.GetBuffer(MAX_PATH));
		// ј так можно узнать где располагаетс€ exe-файл программы, если хотим указать
		// положение каталога с шаблонами относительно положени€  exe-файла
		//GetModuleFileName(AfxGetInstanceHandle(), Path.GetBuffer(MAX_PATH), MAX_PATH);
	  	Path.ReleaseBuffer();
		for(int n=0; n<N_PATTERNS; n++)
		{
			// ‘ормируем путь и им€ шаблона
			// предполагаетс€, что шаблоны лежат в каталоге \Patterns текущего директори€
			PatternName.Format("\\Patterns\\Pattern%d.bmp", n);
			PatternName=Path+PatternName;
			HBITMAP hBMP=NULL;	
			// «агружаем шаблон
			hBMP=(HBITMAP)LoadImage(NULL, PatternName, IMAGE_BITMAP, 0, 0, LR_LOADFROMFILE|LR_DEFAULTCOLOR);
			// ƒобавл€ем изображение шаблона в список шаблонов
			index=m_PatternsList.Add(bm.FromHandle(hBMP) , RGB(0, 0, 0)); 	bm.DeleteObject( );
		}*/
	
	
	// ѕолучаем указатель на элемент управлени€ —писок диалоговой панели
	CListCtrl* pImageListCtrl = (CListCtrl*) m_dlgBarImages.GetDlgItem(IDC_IMAGE_LIST);
	ASSERT(pImageListCtrl!=NULL);
	pImageListCtrl->DeleteAllItems( );
	// ƒобавл€ем в —писок названи€ шаблонов
	CString Caption;
	for(int i=0; i<=index; i++)
	{	Caption.Format(_T("Pat %d"),i+1);
		pImageListCtrl->InsertItem( i, Caption, i );
	}
	// —в€зываем список-элемент управлени€ диалога со списком изображений шаблонов
	pImageListCtrl->SetImageList(&m_PatternsList, LVSIL_NORMAL);
}

void CMainFrame::SetSelectedPattern()
{
	CListCtrl* pImageListCtrl = (CListCtrl*) m_dlgBarImages.GetDlgItem(IDC_IMAGE_LIST);
	ASSERT(pImageListCtrl!=NULL);
	POSITION pos = pImageListCtrl->GetFirstSelectedItemPosition();
	int nItem=-1;
	if (pos != NULL)
		nItem = pImageListCtrl->GetNextSelectedItem(pos);
	if (nItem<0) return; //ничего не выделено
	UINT Pattern_ID=0;
	switch(nItem)
	{
		case 0: Pattern_ID=IDB_PATTERN0; break;
		case 1: Pattern_ID=IDB_PATTERN1; break;
		case 2: Pattern_ID=IDB_PATTERN2; break;
		case 3: Pattern_ID=IDB_PATTERN3; break;
		case 4: Pattern_ID=IDB_PATTERN4; break;
		case 5: Pattern_ID=IDB_PATTERN5; break;
		case 6: Pattern_ID=IDB_PATTERN6; break;
		case 7: Pattern_ID=IDB_PATTERN7; break;
	}
	
	// ѕолучили указатель на документ
	CPainterDoc *pDoc=(CPainterDoc*)GetActiveDocument();
	pDoc->SetPatternForSelected(Pattern_ID);
	pDoc->UpdateAllViews(NULL);   
}

/////////////////////////////////////////////////////////////////////////////
// CMainFrame message handlers


BOOL CMainFrame::OnNotify(WPARAM wParam, LPARAM lParam, LRESULT* pResult) 
{
	if(wParam==IDC_IMAGE_LIST && ((NMHDR*)lParam)->code == NM_CLICK)
		SetSelectedPattern(); // установить выбранный шаблон
	return CFrameWnd::OnNotify(wParam, lParam, pResult);
}
