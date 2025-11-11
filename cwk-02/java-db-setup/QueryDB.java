import java.io.*;
import java.sql.*;
import java.util.*;

public class QueryDB {

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

    public static void queryAllSensorData(Connection database) throws SQLException {
        Statement statement = database.createStatement();
        ResultSet results = statement.executeQuery(
                "SELECT * FROM sensor_data ORDER BY timestamp DESC");

        System.out.println("\n=== ALL SENSOR DATA IN DATABASE ===");
        System.out.println(
                "----------------------------------------------------------------------------------------------------------------------------");
        System.out.printf("| %-4s | %-10s | %-17s | %-18s | %-14s | %-16s | %-24s |%n",
                "ID", "Sensor ID", "Temperature (°C)", "Wind Speed (mph)", "Humidity (%)", "CO2 Level (ppm)", "Timestamp");
        System.out.println(
                "----------------------------------------------------------------------------------------------------------------------------");

        int count = 0;
        while (results.next()) {
            int id = results.getInt("id");
            int sensorId = results.getInt("sensor_id");
            double temperature = results.getDouble("temperature");
            double windSpeed = results.getDouble("wind_speed");
            int relativeHumidity = results.getInt("relative_humidity");
            int co2Level = results.getInt("co2_level");
            String timestamp = results.getString("timestamp");

            // Timestamp to 2 decimal places
            String shortTimestamp = timestamp.substring(0, 24);

            System.out.printf("| %-4d | %-10d | %17.2f | %18.2f | %14d | %16d | %-24s |%n",
                    id, sensorId, temperature, windSpeed,
                    relativeHumidity, co2Level, shortTimestamp);

            count++;
        }
        System.out.printf("----------------------------------------------------------------------------------------------------------------------------%n");
        System.out.println("Total records in database: " + count);
        statement.close();
    }

    public static void queryRecentSensorData(Connection database, int limit) throws SQLException {
        PreparedStatement statement = database.prepareStatement(
                "SELECT TOP (?) * FROM sensor_data ORDER BY timestamp DESC");
        statement.setInt(1, limit);

        ResultSet results = statement.executeQuery();

        System.out.println("\n=== RECENT SENSOR DATA (Last " + limit + " records) ===");
        int count = 0;
        while (results.next()) {
            int sensorId = results.getInt("sensor_id");
            double temperatures = results.getDouble("temperature");
            double windSpeeds = results.getDouble("wind_speed");
            int relativeHumidities = results.getInt("relative_humidity");
            int co2_levels = results.getInt("co2_level");
            String timestamp = results.getString("timestamp");

            System.out.printf("Sensor %d: %.1f°C, %.1f mph, %d%%, %d ppm | %s%n",
                    sensorId, temperatures, windSpeeds, relativeHumidities, co2_levels, timestamp.substring(0, 19));
            count++;
        }
        System.out.println("Displayed: " + count + " records");
        statement.close();
    }

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

            // Show recent data (last 10 records)
            // queryRecentSensorData(database, 10);

            queryAllSensorData(database);

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