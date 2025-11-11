/* mpi Bradcast 
* K Djemame
* September 2024
*/

#include <stdio.h>
#include "mpi.h"

int main( argc, argv )
int argc;
char **argv;
{
    int rank, temp;
    MPI_Init( &argc, &argv );

    MPI_Comm_rank( MPI_COMM_WORLD, &rank );
    do {
	if (rank == 0)
	{ 
            printf("Input a number: ");
	    scanf( "%d", &temp );
        }
	MPI_Bcast( &temp, 1, MPI_INT, 0, MPI_COMM_WORLD );
	
	printf( "Process %d got %d\n", rank, temp );
    } while (temp >= 0);

    MPI_Finalize( );
    return 0;
}

