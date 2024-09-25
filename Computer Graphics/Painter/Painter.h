// Painter.h : main header file for the PAINTER application
//

#if !defined(AFX_PAINTER_H__F8B99245_79CF_11D5_BB4A_20804AC10000__INCLUDED_)
#define AFX_PAINTER_H__F8B99245_79CF_11D5_BB4A_20804AC10000__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"       // main symbols

/////////////////////////////////////////////////////////////////////////////
// CPainterApp:
// See Painter.cpp for the implementation of this class
//

class CPainterApp : public CWinApp
{
public:
	CPainterApp();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CPainterApp)
	public:
	virtual BOOL InitInstance();
	//}}AFX_VIRTUAL

// Implementation
	//{{AFX_MSG(CPainterApp)
	afx_msg void OnAppAbout();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_PAINTER_H__F8B99245_79CF_11D5_BB4A_20804AC10000__INCLUDED_)
