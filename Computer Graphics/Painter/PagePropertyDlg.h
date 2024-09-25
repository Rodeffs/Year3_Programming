#if !defined(AFX_PAGEPROPERTYDLG_H__A81FE4D2_5222_4150_A8F9_A91020C55D95__INCLUDED_)
#define AFX_PAGEPROPERTYDLG_H__A81FE4D2_5222_4150_A8F9_A91020C55D95__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// PagePropertyDlg.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CPagePropertyDlg dialog

class CPagePropertyDlg : public CDialog
{
// Construction
public:
	CPagePropertyDlg(CWnd* pParent = NULL);   // standard constructor

// Dialog Data
	//{{AFX_DATA(CPagePropertyDlg)
	enum { IDD = IDD_PAGE_PROPERTY };
	CSpinButtonCtrl	m_ctlSpinWidth;
	CSpinButtonCtrl	m_ctlSpinHeight;
	UINT	m_uHeight;
	UINT	m_uWidth;
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CPagePropertyDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CPagePropertyDlg)
	virtual BOOL OnInitDialog();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_PAGEPROPERTYDLG_H__A81FE4D2_5222_4150_A8F9_A91020C55D95__INCLUDED_)
