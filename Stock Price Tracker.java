import java.util.*; 
class Stock {
    String symbol;   // Stock ticker symbol (like AAPL)
    double price;    // Current stock price
 
    // Constructor to initialize a stock object with a symbol and starting price.
    Stock(String symbol, double price) {
        this.symbol = symbol;
        this.price = price;
    }
     
    // Simulates updating the stock price with a random change between -2 and +2.
    void updatePrice() {
        Random rand = new Random();
        double change = (rand.nextDouble() * 4) - 2; // -2 to +2
        price += change;
        if (price < 0) price = 0.01;    // ensure price doesn't go negative
    }
 
    void display() {
        System.out.printf("%-6s : $%.2f\n", symbol, price);
    }
}
 
public class StockTracker {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        // Create an array of Stock objects representing the portfolio
        Stock[] portfolio = {
            new Stock("AAPL", 175.00),
            new Stock("GOOGL", 2800.00),
            new Stock("TSLA", 730.00),
            new Stock("AMZN", 3450.00),
            new Stock("MSFT", 299.00)
        };
 
        System.out.println("Welcome to the Stock Tracker!");
        System.out.print("Enter number of simulated updates: ");
        int rounds = scanner.nextInt();   //Read how many update cycles user wants
 
       // Loop to simulate stock price updates for the given number of rounds
        for (int i = 1; i <= rounds; i++) {
            System.out.println("\nUpdate #" + i + ":");
            // Update and display each stock's price
            for (Stock stock : portfolio) {
                stock.updatePrice();
                stock.display();
            }
 
            try {
                Thread.sleep(500); // Delay for realism
            } catch (InterruptedException e) {
                System.out.println("Update interrupted.");
            }
        }
 
        scanner.close();
        System.out.println("\nTracking complete.");
    }
}
