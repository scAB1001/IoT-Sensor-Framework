// TCPClient

import java.io.*;
import java.net.*;

/**
 * @author Karim Djemame
 * 
 * @version 1.1 [2021-09-24]
 * 
 */

class TCPClient {

  public static void main(String args[]) throws Exception {
    String sentence, hostname = "", modifiedSentence;

    if (args.length  > 0) {
      hostname = args[0];
      System.out.println("hostname == " + hostname + "\n");
    } else {
      System.out.println("Usage: \"TCPClient hostname \" ");
      System.exit(0);
    }

    System.out.println("Text to send to Server? \n");
    BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));

    Socket clientSocket = new Socket(hostname, 6789);

    DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
    BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

    sentence = inFromUser.readLine();
    outToServer.writeBytes(sentence + '\n');

    modifiedSentence = inFromServer.readLine();

    System.out.println("FROM SERVER: " + modifiedSentence);

    clientSocket.close();                 
  }
}
