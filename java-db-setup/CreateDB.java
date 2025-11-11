import java.io.*;
import java.sql.*;
import java.util.*;

public class CreateDB {

  public static Connection getConnection() throws IOException, SQLException {
    Properties p = new Properties();
    p.load(new FileInputStream("config.properties"));

    String serverName = p.getProperty("db.server");
    String databaseName = p.getProperty("db.database");
    String username = p.getProperty("db.username");
    String password = p.getProperty("db.password");
    String certificate = p.getProperty("db.certificate");

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

  public static void createSensorTable(Connection database) throws SQLException {
    // Create a Statement object to execute SQL commands
    Statement statement = database.createStatement();


    // Drop existing table, if present
    // TODO: Uncomment when submitting
    // try {
    //   statement.executeUpdate("DROP TABLE sensor_data");
    //   System.out.println("⚠️ Dropped existing sensor_data table");
    // } catch (SQLException error) {
    //   // Catch and ignore SQLException, as this merely indicates
    //   // that the table didn't exist in the first place!
    //   System.out.println("⚠️ sensor_data table did not exist, skipping drop");
    // }

    // Create sensor_data table matching Azure Functions schema
    String createTableSQL = "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='sensor_data' AND xtype='U') " +
        "CREATE TABLE sensor_data ("
        + "id BIGINT IDENTITY(1,1) PRIMARY KEY, "
        + "sensor_id INT NOT NULL, "
        + "temperature DECIMAL(5,2) NOT NULL, "
        + "wind_speed DECIMAL(5,2) NOT NULL, "
        + "relative_humidity INT NOT NULL, "
        + "co2_level INT NOT NULL, "
        + "timestamp DATETIME2 DEFAULT GETDATE(), "
        + "created_at DATETIME2 DEFAULT GETDATE())";

    statement.executeUpdate(createTableSQL);
    System.out.println("✅ Created sensor_data table (or already exists)");

    statement.close();
  }

  public static void main(String[] argv) {
    Connection database = null;
    try {
      database = getConnection();
      System.out.println("✅ Connected to Azure SQL Database");
      createSensorTable(database);
      System.out.println("✅ Database setup complete - ready for Azure Functions");
    } catch (Exception error) {
      System.err.println("❌ Database setup failed:");
      error.printStackTrace();
    } finally {
      // This will always execute, even if an exception has
      // been thrown elsewhere - close the connection to the DB.
      if (database != null) {
        try {
          database.close();
        } catch (Exception error) {
        }
      }
    }
  }
}
