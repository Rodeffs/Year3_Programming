// файл Shapes.h
////////////////////////////////////////////////////
//класс базовая точка
#define MOVE_STEP 100
#define ROTATE_STEP 5
#define SHIFT_HOLD	1
#define CTRL_HOLD	2

class CBasePoint: public CPoint, public CObject
{
 	DECLARE_SERIAL(CBasePoint)
	CPen	m_Pen;	// перо
	CBrush	m_Brush;// кисть
protected:
	// Метод сериализации
	virtual void Serialize(CArchive& ar);
	// Подготавливает контекст устройства
	virtual BOOL PrepareDC(CDC *pDC);
	// Восставливает контекст устройства
	virtual BOOL RestoreDC(CDC *pDC);
public:
	// Данные
	WORD		m_wSize;			//размер фигуры
	int			m_iPenStyle;		//стиль линий
	int			m_iPenWidth;		//ширина линий
	COLORREF	m_rgbPenColor;		//цвет линий
	int			m_iBrushStyle;		//стиль заливки
	COLORREF	m_rgbBrushColor;	//цвет заливки
	DWORD		m_dwPattern_ID;		//идентификатор шаблона заливки
public:		
	// Конструкторы
	CBasePoint();				//конструктор без параметров
	CBasePoint(int x, int y, WORD s);	//конструктор с параметрами
	~CBasePoint(){};			//деструктор
	// Методы
	// Отображает фигуру на экране
	virtual void Show(CDC *pDC);
	// Сообщает область захвата
	virtual void GetRegion(CRgn &Rgn);
	// Устанавливает параметры линий
	virtual BOOL SetPen(COLORREF color, int width =1, int style=PS_SOLID);
	// Устанавливает параметры заливки
	virtual BOOL SetBrush(COLORREF color, DWORD pattern =0, int style=-1);
	// Выполняет преобразование на плоскости
	virtual void Transform(const CPoint &point0, double ang, int a, int b);
	// Реакция на нажатие клавиши
	virtual BOOL OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags, UINT nMyFlags); 
};

////////////////////////////////////////////////////
//класс квадрат
class CSquare: public CBasePoint
{
 	DECLARE_SERIAL(CSquare)   
 protected:  
	 // Метод сериализации
	void Serialize(CArchive& ar);
 public:		
	// Конструкторы
	CSquare(int x, int y, WORD s);
	CSquare();
	~CSquare(){};
//Методы
	// Отображает фигуру на экране
	void Show(CDC *pDC);
	// Сообщает область захвата
	void GetRegion(CRgn &Rgn);
};

////////////////////////////////////////////////////
// MY CODE

class CSector : public CBasePoint {

	DECLARE_SERIAL(CSector);

protected:
	void Serialize(CArchive& ar);

public:
	CSector();

	CSector(int x, int y, WORD s);

	~CSector() {};

	void Show(CDC* pDC);
	// Сообщает область захвата
	void GetRegion(CRgn& Rgn);

};

////////////////////////////////////////////////////
//класс полигон
class CPolygon: public CBasePoint
{
 	DECLARE_SERIAL(CPolygon)   
	BOOL	m_bPolygon;	// режим рисования: 
	// TRUE - заполненный полигон,
	// FALSE - ломаная кривая. Нет, ломаная прямая. Нет, ломаная линия. Во! 

 protected:  
	 // Метод сериализации
	void Serialize(CArchive& ar);
 public:
	 // Динамический массив точек-вершин
	 CArray <CPoint, CPoint> m_PointsArray;
		
	// Конструкторы
	 CPolygon();
	~CPolygon();
//Методы
	// Отображает фигуру на экране
	void Show(CDC *pDC);
	// Сообщает область захвата
	void GetRegion(CRgn &Rgn);
	// Устанавливает режим рисования полигона
	void SetPolygon(BOOL p) {m_bPolygon=p;};
	// Выполняет преобразование на плоскости
	void Transform(const CPoint &point0, double ang, int a, int b);
};

////////////////////////////////////////////////////
// 3D точка
struct POINT3D
{
	double x, y, z;
}; 

//параметры  трехмерной сцены
struct  Perspective
{
	POINT3D	O;					// точка, вокруг которой выполняем поворот
	double	rho, theta, phi,	// полярные координаты точки наблюдения (E)
			d;					// расстояние от E до экрана
	WORD	with_perspective;   // 1- вкл. перспективные преобразования; 0-выкл.
	LONG	dx, dy;				// смещение проекции на экране
};

////////////////////////////////////////////////////
//класс C3DPolygon
//
class C3DPolygon: public CPolygon
{
 	DECLARE_SERIAL(C3DPolygon)   
 protected:  	// метод сериализации	
	void Serialize(CArchive& ar);
 public:		
 	// Конструкторы
	 C3DPolygon(){};
	 ~C3DPolygon(){};
// Данные
	// Динамический массив точек-вершин в мировых координатах
	CArray <POINT3D, POINT3D> m_3DPointsArray;	
// Методы		
	// Добавить точку
	void AddPoint(POINT3D point) {m_3DPointsArray.Add(point);};
	// Расчет экранных координат
	void MakeProjection(Perspective P); 
};


////////////////////////////////////////////////////
//класс C3DShape
class C3DShape: public CBasePoint
{
 	DECLARE_SERIAL(C3DShape)   
 protected:  	// Виртуальный метод сериализации	
	void Serialize(CArchive& ar);
	
 public:		
	//конструкторы
	C3DShape();
	~C3DShape();
//Данные
	Perspective m_Percpective; //параметры обзора
	CTypedPtrList<CObList, C3DPolygon*> m_PtrPolygonList; // список указателей на полигоны
//Методы
	// Расчет проекции
	void MakeProjection();
	// Отображение фигуры на экране
	void Show(CDC *pDC);
	// Сообщает область захвата
	void GetRegion(CRgn &Rgn);
	// Добавить полигон
	void AddPolygon(C3DPolygon *pPolygon);
	// Реакция на нажатие клавиши
	BOOL OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags, UINT nMyFlags);
};

/////////////////////////////////////////////////////////////////////////////////
// Глобальные функции для работы с поверхностями,
// из которых, по-хорошему, надо бы сделать класс C3DSurface

// Добавляет линию пересечения (линию уровня) поверхности,
// заданной массивом точек POINT3D с плоскостью,
// заданной значением level (уровень по Z)
// Параметры:
// pShape - указатель на трехмерный объект, куда будет добавлено сечение
// pSur - указатель на массив точек, задающих пверхность
// x_size, y_size - размер массива точек
// level - уровень секущей плоскости
// color - цвет линии пересечения  
// Возвращаемое значение:
// 0 - неудача
// 1 - успех
int AddRsection(C3DShape *pShape, POINT3D *pSur, int x_size, int y_size, double level,  COLORREF color);

// Добавляет линию пересечения треуголька,
// заданного тремя точками с плоскостью,
// заданной значением level (уровень по Z)
// Параметры:
// p3DPolygon - указатель на полигон, куда будет добавлены точки пересечения
// pP1, pP2, pP3 - указатели на точеки, задающие треугольник
// level - уровень секущей плоскости
void AddTriangleSection(C3DPolygon *p3DPolygon, POINT3D *pP1, POINT3D *pP2, POINT3D *pP3, double level);

// А эти функции вполне можно оставить глобальными

// Рассчитывает координаты x,y точки пересечения отрезка pP1, pP2 с поверхностью level
int CutCross(double level, POINT3D *pP1, POINT3D *pP2, double &x, double &y);
// Рассчитывает расстояние между двумя точками
double Dist(POINT3D *pP1, POINT3D* pP2);
