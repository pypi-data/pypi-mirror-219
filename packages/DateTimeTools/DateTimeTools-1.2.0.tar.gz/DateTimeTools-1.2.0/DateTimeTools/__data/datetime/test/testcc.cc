#include <stdio.h>
#include <datetime.h>


int testsort();
int testcontut();
int testdatediff();
int testdatejoin();
int testdatesplit();
int testdayno();
int testhhmm();
int testjulday();
int testleapyear();
int testmidtime();
int testminusday();
int testtimeindex();
int testplusday();
int testtimediff();
int testunique();
int testunixtime();
int testwhereeq();
int testwithin();

int main() {

	printf("Executing C++ Tests\n");

	int errs = 0;


	errs += testsort();
	errs += testcontut();
	errs += testdatediff();
	errs += testdatejoin();
	errs += testdatesplit();
	errs += testdayno();
	errs += testhhmm();
	errs += testjulday();
	errs += testleapyear();
	errs += testmidtime();
	errs += testminusday();
	errs += testtimeindex();
	errs += testplusday();
	errs += testtimediff();
	errs += testunique();
	errs += testunixtime();
	errs += testwhereeq();
	errs += testwithin();

	if (errs == 0) {
		printf("All tests passed\n");
	} else {
		printf("%d tests failed\n",errs);
	}

	return 0;
}

int testmidtime() {
	printf("Testing mid-time...       ");
	int out = 0;

	int Date0, Date1, Datem;
	float ut0, ut1, utm;

	Date0 = 20010324;
	Date1 = 20020324;
	ut0 = 3.0;
	ut1 = 12.0;
	Datem;
	utm;
	MidTime(Date0,ut0,Date1,ut1,&Datem,&utm);
	if ((Datem != 20010922) || (utm != 19.5)) {
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}

int testminusday() {
	printf("Testing minus day...      ");
	int out = 0;

	int Date = 20040301;
	Date = MinusDay(Date);
	if (Date != 20040229) {
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}

int testtimeindex() {
	printf("Testing time index...     ");
	int out = 0;

	int Date[] = {20010101,20010101,20010103,20010104};
	float ut[] = {12.0,23.0,15.0,4.0};
	int tDate = 20010102;
	float tut = 3.0;

	int ind = NearestTimeIndex(4,Date,ut,tDate,tut);

	if (ind != 1) {
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}

int testplusday() {
	printf("Testing plus day...       ");
	int out = 0;

	int Date = 20040228;
	Date = PlusDay(Date);
	if (Date != 20040229) {
		out = 1;
	}


	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}

int testtimediff() {
	printf("Testing time difference...");
	int out = 0;

	int Date0 = 20010324;
	int Date1 = 20020324;
	float ut0 = 3.0;
	float ut1 = 12.0;
	float dt;
	dt = TimeDifference(Date0,ut0,Date1,ut1);
	if (dt != 365.375) {
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}

int testunique() {
	printf("Testing unique...         ");
	int out = 0;

	float x[] = {1.0,2.0,2.3,4.2,4.2,6.3,6.3};
	float u[] = {1.0,2.0,2.3,4.2,6.3};
	int nu, i;
	float ux[7];

	Unique(7,x,&nu,ux);

	if (nu != 5) {
		out = 1;
	} else {
		for (i=0;i<5;i++) {
			if (ux[i] != u[i]) {
				out = 1;
				//break;
			}
		}
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}

int testunixtime() {
	printf("Testing Unix time...      ");
	int out = 0;

	int Date;
	float ut;
	double unixt;

	Date = 20010405;
	ut = 19.0;
	UnixTime(1,&Date,&ut,&unixt);
	if (unixt != 986497200.0) {
		out = 1;
	}

	UnixTimetoDate(1,&unixt,&Date,&ut);
	if ((Date != 20010405) || (ut != 19.0)) {
		out = 1;
	}


	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}

int testwhereeq() {
	printf("Testing where equal...    ");
	int out = 0;

	double x[] = {1.0,4.0,2.0,4.0,1.0,2.0,2.0};
	int ni, i;
	int ind[7];
	int test[] = {2,5,6};

	WhereEq(7,x,2.0,&ni,ind);
	if (ni != 3) {
		out = 1;
	} else {
		for (i=0;i<3;i++) {
			if (ind[i] != test[i]) {
				out = 1;
				break;
			}
		}
	}



	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}

int testwithin() {
	printf("Testing within range...   ");
	int out = 0;

	int Date[] = {20010101,20010101,20010103,20010104,20010105};
	float ut[] = {12.0,23.0,15.0,4.0,12.0};
	int Date0 = 20010102;
	float ut0 = 12.0;
	int Date1 = 20010105;
	float ut1 = 6.0;

	int ni, i;
	int ind[5];
	int test[] = {2,3};

	WithinTimeRange(5,Date,ut,Date0,ut0,Date1,ut1,&ni,ind);


	if (ni != 2) {
		out = 1;
	} else {
		for (i=0;i<2;i++) {
			if (ind[i] != test[i]) {
				out = 1;
				break;
			}
		}
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}

int testleapyear() {
	printf("Testing leap year...      ");
	int out = 0;

	bool ly;
	int year;

	year = 2001;
	LeapYear(1,&year,&ly);
	if (ly) {
		out = 1;
	}

	year = 2004;
	LeapYear(1,&year,&ly);
	if (!ly) {
		out = 1;
	}


	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;		
}

int testjulday() {
	printf("Testing Julian Date...    ");
	int out = 0;

	double jd;
	int Date;
	float ut;

	Date = 20041230;
	ut = 12.0;
	JulDay(1,&Date,&ut,&jd);
	if (jd != 2453370.0) {
		out = 1;
	}

	jd = 2413370.0;
	JulDaytoDate(1,&jd,&Date,&ut);
	if ((Date != 18950625) || (ut != 12.0)){
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;			
}

int testhhmm() {
	printf("Testing day numbers...    ");
	int out = 0;

	double ut, ms;
	int hh, mm, ss;

	ut = 22.25;
	DectoHHMM(1,&ut,&hh,&mm,&ss,&ms);
	if ((hh != 22) || (mm != 15) || (ss != 0) || (ms != 0.0)) {
		out = 1;
	}
	double hd, md, sd;
	hd = (double) hh;
	md = (double) mm;
	sd = (double) ss;

	HHMMtoDec(1,&hd,&md,&sd,&ms,&ut);
	if (ut != 22.25) {
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}


int testdayno() {
	printf("Testing day numbers...    ");
	int out = 0;	

	int Date, Year, Doy;
	
	Date = 20010324;
	DayNo(1,&Date,&Year,&Doy);
	if ((Year != 2001) || (Doy != 83)) {
		out = 1;
	}

	DayNotoDate(1,&Year,&Doy,&Date);
	if (Date != 20010324) {
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;
}

int testdatesplit() {
	printf("Testing splitting dates...");
	int out = 0;	

	int Date, year, month, day;
	Date = 20010503;
	DateSplit(1,&Date,&year,&month,&day);

	if ((year != 2001) || (month != 5) || (day != 3)) {
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;
}

int testdatejoin() {
	printf("Testing joining dates...  ");
	int out = 0;	

	int Date, year, month, day;
	year = 2001;
	month = 12;
	day = 1;
	DateJoin(1,&year,&month,&day,&Date);

	if (Date != 20011201) {
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;
}


int testsort() {
	printf("Testing bubble sort...    ");
	int out = 0;
	int i;
	float arr0[] = {6.0,2.3,1.2,4.5,9.9};
	float arr1[5];
	float test[] = {1.2,2.3,4.5,6.0,9.9};

	BubbleSort(5,arr0,arr1);

	for (i=0;i<5;i++){
		if(arr1[i] != test[i]){
			out = 1;
			break;
		}
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;
}

int testcontut() {
	printf("Testing Cont UT...        ");
	int out = 0;
	int Date;
	float ut;
	double utc;

	Date = 19500101;
	ut = 0.0;
	ContUT(1,&Date,&ut,&utc);
	if (utc != 0.0) {
		out = 1;
	}

	Date = 20000101;
	ut = 0.0;
	ContUT(1,&Date,&ut,&utc);
	if (utc != 438288.0) {
		out = 1;
	}	

	utc = 0.0;
	ContUTtoDate(1,&utc,&Date,&ut);
	if ((ut != 0.0) || (Date != 19500101)) {
		out = 1;
	}

	utc = 438288.0;
	ContUTtoDate(1,&utc,&Date,&ut);
	if ((ut != 0.0) || (Date != 20000101)) {
		out = 1;
	}

	Date = 19960923;
	ut = 17.5;
	ContUT(1,&Date,&ut,&utc);
	ContUTtoDate(1,&utc,&Date,&ut);
	if ((ut != 17.5) || (Date != 19960923)) {
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;	
}

int testdatediff() {
	printf("Testing Date Difference...");
	int out = 0;

	int diff = DateDifference(19950101,20220324);
	if (diff != 9944) {
		out = 1;
	}

	if (out == 0) {
		printf("pass\n");
	} else {
		printf("fail\n");
	}
	return out;		
}