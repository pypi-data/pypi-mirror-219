copy ..\lib\libdatetime.dll .
gcc -O3 -Wextra -fPIC -I..\include testc.c -o testc -lm -L. -ldatetime
g++ -g -O3 -std=c++17 -Wextra -fPIC -I..\include testcc.cc -o testcc -lm -L. -ldatetime
testc.exe
testcc.exe
del testc.exe
del testcc.exe
del libdatetime.dll