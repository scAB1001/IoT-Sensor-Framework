import java.io.*;
import java.sql.*;
import java.util.*;

public class QueryDB {

    private static final String DASHES = "-------------------------------------------------------------------------------------------------------------------------------------------------------";
    private static final String HEADER = "| %-4s | %-9s | %-17s | %-18s | %-14s | %-16s | %-24s | %-24s |%n";
    private static final String ROW = "| %-4d | %-9d | %17.2f | %18.2f | %14d | %16d | %-20s | %-20s |%n";

    /*
     * Establish connection to Azure SQL Database
     * using credentials from config.properties
     * `connectionUrl` format adapted from:
     * https://learn.microsoft.com/en-us/sql/connect/jdbc/building-the-connection-url
     */
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

        try {
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        } catch (ClassNotFoundException e) {
            throw new SQLException("JDBC Driver not found", e);
        }

        Connection connection = null;
        connection = DriverManager.getConnection(connectionUrl);

        return connection;
    }


    /*
     * Generic method to query sensor_data table with optional ordering and filtering
     * and display results in formatted table
     * `orderBy` - SQL ORDER BY clause (without 'ORDER BY'), or null for no ordering
     * `filter` - SQL WHERE clause (without 'WHERE'), or null for no filtering
     * `title` - Title to display above the results
     */
    public static void querySensorData(Connection database, String orderBy, String filter, String title)
            throws SQLException {
        StringBuilder query = new StringBuilder("SELECT * FROM sensor_data");

        if (filter != null && !filter.isEmpty()) {
            query.append(" WHERE ").append(filter);
        }

        if (orderBy != null && !orderBy.isEmpty()) {
            query.append(" ORDER BY ").append(orderBy);
        }

        Statement statement = database.createStatement();
        ResultSet results = statement.executeQuery(query.toString());

        System.out.println("\n" + title);
        System.out.println(DASHES);
        System.out.printf(HEADER, "ID", "Sensor ID", "Temperature (°C)", "Wind Speed (mph)", "Humidity (%)", "CO2 Level (ppm)", "Timestamp", "Created");
        System.out.println(DASHES);

        int count = 0;
        while (results.next()) {
            int id = results.getInt("id");
            int sensorId = results.getInt("sensor_id");
            double temperature = results.getDouble("temperature");
            double windSpeed = results.getDouble("wind_speed");
            int humidity = results.getInt("relative_humidity");
            int co2Level = results.getInt("co2_level");
            String timestamp = results.getString("timestamp");
            String createdAt = results.getString("created_at");

            // Timestamp to 2 decimal places
            String shortTimestamp = timestamp.substring(0, 24);
            String shortCreatedAt = createdAt.substring(0, 24);

            System.out.printf(ROW, id, sensorId, temperature, windSpeed, humidity, co2Level, shortTimestamp, shortCreatedAt);
            count++;
        }

        System.out.println(DASHES);
        System.out.println("Total records: " + count);
        statement.close();
    }


    public static void queryAllData(Connection database) throws SQLException {
        querySensorData(database, "timestamp DESC", null, "=== ALL SENSOR DATA ===");
    }

    public static void queryBySensor(Connection database) throws SQLException {
        querySensorData(database, "sensor_id, timestamp DESC", null, "=== DATA GROUPED BY SENSOR ===");
    }

    public static void querySensorById(Connection database) throws SQLException {

        Scanner scanner = new Scanner(System.in);
        int sensorId = 0;
        boolean validInput = false;

        try {
            while (!validInput) {
                System.out.print("Which sensor ID would you like to query? (1-20): ");

                if (scanner.hasNextInt()) {
                    sensorId = scanner.nextInt();

                    if (sensorId >= 1 && sensorId <= 20) {
                        validInput = true;
                    } else {
                        System.out.println("❌ Invalid sensor ID: " + sensorId + ". Please enter a number between 1-20.");
                    }
                } else {
                    System.out.println("❌ Invalid input. Please enter a number between 1-20.");
                    scanner.next(); // Clear the invalid input
                }
            }

            querySensorData(database, "timestamp DESC", "sensor_id = " + sensorId,
                    "=== DATA FOR SENSOR " + sensorId + " ===");

        } finally {
            scanner.close();
        }

    }


    /*
     * Get and display basic statistics about the sensor_data table
     * - total records
     * - date range (earliest and latest timestamps)
     * - number of unique sensors
     */
    public static void getDatabaseStats(Connection database) throws SQLException {
        Statement statement = database.createStatement();

        // Get total records
        ResultSet countResult = statement.executeQuery("SELECT COUNT(*) as total FROM sensor_data");
        countResult.next();
        int totalRecords = countResult.getInt("total");

        // Get date range
        ResultSet dateResult = statement
                .executeQuery("SELECT MIN(timestamp) as earliest, MAX(timestamp) as latest FROM sensor_data");
        dateResult.next();
        String earliest = dateResult.getString("earliest");
        String latest = dateResult.getString("latest");

        // Get sensor count
        ResultSet sensorResult = statement
                .executeQuery("SELECT COUNT(DISTINCT sensor_id) as unique_sensors FROM sensor_data");
        sensorResult.next();
        int uniqueSensors = sensorResult.getInt("unique_sensors");

        System.out.println("\n=== DATABASE STATISTICS ===");
        System.out.println("Total records: " + totalRecords);
        System.out.println("Unique sensors: " + uniqueSensors);
        System.out.println("Date range: " + (earliest != null ? earliest.substring(0, 19) : "N/A") +
                " to " + (latest != null ? latest.substring(0, 19) : "N/A"));

        statement.close();
    }

    public static void main(String[] argv) {
        Connection database = null;
        try {
            database = getConnection();
            System.out.println("✅ Connected to Azure SQL Database");

            // Show database stats
            getDatabaseStats(database);

            // Query all data
            queryAllData(database);

            // Query data grouped by sensor
            queryBySensor(database);

            // Query data for a specific sensor (e.g., sensor_id = 3)
            querySensorById(database);

        } catch (Exception error) {
            System.err.println("❌ Database query failed:");
            error.printStackTrace();
        } finally {
            if (database != null) {
                try {
                    database.close();
                } catch (Exception error) {
                }
            }
        }
    }
}