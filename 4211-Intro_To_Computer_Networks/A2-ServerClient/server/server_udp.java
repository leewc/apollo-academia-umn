package server;

import java.io.*;

// Driver class to start the server
class server_udp
{
   public static void main(String argv[])
      {
         if(argv.length < 1)
         {
            System.err.println("Usage: java server.server_udp <port>");
            return;
         }

         try {
            final File curDir = new File("server/");
            UDPServer udpServer = new UDPServer(Integer.parseInt(argv[0]), curDir); 

            System.out.println("Server has these files:");
            udpServer.listFilesForFolder(curDir);

            System.out.println("\n UDP Server is listening ...\n");

            udpServer.start();
         }
         catch(Exception e)
         {
            e.printStackTrace();
         }
      }
}
