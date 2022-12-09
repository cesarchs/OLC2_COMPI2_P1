/*----HEADER----*/
package main;

import (
	"fmt";
	"math" 
);

var T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21, T22, T23, T24, T25, T26, T27, T28, T29, T30, T31, T32, T33, T34, T35, T36, T37, T38, T39, T40, T41, T42, T43, T44, T45, T46, T47, T48, T49, T50, T51, T52, T53, T54, T55, T56, T57, T58, T59, T60, T61, T62, T63, T64, T65, T66, T67, T68, T69, T70, T71, T72, T73, T74, T75, T76, T77, T78, T79, T80, T81, T82, T83, T84, T85, T86, T87, T88, T89, T90, T91, T92, T93, T94, T95, T96, T97, T98, T99, T100, T101, T102, T103, T104, T105, T106, T107 float64;
var P, H float64;
var stack [30101999]float64;
var heap [30101999]float64;

/*-----NATIVES-----*/
func printString(){
	T1=P+1;
	T2=stack[int(T1)];//obtengo posicion en heap de la cadena a imprimir
	L1:
	T3=heap[int(T2)];
	if T3 == -1 {goto L0;}
	fmt.Printf("%c", int(T3));
	T2=T2+1;
	goto L1;
	L0:
	return;
}
func elevateNumber(){
	T10=1;
	L2:
	T8=P+1;
	T9=stack[int(T8)];//obtengo el num a elevar
	T11=P+2;
	T12=stack[int(T11)];//obtengo el exponente
	if T12 <= 0 {goto L3;}
	T10=T10*T9;
	T12=T12-1;
	stack[int(T11)]=T12;
	if T12 != 0 {goto L2;}
	L3:
	T13=P+0;
	stack[int(T13)]=T10;
	return;
}
func IgualdadString(){
	T92=0;
	T93=0;
	T89=P+1;
	T90=stack[int(T89)];//obtengo posicion en heap de la cadena1
	/* -------------CADENA 2----------------- */
	T89=T89+1;
	T91=stack[int(T89)];//obtengo posicion en heap de la cadena2
	/* -------------CADENA 1----------------- */
	L62:
	T94=heap[int(T90)];
	if T94 == -1 {goto L61;}
	L61:
	T95=heap[int(T91)];
	if T95 == -1 {goto L57;}
	if T94 == T95 {goto L58;}
	goto L59;
	L58:
	T93=1;
	goto L60;
	L59:
	T93=0;
	T92=T92-1;
	L60:
	/* INCREMENTO AMBAS POSICIONES DE CADENAS */
	T90=T90+1;
	T91=T91+1;
	goto L62;
	L57:
	if T95 == T94 {goto L64;}
	T93=0;
	L64:
	if T92 == 0 {goto L63;}
	T93=0;
	L63:
	T98=P+0;
	stack[int(T98)]=T93;
	return;
}


func main(){
	/* -------------INICIO INSTRUCCION----------------- */
	/* -------------CADENA----------------- */
	T0=H;
	heap[int(H)]=80;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=98;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=100;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=120;
	H=H+1;
	heap[int(H)]=112;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=105;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=65;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=195;
	H=H+1;
	heap[int(H)]=173;
	H=H+1;
	heap[int(H)]=116;
	H=H+1;
	heap[int(H)]=109;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=116;
	H=H+1;
	heap[int(H)]=105;
	H=H+1;
	heap[int(H)]=99;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* -------------print cadena------------- */
	T4=P+0;
	T4=T4+1;
	stack[int(T4)]=T0;
	P=P+0;
	printString();
	T5=stack[int(P)];
	P=P-0;
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	T6=33*2;
	T7=69-T6;
	/* -------------POTENCIA NUMBER^N ------------- */
	T14=P+0;
	T14=T14+1;
	stack[int(T14)]=25;
	T15=P+0;
	T15=T15+2;
	stack[int(T15)]=T7;
	P=P+0;
	elevateNumber();
	T16=stack[int(P)];
	P=P-0;
	T17=0-T16;
	T18=T17+22;
	T19=32*2;
	T20=T18-T19;
	T21=0-48;
	T22=T21+48;
	/* -------------POTENCIA NUMBER^N ------------- */
	T23=P+0;
	T23=T23+1;
	stack[int(T23)]=33;
	T24=P+0;
	T24=T24+2;
	stack[int(T24)]=T22;
	P=P+0;
	elevateNumber();
	T25=stack[int(P)];
	P=P-0;
	T26=T20-T25;
	/* --------print entero--------- */
	fmt.Printf("%d", int(T26));
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	T27=0-93.555;
	T28=T27+92.12;
	T29=T28-81.33;
	T30=T29+19;
	T31=T30+26;
	T32=T31-68;
	T33=0-7;
	T34=79+11;
	/* -------------DIVIDIDO 0!----------------- */
	if T34 != 0 {goto L4;}
	fmt.Printf("%c", int(77));//M
	fmt.Printf("%c", int(97));//a
	fmt.Printf("%c", int(116));//t
	fmt.Printf("%c", int(104));//h
	fmt.Printf("%c", int(69));//E
	fmt.Printf("%c", int(114));//r
	fmt.Printf("%c", int(114));//r
	fmt.Printf("%c", int(111));//o
	fmt.Printf("%c", int(114));//r
	T35=0;
	goto L5;
	L4:
	T35=T33/T34;
	L5:
	/* -------------DIVIDIDO 0!----------------- */
	if 86 != 0 {goto L6;}
	fmt.Printf("%c", int(77));//M
	fmt.Printf("%c", int(97));//a
	fmt.Printf("%c", int(116));//t
	fmt.Printf("%c", int(104));//h
	fmt.Printf("%c", int(69));//E
	fmt.Printf("%c", int(114));//r
	fmt.Printf("%c", int(114));//r
	fmt.Printf("%c", int(111));//o
	fmt.Printf("%c", int(114));//r
	T36=0;
	goto L7;
	L6:
	T36=T35/86;
	L7:
	T37=T32+T36;
	/* --------print decimal-------- */
	fmt.Printf("%f", T37);
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	T38=8+67;
	T39=T38+74;
	T40=0-86;
	T41=T40+22;
	T42=T41*2;
	/* -------------POTENCIA NUMBER^N ------------- */
	T43=P+0;
	T43=T43+1;
	stack[int(T43)]=1.0;
	T44=P+0;
	T44=T44+2;
	stack[int(T44)]=T42;
	P=P+0;
	elevateNumber();
	T45=stack[int(P)];
	P=P-0;
	T46=T39-T45;
	/* -------------POTENCIA NUMBER^N ------------- */
	T47=P+0;
	T47=T47+1;
	stack[int(T47)]=5;
	T48=P+0;
	T48=T48+2;
	stack[int(T48)]=6;
	P=P+0;
	elevateNumber();
	T49=stack[int(P)];
	P=P-0;
	T50=T46-T49;
	/* --------print decimal-------- */
	fmt.Printf("%f", T50);
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	T51=math.Mod(51,49);
	T52=9.9+90.1;
	T53=T51*T52;
	/* --------print decimal-------- */
	fmt.Printf("%f", T53);
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	T54=9*3;
	T55=46+95;
	T56=math.Mod(85,T55);
	T57=T54*T56;
	T58=0+T57;
	/* --------print entero--------- */
	fmt.Printf("%d", int(T58));
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	/* -------------CADENA----------------- */
	T59=H;
	heap[int(H)]=80;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=98;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=100;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=120;
	H=H+1;
	heap[int(H)]=112;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=105;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=66;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=108;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=121;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=76;
	H=H+1;
	heap[int(H)]=195;
	H=H+1;
	heap[int(H)]=179;
	H=H+1;
	heap[int(H)]=103;
	H=H+1;
	heap[int(H)]=105;
	H=H+1;
	heap[int(H)]=99;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* -------------print cadena------------- */
	T60=P+0;
	T60=T60+1;
	stack[int(T60)]=T59;
	P=P+0;
	printString();
	T61=stack[int(P)];
	P=P-0;
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 56 < 48 {goto L11;}
	goto L9;
	L11:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 68 >= 12 {goto L10;}
	goto L9;
	/* FINALIZO EXPRESION LOGICA */
	
	L10:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 62 != 96 {goto L8;}
	goto L9;
	/* FINALIZO EXPRESION LOGICA */
	
	/* ---------print bool----------- */
	L8:
	fmt.Printf("%c", int(116));//T
	fmt.Printf("%c", int(114));//R
	fmt.Printf("%c", int(117));//U
	fmt.Printf("%c", int(101));//E
	goto L12;
	L9:
	fmt.Printf("%c", int(102));//F
	fmt.Printf("%c", int(97));//A
	fmt.Printf("%c", int(108));//L
	fmt.Printf("%c", int(115));//S
	fmt.Printf("%c", int(101));//E
	L12:
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 21.0 == 20.5 {goto L15;}
	goto L16;
	L16:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 95 >= 94 {goto L15;}
	goto L14;
	/* FINALIZO EXPRESION LOGICA */
	
	L15:
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 19 < 39 {goto L18;}
	goto L17;
	L18:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 83 <= 96 {goto L13;}
	goto L17;
	/* FINALIZO EXPRESION LOGICA */
	
	L17:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 35 < 97 {goto L13;}
	goto L14;
	/* FINALIZO EXPRESION LOGICA */
	
	/* FINALIZO EXPRESION LOGICA */
	
	/* ---------print bool----------- */
	L13:
	fmt.Printf("%c", int(116));//T
	fmt.Printf("%c", int(114));//R
	fmt.Printf("%c", int(117));//U
	fmt.Printf("%c", int(101));//E
	goto L19;
	L14:
	fmt.Printf("%c", int(102));//F
	fmt.Printf("%c", int(97));//A
	fmt.Printf("%c", int(108));//L
	fmt.Printf("%c", int(115));//S
	fmt.Printf("%c", int(101));//E
	L19:
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 68 == 33 {goto L24;}
	goto L25;
	L25:
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 2 < 95 {goto L26;}
	goto L23;
	L26:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 17 == 37 {goto L24;}
	goto L23;
	/* FINALIZO EXPRESION LOGICA */
	
	/* FINALIZO EXPRESION LOGICA */
	
	L24:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 63 <= 9 {goto L20;}
	goto L23;
	/* FINALIZO EXPRESION LOGICA */
	
	L23:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 12 <= 42 {goto L20;}
	goto L22;
	/* FINALIZO EXPRESION LOGICA */
	
	L22:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 25 == 1 {goto L20;}
	goto L21;
	/* FINALIZO EXPRESION LOGICA */
	
	/* ---------print bool----------- */
	L20:
	fmt.Printf("%c", int(116));//T
	fmt.Printf("%c", int(114));//R
	fmt.Printf("%c", int(117));//U
	fmt.Printf("%c", int(101));//E
	goto L27;
	L21:
	fmt.Printf("%c", int(102));//F
	fmt.Printf("%c", int(97));//A
	fmt.Printf("%c", int(108));//L
	fmt.Printf("%c", int(115));//S
	fmt.Printf("%c", int(101));//E
	L27:
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	/* -------------CADENA----------------- */
	T62=H;
	heap[int(H)]=80;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=98;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=100;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=120;
	H=H+1;
	heap[int(H)]=112;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=105;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=65;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=195;
	H=H+1;
	heap[int(H)]=173;
	H=H+1;
	heap[int(H)]=116;
	H=H+1;
	heap[int(H)]=109;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=116;
	H=H+1;
	heap[int(H)]=105;
	H=H+1;
	heap[int(H)]=99;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=44;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=66;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=108;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=121;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=76;
	H=H+1;
	heap[int(H)]=195;
	H=H+1;
	heap[int(H)]=179;
	H=H+1;
	heap[int(H)]=103;
	H=H+1;
	heap[int(H)]=105;
	H=H+1;
	heap[int(H)]=99;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=115;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* -------------print cadena------------- */
	T63=P+0;
	T63=T63+1;
	stack[int(T63)]=T62;
	P=P+0;
	printString();
	T64=stack[int(P)];
	P=P-0;
	fmt.Printf("%c", int(10));
	/* -------------INICIO INSTRUCCION----------------- */
	/* _________INICIO DE IF_________ */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* _________INICIO EXPRESION RELACIONAL_________ */
	/* -------------BOOL----------------- */
	goto L32;
	/* GOTO PARA EVITAR ERROR DE GO */
	goto L33;
	L32:
	T65=1;
	goto L34;
	L33:
	T65=0;
	L34:
	/* -------------BOOL----------------- */
	goto L35;
	/* GOTO PARA EVITAR ERROR DE GO */
	goto L36;
	L35:
	T66=1;
	goto L37;
	L36:
	T66=0;
	L37:
	if T65 == T66 {goto L31;}
	goto L30;
	/* FIN DE EXPRESION RELACIONAL */
	
	L31:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	/* -------------BOOL----------------- */
	goto L39;
	/* GOTO PARA EVITAR ERROR DE GO */
	goto L38;
	L38:
	T67=1;
	goto L40;
	L39:
	T67=0;
	L40:
	/* -------------BOOL----------------- */
	goto L42;
	/* GOTO PARA EVITAR ERROR DE GO */
	goto L41;
	L41:
	T68=1;
	goto L43;
	L42:
	T68=0;
	L43:
	if T67 != T68 {goto L28;}
	goto L30;
	/* FIN DE EXPRESION RELACIONAL */
	
	/* FINALIZO EXPRESION LOGICA */
	
	L30:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	/* -------------BOOL----------------- */
	goto L44;
	/* GOTO PARA EVITAR ERROR DE GO */
	goto L45;
	L44:
	T69=1;
	goto L46;
	L45:
	T69=0;
	L46:
	/* -------------BOOL----------------- */
	goto L48;
	/* GOTO PARA EVITAR ERROR DE GO */
	goto L47;
	L47:
	T70=1;
	goto L49;
	L48:
	T70=0;
	L49:
	if T69 == T70 {goto L28;}
	goto L29;
	/* FIN DE EXPRESION RELACIONAL */
	
	/* FINALIZO EXPRESION LOGICA */
	
	L28:
	/* -------------CADENA----------------- */
	T71=H;
	heap[int(H)]=78;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=116;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=99;
	H=H+1;
	heap[int(H)]=195;
	H=H+1;
	heap[int(H)]=161;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* -------------print cadena------------- */
	T72=P+0;
	T72=T72+1;
	stack[int(T72)]=T71;
	P=P+0;
	printString();
	T73=stack[int(P)];
	P=P-0;
	fmt.Printf("%c", int(10));
	goto L50;
	L29:
	/* -------------CADENA----------------- */
	T74=H;
	heap[int(H)]=69;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=116;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=99;
	H=H+1;
	heap[int(H)]=195;
	H=H+1;
	heap[int(H)]=161;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* -------------print cadena------------- */
	T75=P+0;
	T75=T75+1;
	stack[int(T75)]=T74;
	P=P+0;
	printString();
	T76=stack[int(P)];
	P=P-0;
	fmt.Printf("%c", int(10));
	L50:
	/* -------------INICIO INSTRUCCION----------------- */
	/* _________INICIO DE IF_________ */
	/* ______________INICIO EXPRESION LOGICA______________ */
	/* _________INICIO EXPRESION RELACIONAL_________ */
	T77=1+1;
	T78=1*2;
	/* -------------DIVIDIDO 0!----------------- */
	if 2 != 0 {goto L54;}
	fmt.Printf("%c", int(77));//M
	fmt.Printf("%c", int(97));//a
	fmt.Printf("%c", int(116));//t
	fmt.Printf("%c", int(104));//h
	fmt.Printf("%c", int(69));//E
	fmt.Printf("%c", int(114));//r
	fmt.Printf("%c", int(114));//r
	fmt.Printf("%c", int(111));//o
	fmt.Printf("%c", int(114));//r
	T79=0;
	goto L55;
	L54:
	T79=T78/2;
	L55:
	T80=T77-T79;
	if 1 == T80 {goto L53;}
	goto L52;
	L53:
	/* _________INICIO EXPRESION RELACIONAL_________ */
	if 20.5 == 20.5 {goto L51;}
	goto L52;
	/* FINALIZO EXPRESION LOGICA */
	
	L51:
	/* -------------CADENA----------------- */
	T81=H;
	heap[int(H)]=69;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=116;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=99;
	H=H+1;
	heap[int(H)]=195;
	H=H+1;
	heap[int(H)]=161;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* -------------print cadena------------- */
	T82=P+0;
	T82=T82+1;
	stack[int(T82)]=T81;
	P=P+0;
	printString();
	T83=stack[int(P)];
	P=P-0;
	fmt.Printf("%c", int(10));
	goto L56;
	L52:
	/* -------------CADENA----------------- */
	T84=H;
	heap[int(H)]=78;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=116;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=99;
	H=H+1;
	heap[int(H)]=195;
	H=H+1;
	heap[int(H)]=161;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* -------------print cadena------------- */
	T85=P+0;
	T85=T85+1;
	stack[int(T85)]=T84;
	P=P+0;
	printString();
	T86=stack[int(P)];
	P=P-0;
	fmt.Printf("%c", int(10));
	L56:
	/* -------------INICIO INSTRUCCION----------------- */
	/* _________INICIO DE IF_________ */
	/* _________INICIO EXPRESION RELACIONAL_________ */
	/* -------------CADENA----------------- */
	T87=H;
	heap[int(H)]=72;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=108;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* -------------CADENA----------------- */
	T88=H;
	heap[int(H)]=77;
	H=H+1;
	heap[int(H)]=117;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=100;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* $$$$$$$$$$$$$$$$$$$$$$$$$ COMPARANDO CADENAS $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ */
	/* -------------CADENA == CADENA------------- */
	T99=P+0;
	T99=T99+1;
	stack[int(T99)]=T87;
	T100=P+0;
	T100=T100+2;
	stack[int(T100)]=T88;
	P=P+0;
	IgualdadString();
	T101=stack[int(P)];
	P=P-0;
	if T101 == 1 {goto L67;}
	goto L68;
	L67:
	/* -------------CADENA----------------- */
	T102=H;
	heap[int(H)]=78;
	H=H+1;
	heap[int(H)]=111;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=101;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=116;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=99;
	H=H+1;
	heap[int(H)]=195;
	H=H+1;
	heap[int(H)]=161;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* -------------print cadena------------- */
	T103=P+0;
	T103=T103+1;
	stack[int(T103)]=T102;
	P=P+0;
	printString();
	T104=stack[int(P)];
	P=P-0;
	fmt.Printf("%c", int(10));
	goto L69;
	L68:
	/* -------------CADENA----------------- */
	T105=H;
	heap[int(H)]=69;
	H=H+1;
	heap[int(H)]=110;
	H=H+1;
	heap[int(H)]=116;
	H=H+1;
	heap[int(H)]=114;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=32;
	H=H+1;
	heap[int(H)]=97;
	H=H+1;
	heap[int(H)]=99;
	H=H+1;
	heap[int(H)]=195;
	H=H+1;
	heap[int(H)]=161;
	H=H+1;
	heap[int(H)]=-1;
	H=H+1;
	/* -------------print cadena------------- */
	T106=P+0;
	T106=T106+1;
	stack[int(T106)]=T105;
	P=P+0;
	printString();
	T107=stack[int(P)];
	P=P-0;
	fmt.Printf("%c", int(10));
	L69:

}