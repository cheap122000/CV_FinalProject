
#include <pic.h>
   __CONFIG ( FOSC_INTOSC & WDTE_ON & PWRTE_ON & MCLRE_OFF & CP_ON & CPD_OFF & BOREN_OFF & CLKOUTEN_OFF & IESO_OFF & FCMEN_OFF);
   __CONFIG ( WRT_OFF & PLLEN_OFF & STVREN_OFF & BORV_19 & LVP_OFF);

/*---PIC 腳位定義*/
#define in1 RB0
#define in2 RB1
#define in3 RB2
#define in4 RB3
#define in5 RB4
#define in6 RB5
#define in7 RB6
#define in8 RE3

#define out1 RD0
#define out2 RD1
#define out3 RD2
#define out4 RD3
#define out5 RD4
#define out6 RD5
#define out7 RD6
#define out8 RD7

#define led1 RC0
#define led2 RC1
#define led3 RC2
#define led4 RB7
#define led5 RA4
#define led6 RA5
#define led7 RA6
#define led8 RA7

#define AD0 RA0
#define AD1 RA1
#define AD2 RA2
#define AD3 RA3

#define PWM0 RE0
#define PWM1 RE1
#define PWM2 RE2
/*----以上是，Ver2.1的初始化定義*/


#define	TTLSC 0x41 //TTL起始碼設定 0x 開頭為16進位 設定時請用16進制設定 ASCII碼

////////////////////////////////////
static int x=0;//1~99變數
static int j=0;//1~99變數
char TTLDATA0;
char TTLDATA1;
char TTLDATA2;
char TTLCOUNTER;
int SprayCounter;
/////建構子///////////
void clrdata(void);
char ADRead1(void);
char ADRead2(void);
char Ascii_Change(char chd);
void Ascii_Send(char x);
void Delay_T(int x);

void interrupt int_server(void)//中斷向量
{
	GIE=0;
//	if(TXIF==1)

	CLRWDT();
	CREN=1;
	SYNC=0;
	SPEN=1;

	if(RCIF==1)	//TTL接收旗標判斷
	{
		if(TTLCOUNTER==2)//TTL 第三碼
		{
			TTLCOUNTER=0;
			TTLDATA2=RCREG;
			if((TTLDATA2<0x31)||(TTLDATA2>0x39)){clrdata();TTLCOUNTER=0;}
			else
		{	
/////////////////////////////////////////////
		TXREG=RCREG;//"A";//TTLDATA++;	
		TX9=0;
		SYNC=0;
		TXEN=1;
		SPEN=1;
////////////////////////////////////////////
		}

		}


		if(TTLCOUNTER==1)//TTL 第二碼
		{
			TTLCOUNTER=2;
			TTLDATA1=RCREG;
		if((TTLDATA1==0x30)||(TTLDATA1==0x31))
		{
/////////////////////////////////////////////
		TXREG=RCREG;//"A";//TTLDATA++;	
		TX9=0;
		SYNC=0;
		TXEN=1;
		SPEN=1;
/////////////////////////////////////////////
		}
		else{clrdata();TTLCOUNTER=0;}
		}

		if(RCREG==TTLSC)//TTL 起始碼
		{
			TTLCOUNTER=1;
			TTLDATA0=RCREG;
/////////////////////////////////////////////
		TXREG=RCREG;//"A";//TTLDATA++;	
		TX9=0;
		SYNC=0;
		TXEN=1;
		SPEN=1;
/////////////////////////////////////////////
		}
RCIF=0;
RCIE=1;
	}
	GIE=1;
}


void Start (void)
{
////IO 輸出/輸入 設定 0輸出 1輸入/////////
	TRISA=0b00000011;
	TRISB=0b01111111;
	TRISC=0b10100000;	//ver2.1
	TRISD=0b00000000;
	TRISE=0b00001000;	//ver2.1
////IO 輸出/輸入 設定/////////

////////PORT 初始設定///////////
	PORTA=0b00000000;
	PORTB=0;
	PORTC=0b11000000;
 	PORTD=0;
	PORTE=0;
////////PORT 初始設定///////////
	ANSELA=0B00000011;

	LCDCON=0;
	LCDPS=0;
	LCDREF=0;
	LCDCST=0;
	LCDRL=0;
	LCDSE0=0;
	LCDSE1=0;

	ANSELB=0;
	ANSELA=0;
	ANSELD=0;
	ANSELE=0;


	WPUB=0;

	SPBRGH=0;
	SPBRG=26;
	OSCCON=0b01111010;//頻率設定
//OSCCON=0b00011010;//頻率設定
//OSCCON=SysTemSet;//頻率設定
}

void Sendc(void)
{
	CFGS=0;
	EEPGD=0;
	WREN=1;
	EECON2=0X55;
	EECON2=0X0AA;
	WR=1;
	WREN=0;
	while(EEIF==0)CLRWDT();
	EEIF=0;
}

void clrdata(void)
{
	TTLDATA0=0;
	TTLDATA1=0;
	TTLDATA2=0;
}

//宣告可能用到的變數////-----------------------------------
char W1;
char W2;
char W3;
char W4;
char W5;
char W6;
char t1;
char t2;
char t3;
char t4;
char Tmp;
char WT;
char GetTmp;
char GetAD1;
char ADx;
char xd[17];
char cc;
char aa1;
char aa2;
int a;
char rangeH1;
char rangeH2;
char rangeL1;	
char rangeL2;
char showCase;


void TTL_Ctrl(void)
{
//////////////////TTL 控制 Start/////////////////
	if(TTLDATA0==TTLSC)// 判斷起始碼
	{
		if(TTLDATA1==0x31)//判斷第二碼為ASCII 1 執行
		{
			switch(TTLDATA2)//判斷第三碼為 1~8 開啟RELAY
			{
				case 0x30:
				break;
	
				case 0x31:
				out1=1;//1為開啟RELAY 1
				led1=1;//1為開啟LED 1
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x32:
				out2=1;//1為開啟RELAY 2
				led2=1;//1為開啟LED 2
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x33:
				out3=1;//1為開啟RELAY 3
				led3=1;//1為開啟LED 3
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x34:
				out4=1;//1為開啟RELAY 4
				led4=1;//1為開啟LED 4
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x35:
				out5=1;//1為開啟RELAY 5
				led5=1;//1為開啟LED 5
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x36:
				out6=1;//1為開啟RELAY 6
				led6=1;//1為開啟LED 6
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x37:
				out7=1;//1為開啟RELAY 7
				led7=1;//1為開啟LED 7
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x38:
				out8=1;
				led8=1;
				Delay_T(200);
				out8=0;//0為關閉RELAY 8
				led8=0;//0為關閉LED 8
				check=0;
				clrdata();//執行完畢清除TTL資料
				break;

			}
		}

		if(TTLDATA1==0x30) //判斷第二碼為ASCII 0 執行
		{
			switch(TTLDATA2)//判斷第三碼為 1~8 關閉RELAY
			{
				case 0x30: 
				break;
	
				case 0x31:
				out1=0;//0為關閉RELAY 1
				led1=0;//0為關閉LED 1
				clrdata();//執行完畢清除TTL資料
				
				break;
		
				case 0x32:
				out2=0;//0為關閉RELAY 2
				led2=0;//0為關閉LED 2
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x33:
				out3=0;//0為關閉RELAY 3
				led3=0;//0為關閉LED 3
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x34:
				out4=0;//0為關閉RELAY 4
				led4=0;//0為關閉LED 4
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x35:
				out5=0;//0為關閉RELAY 5
				led5=0;//0為關閉LED 5
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x36:
				out6=0;//0為關閉RELAY 6
				led6=0;//0為關閉LED 6
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x37:
				out7=0;//0為關閉RELAY 7
				led7=0;//0為關閉LED 7
				clrdata();//執行完畢清除TTL資料
				break;
		
				case 0x38:
				out8=1;
				led8=1;
				Delay_T(200);
				out8=0;//0為關閉RELAY 8
				led8=0;//0為關閉LED 8
				check=0;
				clrdata();//執行完畢清除TTL資料
				break;
			}
		}
	}

//////////////////TTL 控制 End/////////////////
}

///////////////////////-----------------------------------


void send_a_word(cc)//送出單個字元
{
	Delay_T(5);
	TXREG=cc;TX9=0;SYNC=0;TXEN=1;SPEN=1;
	clrdata();
}

void Delay_T(int x)//控制延遲
{
	for(int i=0;i<x;i++)
	{	
		CLRWDT();//清除看門狗 防止當機
		_delay(3987);
	}
}





//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
void main(void)//主程式開始
{
	Start();

	CREN=1;
	SYNC=0;
	SPEN=1;
	RCIE=1;
	PEIE=1;
	GIE=1;
	
	
	while(1)
	{
		CLRWDT();//清除看門狗 防止當機
		TTL_Ctrl();
		
	}

}

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

