// PagePropertyDlg.cpp : implementation file
//

#include "stdafx.h"
#include "Painter.h"
#include "PagePropertyDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CPagePropertyDlg dialog


CPagePropertyDlg::CPagePropertyDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CPagePropertyDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CPagePropertyDlg)
	m_uHeight = 0;
	m_uWidth = 0;
	//}}AFX_DATA_INIT
}


void CPagePropertyDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CPagePropertyDlg)
	DDX_Control(pDX, IDC_SPIN_WIDTH, m_ctlSpinWidth);
	DDX_Control(pDX, IDC_SPIN_HEIGHT, m_ctlSpinHeight);
	DDX_Text(pDX, IDC_EDIT_HEIGHT, m_uHeight);
	DDV_MinMaxUInt(pDX, m_uHeight, 0, 297);
	DDX_Text(pDX, IDC_EDIT_WIDTH, m_uWidth);
	DDV_MinMaxUInt(pDX, m_uWidth, 0, 210);
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CPagePropertyDlg, CDialog)
	//{{AFX_MSG_MAP(CPagePropertyDlg)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CPagePropertyDlg message handlers

BOOL CPagePropertyDlg::OnInitDialog() 
{
	CDialog::OnInitDialog();
	
	// TODO: Add extra initialization here
	//установим диапазон прокрутки Spin-элементов
	m_ctlSpinWidth.SetRange(0, 210);
	m_ctlSpinHeight.SetRange(0, 297);
	
	return TRUE;  // return TRUE unless you set the focus to a control
	              // EXCEPTION: OCX Property Pages should return FALSE
}
