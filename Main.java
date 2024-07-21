import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        double averageStartCost = 0;
        double averageEndCost = 0;
        double averageRuntime = 0;
        for (int k = 0; k < 100; k++) {
            int n = 1000;
            int d = 4;
            ArrayList<double[]> positions = new ArrayList<>();
            ArrayList<Integer> initialState = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                double[] randomPosition = new double[d];
                for (int j = 0; j < d; j++) {
                    randomPosition[j] = 25 * Math.random();
                }
                positions.add(randomPosition);
                initialState.add(i);
            }
            AnnealingSchedule as = new ExponentialSchedule(18, 0.95);

            Tsp tsp = new Tsp(positions);
            double startCost = tsp.cost(initialState);
            averageStartCost += startCost;
            long startTime = System.nanoTime();
            double endCost = tsp.cost(tsp.run(initialState, as));
            averageEndCost += endCost;
            long stopTime = System.nanoTime();
            averageRuntime += (double) (stopTime - startTime);
        }
        averageEndCost /= 100;
        averageEndCost /= 100;
        averageRuntime /= 100;
        System.out.println("averageEndCost: " + averageEndCost);
        System.out.println("averageStartCost: " + averageStartCost);
        System.out.println("averageRuntime: " + averageRuntime);
    }
}
