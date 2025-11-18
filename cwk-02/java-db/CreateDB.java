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
    // TODO: Uncomment for submission
    // /*
    try {
      statement.executeUpdate("DROP TABLE sensor_data");
      System.out.println("⚠️ Dropped existing sensor_data table");
    } catch (SQLException error) {
      // Catch and ignore SQLException, as this merely indicates
      // that the table didn't exist in the first place!
      System.out.println("⚠️ sensor_data table did not exist, skipping drop");
    }
    //*/

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

  public static void enableDatabaseChangeTracking(Connection database) throws SQLException {
    Statement statement = database.createStatement();

    try {
      // Enable change tracking at database level (REQUIRED)
      String enableDbTracking = "IF NOT EXISTS (SELECT * FROM sys.change_tracking_databases WHERE database_id = DB_ID()) "
          +
          "BEGIN " +
          "   ALTER DATABASE CURRENT SET CHANGE_TRACKING = ON (CHANGE_RETENTION = 2 DAYS, AUTO_CLEANUP = ON); " +
          "   PRINT 'Database change tracking enabled'; " +
          "END " +
          "ELSE " +
          "   PRINT 'Database change tracking already enabled'";

      statement.executeUpdate(enableDbTracking);
      System.out.println("✅ Database-level change tracking enabled");

    } catch (SQLException e) {
      System.err.println("❌ Failed to enable database change tracking: " + e.getMessage());
      throw e;
    } finally {
      statement.close();
    }
  }

  public static void enableTableChangeTracking(Connection database) throws SQLException {
    Statement statement = database.createStatement();

    try {
      // Enable change tracking for sensor_data table (REQUIRED)
      String enableTableTracking = "IF NOT EXISTS (SELECT * FROM sys.change_tracking_tables ct " +
          "              JOIN sys.tables t ON ct.object_id = t.object_id " +
          "              WHERE t.name = 'sensor_data') " +
          "BEGIN " +
          "   ALTER TABLE sensor_data ENABLE CHANGE_TRACKING; " +
          "   PRINT 'Table change tracking enabled'; " +
          "END " +
          "ELSE " +
          "   PRINT 'Table change tracking already enabled'";

      statement.executeUpdate(enableTableTracking);
      System.out.println("✅ Table-level change tracking enabled for sensor_data");

    } catch (SQLException e) {
      System.err.println("❌ Failed to enable table change tracking: " + e.getMessage());
      throw e;
    } finally {
      statement.close();
    }
  }

  public static void verifyChangeTracking(Connection database) throws SQLException {
    Statement statement = database.createStatement();

    String verifySQL = "SELECT \n" +
        "    DB_NAME() AS database_name,\n" +
        "    t.name AS table_name,\n" +
        "    CASE \n" +
        "        WHEN ct.object_id IS NOT NULL THEN 'ENABLED'\n" +
        "        ELSE 'DISABLED'\n" +
        "    END AS change_tracking_status,\n" +
        "    dct.is_auto_cleanup_on,\n" +
        "    dct.retention_period,\n" +
        "    dct.retention_period_units_desc\n" +
        "FROM sys.tables t\n" +
        "LEFT JOIN sys.change_tracking_tables ct ON t.object_id = ct.object_id\n" +
        "CROSS JOIN sys.change_tracking_databases dct\n" +
        "WHERE t.name = 'sensor_data'";

    ResultSet resultSet = statement.executeQuery(verifySQL);

    System.out.println("\n🔍 CHANGE TRACKING VERIFICATION:");
    System.out.println("=================================");

    if (resultSet.next()) {
      String dbName = resultSet.getString("database_name");
      String tableName = resultSet.getString("table_name");
      String status = resultSet.getString("change_tracking_status");
      boolean autoCleanup = resultSet.getBoolean("is_auto_cleanup_on");
      int retention = resultSet.getInt("retention_period");
      String retentionUnits = resultSet.getString("retention_period_units_desc");

      System.out.println("Database: " + dbName);
      System.out.println("Table: " + tableName);
      System.out.println("Status: " + status);
      System.out.println("Auto Cleanup: " + (autoCleanup ? "ON" : "OFF"));
      System.out.println("Retention: " + retention + " " + retentionUnits);

      if ("ENABLED".equals(status)) {
        System.out.println("✅ READY for Azure SQL Triggers!");
      } else {
        System.out.println("❌ NOT READY - Change tracking not properly enabled");
      }
    } else {
      System.out.println("❌ Could not verify change tracking status");
    }

    resultSet.close();
    statement.close();
  }

  public static void insertSampleData(Connection database) throws SQLException {
    Statement statement = database.createStatement();

    // Insert some sample data to test the table
    String insertSQL = "INSERT INTO sensor_data (sensor_id, temperature, wind_speed, relative_humidity, co2_level) VALUES \n"
        + "(100, 15.5, 12.3, 45, 650),\n"
        + "(101, 16.2, 14.1, 50, 720),\n"
        + "(102, 14.8, 13.7, 48, 680)";

    int rowsInserted = statement.executeUpdate(insertSQL);
    System.out.println("✅ Inserted " + rowsInserted + " sample records for testing");

    statement.close();
  }

  public static void main(String[] argv) {
    Connection database = null;
    try {
      database = getConnection();
      System.out.println("✅ Connected to Azure SQL Database");

      // createSensorTable(database);
      System.out.println("✅ Database setup complete - ready for Azure Functions");

      enableDatabaseChangeTracking(database);
      enableTableChangeTracking(database);
      verifyChangeTracking(database);
      // insertSampleData(database);

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
