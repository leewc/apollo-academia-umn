package server;

import java.io.*;

// Driver class to start the server
class server_tcp 
{
   public static void main(String argv[])
      {
         if(argv.length < 1)
         {
            System.err.println("Usage: java server.server_tcp <port>");
            return;
         }

         try {
            final File curDir = new File("server/");
            TCPServer tcpServer = new TCPServer(Integer.parseInt(argv[0]), curDir); 

            System.out.println("Server has files:");
            tcpServer.listFilesForFolder(curDir);

            System.out.println("\nServer is listening ...\n");

            tcpServer.start();
         }
         catch(Exception e)
         {
            e.printStackTrace();
         }
      }
}
