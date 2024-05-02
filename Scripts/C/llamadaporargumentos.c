#include <stdio.h>

int main(int argc, char *argv[]) {
    // Imprimir el número total de argumentos pasados
    printf("Número total de argumentos: %d\n", argc);

    // Imprimir cada argumento
    printf("Argumentos:\n");
    for (int i = 0; i < argc; i++) {
        printf("argv[%d]: %s\n", i, argv[i]);
    }

    return 0;
}

//Para compilar: gcc ejemplo.c -o ejemplo
//Para ejecutar y mandar argumentos: ./ejemplo argumento1 argumento2 argumento3


//Para generar el código en ensamblador: gcc -S ejemplo.c