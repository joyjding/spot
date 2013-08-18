; < Woof! A Spot --> NASM file for your compiling pleasure /(^.^)\ >

; ----------------
section .text
global mystart ;make the main function externally visible
; ----------------
;START OF PROGRAM

mystart:

MOV dword [x], 4
; less than comparison of x < 4 

MOV EAX, [x]
MOV EBX, 4
CMP EAX, EBX
JL if_0
; greater than comparison of x > 4
MOV EAX,  [x]
MOV EBX, 4
CMP EAX, EBX
JG elseif_0
JMP else_0
if_0:

; prepare the arguments
push dword 5 			; string length arg
push dword woooo          	; string to print arg
push dword 1           		; file descriptor value


; make the system call to write
mov eax, 0x4 			; system call number for writescreen
sub esp, 4 			; move the stack pointer for extra space
int 0x80			; code to execute system call


; clean up the stack
add esp, 16 			; args * 4 bytes/arg + 4 bytes extra space

JMP endif_0
elseif_0:

; prepare the arguments
push dword 4 			; string length arg
push dword booo          	; string to print arg
push dword 1           		; file descriptor value


; make the system call to write
mov eax, 0x4 			; system call number for writescreen
sub esp, 4 			; move the stack pointer for extra space
int 0x80			; code to execute system call


; clean up the stack
add esp, 16 			; args * 4 bytes/arg + 4 bytes extra space

JMP endif_0
else_0:

; prepare the arguments
push dword 4 			; string length arg
push dword What          	; string to print arg
push dword 1           		; file descriptor value


; make the system call to write
mov eax, 0x4 			; system call number for writescreen
sub esp, 4 			; move the stack pointer for extra space
int 0x80			; code to execute system call


; clean up the stack
add esp, 16 			; args * 4 bytes/arg + 4 bytes extra space

JMP endif_0
endif_0:
; --------------------------------------------
; EXIT THE PROGRAM

; prepare the argument for the sys call to exit
push dword 0 			; exit status returned to OS


; make the call to sys call to exit
mov eax, 0x1 			; sys call no. for exit
sub esp, 4 			; give it some extra space
int 0x80 			; make the system call
;----------

section .data

x dd 1
woooo db "woooo"
booo db "booo"
What db "What"
