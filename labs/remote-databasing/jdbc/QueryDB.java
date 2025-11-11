import java.io.*;
import java.sql.*;
import java.util.*;


/**
 * Example of how to query a database using JDBC.
 *
 * <p>The program demonstrates</p>
 * <ul>
 *   <li>Use of properties to hold JDBC driver and database details</li>
 *   <li>Use of the SQL command SELECT</li>
 *   <li>Processing of ResultSet objects</li>
 * </ul>
 *
 * @author Karim Djemame and Nick Efford
 * @version 2.2 [2024-10-02]
 */

public class QueryDB {

/**
   * Establishes a connection to the database.
   *
   * The details of which driver to use, which database to
   * access and the username and password to use are being
   * hard-coded. 
   * Refer to the connection string, JDBC SQL authentication
   * on Azure 
   *
   * @return Connection object representing the connection
   * @throws IOException if properties file cannot be accessed
   * @throws SQLException if connection fails
   */

  public static Connection getConnection() throws IOException, SQLException
  {
    
    // Obtain access parameters and use them to create connection
    Properties p = new Properties();
    p.load(new FileInputStream("config.properties"));

    String serverName = p.getProperty("db.server");
    String databaseName = p.getProperty("db.database");
    String username = p.getProperty("db.username");
    String password = p.getProperty("db.password");
    String certificate = p.getProperty("db.certificate");

    // JDBC connection string for Azure SQL Database
    String connectionUrl = String.format(
        "jdbc:sqlserver://%s:1433;database=%s;user=%s;password=%s;encrypt=true;" +
        "trustServerCertificate=false;hostNameInCertificate=*%s;loginTimeout=30;",
        serverName, databaseName, username, password, certificate);

    // Load JDBC driver
    try {
        Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
    } catch (ClassNotFoundException e) {
        throw new SQLException("JDBC Driver not found", e);
    }

    // Establish connection
    Connection connection = null;
    connection = DriverManager.getConnection(connectionUrl);

    return connection;
  }

  

  /**
     * Queries the database to find student names.
     *
     * @param forename forename to search for in database
     * @param database connection to database
     * @throws SQLException if query fails
     

    public static void findNamesbyForename(String forename, Connection database)
    throws SQLException
    {
      Statement statement = database.createStatement();
      ResultSet results = statement.executeQuery(
      "SELECT * FROM students WHERE forename = '" + forename + "'");
      while (results.next()) {
        String surname = results.getString("surname");
        System.out.println(forename + " " + surname);
      }
      statement.close();
    }
  */


  /**
   * Lists all students in the database.
   */
  public static void listAllStudents(Connection database)
   throws SQLException {
    Statement statement = database.createStatement();
    ResultSet results = statement.executeQuery("SELECT * FROM students ORDER BY surname, forename");
    
    System.out.println("\n=== ALL STUDENTS ===");
    int count = 0;
    while (results.next()) {
      String userID = results.getString("user_id");
      String surname = results.getString("surname");
      String forename = results.getString("forename");
      System.out.printf("%-8s %-15s %-15s%n", userID, surname, forename);
      count++;
    }
    System.out.println("Total students: " + count);
    statement.close();
  }



  /**
   * Queries the database to find student names by forename.
   */
  public static void findNamesbyForename(String forename, Connection database) throws SQLException {
    // Use PreparedStatement to prevent SQL injection
    PreparedStatement statement = database.prepareStatement(
        "SELECT * FROM students WHERE forename LIKE ? ORDER BY surname");
    statement.setString(1, "%" + forename + "%"); // Using LIKE for partial matches
    
    ResultSet results = statement.executeQuery();
    
    System.out.println("\n=== SEARCH RESULTS FOR FORENAME: '" + forename + "' ===");
    int count = 0;
    while (results.next()) {
      String userID = results.getString("user_id");
      String surname = results.getString("surname");
      String foundForename = results.getString("forename");
      System.out.printf("%-8s %-15s %-15s%n", userID, surname, foundForename);
      count++;
    }
    System.out.println("Found: " + count + " student(s)");
    statement.close();
  }



  /**
   * Queries the database to find student names.
   *
   * @param surname surnam to search for in database
   * @param database connection to database
   * @throws SQLException if query fails
   */

  public static void findNamesbySurname(String surname, Connection database) 
   throws SQLException {
    // Use PreparedStatement to prevent SQL injection
    PreparedStatement statement = database.prepareStatement(
        "SELECT * FROM students WHERE surname LIKE ? ORDER BY forename");
    statement.setString(1, "%" + surname + "%"); // Using LIKE for partial matches
    
    ResultSet results = statement.executeQuery();
    
    System.out.println("\n=== SEARCH RESULTS FOR SURNAME: '" + surname + "' ===");
    int count = 0;
    while (results.next()) {
      String userID = results.getString("user_id");
      String foundSurname = results.getString("surname");
      String forename = results.getString("forename");
      System.out.printf("%-8s %-15s %-15s%n", userID, foundSurname, forename);
      count++;
    }
    System.out.println("Found: " + count + " student(s)");
    statement.close();
  }



/**
   * Finds student by user ID.
   */
  public static void findStudentByID(String userID, Connection database) throws SQLException {
    PreparedStatement statement = database.prepareStatement(
        "SELECT * FROM students WHERE user_id = ?");
    statement.setString(1, userID);
    
    ResultSet results = statement.executeQuery();
    
    System.out.println("\n=== SEARCH RESULTS FOR USER ID: '" + userID + "' ===");
    if (results.next()) {
      String foundUserID = results.getString("user_id");
      String surname = results.getString("surname");
      String forename = results.getString("forename");
      System.out.printf("User ID: %s%n", foundUserID);
      System.out.printf("Name: %s %s%n", forename, surname);
    } else {
      System.out.println("No student found with user ID: " + userID);
    }
    statement.close();
  }



  /**
   * Gets database statistics.
   */
  public static void showDatabaseStats(Connection database)
   throws SQLException {
    Statement statement = database.createStatement();
    
    // Get total number of students
    ResultSet countResult = statement.executeQuery("SELECT COUNT(*) as total FROM students");
    countResult.next();
    int totalStudents = countResult.getInt("total");
    
    // Get unique surnames count
    ResultSet surnameResult = statement.executeQuery("SELECT COUNT(DISTINCT surname) as unique_surnames FROM students");
    surnameResult.next();
    int uniqueSurnames = surnameResult.getInt("unique_surnames");
    
    // Get unique forenames count
    ResultSet forenameResult = statement.executeQuery("SELECT COUNT(DISTINCT forename) as unique_forenames FROM students");
    forenameResult.next();
    int uniqueForenames = forenameResult.getInt("unique_forenames");
    
    System.out.println("\n=== DATABASE STATISTICS ===");
    System.out.println("Total students: " + totalStudents);
    System.out.println("Unique surnames: " + uniqueSurnames);
    System.out.println("Unique forenames: " + uniqueForenames);
    
    statement.close();
  }

  /**
   * Main program.
   */

  public static void main(String[] argv)
  {
    // if (argv.length == 0) {
    //   System.err.println("usage: java QueryDB <forename>");
    //   System.exit(1);
    // }

    Scanner input = new Scanner(System.in);
    while (true) {
      System.out.println("\n=== STUDENT DATABASE QUERY SYSTEM ===");
      System.out.println("1. List all students");
      System.out.println("2. Search by forename");
      System.out.println("3. Search by surname");
      System.out.println("4. Search by user ID");
      System.out.println("5. Database statistics");
      System.out.println("6. Exit");
      System.out.print("Choose an option (1-6): ");
      
      int choice = 0;
      if (input.hasNextInt()) {
        choice = input.nextInt();
        input.nextLine(); // Consume newline
      } else {
        input.nextLine(); // Clear invalid input
        System.out.println("Please enter a valid number (1-6).");
        continue;
      }
      
      if (choice == 6) {
        System.out.println("Exiting... Goodbye!");
        break;
      }
      
      Connection connection = null;
      try {
        connection = getConnection();
        
        switch (choice) {
          case 1:
            listAllStudents(connection);
            break;
            
          case 2:
            System.out.print("Enter forename to search: ");
            String forename = input.nextLine().trim();
            if (!forename.isEmpty()) {
              findNamesbyForename(forename, connection);
            } else {
              System.out.println("Forename cannot be empty.");
            }
            break;
            
          case 3:
            System.out.print("Enter surname to search: ");
            String surname = input.nextLine().trim();
            if (!surname.isEmpty()) {
              findNamesbySurname(surname, connection);
            } else {
              System.out.println("Surname cannot be empty.");
            }
            break;
            
          case 4:
            System.out.print("Enter user ID to search: ");
            String userID = input.nextLine().trim();
            if (!userID.isEmpty()) {
              findStudentByID(userID, connection);
            } else {
              System.out.println("User ID cannot be empty.");
            }
            break;
            
          case 5:
            showDatabaseStats(connection);
            break;
            
          default:
            System.out.println("Invalid choice. Please select 1-6.");
        }
        
      } catch (Exception error) {
        System.out.println("Database error: " + error.getMessage());
        error.printStackTrace();
      } finally {
      // This will always execute, even if an exception has
      // been thrown elsewhere in the code - so this is
      // the ideal place to close the connection to the DB...

        if (connection != null) {
          try {
            connection.close();
          }
          catch (Exception error) {}
        }
      }

      if (choice != 6) {
        System.out.print("\nPress Enter to continue...");
        input.nextLine();
      }

    }

    input.close();
  }

}
