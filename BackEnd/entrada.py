def imprimirInicial()
    index = 0
        
        while (index != 12)
            index = index + 1
            if (index == 0 or index == 1 or index == 11 or index == 12) 
                println("*********************************************************************************************************")
            elif (index == 2) 
                println("**********  ***************  ******                 ******                 ******              **********")
            elif (index >= 3 and index <= 5) 
                println("**********  ***************  ******  *********************  *************  ******  **********************")
            elif (index == 6) 
                println("**********  ***************  ******                 ******                 ******  **********************")
            elif (index >= 7 and index <= 9) 
                println("**********  ***************  ********************   ******  *************  ******  **********************")
            elif (index == 10) 
                println("**********                   ******                 ******  *************  ******              **********");
            ;
        ;
;
    
    imprimirInicial()