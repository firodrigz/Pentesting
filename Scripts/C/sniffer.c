//gcc -o captura sniffer.c -lpcap

#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>
#include <arpa/inet.h> // para imprimir en decimal 

//Estructuras
struct in_addr {
    in_addr_t s_addr; // Dirección IPv4 en formato binario (32 bits)
};

//Funciones
void procesar_paquete(u_char *usuario, const struct pcap_pkthdr *encabezado, const u_char *paquete) {
    printf("Capturado un paquete de longitud %d\n", encabezado->len);
}

/* Define una función llamada procesar_paquete que será llamada cada vez que se capture un paquete. 
Esta función toma tres argumentos: un puntero a datos de usuario (que no se utiliza en este ejemplo), un puntero a la estructura pcap_pkthdr que contiene información sobre el paquete capturado y un puntero al paquete capturado.*/

/*void imprimir_en_decimal(unsigned int valor) {
    printf(" %u.%u.%u.%u\n",
            valor & 0xFF,
           (valor >> 8) & 0xFF,
           (valor >> 16) & 0xFF,
           (valor >> 24) & 0xFF);
}
*/
/* Función para dar formato a la respuesta en bits de direccion de red y máscara subred  REEMPLAZADA POR LIBRERÍA #include <arpa/inet.h> FUNCIÓN inet_ntoa()*/

int main(int argc, char *argv[]) {
    
    char error_buffer[PCAP_ERRBUF_SIZE]; // Buffer de errores

    char *interfaz = argv[1]; // Nombre de la interfaz de red ingresado por usuario al ejecutar el comando
    
    struct in_addr direccion_red, mascara_subred; 

    if (argc < 2) {
        fprintf(stderr, "Sintax: %s <nombre_de_interfaz>\n", argv[0]);
        return 1;
    }

    printf("\n[+] Interfaz: %s\n", interfaz);

    //Validaciones de existencia/funcionamiento de interfaz seleccionada
    if (pcap_lookupnet(interfaz, &direccion_red.s_addr, &mascara_subred.s_addr, error_buffer) == -1) { 
        fprintf(stderr, "Error al obtener la dirección de red y la máscara de subred: %s\n", error_buffer);
        return 1;
    }

    // Mostrar la dirección de red y la máscara de subred obtenidas
    printf("[+] Dirección de red: %s\n", inet_ntoa(direccion_red)); //se le pasa la estructura
    printf("[+] Máscara de subred: %s\n\n", inet_ntoa(mascara_subred));

    /*
    // Obtener la lista de interfaces de red disponibles
    pcap_if_t *interfaces;
    if (pcap_findalldevs(&interfaces, error_buffer) == -1) {
        fprintf(stderr, "Error al obtener la lista de interfaces: %s\n", error_buffer);
        return 1;
    }

    // Mostrar la lista de interfaces disponibles y permitir al usuario seleccionar una
    pcap_if_t *interfaz_actual = interfaces;
    int contador = 0;
    while (interfaz_actual != NULL) {
        printf("%d. %s\n", ++contador, interfaz_actual->name);
        interfaz_actual = interfaz_actual->next;
    }
    
    int opcion;
    printf("Seleccione la interfaz de red (ingrese el número correspondiente): ");
    scanf("%d", &opcion);

    // Buscar la interfaz seleccionada por el usuario
    interfaz_actual = interfaces;
    for (int i = 1; i < opcion; ++i) {
        interfaz_actual = interfaz_actual->next;
        if (interfaz_actual == NULL) {
            fprintf(stderr, "Opción inválida\n");
            return 1;
        }
    }

     // Mostrar información detallada sobre la interfaz seleccionada
    printf("Interfaz seleccionada: %s\n", interfaz_actual->name);

    // Recorrer las direcciones de la interfaz seleccionada
    pcap_addr_t *direccion = interfaz_actual->addresses;
    while (direccion != NULL) {
        if (direccion->addr->sa_family == AF_INET) { // Solo direcciones IPv4
            struct sockaddr_in *direccion_ipv4 = (struct sockaddr_in *)direccion->addr;
            struct sockaddr_in *mascara_ipv4 = (struct sockaddr_in *)direccion->netmask;
            printf("Dirección IP: %s\n", inet_ntoa(direccion_ipv4->sin_addr));
            printf("Dirección de red: ");
            imprimir_en_decimal(ntohl(direccion_ipv4->sin_addr.s_addr) & ntohl(mascara_ipv4->sin_addr.s_addr));
            printf("Máscara de subred: ");
            imprimir_en_decimal(ntohl(mascara_ipv4->sin_addr.s_addr));
        }
        direccion = direccion->next;
    }
    */

    // Abrir la interfaz de red seleccionada para la captura de paquetes
    pcap_t *handle = pcap_open_live(interfaz, BUFSIZ, 1, 1000, error_buffer);
    if (handle == NULL) {
        fprintf(stderr, "No se pudo abrir la interfaz %s: %s\n", interfaz, error_buffer);
        return 1;
    }

    // Compilar y establecer un filtro de captura para solo paquetes IP
    struct bpf_program filtro;
    if (pcap_compile(handle, &filtro, "ip", 0, PCAP_NETMASK_UNKNOWN) == -1) {
        fprintf(stderr, "Error al compilar el filtro: %s\n", pcap_geterr(handle));
        return 1;
    }
    if (pcap_setfilter(handle, &filtro) == -1) {
        fprintf(stderr, "Error al establecer el filtro: %s\n", pcap_geterr(handle));
        return 1;
    }

    // Capturar paquetes en un bucle y procesarlos
    pcap_loop(handle, -1, procesar_paquete, NULL);

    // Cerrar la interfaz de captura de paquetes al finalizar
    pcap_close(handle);

    /*
    // Liberar la memoria de la lista de interfaces
    pcap_freealldevs(interfaces);
    */

    return 0;
}
